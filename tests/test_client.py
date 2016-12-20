# -*- coding: utf8 -*-

import json
import uuid
from default import Test, FakeResponse
from mock import patch, MagicMock
from pybossa_discourse.client import DiscourseClient

mock_response = MagicMock()
headers = {'content-type': 'application/json; charset=utf-8'}
mock_response.json.return_value = MagicMock()
mock_response.return_value = MagicMock(headers=headers)

mock_user = MagicMock()
mock_user.is_anonymous.return_value = False
mock_user.email_addr.return_value = 'joebloggs@example.com'


@patch('pybossa_discourse.client.requests.request')
class TestClient(Test):

    def setup(self):
        super(TestClient, self).setUp()
        self.url = self.flask_app.config['DISCOURSE_URL']
        self.api_key = self.flask_app.config['DISCOURSE_API_KEY']
        self.api_username = self.flask_app.config['DISCOURSE_API_USERNAME']
        self.client = DiscourseClient(self.flask_app)

    def get_params(self, **kwargs):
        return dict(api_key=self.api_key,
                    api_username=self.api_username,
                    **kwargs)

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.DiscourseClient._get_unique_id')
    def test_create_user(self, mock_id, mock_request):
        mock_request.return_value = mock_response
        mock_id.return_value = '1234'
        endpoint = '/users'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params(name='1234',
                                 username='1234',
                                 email=mock_user.email_addr,
                                 password='P@ssword',
                                 active='true')
        self.client._create_user()
        assert mock_request.called_with('POST', url, params=params)

    def test_categories(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/categories.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.categories()
        mock_request.assert_called_with('GET', url, params=params)

    def test_category(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/c/1.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.category(1)
        mock_request.assert_called_with('GET', url, params=params)

    def test_latest_topics_in_category(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/c/1/l/latest.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.latest_topics(1)
        mock_request.assert_called_with('GET', url, params=params)

    def test_new_topics_in_category(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/c/1/l/new.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.new_topics(1)
        mock_request.assert_called_with('GET', url, params=params)

    def test_top_topics_in_category(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/c/1/l/top.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.top_topics(1)
        mock_request.assert_called_with('GET', url, params=params)

    def test_subtopics(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/c/2/1.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.subtopics(1, 2)
        mock_request.assert_called_with('GET', url, params=params)

    def test_topic(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/t/1.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.topic(1)
        mock_request.assert_called_with('GET', url, params=params)

    def test_new_topics(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/new.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.new_topics()
        mock_request.assert_called_with('GET', url, params=params)

    def test_latest_topics(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/latest.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.latest_topics()
        mock_request.assert_called_with('GET', url, params=params)

    def test_top_topics(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/top.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.top_topics()
        mock_request.assert_called_with('GET', url, params=params)

    @patch('pybossa_discourse.client.DiscourseClient._get_username')
    def test_user_details(self, mock_get_username, mock_request):
        mock_request.return_value = mock_response
        mock_get_username.return_value = 'joebloggs'
        endpoint = '/users/joebloggs.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.user_details()
        mock_request.assert_called_with('GET', url, params=params)

    @patch('pybossa_discourse.client.DiscourseClient._get_username')
    def test_user_activity(self, mock_get_username, mock_request):
        mock_request.return_value = mock_response
        mock_get_username.return_value = 'joebloggs'
        endpoint = '/user_actions.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params(username='joebloggs')
        self.client.user_activity()
        mock_request.assert_called_with('GET', url, params=params)

    @patch('pybossa_discourse.client.DiscourseClient._get_username')
    def test_user_notifications(self, mock_get_username, mock_request):
        mock_request.return_value = mock_response
        mock_get_username.return_value = 'joebloggs'
        endpoint = '/notifications.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params(username='joebloggs')
        self.client.user_notifications()
        assert mock_request.called_with('GET', url, params)

    @patch('pybossa_discourse.client.DiscourseClient.user_details')
    def test_user_signout(self, mock_user_details, mock_request):
        mock_request.return_value = mock_response
        mock_user_details.return_value = {"user": {"id": 1}}
        endpoint = '/admin/users/1/log_out'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.user_signout()
        mock_request.assert_called_with('POST', url, params=params)

    def test_badges(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/admin/badges.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params()
        self.client.badges()
        mock_request.assert_called_with('GET', url, params=params)

    def test_search(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/search.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params(q='something',
                                 order='posts',
                                 ascending='true')
        self.client.search('something')
        assert mock_request.called_with('GET', url, params)

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    def test_get_username(self, mock_request):
        mock_request.return_value = mock_response
        endpoint = '/admin/users/list/all.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = self.get_params(filter=mock_user.email_addr)
        self.client._get_username()
        assert mock_request.called_with('GET', url, params)
