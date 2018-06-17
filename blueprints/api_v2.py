from flask import Blueprint

from models import groups_info, schedule_ranges
from utils import date
from utils.responses import Error
from utils.schedule_parsing import parse_schedule, ParseException
from utils.transforming.api_v2 import groups_info_to_list
from utils.wrappers import on_exception, content_type_json

api_v2_blueprint = Blueprint('api_v2', __name__)


@api_v2_blueprint.route('/groups.json', methods=['GET'])  # backward compatibility
@api_v2_blueprint.route('/groups/list', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_list():
    return groups_info_to_list(groups_info.find_all())


@api_v2_blueprint.route('/groups/by_faculty.json', methods=['GET'])  # backward compatibility
@api_v2_blueprint.route('/groups/by_faculty', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_by_faculty():
    return groups_info_to_list(groups_info.find_all(), by_faculty=True)


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


@api_v2_blueprint.route('/season/current', methods=['GET'])
@on_exception(500)
@content_type_json
def get_current_season():
    return {
        'season': date.get_current_season()
    }


@api_v2_blueprint.route('/schedule/<group_id>/<season>', methods=['GET'])
@on_exception(500)
@content_type_json
def get_schedule(group_id, season):
    if season == 'autumn':
        season_key = '1'
    elif season == 'spring':
        season_key = '2'
    else:
        return Error(422, 'INVALID_SEASON')

    group_info = groups_info.find_group_by_id(group_id)
    if group_info is None:
        return Error(422, 'NO_SUCH_GROUP')
    else:
        group_name = group_info['group']

    range_info = schedule_ranges.find_by_group_and_season(group_id, season)
    if range_info is None:
        return Error(422, 'NO_SUCH_SCHEDULE')
    else:
        _range = range_info['range']

    try:
        return {
            'group': group_name,
            'date_range': _range,
            'today': date.get_date_indexes(_range[0]),
            'weeks': parse_schedule(group_id, season_key, _range)
        }
    except ParseException as ex:
        return Error(422, str(ex))
