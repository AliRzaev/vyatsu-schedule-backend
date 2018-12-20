from datetime import timedelta
from os import getenv
from typing import List

import requests

from utils.cache import KeyValueStorage, RedisCollectionAdapter
from config.redis import get_instance

CACHE_PREFIX = __name__

_PARSE_API_URL = getenv('PARSE_API_URL')

_SCHEDULE_URL_TEMPLATE = 'https://www.vyatsu.ru/reports/schedule/Group/{}_{}_{}_{}.pdf'

_SCHEDULE_CACHE = KeyValueStorage(
    RedisCollectionAdapter(get_instance(), timedelta(days=14)))


class ParseException(Exception):
    pass


def fetch_schedule_from_service(group_id: str, season_key: str, _range: List[str]) -> dict:
    api_url = _PARSE_API_URL + '/api/v1/parse_pdf'
    pdf_url = _SCHEDULE_URL_TEMPLATE.format(group_id, season_key, _range[0], _range[1])

    response = requests.get(api_url, params={'url': pdf_url})
    response.raise_for_status()

    data = response.json()

    if 'success' in data['meta']:
        return data['data']['schedule']
    elif 'error' in data['meta']:
        raise ParseException(data['meta']['error'])
    else:
        raise ParseException('PDF_PARSE_ERROR')


def fetch_schedule(group_id: str, season_key: str, _range: List[str]) -> dict:
    schedule_key = f'{CACHE_PREFIX}_schedule_{group_id}_{season_key}'
    try:
        cached_schedule = _SCHEDULE_CACHE[schedule_key]
        if cached_schedule['range'] != _range:
            raise Exception('Outdated schedule')
        else:
            return cached_schedule['schedule']
    except (KeyError, Exception):
        actual_schedule = fetch_schedule_from_service(group_id, season_key, _range)

        _SCHEDULE_CACHE[schedule_key] = {
            'schedule': actual_schedule,
            'range': _range
        }

        return actual_schedule
