from functools import lru_cache
from os import getenv

import requests

from utils.groups_info import DateRange

_PDF2JSON_API_URL = getenv('PDF2JSON_API_URL')

_URL_TEMPLATE = 'https://www.vyatsu.ru/reports/schedule/Group/{}_{}_{}_{}.pdf'


class ParseException(Exception):
    pass


@lru_cache(maxsize=512)
def fetch_schedule(group_id: str, season_key: str, range_: DateRange):
    api_url = _PDF2JSON_API_URL + '/api/v2/convert'
    pdf_url = _URL_TEMPLATE.format(group_id, season_key,
                                   range_[0], range_[1])

    response = requests.get(api_url, params={'url': pdf_url})
    response.raise_for_status()

    data = response.json()

    if 'success' in data['meta']:
        return data['data']['schedule']
    elif 'error' in data['meta']:
        raise ParseException(data['meta']['error'])
    else:
        raise ParseException('PDF_PARSE_ERROR')
