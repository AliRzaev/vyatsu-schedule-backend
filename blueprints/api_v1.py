from flask import Blueprint

from utils import groups_info, date_ranges_info
from utils.responses import Error
from utils.schedule import fetch_schedule, ParseException
from utils.transforming.api_v1 import groups_info_to_dict
from utils.wrappers import on_exception, content_type_json

api_v1_blueprint = Blueprint('api_v1', __name__)


@api_v1_blueprint.route('/groups.json', methods=['GET'])  # backward compatibility
@api_v1_blueprint.route('/groups/list', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_list():
    return groups_info_to_dict(groups_info.get_groups_info())


@api_v1_blueprint.route('/groups/by_faculty.json', methods=['GET'])  # backward compatibility
@api_v1_blueprint.route('/groups/by_faculty', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_by_faculty():
    return groups_info_to_dict(groups_info.get_groups_info(), by_faculty=True)


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
    if season == 'autumn':
        season_key = '1'
    elif season == 'spring':
        season_key = '2'
    else:
        return Error(422, 'INVALID_SEASON')

    group_name = groups_info.get_group_name(group_id)
    if group_name is None:
        return Error(422, 'NO_SUCH_GROUP')

    range_ = date_ranges_info.get_date_range(group_id, season)
    if range_ is None:
        return Error(422, 'NO_SUCH_SCHEDULE')

    try:
        return {
            'group': group_name,
            'date_range': range_,
            'weeks': fetch_schedule(group_id, season_key, range_)
        }
    except ParseException as ex:
        return Error(422, str(ex))
