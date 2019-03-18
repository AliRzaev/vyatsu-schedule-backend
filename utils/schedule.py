from functools import lru_cache
from os import getenv

import requests
import xlrd

from utils.extractors import DateRange

_PDF2JSON_API_URL = getenv('PDF2JSON_API_URL')

_GROUP_URL_TEMPLATE = 'https://www.vyatsu.ru/reports/schedule/Group/{}_{}_{}_{}.pdf'

_DEPARTMENT_URL_TEMPLATE = 'https://www.vyatsu.ru/reports/schedule/prepod/{}_{}_{}_{}.xls'


class ParseException(Exception):
    pass


@lru_cache(maxsize=512)
def fetch_group_schedule(group_id: str, season_key: str, range_: DateRange):
    api_url = _PDF2JSON_API_URL + '/api/v2/convert'
    pdf_url = _GROUP_URL_TEMPLATE.format(group_id, season_key,
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


@lru_cache(maxsize=512)
def fetch_department_schedule(department_id: str, season_key: str,
                              range_: DateRange):
    def build_teacher_schedule(cols):
        teacher_name = cols[0]
        schedule = [
            cols[1 + i * 7:1 + i * 7 + 7] for i in range(12)
        ]
        return {
            'teacher': teacher_name,
            'schedule': [schedule[:6], schedule[6:]]
        }

    xls_url = _DEPARTMENT_URL_TEMPLATE.format(department_id, season_key,
                                              range_[0], range_[1])

    response = requests.get(xls_url)
    response.raise_for_status()

    workbook = xlrd.open_workbook(file_contents=response.content)
    sheet = workbook.sheet_by_index(0)
    teachers_count = sheet.row_len(1) - 2

    if teachers_count < 1:
        return []
    else:
        teachers_schedules = [
            build_teacher_schedule(sheet.col_values(i + 2, 1))
            for i in range(teachers_count)
            if sheet.cell_value(1, i + 2) != ''
        ]

        return teachers_schedules
