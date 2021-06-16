from flask import abort, request
from flask_restful import Resource, reqparse
from school_api.models import GroupModel, StudentModel, CourseModel, student_course, db
from school_api.services.services import *
from ...schema.school_schema import GroupSchema, StudentSchema, CourseSchema
from sqlalchemy.orm.exc import FlushError


class Students(Resource):
    def get(self):
        """
        All students
        ---
        tags:
            - Students
        description: "Returns all students"
        parameters:
          - name: "course_name"
            in: query
            description: "Response will contain only students assigned to course(by course name)"
            type: "string"
        responses:
          200:
            description: all students
            schema:
              type: array
              items:
                $ref: "#/definitions/student"
        produces:
            - application/json
        """
        parser = reqparse.RequestParser()
        parser.add_argument('course_name', type=str)
        args = parser.parse_args()
        course_name = args['course_name']

        if course_name:
            students = select_students_on_course_by_name(course_name)
        else:
            students = StudentModel.query.all()
        students = StudentSchema().dump(students, many=True)

        return students

    def post(self):
        """
        Create student
        ---
        tags:
            - Students
        description: "Add new student to database"
        consumes:
            - application/json
        parameters:
          - name: "first name"
            in: "body"
            description: "student first name"
            required: true
            schema:
              type: "object"
              properties:
                first_name:
                  type: string
          - name: "last_name"
            in: "body"
            description: "student last name"
            required: true
            schema:
              type: "object"
              properties:
                last_name:
                  type: string
          - name: "group_id"
            in: "body"
            description: "group id"
            required: false
            schema:
              type: "object"
              properties:
                group_id:
                  type: integer
        responses:
          201:
            description: student was created
            schema:
                $ref: "#/definitions/student"
          400:
            description: Invalid input
        produces:
            - application/json
        """
        req = request.get_json()
        first_name = req.get('first_name')
        last_name = req.get('last_name')
        group_id = req.get('group_id')

        student = add_student(first_name, last_name)
        if group_id:
            add_student_to_group(student.id, group_id)

        student = StudentSchema().dump(student)

        return student, 201


class Student(Resource):
    def get(self, student_id):
        """
        Get student by id
        ---
        tags:
            - Students
        description: Returns a single student
        parameters:
          - name: "student_id"
            in: "path"
            description: "ID of student to return"
            required: true
        responses:
          200:
            description: student
            schema:
              $ref: "#/definitions/student"
          404:
            description: student does not exist
        produces:
            - application/json
        """
        student = StudentModel.query.get_or_404(student_id)
        student = StudentSchema().dump(student)

        return student

    def put(self, student_id):
        """
        Edit student
        ---
        tags:
            - Students
        description: "Rename or change student group"
        consumes:
            - application/json
        parameters:
          - name: "student_id"
            in: "path"
            description: "ID of student"
            required: true
          - name: "first name"
            in: "body"
            description: "student first name"
            required: false
            schema:
              type: "object"
              properties:
                first_name:
                  type: string
          - name: "last_name"
            in: "body"
            description: "student last name"
            required: false
            schema:
              type: "object"
              properties:
                last_name:
                  type: string
          - name: "group_id"
            in: "body"
            description: "group id"
            required: false
            schema:
              type: "object"
              properties:
                group_id:
                  type: integer
        responses:
          200:
            description: edit successful
            schema:
              $ref: "#/definitions/student"
          404:
            description: student does not exist
          500:
            description: Invalid input
        produces:
            - application/json
        """
        req = request.get_json()
        first_name = req.get('first_name')
        last_name = req.get('last_name')
        group_id = req.get('group_id')

        student = edit_student(student_id, first_name, last_name)

        if group_id:
            if student.group_id:
                remove_student_from_group(student,  student.group_id)
            add_student_to_group(student.id, group_id)

        student = StudentSchema().dump(student)

        return student

    def delete(self, student_id):
        """
        Delete student
        ---
        tags:
            - Students
        description: Delete group by id
        parameters:
          - name: "student_id"
            in: "path"
            description: "ID of student to delete"
            required: true
        responses:
          204:
            description: student deleted
          404:
            description: student does not exist
        """
        del_student(student_id)

        return None, 204


class CoursesByStudent (Resource):
    def get(self, student_id):
        """
        All courses assigned to student
        ---
        tags:
            - Students
        description: Returns all student courses
        parameters:
          - name: "student_id"
            in: "path"
            description: "ID of student"
            required: true
        responses:
          200:
            description: courses
            schema:
              type: array
              items:
                $ref: "#/definitions/course"
          404:
            description: student does not exist
        produces:
            - application/json
        """
        main_query = (db.session.query(CourseModel)
                      .join(CourseModel.students)
                      .filter(StudentModel.id == student_id))
        courses = main_query.all()
        courses = CourseSchema().dump(courses, many=True)
        return courses

    def post(self, student_id):
        """
        Assign student to courses
        ---
        tags:
            - Students
        parameters:
          - name: "student_id"
            in: "path"
            description: "ID of student"
            required: true
          - name: "courses"
            in: "body"
            description: "list of course ids that will be added to student"
            required: true
            schema:
              type: "object"
              properties:
                courses:
                  type: array
                  items: integer
                  example: [1, 2, 3]
        responses:
          200:
            description: courses
            schema:
              type: array
              items:
                $ref: "#/definitions/course"
          404:
            description: student does not exist
          500:
            description: bad request
        consumes:
          - application/json
        """
        req = request.get_json()
        courses = req.get('courses')
        student = StudentModel.query.get_or_404(student_id)
        for course_id in courses:
            try:
                student.courses.append(CourseModel.query.get_or_404(course_id))
            except FlushError:
                abort(400, f'student with id={student_id} does not exist')
        db.session.commit()

        return None, 201

    def delete(self, student_id):
        """
        Remove student from courses
        ---
        tags:
            - Students
        parameters:
          - name: "student_id"
            in: "path"
            description: "ID of student"
            required: true
          - name: "courses"
            in: "body"
            description: "list of students ids that will be removed from group"
            required: true
            schema:
              type: "object"
              properties:
                courses:
                  type: array
                  items: integer
                  example: [1, 2, 3]
        responses:
          200:
            description: courses
          404:
            description: student does not exist
          500:
            description: bad request
        consumes:
          - application/json
        """
        req = request.get_json(force=True)
        courses = req.get('courses')
        student = StudentModel.query.get_or_404(student_id)
        for course_id in courses:
            try:
                student.courses.remove(CourseModel.query.get_or_404(course_id))
            except FlushError:
                abort(400, f'student with id={student_id} does not exist')
            except ValueError:
                abort(400, f'student with id={student_id} is not assigned to course')
        db.session.commit()

        return None
