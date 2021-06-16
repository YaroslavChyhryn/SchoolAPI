from school_api.models import (StudentModel as Student,
                               GroupModel as Group,
                               CourseModel as Course,
                               student_course,
                               db)
from flask import abort


def add_group(name):
    # todo name validator
    group = Group(name=name)
    db.session.add(group)
    db.session.commit()

    return group


def edit_group(group_id, name):
    # todo name validator
    if Group.query.filter_by(name=name).first() is not None:
        abort(400, f'group with name {name} already exist')
    group = Group.query.get_or_404(group_id)
    group.name = name
    db.session.commit()

    return group


def del_group(group_id):
    group = Group.query.get_or_404(group_id)
    db.session.delete(group)
    db.session.commit()

    return True


def add_student(first_name, last_name):
    # todo first name last name  validator
    student = Student(first_name=first_name, last_name=last_name, group_id=None)
    db.session.add(student)
    db.session.commit()

    return student


def edit_student(student_id, first_name=None, last_name=None):
    # todo first name last name  validator
    student = Student.query.get_or_404(student_id)
    if first_name:
        student.first_name = first_name
    if last_name:
        student.last_name = last_name
    db.session.commit()

    return student


def del_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()

    return True


def add_course(name, description=None):
    course = Course(name=name, description=description)
    db.session.add(course)
    db.session.commit()

    return course


def edit_course(course_id, name=None, description=None):
    course = Course.query.get_or_404(course_id)
    if name:
        if Course.query.filter_by(name=name).first() is not None:
            abort(400, f'course with name {name} already exist')
        course.name = name
    if description:
        course.description = description
    db.session.commit()

    return course


def del_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()

    return True


def add_student_to_group(student_id, group_id):
    # todo force param or another function for edit students group if student already assigned to group
    group = Group.query.get_or_404(group_id)
    group.students.append(Student.query.get_or_404(student_id))
    db.session.commit()

    return group


def remove_student_from_group(student, group_id):
    group = Group.query.get_or_404(group_id)
    group.students.remove(student)
    db.session.commit()

    return group


def select_group_with_less_students(number_of_students):
    main_query = (db.session.query(Group)
                  .join(Group.students)
                  .group_by(Group.id)
                  .having(db.func.count(Group.id) <= number_of_students))

    groups = main_query.all()
    return groups


def select_students_on_course_by_name(course_name):
    main_query = db.session.query(Student).join(Student.courses).filter(Course.name == course_name)
    students = main_query.all()
    return students
