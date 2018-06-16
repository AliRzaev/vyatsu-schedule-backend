from os import getenv
from typing import List
import requests


_PARSE_API_URL = getenv('PARSE_API_URL')
_SCHEDULE_URL_TEMPLATE = 'https://www.vyatsu.ru/reports/schedule/Group/{}_{}_{}_{}.pdf'


class ParseException(Exception):
    pass


def parse_schedule(group_id: str, season_key: str, _range: List[str]) -> dict:
    api_url = _PARSE_API_URL + '/api/v1/parse_pdf'
    pdf_url = _SCHEDULE_URL_TEMPLATE.format(group_id, season_key, _range[0], _range[1])

    response = requests.get(api_url, params={'url': pdf_url})
    data = response.json()

    if 'success' in data['meta']:
        return data['data']['schedule']
    elif 'error' in data['meta']:
        raise ParseException(data['meta']['error'])
    else:
        raise ParseException('PDF_PARSE_ERROR')
