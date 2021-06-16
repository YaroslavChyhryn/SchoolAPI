from tests.BaseCase import BaseCase
from school_api.models.models import StudentModel, CourseModel, db
import json


class TestStudents(BaseCase):
    def test_get_all_students(self):
        with self.app.app_context():
            response = self.client.get('api/v1/students')
            self.assertEqual(response.status_code, 200)
            # len 200 based on test data
            self.assertEqual(len(response.json), 200)

    def test_get_wrong_student_id(self):
        with self.app.app_context():
            response = self.client.get('api/v1/students/1000000')
            self.assertEqual(response.status_code, 404)

    def test_create_student(self):
        with self.app.app_context():
            first_name = 'foo'
            last_name = 'bar'
            group_id = 1
            response = self.client.post(f'api/v1/students',
                                        data=json.dumps({'first_name': first_name,
                                                         'last_name': last_name,
                                                         'group_id': group_id}),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 201)

            new_student = response.json
            student_in_db = (db.session.query(StudentModel)
                             .filter(StudentModel.first_name == first_name,
                                     StudentModel.last_name == last_name)
                             .first())
            self.assertEqual(new_student['first_name'], student_in_db.first_name)
            self.assertEqual(new_student['last_name'], student_in_db.last_name)

    def test_get_student_by_id(self):
        with self.app.app_context():
            student_id = 1
            response = self.client.get(f'api/v1/students/{student_id}')
            self.assertEqual(response.status_code, 200)

            student = response.json
            self.assertEqual(student['id'], student_id)

    def test_edit_student(self):
        with self.app.app_context():
            student_id = 5
            first_name = 'Rick'
            last_name = 'Pickle'
            group_id = 1
            response = self.client.put(f'api/v1/students/{student_id}',
                                        data=json.dumps({'first_name': first_name,
                                                         'last_name': last_name,
                                                         'group_id': group_id}),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 200)

            edited_student = response.json
            student_in_db = StudentModel.query.get(student_id)
            self.assertEqual(edited_student['first_name'], student_in_db.first_name)
            self.assertEqual(edited_student['last_name'], student_in_db.last_name)

    def test_delete_student(self):
        with self.app.app_context():
            student_id = 1
            response = self.client.delete(f'api/v1/students/{student_id}')
            self.assertEqual(response.status_code, 204)

            course = StudentModel.query.get(student_id)
            self.assertEqual(course, None)

    def test_delete_with_wrong_id(self):
        with self.app.app_context():
            response = self.client.delete(f'api/v1/students/1000000')
            self.assertEqual(response.status_code, 404)

    def test_get_student_courses(self):
        with self.app.app_context():
            student_id = 1
            response = self.client.get(f'api/v1/students/{student_id}/courses')
            for course in response.json:
                self.assertIn(student_id,  course['students'])

    def test_add_courses_to_student(self):
        with self.app.app_context():
            student_id = 2
            # course ids based on test db
            courses_for_add = {'courses': [7, 8, 9]}
            response = self.client.post(f'api/v1/students/{student_id}/courses',
                                        data=json.dumps(courses_for_add),
                                        content_type='application/json')

            student_courses = (db.session.query(CourseModel.id)
                               .join(CourseModel.students)
                               .filter(StudentModel.id == student_id)
                               .all())

            for course_id in courses_for_add['courses']:
                self.assertIn((course_id,), student_courses)

    def test_remove_courses_from_student(self):
        with self.app.app_context():
            student_id = 2
            # course ids based on test db
            courses_for_remove = {'courses': [7, 8, 9]}
            response = self.client.delete(f'api/v1/students/{student_id}/courses',
                                          data=json.dumps(courses_for_remove),
                                          content_type='application/json')

            student_courses = (db.session.query(CourseModel.id)
                               .join(CourseModel.students)
                               .filter(StudentModel.id == student_id)
                               .all())

            for course_id in courses_for_remove['courses']:
                self.assertNotIn((course_id,), student_courses)

    def test_students_by_course_name(self):
        with self.app.app_context():
            course = CourseModel.query.get(1)
            response = self.client.get(f'api/v1/students?course_name={course.name}')
            self.assertEqual(response.status_code, 200)

            students_by_name = response.json

            response = self.client.get(f'api/v1/courses/{course.id}/students')
            students_by_id = response.json
            self.assertEqual(students_by_name, students_by_id)
