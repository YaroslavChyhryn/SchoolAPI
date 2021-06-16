import unittest
import json

from tests.BaseCase import BaseCase
from school_api.models.models import GroupModel, db


class TestGroups(BaseCase):
    def test_get_all_groups(self):
        with self.app.app_context():
            response = self.client.get('api/v1/groups')
            self.assertEqual(response.status_code, 200)
            # len 10 based on test data
            self.assertEqual(len(response.json), 10)

    def test_get_wrong_group_id(self):
        with self.app.app_context():
            response = self.client.get('api/v1/groups/1000000')
            self.assertEqual(response.status_code, 404)

    def test_create_group(self):
        with self.app.app_context():
            group_name = "ЯЯ-99"
            response = self.client.post(f'api/v1/groups',
                                        data=json.dumps({'group_name': group_name}),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 201)

            new_group = response.json
            group_in_db = db.session.query(GroupModel).filter(GroupModel.name == group_name).first()
            self.assertEqual(new_group['name'], group_in_db.name)

    def test_get_group_by_id(self):
        with self.app.app_context():
            group_id = 1
            response = self.client.get(f'api/v1/groups/{group_id}')
            self.assertEqual(response.status_code, 200)

            group = response.json
            self.assertEqual(group['id'], group_id)

    def test_rename_group(self):
        with self.app.app_context():
            group_id = 5
            group_name = GroupModel.query.get(1).name
            response = self.client.put(f'api/v1/groups/{group_id}',
                                       data=json.dumps({'group_name': group_name}),
                                       content_type='application/json')
            self.assertEqual(response.status_code, 400)

            group_name = 'ЯЯ-99'
            response = self.client.put(f'api/v1/groups/{group_id}',
                                       data=json.dumps({'group_name': group_name}),
                                       content_type='application/json')
            self.assertEqual(response.status_code, 200)

            group = response.json
            group_in_db = db.session.query(GroupModel).filter(GroupModel.name == group_name).first()
            self.assertEqual(group['name'], group_in_db.name)

    def test_delete_group(self):
        with self.app.app_context():
            response = self.client.delete(f'api/v1/groups/1')
            self.assertEqual(response.status_code, 204)

            group = GroupModel.query.get(1)
            self.assertEqual(group, None)

    def test_delete_with_wrong_id(self):
        with self.app.app_context():
            response = self.client.delete(f'api/v1/groups/1000000')
            self.assertEqual(response.status_code, 404)

    def test_get_students_in_group(self):
        with self.app.app_context():
            group_id = 1
            response = self.client.get(f'api/v1/groups/{group_id}/students')
            students = response.json
            for student in students:
                self.assertEqual(student['group'], group_id)

    def test_add_students_to_group(self):
        with self.app.app_context():
            group_id = 1

            response = self.client.get(f'api/v1/groups/{group_id}/students')
            students_before = response.json

            # student ids based on test db
            students_for_add = {'students': [31, 32, 33]}

            response = self.client.post(f'api/v1/groups/{group_id}/students',
                                        data=json.dumps(students_for_add),
                                        content_type='application/json')

            response = self.client.get(f'api/v1/groups/{group_id}/students')
            students_after = response.json

            number_of_students = len(students_after)-len(students_before)

            self.assertEqual(number_of_students, 3)

    def test_remove_students_from_group(self):
        with self.app.app_context():
            group_id = 1

            response = self.client.get(f'api/v1/groups/{group_id}/students')
            students_before = response.json

            # student ids based on test db
            students_for_del = {'students': [1, 2, 3]}

            response = self.client.delete(f'api/v1/groups/{group_id}/students',
                                          data=json.dumps(students_for_del),
                                          content_type='application/json')

            response = self.client.get(f'api/v1/groups/{group_id}/students')
            students_after = response.json

            number_of_students = len(students_before) - len(students_after)

            self.assertEqual(number_of_students, 3)

    def test_get_group_with_less_students(self):
        with self.app.app_context():
            number_of_students = 20

            response = self.client.get(f'api/v1/groups?max_students=20')

            groups = response.json

            for group in groups:
                students_in_group = len(group['students'])
                self.assertLess(students_in_group, number_of_students)
