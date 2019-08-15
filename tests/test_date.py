from datetime import date
from unittest import TestCase

from utils.date import get_date_indexes, get_current_season, as_date


class TestDateIndexes(TestCase):

    def test_left_boundary(self):
        """
        The first day of the given date range gets indexes (0, 0)
        """
        first_date = '12032018'
        today = date(2018, 3, 12)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 0, 'Week index must be 0')

    def test_odd_sunday(self):
        """
        The first (odd) Sunday of the given date range gets indexes of the next
        day, i.e. (1, 0)
        """
        first_date = '12032018'
        today = date(2018, 3, 18)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 1, 'Week index must be 1')

    def test_even_sunday(self):
        """
        The second (even) Sunday of the given date range gets indexes of the next
        day (by modulo 14), i.e. (0, 0)
        """
        first_date = '12032018'
        today = date(2018, 3, 25)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 0, 'Week index must be 0')

    def test_day_before_left_boundary(self):
        """
        The day before the first day of the given date range gets indexes of the
        first day of the date range, i. e. (0, 0)
        """
        first_date = '12032018'
        today = date(2018, 3, 11)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 0, 'Week index must be 0')

    def test_day_after_right_boundary(self):
        """
        The day after the last day of the given date range gets indexes of the
        first day of the date range (by modulo 14), i. e. (0, 0)
        """
        first_date = '12032018'
        today = date(2018, 3, 26)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 0, 'Week index must be 0')

    def test_from_monday_to_saturday_odd(self):
        """
        Test indexes for the first six days of the given date range
        """
        first_date = '12032018'

        for d in range(12, 18):
            today = date(2018, 3, d)
            week, day = get_date_indexes(first_date, today)

            self.assertEqual(day, d - 12, f'Day index must be {d - 12}')
            self.assertEqual(week, 0, 'Week index must be 0')

    def test_from_monday_to_saturday_even(self):
        """
        Test indexes for the first six days (the second week) of the given
        date range
        """
        first_date = '12032018'

        for d in range(19, 24):
            today = date(2018, 3, d)
            week, day = get_date_indexes(first_date, today)

            self.assertEqual(day, d - 19, f'Day index must be {d - 19}')
            self.assertEqual(week, 1, 'Week index must be 1')


class TestCurrentSeason(TestCase):

    def test_autumn_boundaries(self):
        season = get_current_season(date(2018, 8, 1))

        self.assertEqual(season, 'autumn', 'August, 1 belongs to autumn season')

        season = get_current_season(date(2018, 12, 31))

        self.assertEqual(season, 'autumn',
                         'December, 31 belongs to autumn season')

    def test_spring_boundaries(self):
        season = get_current_season(date(2018, 1, 1))

        self.assertEqual(season, 'spring',
                         'January, 1 belongs to spring season')

        season = get_current_season(date(2018, 7, 31))

        self.assertEqual(season, 'spring', 'July, 31 belongs to spring season')


class TestAsDate(TestCase):

    def test_as_date(self):
        date_str = '31102018'

        actual = as_date(date_str)
        expected = date(2018, 10, 31)

        self.assertEqual(actual, expected, 'Date must be date(2018, 10, 31)')

    def test_as_date_invalid_str(self):
        date_str = '31112018'

        self.assertRaises(ValueError, as_date, date_str)
