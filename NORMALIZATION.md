# Normalization Report

---

# 1. Initial Database Structure

The initial database design for the Academic Progress Management System contained five primary tables:

- students
- courses
- enrollments
- assignments
- submissions

At the beginning, some descriptive information such as `program_name` and `instructor_name` was stored directly inside the main entity tables. Although the structure was functional, it introduced repeated data and increased the possibility of redundancy and maintenance issues as the database grew.

The purpose of normalization was to improve the overall database structure by reducing duplication, improving consistency, and ensuring better relational integrity.

---

# 2. Functional Dependencies

## Students Table
- student_id → full_name, email, program_name, student_status, created_at
- email → full_name, program_name, student_status

## Courses Table
- course_id → course_name, instructor_name, start_date, end_date, created_at

## Enrollments Table
- enrollment_id → student_id, course_id, enrollment_date, progress_percent, record_source
- student_id, course_id → enrollment_date, progress_percent, record_source

## Assignments Table
- assignment_id → course_id, title, max_score, due_date, created_at
- course_id, title → max_score, due_date

## Submissions Table
- submission_id → assignment_id, student_id, submitted_at, score, grader_note, last_updated
- assignment_id, student_id → submitted_at, score, grader_note, last_updated

These dependencies helped identify where transitive dependencies and repeated information existed within the original schema.

---

# 3. Data Anomalies Identified

## Update Anomalies
Repeated values such as `program_name` and `instructor_name` created update problems.  
For example:
- Updating a program name required modifying multiple student records.
- Updating an instructor name required changing several course rows.

## Insertion Anomalies
The original design did not allow independent insertion of certain entities.
For example:
- A program could not exist without at least one student.
- An instructor could not be stored without assigning a course.

## Deletion Anomalies
Removing records could unintentionally remove important information.
For example:
- Deleting the final student from a program removed all information about that program.
- Deleting the last course taught by an instructor removed the instructor information completely.

These anomalies showed that the original schema required decomposition into a more normalized structure.

---

# 4. Normalization Process

## Step 1: Program Table Separation

The `students` table originally stored repeating `program_name` values.  
To remove redundancy, the following decomposition was performed:

### Before
students(student_id, full_name, email, program_name, student_status)

### After
- programs(program_id, program_name)
- students(student_id, full_name, email, program_id, student_status)

This ensured that program information is stored only once and referenced through a foreign key.

---

## Step 2: Instructor Table Separation

The `courses` table originally stored repeating instructor names.

### Before
courses(course_id, course_name, instructor_name)

### After
- instructors(instructor_id, instructor_name)
- courses(course_id, course_name, instructor_id)

This removed repeated instructor data and improved maintainability.

---

## Step 3: Relationship and Constraint Improvements

The `enrollments` and `submissions` tables were refined using unique constraints and foreign keys.

### Enrollment Constraint
UNIQUE(student_id, course_id)

This prevents duplicate student enrollments for the same course.

### Submission Constraint
UNIQUE(assignment_id, student_id)

This ensures one submission per student per assignment.

These changes improved data integrity and relationship consistency across the database.

---

# 5. Final Database Structure

## Programs
- program_id (PK)
- program_name (UNIQUE)

## Instructors
- instructor_id (PK)
- instructor_name (UNIQUE)

## Students
- student_id (PK)
- full_name
- email (UNIQUE)
- program_id (FK)
- student_status
- created_at

## Courses
- course_id (PK)
- course_name
- instructor_id (FK)
- start_date
- end_date
- created_at

## Enrollments
- enrollment_id (PK)
- student_id (FK)
- course_id (FK)
- enrollment_date
- progress_percent
- record_source
- UNIQUE(student_id, course_id)

## Assignments
- assignment_id (PK)
- course_id (FK)
- title
- max_score
- due_date
- created_at

## Submissions
- submission_id (PK)
- assignment_id (FK)
- student_id (FK)
- submitted_at
- score
- grader_note
- last_updated
- UNIQUE(assignment_id, student_id)

---

# 6. Why This Design is in 3NF

The final schema satisfies the requirements of Third Normal Form (3NF) because:

- Every table contains a clearly defined primary key.
- All non-key attributes depend only on the primary key.
- No transitive dependencies exist in the final design.
- Repeating descriptive attributes such as instructor names and program names were separated into dedicated tables.
- Foreign keys properly maintain relationships between entities.
- Unique constraints enforce consistency and prevent duplicate records.

This design minimizes redundancy while improving scalability and maintainability.

---

# 7. How This Connects to the Application

The normalized database directly supports the functionality of the Academic Progress Management System application.

## Students Module
The `students` table stores student information while linking each student to a program through `program_id`.

## Courses Module
The `courses` table connects each course to an instructor using `instructor_id`.

## Enrollment Module
The `enrollments` table manages the many-to-many relationship between students and courses.

## Assignment and Submission Module
Assignments belong to courses, while submissions track student performance and grading information.

## Dashboard and Analytics
The normalized relationships allow the dashboard to calculate:
- total students
- total enrollments
- average progress
- assignment statistics
- submission summaries

The design also improves query efficiency and keeps the application logic cleaner and easier to maintain.

---

## 8. Conclusion

The normalization process significantly improved the quality of the database design for the Academic Progress Management System. By separating repeating data into independent relational tables, the final schema reduced redundancy, eliminated update and deletion anomalies, and strengthened overall data integrity.

The database was successfully transformed into Third Normal Form (3NF), resulting in a cleaner and more scalable structure that supports CRUD operations, dashboard reporting, enrollment management, assignment tracking, and submission processing efficiently.

The final design is well-structured, maintainable, and aligned with the functional requirements of the DBMS Project 3 application.

