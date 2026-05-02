# DBMS Project 3 - Academic Progress Tracker

## Project Description
This full-stack Flask application manages students, courses, enrollments, assignments, and submissions for an academic progress tracking system. It is designed for instructors or academic staff who need to monitor course enrollment, assignment performance, and student progress from a normalized relational database.

## Technical Stack
- Python 3
- Flask
- SQLAlchemy ORM
- SQLite for local development
- HTML5, CSS3, Bootstrap, and Jinja2 templates
- Git for version control

## Main Features
- Multi-table CRUD for students and courses
- Relationship management between courses, enrollments, assignments, and students
- Transaction logic when a submission is created and enrollment progress is updated together
- Server-side validation for empty strings, invalid email, invalid dates, negative scores, and invalid progress
- Dashboard using COUNT and AVG aggregate functions
- 3NF schema with separated Programs and Instructors lookup tables

## Installation Instructions
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Database Setup
Option A: initialize using SQLAlchemy models:
```bash
flask --app run.py init-db
```

Option B: run the SQL schema manually:
```bash
sqlite3 instance/project3.db < schema.sql
```

## Run the Application
```bash
python run.py
```
Open the local server in your browser. Use `/seed` once to load sample data.

## Navigation Guide
- `/` Summary dashboard
- `/students` Student list, create, edit, delete
- `/courses` Course list and course detail relationship view
- `/enrollments/new` Create a course enrollment
- `/submissions/new` Create a submission and update progress in one transaction

## Git Repository Submission
After placing these files in your GitHub repository, submit the repository URL. The repository must include the full commit history, `.gitignore`, source code, schema, normalization report, README, and AI log.
