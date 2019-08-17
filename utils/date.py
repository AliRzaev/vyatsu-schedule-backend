from datetime import date, timedelta, datetime
from email.utils import formatdate
from time import mktime
from typing import Tuple


def as_date(date_str: str) -> date:
    """
    Return a date corresponding to a date_str in the format 'ddMMyyyy'.
    """
    d = int(date_str[:2])
    m = int(date_str[2:4])
    y = int(date_str[4:])
    return date(y, m, d)


def as_rfc2822(date_: date) -> str:
    """
    Return a date string as per RFC 2822.
    """
    stamp = mktime(datetime(date_.year, date_.month, date_.day).timetuple())
    return formatdate(stamp, usegmt=True)


def get_date_indexes(first_date: str, today: date = None) -> Tuple[int, int]:
    """
    Compute week and day indexes of the given day from the first day
    of the date range of schedule. If the given day is Sunday, function returns
    indexes for a next day by modulo 14.

    :param first_date: the beginning of the date range
    :param today: the day the indexes will be computed for
    :return: tuple of two numbers: week index (0..1) and day index (0..5)
    """
    if today is None:
        today = get_moscow_today()

    begin = as_date(first_date)

    diff = (today - begin).days
    week_index = (diff // 7) % 2
    day_index = diff % 7

    if day_index == 6:  # sunday, go to monday
        day_index = (day_index + 1) % 7
        week_index = (week_index + 1) % 2

    return week_index, day_index


def get_current_season(today: date = None) -> str:
    """
    Determine a season the given day belongs to.
    Season 'autumn': from August, 1 to December, 31.
    Season 'spring': from January, 1 to July, 31.

    :param today: the day the season will be determined for
    :return: 'autumn' or 'spring'
    """
    if today is None:
        today = get_moscow_today()

    if 8 <= today.month <= 12:
        return 'autumn'
    else:
        return 'spring'


# TODO: write unit tests
def get_date_by_indexes(first_date: str, week_index: int, day_index) -> str:
    """
    Get the date that corresponds the given day and week
    indexes according to the beginning of the date range.

    :param first_date: the beginning of the date range as string of
                       the following format: 'ddMMyyyy'
    :param week_index: week index (0..1)
    :param day_index: day index (0..6)
    :return: the date as string of the following format: 'ddMMyyyy'
    """
    day_offset = week_index * 7 + day_index
    delta = timedelta(days=day_offset)

    begin = as_date(first_date)
    begin += delta

    return '{d:02}{m:02}{y:04}'.format(d=begin.day, m=begin.month, y=begin.year)


def get_date_of_weekday(weekday: int, today: date = None) -> date:
    """
    Get the nearest (may be today) date of the given weekday (0..6).
    """
    if today is None:
        today = get_moscow_today()

    offset = (7 + weekday - today.weekday()) % 7
    return today + timedelta(days=offset)


def get_moscow_today() -> date:
    return (datetime.utcnow() + timedelta(hours=3)).date()
