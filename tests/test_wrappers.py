from unittest import TestCase
from flask import Response
from utils.wrappers import on_exception, comparable_mixin, content_type_json
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


class TestComparableMixin(TestCase):

    @comparable_mixin
    class Cls:

        def __init__(self, key):
            self.key = key

        def __lt__(self, other):
            return self.key < other.key

    def setUp(self):
        self.val = self.Cls(5)

    def test_lt(self):
        other = self.Cls(6)

        self.assertLess(self.val, other, '__lt__ does not work')

    def test_gt(self):
        other = self.Cls(4)

        self.assertGreater(self.val, other, '__gt__ does not work')

    def test_le(self):
        other = self.Cls(5)

        self.assertLessEqual(self.val, other, '__le__ does not work')

    def test_ge(self):
        other = self.Cls(5)

        self.assertGreaterEqual(self.val, other, '__ge__ does not work')

    def test_eq(self):
        other = self.Cls(5)

        self.assertEqual(self.val, other, '__eq__ does not work')

    def test_ne(self):
        other = self.Cls(6)

        self.assertNotEqual(self.val, other, '__ne__ does not work')


class TestContentTypeJson(TestCase):

    @content_type_json
    def _foo(self, data):
        return data

    def test_list(self):
        data = [1, 2, 3]

        resp = self._foo(data)
        resp_data = resp.json

        self.assertEqual(data, resp_data, 'Data mismatch')

    def test_dict(self):
        data = {
            '1': 'one',
            '2': 'two'
        }

        resp = self._foo(data)
        resp_data = resp.json

        self.assertEqual(data, resp_data, 'Data mismatch')

    def test_non_json_type(self):
        data = 'some string'

        resp = self._foo(data)
        resp_data = resp

        self.assertTrue(isinstance(resp_data, str), 'Data type mismatch')
        self.assertEqual(data, resp_data, 'Data mismatch')

    def test_mime_type(self):
        data = [1, 2, 3]

        resp = self._foo(data)

        mime_type = resp.mimetype

        self.assertEqual(mime_type, 'application/json', "Mimetype must be equal to 'application/json'")

    def test_status_code(self):
        data = [1, 2, 3]

        resp = self._foo(data)

        status_code = resp.status_code

        self.assertEqual(status_code, 200, 'Status code must be equal to 200')

    def test_encoding_raises_error(self):
        data = [1, b'\02']

        self.assertRaises(TypeError, self._foo, data)
