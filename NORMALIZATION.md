# Normalization Report - 3rd Normal Form Audit

## 1. Starting Schema Reviewed
The original database contained five main tables: students, courses, enrollments, assignments, and submissions.

## 2. Original Functional Dependencies
### students
- student_id -> full_name, email, program_name, student_status, created_at
- email -> full_name, program_name, student_status
- program_name describes a program and can repeat for many students

### courses
- course_id -> course_name, instructor_name, start_date, end_date, created_at
- instructor_name repeats across multiple courses when one instructor teaches more than one course

### enrollments
- enrollment_id -> student_id, course_id, enrollment_date, progress_percent, record_source
- student_id, course_id -> enrollment_date, progress_percent, record_source

### assignments
- assignment_id -> course_id, title, max_score, due_date, created_at
- course_id, title -> max_score, due_date

### submissions
- submission_id -> assignment_id, student_id, submitted_at, score, grader_note, last_updated
- assignment_id, student_id -> submitted_at, score, grader_note, last_updated

## 3. Anomaly Identification
### Update anomalies
If program names are stored directly in the students table, changing a program name requires updating every student record in that program. If instructor names are stored directly in courses, correcting an instructor name requires updating every course row taught by that instructor.

### Insertion anomalies
A new program cannot be stored unless at least one student exists in that program. A new instructor cannot be stored unless at least one course exists for that instructor.

### Deletion anomalies
Deleting the last student in a program removes the only record of that program. Deleting the last course taught by an instructor removes the only record of that instructor.

## 4. Decomposition Steps
### Step 1: Separate program data
Original students table included repeating program_name values.

Decomposition:
- programs(program_id, program_name)
- students(student_id, full_name, email, program_id, student_status, created_at)

Reason: program_name depends on the program entity, not directly on each student row.

### Step 2: Separate instructor data
Original courses table included repeating instructor_name values.

Decomposition:
- instructors(instructor_id, instructor_name)
- courses(course_id, course_name, instructor_id, start_date, end_date, created_at)

Reason: instructor_name depends on the instructor entity, not directly on each course row.

### Step 3: Enforce relationship tables and candidate keys
The enrollments table represents the relationship between students and courses. A unique constraint on student_id and course_id prevents duplicate enrollment rows.

The submissions table represents student work for assignments. A unique constraint on assignment_id and student_id prevents duplicate submissions for the same assignment by the same student.

## 5. Final 3NF Relational Schema
- programs(program_id PK, program_name UNIQUE)
- instructors(instructor_id PK, instructor_name UNIQUE)
- students(student_id PK, full_name, email UNIQUE, program_id FK, student_status, created_at)
- courses(course_id PK, course_name, instructor_id FK, start_date, end_date, created_at)
- enrollments(enrollment_id PK, student_id FK, course_id FK, enrollment_date, progress_percent, record_source, UNIQUE(student_id, course_id))
- assignments(assignment_id PK, course_id FK, title, max_score, due_date, created_at)
- submissions(submission_id PK, assignment_id FK, student_id FK, submitted_at, score, grader_note, last_updated, UNIQUE(assignment_id, student_id))

## 6. 3NF Justification
Each table has a primary key. Every non-key attribute depends on the key, the whole key, and nothing but the key. Repeating descriptive attributes such as program_name and instructor_name were moved into their own tables to remove transitive dependencies. Relationship tables use foreign keys and uniqueness constraints to preserve data integrity.
