from flask import Blueprint
from utils.wrappers import on_exception, content_type_json

api_v1_blueprint = Blueprint('api_v1', __name__)


@api_v1_blueprint.route('/groups.json', methods=['GET'])  # backward compatibility
@api_v1_blueprint.route('/groups/list', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_list():
    return {
        'meta': '/groups/list'
    }


@api_v1_blueprint.route('/groups/by_faculty.json', methods=['GET'])  # backward compatibility
@api_v1_blueprint.route('/groups/by_faculty', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_by_faculty():
    return {
        'meta': '/groups/by_faculty'
    }


@api_v1_blueprint.route('/calls', methods=['GET'])
@on_exception(500)
@content_type_json
def get_calls():
    return [
        ["8:20", "9:50"],
        ["10:00", "11:30"],
        ["11:45", "13:15"],
        ["14:00", "15:30"],
        ["15:45", "17:15"],
        ["17:20", "18:50"],
        ["18:55", "20:25"]
    ]


@api_v1_blueprint.route('/schedule/<group_id>/<season>', methods=['GET'])
@on_exception(500)
@content_type_json
def get_schedule(group_id, season):
    return {
        'meta': '/schedule/{}/{}'.format(group_id, season)
    }
