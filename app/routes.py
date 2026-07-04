"""
Routes for the AWS DevOps Professional Mock Test Lab.

Quiz progress (which questions are active, the current index, the
user's selected answers, and which questions have been checked) is
kept in the Flask session. This avoids needing a separate "attempt"
database table while still letting a user navigate back and forth
between questions with their answers preserved.
"""

from flask import (
    Blueprint, render_template, redirect, url_for, request, session, flash, current_app
)
from app import db
from app.models import Category, Question

main_bp = Blueprint("main", __name__)

# Session key used to store all quiz-in-progress state.
QUIZ_SESSION_KEY = "active_quiz"


def get_active_quiz():
    """Return the dict describing the quiz currently in progress, or None."""
    return session.get(QUIZ_SESSION_KEY)


def save_active_quiz(quiz_state):
    """Persist quiz state back into the session (Flask sessions need reassignment)."""
    session[QUIZ_SESSION_KEY] = quiz_state
    session.modified = True


# ---------------------------------------------------------------------------
# Home page
# ---------------------------------------------------------------------------
@main_bp.route("/")
def home():
    """Landing page with Start Quiz / Categories buttons and About section."""
    total_questions = Question.query.count()
    total_categories = Category.query.count()
    return render_template(
        "index.html",
        total_questions=total_questions,
        total_categories=total_categories,
    )


# ---------------------------------------------------------------------------
# Categories page
# ---------------------------------------------------------------------------
@main_bp.route("/categories")
def categories():
    """List every category with its question count so the user can pick one."""
    all_categories = Category.query.order_by(Category.name).all()
    return render_template("categories.html", categories=all_categories)


# ---------------------------------------------------------------------------
# Quiz: start (also supports a mixed "All Categories" quiz)
# ---------------------------------------------------------------------------
@main_bp.route("/quiz/start/<int:category_id>")
def start_quiz(category_id):
    """Initialize a new quiz session for a single category."""
    category = Category.query.get_or_404(category_id)
    questions = Question.query.filter_by(category_id=category.id).all()

    if not questions:
        flash("This category has no questions yet.", "warning")
        return redirect(url_for("main.categories"))

    _initialize_quiz_session(
        question_ids=[q.id for q in questions],
        title=f"{category.name} Quiz",
    )
    return redirect(url_for("main.quiz_question", index=0))


@main_bp.route("/quiz/start-all")
def start_quiz_all():
    """Initialize a quiz session covering every question in every category."""
    questions = Question.query.all()

    if not questions:
        flash("No questions are available yet.", "warning")
        return redirect(url_for("main.home"))

    _initialize_quiz_session(
        question_ids=[q.id for q in questions],
        title="Full Mock Test (All Categories)",
    )
    return redirect(url_for("main.quiz_question", index=0))


def _initialize_quiz_session(question_ids, title):
    """Helper that builds a fresh quiz_state dict and saves it to the session."""
    quiz_state = {
        "title": title,
        "question_ids": question_ids,
        "current_index": 0,
        # answers: {str(question_id): "A"/"B"/"C"/"D"}
        "answers": {},
        # checked: {str(question_id): True} once "Check Answer" has been clicked
        "checked": {},
    }
    save_active_quiz(quiz_state)


# ---------------------------------------------------------------------------
# Quiz: display a specific question by index
# ---------------------------------------------------------------------------
@main_bp.route("/quiz/question/<int:index>")
def quiz_question(index):
    """Render the question at the given index of the active quiz."""
    quiz_state = get_active_quiz()
    if not quiz_state:
        flash("Please start a quiz first.", "info")
        return redirect(url_for("main.categories"))

    total = len(quiz_state["question_ids"])

    # Guard against an out-of-range index (e.g. manual URL editing).
    if index < 0 or index >= total:
        return redirect(url_for("main.quiz_question", index=0))

    quiz_state["current_index"] = index
    save_active_quiz(quiz_state)

    question_id = quiz_state["question_ids"][index]
    question = Question.query.get_or_404(question_id)

    selected_answer = quiz_state["answers"].get(str(question_id))
    is_checked = quiz_state["checked"].get(str(question_id), False)

    is_correct = None
    if is_checked and selected_answer:
        is_correct = (selected_answer == question.correct_answer)

    progress_percent = round(((index + 1) / total) * 100)

    return render_template(
        "quiz.html",
        quiz_title=quiz_state["title"],
        question=question,
        options=question.options_dict(),
        index=index,
        total=total,
        selected_answer=selected_answer,
        is_checked=is_checked,
        is_correct=is_correct,
        progress_percent=progress_percent,
        is_last_question=(index == total - 1),
    )


# ---------------------------------------------------------------------------
# Quiz: check the selected answer for the current question
# ---------------------------------------------------------------------------
@main_bp.route("/quiz/check/<int:index>", methods=["POST"])
def check_answer(index):
    """Store the user's selected option and mark the question as checked."""
    quiz_state = get_active_quiz()
    if not quiz_state:
        flash("Please start a quiz first.", "info")
        return redirect(url_for("main.categories"))

    total = len(quiz_state["question_ids"])
    if index < 0 or index >= total:
        return redirect(url_for("main.quiz_question", index=0))

    question_id = quiz_state["question_ids"][index]

    # If this question was already checked, do not allow the answer to change
    # (this enforces "prevent changing the selected answer after checking").
    if not quiz_state["checked"].get(str(question_id), False):
        selected_option = request.form.get("selected_option")
        if selected_option in ("A", "B", "C", "D"):
            quiz_state["answers"][str(question_id)] = selected_option
            quiz_state["checked"][str(question_id)] = True
            save_active_quiz(quiz_state)
        else:
            flash("Please select an option before checking your answer.", "warning")

    return redirect(url_for("main.quiz_question", index=index))


# ---------------------------------------------------------------------------
# Quiz: finish and show results
# ---------------------------------------------------------------------------
@main_bp.route("/quiz/finish")
def finish_quiz():
    """Calculate the score for the active quiz and render the results page."""
    quiz_state = get_active_quiz()
    if not quiz_state:
        flash("Please start a quiz first.", "info")
        return redirect(url_for("main.categories"))

    question_ids = quiz_state["question_ids"]
    total_questions = len(question_ids)

    correct_count = 0
    answered_count = 0

    for qid in question_ids:
        qid_str = str(qid)
        if quiz_state["checked"].get(qid_str):
            answered_count += 1
            question = Question.query.get(qid)
            if question and quiz_state["answers"].get(qid_str) == question.correct_answer:
                correct_count += 1

    wrong_count = answered_count - correct_count
    unanswered_count = total_questions - answered_count

    percentage = round((correct_count / total_questions) * 100, 1) if total_questions else 0
    pass_threshold = current_app.config.get("PASS_PERCENTAGE", 72)
    passed = percentage >= pass_threshold

    return render_template(
        "result.html",
        quiz_title=quiz_state["title"],
        total_questions=total_questions,
        correct_count=correct_count,
        wrong_count=wrong_count,
        unanswered_count=unanswered_count,
        percentage=percentage,
        pass_threshold=pass_threshold,
        passed=passed,
    )


# ---------------------------------------------------------------------------
# Quiz: restart (clear session state)
# ---------------------------------------------------------------------------
@main_bp.route("/quiz/restart")
def restart_quiz():
    """Clear the active quiz from the session and return to categories."""
    session.pop(QUIZ_SESSION_KEY, None)
    return redirect(url_for("main.categories"))
