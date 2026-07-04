"""
Entry point for the AWS DevOps Professional Mock Test Lab.

Run this file to start the Flask development server:

    python run.py

The application factory (create_app) takes care of:
- Creating the Flask app
- Configuring SQLAlchemy
- Creating the SQLite database if it does not exist
- Seeding sample categories/questions on first run
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True is fine for local practice/testing use.
    # host="0.0.0.0" allows access from other devices on the same network if needed.
    app.run(debug=True, host="0.0.0.0", port=5000)
