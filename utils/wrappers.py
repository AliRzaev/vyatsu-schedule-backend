from flask import Response
from json import dumps
from utils.logging import get_logger


_logger = get_logger(__name__)


class on_exception:
    def __init__(self, status_code=500):
        self._status_code = status_code

    def __call__(self, route):
        def wrapper_fun(*args, **kwargs):
            try:
                return route(*args, **kwargs)
            except Exception as ex:
                _logger.exception('Error occurred at {}'.format(route.__name__))
                return Response(str(ex), self._status_code)

        wrapper_fun.__name__ = route.__name__

        return wrapper_fun


def content_type_json(route):
    def wrapper_fun(*args, **kwargs):
        route_res = route(*args, **kwargs)
        if isinstance(route_res, Response):
            return route_res
        else:
            return dumps(route_res, ensure_ascii=False)

    wrapper_fun.__name__ = route.__name__

    return wrapper_fun
