from .models.models import (StudentModel as Student,
                            GroupModel as Group,
                            CourseModel as Course,
                            student_course,
                            db)


def create_tables(app):
    with app.app_context():
        db.create_all()


def drop_tables(app):
    with app.app_context():
        db.drop_all()
