from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from . import db
from .models import Program, Instructor, Student, Course, Enrollment, Assignment, Submission

main = Blueprint('main', __name__)

def required(value, field):
    if not value or not value.strip():
        raise ValueError(f'{field} is required.')
    return value.strip()

def parse_date(value, field):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError as exc:
        raise ValueError(f'{field} must be a valid date.') from exc

@main.route('/')
def dashboard():
    totals = {
        'students': db.session.scalar(db.select(func.count(Student.student_id))),
        'courses': db.session.scalar(db.select(func.count(Course.course_id))),
        'enrollments': db.session.scalar(db.select(func.count(Enrollment.enrollment_id))),
        'submissions': db.session.scalar(db.select(func.count(Submission.submission_id))),
        'average_score': db.session.scalar(db.select(func.avg(Submission.score))) or 0,
        'average_progress': db.session.scalar(db.select(func.avg(Enrollment.progress_percent))) or 0,
    }
    course_summary = db.session.query(
        Course.course_name,
        func.count(Enrollment.enrollment_id).label('enrolled'),
        func.avg(Enrollment.progress_percent).label('avg_progress')
    ).outerjoin(Enrollment).group_by(Course.course_id).all()
    return render_template('dashboard.html', totals=totals, course_summary=course_summary)

@main.route('/students')
def students():
    return render_template('students.html', students=Student.query.order_by(Student.full_name).all())

@main.route('/students/new', methods=['GET', 'POST'])
def new_student():
    if request.method == 'POST':
        try:
            full_name = required(request.form.get('full_name'), 'Full name')
            email = required(request.form.get('email'), 'Email')
            program_name = required(request.form.get('program_name'), 'Program')
            status = required(request.form.get('student_status'), 'Status')
            if '@' not in email:
                raise ValueError('Email must contain @.')
            program = Program.query.filter_by(program_name=program_name).first() or Program(program_name=program_name)
            db.session.add(program)
            db.session.add(Student(full_name=full_name, email=email, program=program, student_status=status))
            db.session.commit()
            flash('Student saved successfully.', 'success')
            return redirect(url_for('main.students'))
        except Exception as error:
            db.session.rollback()
            flash(str(error), 'danger')
    return render_template('student_form.html')

@main.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        try:
            student.full_name = required(request.form.get('full_name'), 'Full name')
            student.email = required(request.form.get('email'), 'Email')
            student.student_status = required(request.form.get('student_status'), 'Status')
            program_name = required(request.form.get('program_name'), 'Program')
            student.program = Program.query.filter_by(program_name=program_name).first() or Program(program_name=program_name)
            db.session.commit()
            flash('Student updated.', 'success')
            return redirect(url_for('main.students'))
        except Exception as error:
            db.session.rollback()
            flash(str(error), 'danger')
    return render_template('student_form.html', student=student)

@main.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted.', 'warning')
    return redirect(url_for('main.students'))

@main.route('/courses')
def courses():
    return render_template('courses.html', courses=Course.query.order_by(Course.course_name).all())

@main.route('/courses/new', methods=['GET', 'POST'])
def new_course():
    if request.method == 'POST':
        try:
            name = required(request.form.get('course_name'), 'Course name')
            instructor_name = required(request.form.get('instructor_name'), 'Instructor')
            start_date = parse_date(request.form.get('start_date'), 'Start date')
            end_date = parse_date(request.form.get('end_date'), 'End date')
            if end_date < start_date:
                raise ValueError('End date cannot be before start date.')
            instructor = Instructor.query.filter_by(instructor_name=instructor_name).first() or Instructor(instructor_name=instructor_name)
            db.session.add(instructor)
            db.session.add(Course(course_name=name, instructor=instructor, start_date=start_date, end_date=end_date))
            db.session.commit()
            flash('Course saved successfully.', 'success')
            return redirect(url_for('main.courses'))
        except Exception as error:
            db.session.rollback()
            flash(str(error), 'danger')
    return render_template('course_form.html')

@main.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)

@main.route('/courses/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted.', 'warning')
    return redirect(url_for('main.courses'))

@main.route('/enrollments/new', methods=['GET', 'POST'])
def new_enrollment():
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('student_id'))
            course_id = int(request.form.get('course_id'))
            progress = float(request.form.get('progress_percent') or 0)
            if progress < 0 or progress > 100:
                raise ValueError('Progress must be between 0 and 100.')
            enrollment = Enrollment(
                student_id=student_id,
                course_id=course_id,
                enrollment_date=parse_date(request.form.get('enrollment_date'), 'Enrollment date'),
                progress_percent=progress,
                record_source=required(request.form.get('record_source'), 'Record source')
            )
            db.session.add(enrollment)
            db.session.commit()
            flash('Enrollment created.', 'success')
            return redirect(url_for('main.course_detail', course_id=course_id))
        except Exception as error:
            db.session.rollback()
            flash(str(error), 'danger')
    return render_template('enrollment_form.html', students=Student.query.all(), courses=Course.query.all())

@main.route('/submissions/new', methods=['GET', 'POST'])
def new_submission():
    if request.method == 'POST':
        try:
            assignment = Assignment.query.get_or_404(int(request.form.get('assignment_id')))
            score = float(request.form.get('score'))
            if score < 0 or score > assignment.max_score:
                raise ValueError('Score must be from 0 to the assignment maximum score.')
            # Transaction feature: save a submission and update enrollment progress together.
            submission = Submission(
                assignment_id=assignment.assignment_id,
                student_id=int(request.form.get('student_id')),
                submitted_at=datetime.now(),
                score=score,
                grader_note=request.form.get('grader_note', '').strip()
            )
            db.session.add(submission)
            enrollment = Enrollment.query.filter_by(student_id=submission.student_id, course_id=assignment.course_id).first()
            if enrollment:
                enrollment.progress_percent = min(float(enrollment.progress_percent) + 5, 100)
            db.session.commit()
            flash('Submission saved and progress updated in one transaction.', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as error:
            db.session.rollback()
            flash(str(error), 'danger')
    return render_template('submission_form.html', students=Student.query.all(), assignments=Assignment.query.all())

@main.route('/seed')
def seed_data():
    if Student.query.first():
        flash('Seed data already exists.', 'info')
        return redirect(url_for('main.dashboard'))
    cs = Program(program_name='Computer Science')
    ds = Program(program_name='Data Science')
    inst1 = Instructor(instructor_name='Dr. Miller')
    inst2 = Instructor(instructor_name='Prof. Shah')
    s1 = Student(full_name='Asha Kumar', email='asha@example.edu', program=cs, student_status='Active')
    s2 = Student(full_name='Brian Lee', email='brian@example.edu', program=ds, student_status='Active')
    c1 = Course(course_name='Database Management Systems', instructor=inst1, start_date=parse_date('2026-01-15','Start'), end_date=parse_date('2026-05-10','End'))
    c2 = Course(course_name='Python Web Development', instructor=inst2, start_date=parse_date('2026-01-20','Start'), end_date=parse_date('2026-05-05','End'))
    a1 = Assignment(course=c1, title='Normalization Report', max_score=100, due_date=parse_date('2026-03-01','Due'))
    db.session.add_all([cs, ds, inst1, inst2, s1, s2, c1, c2, a1])
    db.session.flush()
    db.session.add_all([
        Enrollment(student=s1, course=c1, enrollment_date=parse_date('2026-01-16','Enrollment'), progress_percent=30, record_source='Registrar'),
        Enrollment(student=s2, course=c1, enrollment_date=parse_date('2026-01-17','Enrollment'), progress_percent=20, record_source='Registrar')
    ])
    db.session.commit()
    flash('Sample data inserted.', 'success')
    return redirect(url_for('main.dashboard'))
