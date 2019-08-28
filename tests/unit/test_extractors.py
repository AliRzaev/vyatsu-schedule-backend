from utils.extractors import extract_date_ranges, extract_groups, \
    extract_departments, extract_departments_date_ranges


class TestExtractors:

    def test_extract_groups(self, groups_page, groups_info):
        actual = sorted(extract_groups(groups_page))
        expected = groups_info

        assert actual == expected, 'Data mismatch'

    def test_extract_date_ranges(self, groups_page, groups_ranges):
        actual = extract_date_ranges(groups_page)
        expected = groups_ranges

        assert actual == expected, 'Data mismatch'

    def test_extract_departments(self, departments_page, departments_info):
        actual = sorted(extract_departments(departments_page))
        expected = departments_info

        assert actual == expected, 'Data mismatch'

    def test_extract_departments_date_ranges(self, departments_page,
                                             departments_ranges):
        actual = extract_departments_date_ranges(departments_page)
        expected = departments_ranges

        assert actual == expected, 'Data mismatch'
