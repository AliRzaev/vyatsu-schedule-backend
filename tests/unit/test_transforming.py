from utils.transforming import api_v1, api_v2


class TestTransformingV1:

    def test_groups_list(self, groups_info, groups_list_v1):
        actual = api_v1.groups_info_to_dict(tuple(groups_info))
        expected = groups_list_v1

        assert actual == expected, 'Invalid transformation'

    def test_groups_by_faculty(self, groups_info, groups_by_faculty_v1):
        actual = api_v1.groups_info_to_dict(tuple(groups_info), True)
        expected = groups_by_faculty_v1

        assert actual == expected, 'Invalid transformation'


class TestTransformingV2:

    def test_groups_list(self, groups_info, groups_list_v2):
        actual = api_v2.groups_info_to_list(tuple(groups_info))
        expected = groups_list_v2

        assert actual == expected, 'Invalid transformation'

    def test_groups_by_faculty(self, groups_info, groups_by_faculty_v2):
        actual = api_v2.groups_info_to_list(tuple(groups_info), True)
        expected = groups_by_faculty_v2

        assert actual == expected, 'Invalid transformation'

    def test_departments_list(self, departments_info, departments_list_v2):
        actual = api_v2.departments_info_to_list(tuple(departments_info))
        expected = departments_list_v2

        assert actual == expected, 'Invalid transformation'

    def test_departments_by_faculty(self, departments_info,
                                    departments_by_faculty_v2):
        actual = api_v2.departments_info_to_list(tuple(departments_info), True)
        expected = departments_by_faculty_v2

        assert actual == expected, 'Invalid transformation'
