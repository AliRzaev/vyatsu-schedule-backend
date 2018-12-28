from flask import Blueprint

from utils import date
from utils import groups_info
from utils.responses import Error
from utils.schedule import fetch_schedule, ParseException
from utils.transforming.api_v2 import groups_info_to_list
from utils.wrappers import on_exception, content_type_json

api_v2_blueprint = Blueprint('api_v2', __name__)


@api_v2_blueprint.route('/groups.json', methods=['GET'])  # backward compatibility
@api_v2_blueprint.route('/groups/list', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_list():
    return groups_info_to_list(groups_info.get_groups())


@api_v2_blueprint.route('/groups/by_faculty.json', methods=['GET'])  # backward compatibility
@api_v2_blueprint.route('/groups/by_faculty', methods=['GET'])
@on_exception(500)
@content_type_json
def get_groups_by_faculty():
    return groups_info_to_list(groups_info.get_groups(), by_faculty=True)


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

    group_name = groups_info.get_group_name(group_id)
    if group_name is None:
        return Error(422, 'NO_SUCH_GROUP')

    range_ = groups_info.get_date_range(group_id, season)
    if range_ is None:
        return Error(422, 'NO_SUCH_SCHEDULE')

    try:
        w, d = date.get_date_indexes(range_[0])
        today = date.get_date_by_indexes(range_[0], w, d)
        return {
            'group': group_name,
            'date_range': {
                'begin': range_[0],
                'end': range_[1]
            },
            'today': {
                'week': w,
                'dayOfWeek': d,
                'date': today
            },
            'weeks': fetch_schedule(group_id, season_key, range_)
        }
    except ParseException as ex:
        return Error(422, str(ex))
