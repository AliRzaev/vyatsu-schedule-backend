class TestApiV1Groups:
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def test_groups_list(self, flask_app, groups_list_v1, prefetch_groups):
        with flask_app.test_client() as client:
            with flask_app.app_context():
                prefetch_groups()

            response = client.get('/api/v1/groups/list')
            actual = response.json
            expected = groups_list_v1

            assert actual == expected, 'Invalid data'

    def test_groups_by_faculty(self, flask_app, groups_by_faculty_v1,
                               prefetch_groups):
        with flask_app.test_client() as client:
            with flask_app.app_context():
                prefetch_groups()

            response = client.get('/api/v1/groups/by_faculty')
            actual = response.json
            expected = groups_by_faculty_v1

            assert actual == expected, 'Invalid data'


class TestApiV1Calls:

    def test_calls(self, flask_app, calls_v1):
        with flask_app.test_client() as client:
            response = client.get('/api/v1/calls')
            actual = response.json
            expected = calls_v1

            assert actual == expected, 'Invalid data'
