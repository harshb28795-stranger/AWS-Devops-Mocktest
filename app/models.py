"""
Database models for the AWS DevOps Professional Mock Test Lab.

Two tables are used:
    - Category: quiz categories (e.g., SDLC Automation, Security & Compliance)
    - Question: individual multiple-choice questions linked to a category
"""

from app import db


class Category(db.Model):
    """A quiz category, e.g. 'Security & Compliance'."""

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    # A category can have many questions. cascade delete keeps things tidy
    # if a category is ever removed.
    questions = db.relationship(
        "Question", backref="category", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


class Question(db.Model):
    """A single multiple-choice question belonging to a Category."""

    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)

    # Stored as 'A', 'B', 'C', or 'D'
    correct_answer = db.Column(db.String(1), nullable=False)

    explanation = db.Column(db.Text, nullable=False)

    def options_dict(self):
        """Return the four options as a dict keyed by letter.

        Centralizing this avoids repeating the same {'A': self.option_a, ...}
        pattern in multiple templates/routes.
        """
        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }

    def __repr__(self):
        return f"<Question {self.id}: {self.question_text[:40]}>"
