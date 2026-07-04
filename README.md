# AWS DevOps Professional Mock Test Lab

A lightweight Flask web application for practicing **AWS Certified DevOps
Engineer – Professional** exam-style questions. Runs comfortably on a
laptop with 8GB RAM — no Docker, no external services, just Python and
SQLite.

## Features

- Home page with an About section and quick stats
- Six exam-domain categories:
  - SDLC Automation
  - Configuration Management
  - Monitoring & Logging
  - Incident & Event Response
  - High Availability
  - Security & Compliance
- 30 original, scenario-based practice questions (5 per category), each with
  four options and a detailed explanation
- One-question-at-a-time quiz flow with:
  - Radio button selection
  - Check Answer button (answer locks once checked)
  - Correct answer highlighting + explanation
  - Next / Previous navigation
  - Progress bar and question counter
- Score page with total/correct/wrong counts, percentage, and Pass/Fail
- SQLite database auto-created and auto-seeded on first run
- Bootstrap 5, responsive, AWS-inspired blue/navy/orange theme

## Technology Stack

- Python 3.12
- Flask
- Flask-SQLAlchemy
- SQLite
- Bootstrap 5 (via CDN)
- HTML / CSS / Vanilla JavaScript

## Project Structure

```
aws_devops_quiz/
├── app/
│   ├── __init__.py       # Flask application factory
│   ├── models.py         # Category and Question SQLAlchemy models
│   ├── routes.py         # All application routes (blueprint)
│   └── seed_data.py      # Categories + 30 sample questions, auto-seeded
├── templates/
│   ├── base.html          # Shared layout, navbar, footer
│   ├── index.html         # Home page
│   ├── categories.html    # Category selection page
│   ├── quiz.html          # Quiz question page
│   └── result.html        # Score / results page
├── static/
│   ├── css/style.css      # AWS-inspired theme
│   └── js/quiz.js         # Client-side UX enhancements
├── instance/               # SQLite database file lives here (auto-created)
├── config.py               # App configuration (DB path, secret key, etc.)
├── run.py                  # Application entry point
├── requirements.txt
└── README.md
```

## Installation

### 1. Prerequisites

- Python 3.12 installed (Python 3.9+ should also work)
- `pip` available on your PATH

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Database Initialization

No manual database setup is required. The first time you run the app:

1. Flask-SQLAlchemy creates the SQLite database file at
   `instance/quiz.db` if it does not already exist.
2. The app automatically inserts the 6 categories and 30 sample
   questions into the database (this only happens once — restarting
   the app will not create duplicate data).

If you ever want to reset the data, simply stop the app, delete
`instance/quiz.db`, and start the app again — it will be recreated and
reseeded automatically.

## Running the Application

```bash
python run.py
```

Then open your browser to:

```
http://127.0.0.1:5000
```

## How to Use

1. From the **Home** page, click **Start Quiz** (all categories) or
   **Categories** to pick a specific exam domain.
2. Answer each question by selecting an option, then click
   **Check Answer** to see if you were correct, view the highlighted
   correct answer, and read the explanation.
3. Use **Next** / **Previous** to move through the quiz. Once a
   question is checked, its selected answer is locked.
4. After the last question, click **Finish Quiz** to see your score,
   percentage, and Pass/Fail result.
5. Click **Restart Quiz** to clear your progress and try again.

## Notes

- Quiz progress is stored in the Flask session (server-side, cookie
  reference only), so it resets if the server restarts or the session
  cookie is cleared.
- The passing threshold is configurable in `config.py`
  (`PASS_PERCENTAGE`, default 72%, matching the real AWS exam's scaled
  passing score of 750/1000).
- This project intentionally excludes Docker, Jenkins, Terraform,
  Ansible, Kubernetes, AWS deployment configuration, and CI/CD
  pipelines — it is a standalone local study tool only.
