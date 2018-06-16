from flask import Response
from json import dumps


class Error(Response):

    def __init__(self, status: int, message: str):
        response = dumps({
            'error': message
        }, ensure_ascii=False)

        super(Response, self).__init__(
            status=status,
            response=response,
            mimetype='application/json'
        )
