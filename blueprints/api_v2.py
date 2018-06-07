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
    return {
        'meta': '/calls'
    }


@api_v2_blueprint.route('/schedule/<group_id>/<season>', methods=['GET'])
@on_exception(500)
@content_type_json
def get_schedule(group_id, season):
    return {
        'meta': '/schedule/{}/{}'.format(group_id, season)
    }
