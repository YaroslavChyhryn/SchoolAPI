import unittest
from school_api.app import create_app
from school_api.db import create_tables, drop_tables
from school_api.data_generator import test_db


class BaseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('test')

    def setUp(self):
        drop_tables(self.app)
        create_tables(self.app)
        test_db(self.app)

        with self.app.app_context():
            self.client = self.app.test_client()

    def tearDown(self):
        drop_tables(self.app)
