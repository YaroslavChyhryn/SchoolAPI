from flask import abort, request
from flask_restful import Resource, reqparse
from school_api.models import GroupModel, StudentModel, CourseModel, student_course, db
from school_api.services.services import *
from ...schema.school_schema import GroupSchema, StudentSchema, CourseSchema
from sqlalchemy.orm.exc import FlushError


class Groups(Resource):
    def get(self):
        """
        All groups
        ---
        tags:
            - Groups
        description: "Returns all groups"
        parameters:
          - name: "max_students"
            in: query
            description: "Response will contain only groups with less or equal students"
            type: "integer"
        responses:
          200:
            description: all groups
            schema:
              type: array
              items:
                $ref: "#/definitions/group"
        produces:
            - application/json
        """
        parser = reqparse.RequestParser()
        parser.add_argument('max_students', type=int)

        args = parser.parse_args()
        max_students = args['max_students']

        if max_students:
            groups = select_group_with_less_students(max_students)
        else:
            groups = GroupModel.query.all()

        groups = GroupSchema().dump(groups, many=True)

        return groups

    def post(self):
        """
        Create group
        ---
        tags:
            - Groups
        description: "Add new group to database"
        consumes:
            - application/json
        parameters:
          - name: "group_name"
            in: "body"
            description: "New group name"
            required: true
            schema:
              type: "object"
              properties:
                group_name:
                  type: string
        responses:
          201:
            description: group was created
            schema:
              $ref: "#/definitions/group"
          400:
            description:  Invalid input
        produces:
            - application/json
        """
        req = request.get_json(force=True)
        name = req.get('group_name')

        group = add_group(name)
        group = GroupSchema().dump(group)

        return group, 201


class Group(Resource):
    def get(self, group_id):
        """
        Get group by id
        ---
        tags:
            - Groups
        description: Returns a single group
        parameters:
          - name: "group_id"
            in: "path"
            description: "ID of group to return"
            required: true
        responses:
          200:
            description: group data
            schema:
              $ref: "#/definitions/group"
          404:
            description: group does not exist
        produces:
            - application/json
        """
        group = GroupModel.query.get_or_404(group_id)
        group = GroupSchema().dump(group)

        return group

    def put(self, group_id):
        """
        Edit group
        ---
        tags:
            - Groups
        description: Rename group
        consumes:
            - application/json
        parameters:
          - name: "group_id"
            in: "path"
            description: "ID of student"
            required: true
          - name: "group_name"
            in: "body"
            description: "group name"
            required: true
            schema:
              type: "object"
              properties:
                group_name:
                  type: string
        responses:
          200:
            description: edit successful
            schema:
              $ref: "#/definitions/group"
          404:
            description: group does not exist
          500:
            description: Invalid input
        produces:
            - application/json
        """
        req = request.get_json(force=True)
        name = req.get('group_name')

        group = edit_group(group_id, name)
        group = GroupSchema().dump(group)

        return group

    def delete(self, group_id):
        """
        Delete group
        ---
        tags:
            - Groups
        description: Delete group by id
        parameters:
          - name: "group_id"
            in: "path"
            description: "ID of group to delete"
            required: true
        responses:
          204:
            description: group deleted
          404:
            description: group does not exist
        """
        del_group(group_id)

        return None, 204


class StudentsByGroup (Resource):
    def get(self, group_id):
        """
        All students in group
        ---
        tags:
            - Groups
        description: Returns all students in group
        parameters:
          - name: "group_id"
            in: "path"
            description: "ID of course"
            required: true
        responses:
          200:
            description: students in group
            schema:
              type: array
              items:
                $ref: "#/definitions/student"
          404:
            description: group does not exist
        produces:
            - application/json
        """
        main_query = (db.session.query(StudentModel)
                      .join(StudentModel.group)
                      .filter(GroupModel.id == group_id))
        students = main_query.all()

        students = StudentSchema().dump(students, many=True)

        return students

    def post(self, group_id):
        """
        Add students to group
        ---
        tags:
            - Groups
        parameters:
          - name: "group_id"
            in: "path"
            description: "ID of course"
            required: true
          - name: "students"
            in: "body"
            description: "list of students ids that will be added to group"
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
            description: students in group
            schema:
              type: array
              items:
                $ref: "#/definitions/student"
          404:
            description: group does not exist
          500:
            description: bad request
        consumes:
            - application/json
        produces:
            - application/json
        """
        req = request.get_json()
        students = req.get('students')
        group = GroupModel.query.get_or_404(group_id)
        # todo validate students ids
        for student_id in students:
            group.students.append(StudentModel.query.get_or_404(student_id))
        db.session.commit()

        return None, 201

    def delete(self, group_id):
        """
        Remove students from group
        ---
        tags:
            - Groups
        parameters:
          - name: "group_id"
            in: "path"
            description: "ID of group"
            required: true
          - name: "students"
            in: "body"
            description: "list of students ids that will be removed from group"
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
            description: students ware deleted from group
          404:
            description: group does not exist
          500:
            description: bad request
        consumes:
            - application/json
        """
        req = request.get_json()
        students = req.get('students')

        group = GroupModel.query.get_or_404(group_id)
        for student_id in students:
            try:
                group.students.remove(StudentModel.query.get_or_404(student_id))
            except ValueError:
                abort(400, f'student with id={student_id} is not in group')
        db.session.commit()

        return None
