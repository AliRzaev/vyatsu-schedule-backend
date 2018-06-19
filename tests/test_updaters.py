from unittest import TestCase
from updaters.groups_updater import get_groups_with_faculty, URL
from updaters.ranges_updater import build_arg_parser, get_date_ranges, P_SPRING, P_AUTUMN
import re


class TestGroupsUpdater(TestCase):

    def test_groups_extracting(self):
        def test_item(item):
            faculty, group_name, group_id = item

            if faculty is None or group_name is None or group_id is None:
                return False

            if group_name == '' or faculty == '':
                return False

            if not group_id.isnumeric():
                return False

            return True

        data = list(get_groups_with_faculty(URL))

        self.assertTrue(len(data) > 0, 'No groups were extracted')
        print(f'{len(data)} groups were extracted')
        self.assertTrue(all(test_item(item) for item in data), 'Invalid data')


class TestRangesUpdaterArgs(TestCase):

    def test_args_force_short(self):
        cmd_args = ['-f']  # shorthand for '--force'
        parser = build_arg_parser()
        args = parser.parse_args(cmd_args)

        self.assertTrue(args.force, "Argument '-f' wasn't recognized")

    def test_args_force_full(self):
        cmd_args = ['--force']
        parser = build_arg_parser()
        args = parser.parse_args(cmd_args)

        self.assertTrue(args.force, "Argument '--force' wasn't recognized")

    def test_args_drop_old_short(self):
        cmd_args = ['-d']  # shorthand for '--drop-old'
        parser = build_arg_parser()
        args = parser.parse_args(cmd_args)

        self.assertTrue(args.drop_old, "Argument '-d' wasn't recognized")

    def test_args_drop_old_full(self):
        cmd_args = ['--drop-old']
        parser = build_arg_parser()
        args = parser.parse_args(cmd_args)

        self.assertTrue(args.drop_old, "Argument '--drop-old' wasn't recognized")


class TestRangesUpdater(TestCase):

    @staticmethod
    def _item_test(item):
        pattern = re.compile(r'\d{8}')

        group_id, _range = item

        if _range is None or group_id is None:
            return False

        if not group_id.isnumeric() or \
                not _range[0].isnumeric() or \
                not _range[1].isnumeric():
            return False

        if re.match(pattern, _range[0]) is None or \
                re.match(pattern, _range[1]) is None:
            return False

        return True

    def test_ranges_extracting_autumn(self):

        data = get_date_ranges(P_AUTUMN)

        self.assertTrue(len(data) > 0, 'No ranges were extracted')
        print(f"Season 'autumn': {len(data)} ranges")
        self.assertTrue(all(self._item_test(item) for item in data.items()), 'Invalid data')

    def test_ranges_extracting_spring(self):

        data = get_date_ranges(P_SPRING)

        self.assertTrue(len(data) > 0, 'No ranges were extracted')
        print(f"Season 'spring': {len(data)} ranges")
        self.assertTrue(all(self._item_test(item) for item in data.items()), 'Invalid data')
