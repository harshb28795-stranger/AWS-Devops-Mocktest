"""
Application factory for the AWS DevOps Professional Mock Test Lab.

Using the factory pattern keeps the app modular and testable: the
Flask app, database, routes, and seed logic are all wired together
in one place instead of being scattered across the codebase.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# The db object is created here (unbound) and attached to the app
# inside create_app(). Other modules (models.py, routes.py) import
# this same 'db' instance to stay in sync with the app.
db = SQLAlchemy()


def create_app(config_object="config.Config"):
    """Create and configure the Flask application instance."""

    app = Flask(__name__)
    app.config.from_object(config_object)

    # Make sure the "instance" folder exists so SQLite has somewhere to write.
    instance_path = os.path.join(os.path.dirname(app.root_path), "instance")
    os.makedirs(instance_path, exist_ok=True)

    # Bind SQLAlchemy to this Flask app.
    db.init_app(app)

    # Import models here (after db.init_app) so SQLAlchemy knows about them
    # before we create tables.
    from app import models

    # Register the blueprint containing all application routes.
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Create tables and seed sample data automatically on first startup.
    with app.app_context():
        db.create_all()
        from app.seed_data import seed_database
        seed_database()

    return app
