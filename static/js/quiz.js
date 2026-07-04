/*
 * Vanilla JavaScript enhancements for the AWS DevOps Professional Mock Test Lab.
 * These are purely UX improvements - all real validation/scoring happens on
 * the Flask server, so the app still works correctly with JavaScript disabled.
 */

document.addEventListener("DOMContentLoaded", function () {

    // -------------------------------------------------------------------
    // 1) Highlight the selected option row before the form is submitted,
    //    and keep the "Check Answer" button disabled until a choice is made.
    // -------------------------------------------------------------------
    var quizForm = document.getElementById("quizForm");

    if (quizForm) {
        var optionRows = quizForm.querySelectorAll(".option-selectable");
        var checkButton = quizForm.querySelector("button[type=submit]");

        // Disable the Check Answer button until an option is chosen.
        if (checkButton) {
            checkButton.disabled = true;
        }

        optionRows.forEach(function (row) {
            row.addEventListener("click", function () {
                // Remove the "chosen" highlight from every row first.
                optionRows.forEach(function (r) {
                    r.classList.remove("option-chosen");
                });
                // Highlight the row the user just clicked.
                row.classList.add("option-chosen");

                // Enable the Check Answer button now that something is selected.
                if (checkButton) {
                    checkButton.disabled = false;
                }
            });
        });
    }

    // -------------------------------------------------------------------
    // 2) Confirm before restarting a quiz, so progress isn't lost by accident.
    // -------------------------------------------------------------------
    var restartLinks = document.querySelectorAll("a[href*='/quiz/restart']");
    restartLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            var confirmed = window.confirm(
                "Are you sure you want to restart? Your current quiz progress will be lost."
            );
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // -------------------------------------------------------------------
    // 3) Animate the progress bar width slightly for a smoother feel.
    // -------------------------------------------------------------------
    var progressBar = document.querySelector(".aws-progress-bar");
    if (progressBar) {
        var targetWidth = progressBar.style.width;
        progressBar.style.width = "0%";
        // Small delay lets the browser render 0% before transitioning up.
        window.setTimeout(function () {
            progressBar.style.transition = "width 0.4s ease";
            progressBar.style.width = targetWidth;
        }, 50);
    }
});
