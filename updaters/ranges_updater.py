import re
import requests
from utils.wrappers import comparable_mixin
from datetime import date

P_AUTUMN = re.compile(r'/reports/schedule/Group/(\d{4})_1_(\d{8})_(\d{8})\.pdf')
P_SPRING = re.compile(r'/reports/schedule/Group/(\d{4})_2_(\d{8})_(\d{8})\.pdf')

URL = 'https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html'


@comparable_mixin
class DateRange:

    def __init__(self, first, second):
        self.first = first
        self.second = second

        d = int(first[:2])
        m = int(first[2:4])
        y = int(first[4:])
        self.first_date = date(y, m, d)

    def __lt__(self, other):
        return self.first_date < other.first_date


def get_date_ranges(pattern):
    html = requests.get(URL).text

    date_ranges = dict()

    for match in re.finditer(pattern, html):
        group_id, first, second = match.groups()
        new_range = DateRange(first, second)

        if group_id not in date_ranges:
            date_ranges[group_id] = new_range
        elif new_range > date_ranges[group_id]:
            date_ranges[group_id] = new_range

    return {group_id: (date_range.first, date_range.second) for group_id, date_range in date_ranges.items()}
