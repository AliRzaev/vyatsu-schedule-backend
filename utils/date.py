from datetime import date
from typing import Tuple


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
        today = date.today()

    d = int(first_date[:2])
    m = int(first_date[2:4])
    y = int(first_date[4:])
    begin = date(y, m, d)

    diff = (today - begin).days
    week_index = (diff // 7) % 2
    day_index = diff % 7

    if day_index == 5:  # sunday, go to monday
        day_index = (day_index + 1) % 7
        week_index = (week_index + 1) % 2

    return week_index, day_index
