from . import db

class Program(db.Model):
    __tablename__ = 'programs'
    program_id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(100), nullable=False, unique=True)
    students = db.relationship('Student', back_populates='program')

class Instructor(db.Model):
    __tablename__ = 'instructors'
    instructor_id = db.Column(db.Integer, primary_key=True)
    instructor_name = db.Column(db.String(100), nullable=False, unique=True)
    courses = db.relationship('Course', back_populates='instructor')

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.program_id'), nullable=False)
    student_status = db.Column(db.String(20), nullable=False, default='Active')
    program = db.relationship('Program', back_populates='students')
    enrollments = db.relationship('Enrollment', back_populates='student', cascade='all, delete-orphan')
    submissions = db.relationship('Submission', back_populates='student', cascade='all, delete-orphan')

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.instructor_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    instructor = db.relationship('Instructor', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course', cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', back_populates='course', cascade='all, delete-orphan')

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    progress_percent = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    record_source = db.Column(db.String(50), nullable=False)
    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='uq_student_course'),)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    assignment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    course = db.relationship('Course', back_populates='assignments')
    submissions = db.relationship('Submission', back_populates='assignment', cascade='all, delete-orphan')

class Submission(db.Model):
    __tablename__ = 'submissions'
    submission_id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    submitted_at = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Numeric(5, 2), nullable=False)
    grader_note = db.Column(db.String(255))
    assignment = db.relationship('Assignment', back_populates='submissions')
    student = db.relationship('Student', back_populates='submissions')
    __table_args__ = (db.UniqueConstraint('assignment_id', 'student_id', name='uq_assignment_student'),)
