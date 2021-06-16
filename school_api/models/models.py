from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# todo unique combination student_id course_id
student_course = db.Table('student_model',
                          db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                          db.Column('course_id', db.Integer, db.ForeignKey('course.id')))


class CourseModel(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())

    students = db.relationship('StudentModel',  secondary=student_course)

    def __repr__(self):
        return f'course name: {self.name}'


class GroupModel(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    students = db.relationship('StudentModel', backref='group')

    def __repr__(self):
        return f'group name: {self.name}'


class StudentModel(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'),  nullable=True)
    courses = db.relationship('CourseModel',  secondary=student_course)

    def __repr__(self):
        return f'first name: {self.first_name}, last name: {self.last_name}'
