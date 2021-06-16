from flask import abort, request
from flask_restful import Resource
from school_api.models import GroupModel, StudentModel, CourseModel, student_course, db
from school_api.services.services import *
from ...schema.school_schema import GroupSchema, StudentSchema, CourseSchema
from sqlalchemy.orm.exc import FlushError


class Courses(Resource):
    def get(self):
        """
        All courses
        ---
        tags:
            - Courses
        description: "Returns all courses"
        responses:
          200:
            description: all courses
            schema:
              type: array
              items:
                $ref: "#/definitions/course"
        produces:
            - application/json
        """
        courses = GroupModel.query.all()
        courses = CourseSchema().dump(courses, many=True)

        return courses

    def post(self):
        """
        Create course
        ---
        tags:
            - Courses
        description: "Add new course to database"
        consumes:
          - application/json
        parameters:
          - name: "course_name"
            in: "body"
            description: "New course name"
            required: true
            schema:
              type: "object"
              properties:
                course_name:
                  type: string
          - name: "description"
            in: "body"
            description: "description of course"
            required: false
            schema:
              type: "object"
              properties:
                description:
                  type: string
        responses:
          201:
            description: course was created
            schema:
              $ref: "#/definitions/course"
          400:
            description:  Invalid input
        produces:
            - application/json
        """
        req = request.get_json()
        name = req.get('course_name')
        description = req.get('description')
        if name is None:
            abort(400)
        course = add_course(name, description)
        course = CourseSchema().dump(course)

        return course, 201


class Course(Resource):
    def get(self, course_id):
        """
        Get course by id
        ---
        tags:
            - Courses
        description: Returns a single course
        parameters:
          - name: "course_id"
            in: "path"
            description: "ID of course to return"
            required: true
        responses:
          200:
            description: course
            schema:
                $ref: "#/definitions/course"
          404:
            description: course does not exist
        produces:
            - application/json
        """
        course = CourseModel.query.get_or_404(course_id)
        course = CourseSchema().dump(course)

        return course

    def put(self, course_id):
        """
        Edit course
        ---
        tags:
            - Courses
        description: Rename group or change description
        consumes:
          - application/json
        parameters:
          - name: "course_id"
            in: "path"
            description: "ID of student"
            required: true
          - name: "course_name"
            in: "body"
            description: "New course name"
            required: true
            schema:
              type: "object"
              properties:
                course_name:
                  type: string
          - name: "description"
            in: "body"
            description: "description of course"
            required: false
            schema:
              type: "object"
              properties:
                description:
                  type: string
        responses:
          200:
            description: edit successful
            schema:
              $ref: "#/definitions/course"
          404:
            description: course does not exist
          500:
            description: Invalid input
        produces:
            - application/json
        """
        req = request.get_json(force=True)
        name = req.get('course_name')
        description = req.get('description')

        course = edit_course(course_id, name, description)
        course = CourseSchema().dump(course)

        return course

    def delete(self, course_id):
        """
        Delete course
        ---
        tags:
            - Courses
        description: Delete course by id
        parameters:
          - name: "course_id"
            in: "path"
            description: "ID of course to delete"
            required: true
        responses:
          204:
            description: course deleted
          404:
            description: course does not exist
        """
        del_course(course_id)

        return None, 204


class StudentsByCourse (Resource):
    def get(self, course_id):
        """
        All students on course
        ---
        tags:
          - Courses
        description: Returns all students on this course
        parameters:
          - name: "course_id"
            in: "path"
            description: "ID of course"
            required: true
        responses:
          200:
            description: students
            schema:
              type: array
              items:
                $ref: "#/definitions/student"
          404:
            description: course does not exist
        produces:
            - application/json
        """
        main_query = (db.session.query(StudentModel)
                      .join(StudentModel.courses)
                      .filter(CourseModel.id == course_id))
        students = main_query.all()
        students = StudentSchema().dump(students, many=True)
        return students

    def post(self, course_id):
        """
        Add students to course
        ---
        tags:
            - Courses
        parameters:
          - name: "course_id"
            in: "path"
            description: "ID of course"
            required: true
          - name: "students"
            in: "body"
            description: "list of students ids that will be added to course"
            required: true
            schema:
              type: "object"
              properties:
                students:
                  type: array
                  items: integer
                  example: [1, 2, 3]
        responses:
          200:
            description: students
            schema:
              type: array
              items:
                $ref: "#/definitions/student"
          404:
            description: course does not exist
          500:
            description: bad request
        consumes:
            - application/json
        """
        req = request.get_json(force=True)
        students = req.get('students')
        course = CourseModel.query.get_or_404(course_id)
        for student_id in students:
            try:
                course.students.append(StudentModel.query.get_or_404(student_id))
            except FlushError:
                abort(400, f'student with id={student_id} does not exist')
        db.session.commit()

        return None, 201

    def delete(self, course_id):
        """
        Remove students from course
        ---
        tags:
            - Courses
        parameters:
          - name: "course_id"
            in: "path"
            description: "ID of course"
            required: true
          - name: "students"
            in: "body"
            description: "list of students ids that will be removed from course"
            required: true
            schema:
              type: "object"
              properties:
                students:
                  type: array
                  items: integer
                  example: [1, 2, 3]
        responses:
          200:
            description: students
          404:
            description: course does not exist
          500:
            description: bad request
        consumes:
          - application/json
        """
        req = request.get_json()
        students = req.get('students')
        course = CourseModel.query.get_or_404(course_id)
        for student_id in students:
            try:
                course.students.remove(StudentModel.query.get_or_404(student_id))
            except ValueError:
                abort(400, f'student with id={student_id} does not exist')
        db.session.commit()

        return None, 204
