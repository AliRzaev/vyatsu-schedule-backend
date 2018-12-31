from datetime import date, timedelta, datetime
from typing import Tuple


def as_date(date_str: str) -> date:
    """
    Return the date corresponding to a date_str in the format ddMMyyyy
    """
    d = int(date_str[:2])
    m = int(date_str[2:4])
    y = int(date_str[4:])
    return date(y, m, d)


def get_date_indexes(first_date: str, today: date = None) -> Tuple[int, int]:
    """
    Compute week and day indexes from the begin of the first
    day of schedule range for today or another given day.
    If the given is sunday, function returns indexes of the
    next day after sunday.
    :param first_date: the begin of the schedule range
    :param today: the day for which indexes will be computed.
    :return: tuple of two numbers: week index (0 or 1) and day index (from 0 to 5 inclusive)
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
    Determine which season does given day belong to.
    Season 'autumn': from 1st August to 31st December.
    Season 'spring': from 1st January to 31st July
    :param today: the day for which season will be determined
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
    Get the date that corresponds given day and week indexes according to the begin date - first_date
    :param first_date: date string of the following format: 'ddMMyyyy'
    :param week_index: week index from 0 to 1
    :param day_index: day index, from 0 to 6
    :return: date string of the following format: 'ddMMyyyy'
    """
    day_offset = week_index * 7 + day_index
    delta = timedelta(days=day_offset)

    begin = as_date(first_date)
    begin += delta

    return '{d:02}{m:02}{y:04}'.format(d=begin.day, m=begin.month, y=begin.year)


def get_date_of_weekday(weekday: int, today: date = None) -> date:
    """
    Get the nearest (may be today) date of the weekday
    """
    if today is None:
        today = get_moscow_today()

    offset = (7 + weekday - today.weekday()) % 7
    return today + timedelta(days=offset)


def get_moscow_today() -> date:
    return (datetime.utcnow() + timedelta(hours=3)).date()
