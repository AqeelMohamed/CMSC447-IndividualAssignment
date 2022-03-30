import sqlite3
from flask import render_template, session, flash, redirect, url_for
from app import app
from app.forms import *

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/schedule')
def schedule():
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute("select instructor.name, course.title from instructor inner join course on course.instructor_id = instructor.instructor_id")
    return render_template('schedule.html', list=crsr.fetchall())

@app.route('/student', methods=['GET', 'POST'])
def student():
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute("select name from student")
    students = [x[0] for x in crsr.fetchall()]
    return render_template('student.html', list=students)

@app.route('/add_student', methods=['GET', 'POST'])
def addStudent():
    form = AddStudent()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute("select student.student_id, student.name from student")
    studentList = crsr.fetchall()
    if form.validate_on_submit():
        flash('Student {} with ID {} and {} credits has been added!'.format(
            form.name.data, form.student_id.data, form.credits_earned.data
        ))

        # Add entry to database
        crsr.execute("INSERT INTO student(student_id, credits_earned, name) VALUES (?, ?, ?)", (form.student_id.data, form.credits_earned.data, form.name.data))
        connection.commit()

        return redirect('/add_student')
    return render_template('add_student.html', title='Add Student', form=form, studentList=studentList)

@app.route('/add_instructor', methods=['GET', 'POST'])
def addInstructor():
    form = AddInstructor()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute('SELECT instructor.instructor_id, instructor.name from instructor')
    insList = crsr.fetchall()
    if form.validate_on_submit():
        flash('Instructor {} with ID {} and part of the {} department has been added!'.format(
            form.name.data, form.instructor_id.data, form.department.data
        ))

        # Add entry to database
        crsr.execute("INSERT INTO instructor(instructor_id, name, department) VALUES (?, ?, ?)", (form.instructor_id.data, form.name.data, form.department.data))
        connection.commit()

        return redirect('/add_instructor')
    return render_template('add_instructor.html', title='Add Instructor', form=form, insList=insList)

@app.route('/add_course', methods=['GET', 'POST'])
def addCourse():
    form = AddCourse()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute('SELECT instructor.instructor_id, instructor.name from instructor')
    insList = crsr.fetchall()
    crsr.execute('SELECT course.course_id, course.title from course')
    courseList = crsr.fetchall()
    if form.validate_on_submit():
        flash('Course {} with ID {} and taught by instructor {} has been added!'.format(
            form.title.data, form.course_id.data, form.instructor_id.data 
        ))

        # Add entry to database
        crsr.execute("INSERT INTO course (course_id, instructor_id, title) VALUES (?, ?, ?)", (form.course_id.data, form.instructor_id.data, form.title.data))
        connection.commit()

        return redirect('/add_course')
    return render_template('add_course.html', title='Add Course', form=form, insList=insList, courseList=courseList)

@app.route('/remove_student', methods=['GET', 'POST'])
def removeStudent():
    form = RemoveStudent()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute("select student.student_id, student.name from student")
    studentList = crsr.fetchall()

    if form.validate_on_submit():
        flash('Student ID {} has been removed!'.format(form.student_id.data))

        # Remove entry from database
        crsr.execute('DELETE FROM student where student.student_id = ?', (form.student_id.data,))
        connection.commit()

        return redirect('/remove_student')
    return render_template('remove_student.html', title='Remove Student', form=form, studentList=studentList)

@app.route('/remove_instructor', methods=['GET', 'POST'])
def removeInstructor():
    form = RemoveInstructor()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute('SELECT instructor.instructor_id, instructor.name from instructor')
    insList = crsr.fetchall()
    if form.validate_on_submit():
        flash('Instructor ID {} has been removed!'.format(form.instructor_id.data))

        # Add entry to database
        crsr.execute('DELETE FROM instructor where instructor.instructor_id = ?', (form.instructor_id.data,))
        connection.commit()

        return redirect('/remove_instructor')
    return render_template('remove_instructor.html', title='Remove Instructor', form=form, insList=insList)

@app.route('/remove_course', methods=['GET', 'POST'])
def removeCourse():
    form = RemoveCourse()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute('SELECT course.course_id, course.title from course')
    courseList = crsr.fetchall()
    if form.validate_on_submit():
        flash('Course ID {} has been removed!'.format(form.course_id.data))

        # Add entry to database
        crsr.execute('SELECT record.course_id from record where record.course_id = ?', (form.course_id.data,))
        if len(crsr.fetchall()) != 0:
            crsr.execute('DELETE FROM record where record.course_id = ?', (form.course_id.data,))
        crsr.execute('DELETE FROM course where course.course_id = ?', (form.course_id.data,))
        connection.commit()

        return redirect('/remove_course')
    return render_template('remove_course.html', title='Remove Course', form=form, courseList=courseList)


@app.route('/ask_for_id', methods=['GET', 'POST'])
def askForStudentID():
    form = AskForStudentID()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()
    crsr.execute("select student.student_id, student.name from student")
    studentList = crsr.fetchall()

    if form.validate_on_submit():
        session['student_id'] = form.student_id.data
        return redirect(url_for('studentSchedule'))
    return render_template('ask_for_studentID.html', title='Student ID', form=form, studentList=studentList)

@app.route('/student_schedule', methods=['GET', 'POST'])
def studentSchedule():
    if session['student_id']:
        connection = sqlite3.connect("app.db")
        crsr = connection.cursor()
        crsr.execute('select student.name, course.course_id, course.title, record.grade from student join record on student.student_id = record.student_id join course on course.course_id = record.course_id and student.student_id = ?', (session['student_id'],))
        studentSchedule = crsr.fetchall()
        crsr.execute('select student.name from student where student.student_id = ?', (session['student_id'],))
        studentName = crsr.fetchall()

        return render_template('student_schedule.html', title='Student ID', studentSchedule=studentSchedule, studentName=studentName[0])

@app.route('/add_course_to_student', methods=['GET', 'POST'])
def addCourseToStudent():
    form = AddCourseToStudent()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()

    crsr.execute('select student.name, course.course_id, course.title, record.grade from student join record on student.student_id = record.student_id join course on course.course_id = record.course_id and student.student_id = ?', (session['student_id'],))
    studentSchedule = crsr.fetchall()

    crsr.execute('select student.name from student where student.student_id = ?', (session['student_id'],))
    studentName = crsr.fetchall()

    crsr.execute('SELECT course.course_id, course.title from course')
    courseList = crsr.fetchall()
    if session['student_id']:
        if form.validate_on_submit():
            crsr.execute('INSERT INTO record (grade, course_id, student_id) VALUES (?, ?, ?)', (100, form.course_id.data, session['student_id']))
            connection.commit()

            flash('Course ID {} has been added!'.format(form.course_id.data))

            return redirect(url_for('addCourseToStudent'))

    return render_template('student_add_class.html', title='Add class to Student',  form=form, studentName=studentName, studentSchedule=studentSchedule, courseList=courseList)

@app.route('/remove_course_from_student', methods=['GET', 'POST'])
def removeCourseFromStudent():
    form = RemoveCourseFromStudent()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()

    crsr.execute('select student.name, course.course_id, course.title, record.grade from student join record on student.student_id = record.student_id join course on course.course_id = record.course_id and student.student_id = ?', (session['student_id'],))
    studentSchedule = crsr.fetchall()

    crsr.execute('select student.name from student where student.student_id = ?', (session['student_id'],))
    studentName = crsr.fetchall()

    if session['student_id']:
        if form.validate_on_submit():
            crsr.execute('DELETE from record where record.course_id = ? and record.student_id = ?', (form.course_id.data, session['student_id']))
            connection.commit()

            flash('Course ID {} has been removed from {}!'.format(form.course_id.data, studentName))

            return redirect(url_for('removeCourseFromStudent'))

    return render_template('student_remove_class.html', title='Add class to Student', form=form,  studentSchedule=studentSchedule, studentName=studentName)

@app.route('/change_grade', methods=['GET', 'POST'])
def changeGradeInClass():
    form = ChangeGradeInClass()
    connection = sqlite3.connect("app.db")
    crsr = connection.cursor()

    crsr.execute('select student.name, course.course_id, course.title, record.grade from student join record on student.student_id = record.student_id join course on course.course_id = record.course_id and student.student_id = ?', (session['student_id'],))
    studentSchedule = crsr.fetchall()

    crsr.execute('select student.name from student where student.student_id = ?', (session['student_id'],))
    studentName = crsr.fetchall()

    if session['student_id']:
        if form.validate_on_submit():
            crsr.execute('UPDATE record SET grade = ? where record.student_id = ? and record.course_id = ?;', (form.grade.data,  session['student_id'], form.course_id.data))
            connection.commit()

            flash('Course ID {} has been updated to {}!'.format(form.course_id.data, form.grade.data))

            return redirect(url_for('changeGradeInClass'))

    return render_template('change_grade_in_class.html', title='Change Grade in Class', form=form,  studentSchedule=studentSchedule, studentName=studentName)