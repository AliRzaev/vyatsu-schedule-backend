from unittest import TestCase
from updaters.groups_updater import get_groups_with_faculty, URL


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
        print(len(data))
        self.assertTrue(all(test_item(item) for item in data), 'Invalid data')
