import string
import itertools
import random
from .models.models import (StudentModel as Student,
                            GroupModel as Group,
                            CourseModel as Course,
                            student_course,
                            db)


random.seed(42)


def create_random_groups():
    alphabetic_pairs = list(itertools.combinations_with_replacement(string.digits, 2))
    digit_pairs = list(itertools.combinations_with_replacement(string.ascii_uppercase, 2))

    alphabetic_pairs = [''.join(pair) for pair in alphabetic_pairs]
    digit_pairs = [''.join(pair) for pair in digit_pairs]

    groups = random.sample(list(itertools.product(digit_pairs, alphabetic_pairs)), 10)

    groups = ['-'.join(s) for s in groups]

    return groups


def create_random_students():
    first_names = ['Cristen', 'Kara', 'Fausto', 'Elizbeth', 'Marinda', 'Buddy', 'Lyla', 'Jeremiah', 'Raeann',
                   'Micheline', 'Sylvester', 'Cortez', 'Cherly', 'Angel', 'Ramona', 'Raul', 'Olympia', 'Zulma',
                   'Lourie', 'Alba']
    last_names = ['Forrest', 'Stewart', 'Molina', 'Rowe', 'Harrison', 'Humphreys', 'Lewis', 'Harmon', 'Oliver',
                  'Whelan', 'Glover', 'Castillo', 'Guerrero', 'Briggs', 'Richardson', 'Gonzalez', 'Baker', 'Wilson',
                  'Duncan', 'Black']

    students = random.sample(list(itertools.product(first_names, last_names)), 200)

    return students


def assign_students_to_courses(app):
    with app.app_context():
        students = Student.query.all()
        courses = Course.query.all()
        for student in students:
            for course in random.sample(courses, k=random.randint(1, 3)):
                db.session.execute(student_course.insert().values(student_id=student.id, course_id=course.id))

        db.session.commit()


def test_db(app):
    courses = [('English', 'Study of literature (especially novels, plays, short stories, and poetry)'),
               ('Math', 'Includes the study of such topics as quantity (number theory), structure (algebra),'
                        ' space (geometry), and change (mathematical analysis).'),
               ('Biology', 'Natural science that studies life and living organisms, including their physical structure,'
                           ' chemical processes, molecular interactions, physiological mechanisms,'
                           ' development and evolution.'),
               ('Chemistry', 'Scientific discipline involved with elements and compounds composed of atoms, '
                             'molecules and ions: their composition, structure, properties, behavior and the changes'
                             ' they undergo during a reaction with other substances.'),
               ('Physics', 'Natural science that studies matter, its motion and behavior through space and time, '
                           'and the related entities of energy and force.'),
               ('Economics', 'Social science that studies how people interact with things of value; in particular, '
                             'the production, distribution, and consumption of goods and services.'),
               ('Geography', 'Science devoted to the study of the lands, features, inhabitants, and phenomena '
                             'of the Earth and planets.'),
               ('History', 'Study of the past.'),
               ('Arts', 'Refers to the theory, human application and physical expression of creativity found in'
                        ' human cultures and societies through skills and imagination in order to produce objects,'
                        ' environments and experiences.'),
               ('Computer science', 'Study of algorithmic processes and computational machines.')]

    students = create_random_students()
    groups = create_random_groups()

    with app.app_context():
        for group in groups:
            group = Group(name=group)
            for _ in range(random.randint(10, 30)):
                try:
                    first_name, last_name = students.pop()
                except IndexError:
                    break
                Student(first_name=first_name, last_name=last_name, group=group)
            db.session.add(group)

        db.session.commit()

        if students:
            for student in students:
                first_name, last_name = student
                db.session.add(Student(first_name=first_name, last_name=last_name))
            db.session.commit()

        for course in courses:
            name, description = course
            db.session.add(Course(name=name, description=description))

        db.session.commit()

        assign_students_to_courses(app)
