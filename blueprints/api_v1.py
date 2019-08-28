from datetime import timedelta

from flask import Blueprint, jsonify

from utils.date import get_moscow_today
from utils.repository import get_repository
from utils.responses import error_response
from utils.schedule import fetch_group_schedule, ParseException
from utils.transforming.api_v1 import groups_info_to_dict
from utils.wrappers import on_exception, immutable, expires

api_v1_blueprint = Blueprint('api_v1', __name__)


@api_v1_blueprint.route('/groups/list', methods=['GET'])
@on_exception(500)
@expires(lambda: get_moscow_today() + timedelta(days=1))
def get_groups_list():
    groups = get_repository().get_groups()
    return jsonify(groups_info_to_dict(groups))


@api_v1_blueprint.route('/groups/by_faculty', methods=['GET'])
@on_exception(500)
@expires(lambda: get_moscow_today() + timedelta(days=1))
def get_groups_by_faculty():
    groups = get_repository().get_groups()
    return jsonify(groups_info_to_dict(groups, by_faculty=True))


@api_v1_blueprint.route('/calls', methods=['GET'])
@on_exception(500)
@immutable
def get_calls():
    return jsonify([
        ["8:20", "9:50"],
        ["10:00", "11:30"],
        ["11:45", "13:15"],
        ["14:00", "15:30"],
        ["15:45", "17:15"],
        ["17:20", "18:50"],
        ["18:55", "20:25"]
    ])


@api_v1_blueprint.route('/schedule/<group_id>/<season>', methods=['GET'])
@on_exception(500)
@expires(lambda: get_moscow_today() + timedelta(days=1))
def get_schedule(group_id, season):
    if season == 'autumn':
        season_key = '1'
    elif season == 'spring':
        season_key = '2'
    else:
        return error_response(422, 'INVALID_SEASON')

    group_name = get_repository().get_group_name(group_id)
    if group_name is None:
        return error_response(422, 'NO_SUCH_GROUP')

    range_ = get_repository().get_group_date_range(group_id, season)
    if range_ is None:
        return error_response(422, 'NO_SUCH_SCHEDULE')

    try:
        return jsonify({
            'group': group_name,
            'date_range': range_,
            'weeks': fetch_group_schedule(group_id, season_key, range_)
        })
    except ParseException as ex:
        return error_response(422, str(ex))
