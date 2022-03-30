import sqlite3
from flask import flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

# Required Forms that are needed
class AddStudent(FlaskForm):
    def checkForStudent(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select student.student_id from student where student.student_id == ?', (form.student_id.data,))
        if len(crsr.fetchall()) != 0:
            flash('Student already exists! Please make sure ID is unique!')
            redirect(url_for('addStudent'))
            raise ValidationError('Student already exists! Please make sure ID is unique!')

        return True
        
    student_id = IntegerField('Student ID', validators=[DataRequired('Not Allowed'), checkForStudent])
    name = StringField('Student Name', validators=[DataRequired('Not Allowed')])
    credits_earned = IntegerField('Credits Earned', validators=[DataRequired('Not Allowed')])
    submit = SubmitField('Add Student')

class AddCourse(FlaskForm):
    def checkForInstructor(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select instructor.instructor_id from instructor where instructor.instructor_id == ?', (form.instructor_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Instructor does not exist! Please make sure ID is in the instructor table!')
            redirect(url_for('addCourse'))
            raise ValidationError('Instructor does not exist! Please make sure ID is in the instructor table!')
        return True

    def checkForCourse(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select course.course_id from course where course.course_id == ?', (form.course_id.data,))
        if len(crsr.fetchall()) != 0:
            flash('Course already exists! Please make sure ID is unique!')
            redirect(url_for('addCourse'))
            raise ValidationError('Course already exists! Please make sure ID is unique!')
        return True

    course_id = IntegerField('Course ID', validators=[DataRequired(), checkForCourse])
    instructor_id = IntegerField('Instructor ID', validators=[DataRequired(), checkForInstructor])
    title = StringField('Course Title', validators=[DataRequired()])
    submit = SubmitField('Add Course')

class AddInstructor(FlaskForm):
    def checkForInstructor(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select instructor.instructor_id from instructor where instructor.instructor_id == ?', (form.instructor_id.data,))
        if len(crsr.fetchall()) != 0:
            flash('Instructor already exists! Please make sure ID is unique!')
            redirect(url_for('addInstructor'))
            raise ValidationError('Instructor already exists! Please make sure ID is unique!')
        return True

    instructor_id = IntegerField('Instructor ID', validators=[DataRequired(), checkForInstructor])
    name = StringField('Instructor Name', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Add Instructor')

class RemoveStudent(FlaskForm):
    def checkForStudent(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select student.student_id from student where student.student_id == ?', (form.student_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Student does not exist! Please make sure ID is in the Student Table!')
            redirect(url_for('removeStudent'))
            raise ValidationError('Student does not exist! Please make sure ID is in the Student Table!')
        return True
    
    student_id = IntegerField('Student ID', validators=[DataRequired('Not Allowed'), checkForStudent])
    submit = SubmitField('Remove Student')

class RemoveInstructor(FlaskForm):
    def checkForInstructor(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select instructor.instructor_id from instructor where instructor.instructor_id == ?', (form.instructor_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Instructor does not exist! Please make sure ID is in the Instructor Table!')
            redirect(url_for('removeInstructor'))
            raise ValidationError('Instructor does not exist! Please make sure ID is in the Instructor Table!')
        return True
    
    instructor_id = IntegerField('Instructor ID', validators=[DataRequired('Not Allowed'), checkForInstructor])
    submit = SubmitField('Remove Instructor')

class RemoveCourse(FlaskForm):
    def checkForCourse(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select course.course_id from course where course.course_id == ?', (form.course_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Course does not exist! Please make sure ID is in the Course Table!')
            redirect(url_for('removeCourse'))
            raise ValidationError('Course does not exist! Please make sure ID is in the Course Table!')
        return True
    
    course_id = IntegerField('Course ID', validators=[DataRequired('Not Allowed'), checkForCourse])
    submit = SubmitField('Remove Course')

class AskForStudentID(FlaskForm):
    def checkForStudent(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select student.student_id from student where student.student_id == ?', (form.student_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Student does not exist! Please make sure ID is in the Student Table!')
            redirect(url_for('askForStudentID'))
            raise ValidationError('Student does not exist! Please make sure ID is in the Student Table!')
        return True
    
    student_id = IntegerField('Student ID', validators=[DataRequired('Not Allowed'), checkForStudent])
    submit = SubmitField('See Student Schedule')

class AddCourseToStudent(FlaskForm):
    def checkForCourse(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select course.course_id from course where course.course_id == ?', (form.course_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Course does not exist! Please make sure ID is in the Course Table!')
            redirect(url_for('addCourseToStudent'))
            raise ValidationError('Course does not exist! Please make sure ID is in the Course Table!')
        return True
    
    def checkForDuplicateClass(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select student.name, course.title, record.grade from student join record on student.student_id = record.student_id join course on course.course_id = record.course_id and student.student_id = ? and course.course_id = ?', (session['student_id'], form.course_id.data,))
        if len(crsr.fetchall()) != 0:
            flash('This student is already enrolled in that course! Choose another!')
            redirect(url_for('addCourseToStudent'))
            raise ValidationError('This student is already enrolled in that course! Choose another!')

    course_id = IntegerField('Course ID', validators=[DataRequired('Not Allowed'), checkForCourse, checkForDuplicateClass])
    submit = SubmitField('Add Course to Student') 

class RemoveCourseFromStudent(FlaskForm):
    def checkForCourse(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select course.course_id from course where course.course_id == ?', (form.course_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Course does not exist! Please make sure ID is in the Course Table!')
            redirect(url_for('removeCourseFromStudent'))
            raise ValidationError('Course does not exist! Please make sure ID is in the Course Table!')
        return True

    def checkStudentHasCourse(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select student.name, course.title, record.grade from student join record on student.student_id = record.student_id join course on course.course_id = record.course_id and student.student_id = ? and course.course_id = ?', (session['student_id'], form.course_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Student is not enrolled in that class! Choose another!')
            redirect(url_for('removeCourseFromStudent'))
            raise ValidationError('Student is not enrolled in that class! Choose another!')
        return True

    course_id = IntegerField('Course ID', validators=[DataRequired('Not Allowed'), checkForCourse, checkStudentHasCourse])
    submit = SubmitField('Remove Student from Course') 

class ChangeGradeInClass(FlaskForm):
    def checkStudentHasCourse(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select student.name, course.title, record.grade from student join record on student.student_id = record.student_id join course on course.course_id = record.course_id and student.student_id = ? and course.course_id = ?', (session['student_id'], form.course_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Student is not enrolled in that class! Choose another!')
            redirect(url_for('changeGradeInClass'))
            raise ValidationError('Student is not enrolled in that class! Choose another!')
        return True

    def checkForValidGrade(form, field):
        if form.grade.data >= 0 and form.grade.data <= 100:
            return True
        flash('That grade is not allowed! Choose one between 0-100!')
        redirect(url_for('changeGradeInClass'))
        raise ValidationError('That grade is not allowed! Choose one between 0-100!')

    def checkForCourse(form, field):
        connection = sqlite3.connect('app.db')
        crsr = connection.cursor()
        crsr.execute('select course.course_id from course where course.course_id == ?', (form.course_id.data,))
        if len(crsr.fetchall()) == 0:
            flash('Course does not exist! Please make sure ID is in the Course Table!')
            redirect(url_for('changeGradeInClass'))
            raise ValidationError('Course does not exist! Please make sure ID is in the Course Table!')
        return True
    
    course_id = IntegerField('Course ID', validators=[DataRequired('Not Allowed'), checkForCourse, checkStudentHasCourse])
    grade = IntegerField('Grade', validators=[DataRequired('Not Allowed'), checkForValidGrade])
    submit = SubmitField('Change grade in class')