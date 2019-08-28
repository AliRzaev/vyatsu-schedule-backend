import responses

from utils import prefetch
from utils.repository import get_repository
from utils.university import GROUPS_INFO_URL, DEPARTMENTS_INFO_URL


class TestPrefetch:
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    @responses.activate
    def test_prefetch_command(self, flask_app, groups_page, departments_page,
                              groups_info, departments_info):
        responses.add(responses.GET, GROUPS_INFO_URL, groups_page,
                      content_type='text/html; charset=utf8')
        responses.add(responses.GET, DEPARTMENTS_INFO_URL, departments_page,
                      content_type='text/html; charset=utf8')

        with flask_app.app_context():
            get_repository().drop_all()

        runner = flask_app.test_cli_runner()
        result = runner.invoke(args=['prefetch', '--force'])
        assert result.exit_code == 0
        assert result.exception is None

        with flask_app.app_context():
            groups = sorted(get_repository().get_groups())
            departments = sorted(get_repository().get_departments())

            assert groups == groups_info, 'Invalid data'
            assert departments == departments_info, 'Invalid data'

    @responses.activate
    def test_prefetch(self, flask_app, groups_page, departments_page,
                      groups_info, departments_info):
        responses.add(responses.GET, GROUPS_INFO_URL, groups_page,
                      content_type='text/html; charset=utf8')
        responses.add(responses.GET, DEPARTMENTS_INFO_URL, departments_page,
                      content_type='text/html; charset=utf8')

        with flask_app.app_context():
            get_repository().drop_all()

            prefetch.prefetch()

            groups = sorted(get_repository().get_groups())
            departments = sorted(get_repository().get_departments())

            assert groups == groups_info, 'Invalid data'
            assert departments == departments_info, 'Invalid data'
