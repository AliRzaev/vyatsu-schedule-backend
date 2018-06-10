from flask import Blueprint
from utils.wrappers import on_exception, content_type_json

api_v2_blueprint = Blueprint('api_v2', __name__)


@api_v2_blueprint.route('/groups.json', methods=['GET'])  # backward compatibility
@api_v2_blueprint.route('/groups/list', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_list():
    return {
        'meta': '/groups/list'
    }


@api_v2_blueprint.route('/groups/by_faculty.json', methods=['GET'])  # backward compatibility
@api_v2_blueprint.route('/groups/by_faculty', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_by_faculty():
    return {
        'meta': '/groups/by_faculty'
    }


@api_v2_blueprint.route('/calls', methods=['GET'])
@on_exception(500)
@content_type_json
def get_calls():
    return [
        {"start": "8:20", "end": "9:50"},
        {"start": "10:00", "end": "11:30"},
        {"start": "11:45", "end": "13:15"},
        {"start": "14:00", "end": "15:30"},
        {"start": "15:45", "end": "17:15"},
        {"start": "17:20", "end": "18:50"},
        {"start": "18:55", "end": "20:25"}
    ]


@api_v2_blueprint.route('/schedule/<group_id>/<season>', methods=['GET'])
@on_exception(500)
@content_type_json
def get_schedule(group_id, season):
    return {
        'meta': '/schedule/{}/{}'.format(group_id, season)
    }
