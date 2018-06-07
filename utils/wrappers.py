from flask import Response
from json import dumps
from utils.logging import get_logger


_logger = get_logger(__name__)


class on_exception:
    """
    Decorator for handling exceptions in routes and converting to appropriate responses.
    """
    def __init__(self, status_code=500):
        """
        Create a decorator that will send response with specified status code
        if some exceptions will be occurred during function call
        :param status_code: HTTP status code for response
        """
        self._status_code = status_code

    def __call__(self, route):
        """
        Decorate given function
        :param route: the function to be wrapped
        :return: callable object
        """
        def wrapper_fun(*args, **kwargs):
            try:
                return route(*args, **kwargs)
            except Exception as ex:
                _logger.exception('Error occurred at {}'.format(route.__name__))
                return Response(str(ex), self._status_code)

        wrapper_fun.__name__ = route.__name__

        return wrapper_fun


def content_type_json(route):
    """
    This decorator converts the result of the wrapped function into JSON string.
    :param route: the function to be wrapped
    :return: JSON string or unmodified result (if result isn't a list or a dict).
    :raise JSONDecodeError if some errors occur during serialization.
    """
    def wrapper_fun(*args, **kwargs):
        route_res = route(*args, **kwargs)
        if isinstance(route_res, Response):
            return route_res
        else:
            return dumps(route_res, ensure_ascii=False)

    wrapper_fun.__name__ = route.__name__

    return wrapper_fun
