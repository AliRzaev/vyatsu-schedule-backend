from os import getenv
from typing import List
import requests


_PARSE_API_URL = getenv('PARSE_API_URL')
_SCHEDULE_URL_TEMPLATE = 'https://www.vyatsu.ru/reports/schedule/Group/{}_{}_{}_{}.pdf'


def parse_schedule(group_id: str, season: str, _range: List[str]) -> dict:
    if season == 'autumn':
        season_key = 1
    elif season == 'spring':
        season_key = 2
    else:
        raise Exception('INVALID_SEASON')

    api_url = _PARSE_API_URL + '/api/v1/parse_pdf'
    pdf_url = _SCHEDULE_URL_TEMPLATE.format(group_id, season_key, _range[0], _range[1])

    response = requests.get(api_url, params={'url': pdf_url})
    data = response.json()

    if 'success' in data['meta']:
        return data['data']['schedule']
    elif 'error' in data['meta']:
        raise Exception(data['meta']['error'])
    else:
        raise Exception('PDF_PARSE_ERROR')
