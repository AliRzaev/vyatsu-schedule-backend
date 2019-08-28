from flask import Response

from utils.wrappers import on_exception


class TestOnException:

    def test_ok(self):
        @on_exception()
        def foo():
            return 'OK'

        val = foo()

        assert val == 'OK', 'Invalid returned value'

    def test_name_preserving(self):
        def specific_name():
            return 'OK'

        wrapped = on_exception()(specific_name)

        assert hasattr(wrapped, '__name__'), \
            "Wrapped function doesn't have attribute '__name__'"
        assert wrapped.__name__ == 'specific_name', \
            "Wrapped function's name wasn't preserved"

    def test_failure_response(self):
        @on_exception()
        def fail_foo():
            raise Exception('Failure')

        val = fail_foo()

        assert isinstance(val, Response), \
            'Return value must be an instance of flask.Response'

        data = val.json
        expected_data = {
            'error': 'Failure'
        }

        assert data == expected_data, 'Invalid response body'

    def test_failure_default_status_code(self):
        @on_exception()
        def fail_foo():
            raise Exception('Failure')

        val = fail_foo()

        assert val.status_code == 500, \
            'Default status code must be equal to 500'

    def test_failure_custom_status_code(self):
        @on_exception(422)
        def fail_foo():
            raise Exception('Failure')

        val = fail_foo()

        assert val.status_code == 422, 'Invalid custom status code'

    def test_failure_mime_type(self):
        @on_exception()
        def fail_foo():
            raise Exception('Failure')

        val = fail_foo()

        assert val.mimetype == 'application/json', \
            "Mimetype must be equal to 'application/json'"
