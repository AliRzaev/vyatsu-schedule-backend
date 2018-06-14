from unittest import TestCase

from server import app


class TestApiV1(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass
