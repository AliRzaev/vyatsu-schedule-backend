from flask import jsonify, make_response


def error_response(status: int, message: str):
    response = jsonify({'error': message})
    return make_response((response, status, ()))
