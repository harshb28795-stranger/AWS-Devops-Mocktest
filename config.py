"""
Configuration file for the AWS DevOps Professional Mock Test Lab.
Keeping configuration in one place makes it easy to change settings
(like the database location or secret key) without touching app code.
"""

import os

# Base directory of the project (folder where this file lives)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class used by the Flask application factory."""

    # Secret key is required by Flask to securely sign the session cookie.
    # The quiz relies on Flask sessions to track progress, so this matters.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # SQLite database stored inside an "instance" folder next to the project.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'quiz.db')}"
    )

    # Disable a feature we don't need; saves a small amount of memory/overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pass/fail threshold (percentage) used on the results page.
    PASS_PERCENTAGE = 72
