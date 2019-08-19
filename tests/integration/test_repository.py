from utils.repository import get_repository


class TestRepository:
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def test_get_departments(self, flask_app, departments_info,
                             prefetch_departments):
        with flask_app.app_context():
            prefetch_departments()

            actual = sorted(get_repository().get_departments())
            expected = departments_info

            assert actual == expected, 'Invalid data'

    def test_get_groups(self, flask_app, groups_info, prefetch_groups):
        with flask_app.app_context():
            prefetch_groups()

            actual = sorted(get_repository().get_groups())
            expected = groups_info

            assert actual == expected, 'Invalid data'
