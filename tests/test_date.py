from unittest import TestCase
from datetime import date
from utils.date import get_date_indexes, get_current_season


class TestDateIndexes(TestCase):

    def test_left_boundary(self):
        first_date = '12032018'
        today = date(2018, 3, 12)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 0, 'Week index must be 0')

    def test_odd_sunday(self):
        first_date = '12032018'
        today = date(2018, 3, 18)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 1, 'Week index must be 0')

    def test_even_sunday(self):
        first_date = '12032018'
        today = date(2018, 3, 25)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 0, 'Week index must be 0')

    def test_day_before_left_boundary(self):
        first_date = '12032018'
        today = date(2018, 3, 11)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 0, 'Week index must be 0')

    def test_day_after_right_boundary(self):
        first_date = '12032018'
        today = date(2018, 3, 26)

        week, day = get_date_indexes(first_date, today)

        self.assertEqual(day, 0, 'Day index must be 0')
        self.assertEqual(week, 0, 'Week index must be 0')

    def test_from_monday_to_saturday_odd(self):
        first_date = '12032018'

        for d in range(12, 18):
            today = date(2018, 3, d)
            week, day = get_date_indexes(first_date, today)

            self.assertEqual(day, d - 12, f'Day index must be {d - 12}')
            self.assertEqual(week, 0, 'Week index must be 0')

    def test_from_monday_to_saturday_even(self):
        first_date = '12032018'

        for d in range(19, 24):
            today = date(2018, 3, d)
            week, day = get_date_indexes(first_date, today)

            self.assertEqual(day, d - 19, f'Day index must be {d - 19}')
            self.assertEqual(week, 1, 'Week index must be 1')


class TestCurrentSeason(TestCase):

    def test_autumn_boundaries(self):
        season = get_current_season(date(2018, 9, 1))

        self.assertEqual(season, 'autumn', '1st September belongs to autumn season')

        season = get_current_season(date(2018, 12, 31))

        self.assertEqual(season, 'autumn', '31st December belongs to autumn season')

    def test_spring_boundaries(self):
        season = get_current_season(date(2018, 1, 1))

        self.assertEqual(season, 'spring', '1st January belongs to spring season')

        season = get_current_season(date(2018, 8, 31))

        self.assertEqual(season, 'spring', '31st August belongs to spring season')
