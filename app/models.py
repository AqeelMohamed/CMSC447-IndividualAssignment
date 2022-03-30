from app import db

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    credits_earned = db.Column(db.Integer)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Student {}> has {} credits'.format(self.name, self.credits_earned)

class Instructor(db.Model):
    instructor_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    department = db.Column(db.String)

    def __repr__(self):
        return '<Instructor {}:{}> is a part of {}'.format(self.instructor_id, self.instructor_name, self.course_department)

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.instructor_id'))
    title = db.Column(db.String)
    
    def __repr__(self):
        return '<Course {}:>'.format(self.title)

class Record(db.Model):
    grade = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    db.PrimaryKeyConstraint(course_id, student_id)

    def __repr__(self):
        return '<Student {}> earned a {} in <Course {}>'.format(self.student_id, self.grade, self.course_id)