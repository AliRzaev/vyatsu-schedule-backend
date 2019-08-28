class TestApiV2Groups:
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def test_groups_list(self, flask_app, groups_list_v2, prefetch_groups):
        with flask_app.test_client() as client:
            with flask_app.app_context():
                prefetch_groups()

            response = client.get('/api/v2/groups/list')
            actual = response.json
            expected = groups_list_v2

        assert actual == expected, 'Invalid data'

    def test_groups_by_faculty(self, flask_app, groups_by_faculty_v2,
                               prefetch_groups):
        with flask_app.test_client() as client:
            with flask_app.app_context():
                prefetch_groups()

            response = client.get('/api/v2/groups/by_faculty')
            actual = response.json
            expected = groups_by_faculty_v2

            assert actual == expected, 'Invalid data'


class TestApiV2Departments:
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def test_departments_list(self, flask_app, departments_list_v2,
                              prefetch_departments):
        with flask_app.test_client() as client:
            with flask_app.app_context():
                prefetch_departments()

            response = client.get('/api/v2/departments/list')
            actual = response.json
            expected = departments_list_v2

            assert actual == expected, 'Invalid data'

    def test_departments_by_faculty(self, flask_app, departments_by_faculty_v2,
                                    prefetch_departments):
        with flask_app.test_client() as client:
            with flask_app.app_context():
                prefetch_departments()

            response = client.get('/api/v2/departments/by_faculty')
            actual = response.json
            expected = departments_by_faculty_v2

            assert actual == expected, 'Invalid data'


class TestApiV2Calls:

    def test_calls(self, flask_app, calls_v2):
        with flask_app.test_client() as client:
            response = client.get('/api/v2/calls')
            actual = response.json
            expected = calls_v2

            assert actual == expected, 'Invalid data'
