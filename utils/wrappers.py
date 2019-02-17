from functools import wraps
from json import dumps

from flask import Response

from utils.date import as_rfc2822


class on_exception:
    """
    Decorator for handling exceptions in routes and
    converting to appropriate responses.
    """
    def __init__(self, status_code=500):
        """
        Create a decorator that will send response with specified status code
        if some exceptions will be occurred during function call.

        :param status_code: HTTP status code for response
        """
        self._status_code = status_code

    def __call__(self, route):
        """
        Decorate given function.

        :param route: the function to be wrapped
        :return: callable object
        """
        @wraps(route)
        def wrapper_fun(*args, **kwargs):
            try:
                return route(*args, **kwargs)
            except Exception as ex:
                response = dumps({
                    'error': str(ex)[:40]
                })
                return Response(
                    response=response,
                    status=self._status_code,
                    mimetype='application/json'
                )

        return wrapper_fun


def no_cache(route):
    """
    Turn off caching for the responses of the given route.
    """
    @wraps(route)
    def wrapper_fun(*args, **kwargs):
        route_res = route(*args, **kwargs)

        if isinstance(route_res, Response):
            route_res.headers.set('Cache-Control',
                                  'no-cache, no-store, must-revalidate')
            return route_res
        else:
            raise TypeError('Route must return a Response object')

    return wrapper_fun


def immutable(route):
    """
    Aggressive caching, store the responses of the given route
    in cache as much as possible.
    """
    @wraps(route)
    def wrapper_fun(*args, **kwargs):
        route_res = route(*args, **kwargs)

        if isinstance(route_res, Response):
            route_res.headers.set('Cache-Control',
                                  'public, max-age=31536000')
            return route_res
        else:
            raise TypeError('Route must return a Response object')

    return wrapper_fun


class expires:
    """
    Set HTTP header Expires with date obtained from date_fun function.
    """
    def __init__(self, date_fun):
        """
        :param date_fun: callable that returns instance of datetime.date class.
        """
        self._date_fun = date_fun

    def __call__(self, route):
        @wraps(route)
        def wrapper_fun(*args, **kwargs):
            route_res = route(*args, **kwargs)

            if isinstance(route_res, Response):
                route_res.headers.set('Expires', as_rfc2822(self._date_fun()))
                return route_res
            else:
                raise TypeError('Route must return a Response object')

        return wrapper_fun
