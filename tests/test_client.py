# -*- coding: utf8 -*-

import json
from default import Test
from mock import patch, MagicMock
from pybossa_discourse.client import DiscourseClient


mock_request = MagicMock()
headers = {'content-type': 'application/json; charset=utf-8'}
content = json.dumps({'user': {'username': 'joebloggs', 'id': '1'}})
mock_request.return_value = MagicMock(headers=headers, content=content)

mock_user = MagicMock()
mock_user.email_addr.return_value = 'joebloggs'


class TestClient(Test):

    def setup(self):
        super(TestClient, self).setUp()
        self.url = self.flask_app.config['DISCOURSE_URL']
        self.client = DiscourseClient(self.flask_app)

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_categories(self):
        endpoint = '/categories.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.categories()
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_category(self):
        endpoint = '/c/1.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.category(1)
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_latest_topics_in_category(self):
        endpoint = '/c/1/l/latest.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.latest_topics(1)
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_new_topics_in_category(self):
        endpoint = '/c/1/l/new.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.new_topics(1)
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_top_topics_in_category(self):
        endpoint = '/c/1/l/top.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.top_topics(1)
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_subtopics(self):
        endpoint = '/c/2/1.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.subtopics(1, 2)
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_topic(self):
        endpoint = '/t/1.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.topic(1)
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_new_topics(self):
        endpoint = '/new.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.new_topics()
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_latest_topics(self):
        endpoint = '/latest.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.latest_topics()
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_top_topics(self):
        endpoint = '/top.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.top_topics()
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_details(self):
        endpoint = '/users/joebloggs.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.user_details()
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_activity(self):
        endpoint = '/user_actions.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = {'username': 'joebloggs'}
        self.client.user_activity()
        assert mock_request.called_with('GET', url, params)

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_messages(self):
        endpoint = '/topics/private-messages/joebloggs.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.user_messages()
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_notifications(self):
        endpoint = '/notifications.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = {'username': 'joebloggs'}
        self.client.user_notifications()
        assert mock_request.called_with('GET', url, params)

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_signout(self):
        endpoint = '/admin/users/1/log_out'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.user_signout()
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_badges(self):
        endpoint = '/admin/badges.json'
        url = '{0}{1}'.format(self.url, endpoint)
        self.client.badges()
        assert mock_request.called_with('GET', url, dict())

    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_search(self):
        endpoint = '/search.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = {'q': 'something', 'order': 'posts', 'ascending': 'true'}
        self.client.search('something')
        assert mock_request.called_with('GET', url, params)

    @patch('pybossa_discourse.client.DiscourseClient._create_user')
    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_get_name_returns_none_when_create_user_fails(self, mock_create):
        mock_create.return_value = []
        endpoint = '/admin/users/list/all.json'
        url = '{0}{1}'.format(self.url, endpoint)
        params = {'filter': 'me@me.com'}
        self.client._get_username()
        assert mock_request.called_with('GET', url, params)
