from flask import Blueprint
from flask_restful import Api
from .group import Groups, Group, StudentsByGroup
from .student import Students, Student, CoursesByStudent
from .course import Courses, Course, StudentsByCourse


api_bp = Blueprint('api_v1', __name__)
api = Api(api_bp)


api.add_resource(Groups, '/groups')
api.add_resource(Group, '/groups/<group_id>')
api.add_resource(StudentsByGroup, '/groups/<group_id>/students')

api.add_resource(Students, '/students')
api.add_resource(Student, '/students/<student_id>')
api.add_resource(CoursesByStudent, '/students/<student_id>/courses')

api.add_resource(Courses, '/courses')
api.add_resource(Course, '/courses/<course_id>')
api.add_resource(StudentsByCourse, '/courses/<course_id>/students')
