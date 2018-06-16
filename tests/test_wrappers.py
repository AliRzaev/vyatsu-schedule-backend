from unittest import TestCase
from flask import Response
from utils.wrappers import on_exception, content_type_json
from utils import wrappers
from utils.logging import get_logger
from logging import CRITICAL


class TestOnException(TestCase):

    def setUp(self):
        get_logger(wrappers.__name__).setLevel(CRITICAL)  # disable logging

    def test_ok(self):
        @on_exception()
        def foo():
            return 'OK'

        val = foo()

        self.assertEqual(val, 'OK', 'Invalid returned value')

    def test_name_preserving(self):
        def specific_name():
            return 'OK'

        wrapped = on_exception()(specific_name)

        self.assertTrue(hasattr(wrapped, '__name__'), "Wrapped function doesn't have attribute '__name__'")
        self.assertEqual(wrapped.__name__, 'specific_name', "Wrapped function's name wasn't preserved")

    def test_failure_response(self):
        @on_exception()
        def fail_foo():
            raise Exception('Failure')

        val = fail_foo()

        self.assertIsInstance(val, Response, 'Return value must be an instance of flask.Response')

        data = val.json
        expected_data = {
            'error': 'Failure'
        }

        self.assertEqual(data, expected_data, 'Invalid response body')

    def test_failure_default_status_code(self):
        @on_exception()
        def fail_foo():
            raise Exception('Failure')

        val = fail_foo()

        self.assertEqual(val.status_code, 500, 'Default status code must be equal to 500')

    def test_failure_custom_status_code(self):
        @on_exception(422)
        def fail_foo():
            raise Exception('Failure')

        val = fail_foo()

        self.assertEqual(val.status_code, 422, 'Invalid custom status code')

    def test_failure_mime_type(self):
        @on_exception()
        def fail_foo():
            raise Exception('Failure')

        val = fail_foo()

        self.assertEqual(val.mimetype, 'application/json', "Mimetype must be equal to 'application/json'")
