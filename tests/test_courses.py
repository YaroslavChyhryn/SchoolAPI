from tests.BaseCase import BaseCase
from school_api.models.models import CourseModel, StudentModel, db
import json


class TestCourses(BaseCase):
    def test_get_all_courses(self):
        with self.app.app_context():
            response = self.client.get('api/v1/courses')
            self.assertEqual(response.status_code, 200)
            # len 10 based on test data
            self.assertEqual(len(response.json), 10)

    def test_get_wrong_course_id(self):
        with self.app.app_context():
            response = self.client.get('api/v1/courses/42')
            self.assertEqual(response.status_code, 404)

    def test_create_course(self):
        with self.app.app_context():
            course_name = 'Magick'
            description = 'description'

            response = self.client.post(f'api/v1/courses',
                                        data=json.dumps({'course_name': course_name,
                                                        'description': description}),
                                        content_type='application/json')

            self.assertEqual(response.status_code, 201)

            new_course = response.json
            course_in_db = db.session.query(CourseModel).filter(CourseModel.name == course_name).first()
            self.assertEqual(new_course['name'], course_in_db.name)

    def test_get_course_by_id(self):
        with self.app.app_context():
            course_id = 1
            response = self.client.get(f'api/v1/courses/{course_id}')
            self.assertEqual(response.status_code, 200)

            course = response.json
            self.assertEqual(course['id'], course_id)

    def test_edit_course(self):
        with self.app.app_context():
            course_id = 5
            course_name = CourseModel.query.get(1).name
            response = self.client.put(f'api/v1/courses/{course_id}',
                                       data=json.dumps({'course_name': course_name}),
                                       content_type='application/json')
            self.assertEqual(response.status_code, 400)

            course_name = 'Magic'
            description = 'description'

            response = self.client.put(f'api/v1/courses/{course_id}',
                                       data=json.dumps({'course_name': course_name,
                                                        'description': description}),
                                       content_type='application/json')
            self.assertEqual(response.status_code, 200)

            course = response.json
            course_in_db = db.session.query(CourseModel).filter(CourseModel.name == course_name).first()
            self.assertEqual(course['name'], course_in_db.name)

    def test_delete_course(self):
        with self.app.app_context():
            course_id = 1
            response = self.client.delete(f'api/v1/courses/{course_id}')
            self.assertEqual(response.status_code, 204)

            course = CourseModel.query.get(course_id)
            self.assertEqual(course, None)

    def test_delete_with_wrong_id(self):
        with self.app.app_context():
            response = self.client.delete(f'api/v1/courses/1000000')
            self.assertEqual(response.status_code, 404)

    def test_get_students_in_course(self):
        with self.app.app_context():
            course_id = 1
            response = self.client.get(f'api/v1/courses/{course_id}/students')
            students = response.json
            for student in students:
                self.assertIn(course_id,  student['courses'])

    def test_add_students_to_course(self):
        with self.app.app_context():
            course_id = 2
            # student ids based on test db
            students_for_add = {'students': [31, 32, 33]}
            response = self.client.post(f'api/v1/courses/{course_id}/students',
                                        data=json.dumps(students_for_add),
                                        content_type='application/json')

            students_on_course = (db.session.query(StudentModel.id)
                                  .join(StudentModel.courses)
                                  .filter(CourseModel.id == course_id)
                                  .all())

            for student_id in students_for_add['students']:
                self.assertIn((student_id,), students_on_course)

    def test_remove_students_from_course(self):
        with self.app.app_context():
            course_id = 2
            # student ids based on test db
            students_on_course = (db.session.query(StudentModel.id)
                                  .join(StudentModel.courses)
                                  .filter(CourseModel.id == course_id)
                                  .all())

            students_for_remove = students_on_course[:3]
            students_for_remove = {'students': [student[0] for student in students_for_remove]}

            response = self.client.delete(f'api/v1/courses/{course_id}/students',
                                          data=json.dumps(students_for_remove),
                                          content_type='application/json')
            self.assertEqual(response.status_code, 204)
            students_on_course = (db.session.query(StudentModel.id)
                                  .join(StudentModel.courses)
                                  .filter(CourseModel.id == course_id)
                                  .all())

            for student_id in students_for_remove['students']:
                self.assertNotIn((student_id,), students_on_course)
