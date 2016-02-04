# -*- coding: utf8 -*-

import json
from default import Test
from mock import patch, MagicMock

mock_request = MagicMock()
headers = {'content-type': 'application/json; charset=utf-8'}
content = json.dumps({'user': {'username': 'joebloggs', 'id': '1'}})
mock_request.return_value = MagicMock(headers=headers, content=content)

mock_user = MagicMock()
mock_user.email_addr.return_value = 'joebloggs'


class TestClient(Test):


    def setUp(self):
        super(TestClient, self).setUp()
        self.client = self.flask_app.extensions['discourse']['client']


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_categories(self):
        endpoint = '/categories.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.categories()

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_category(self):
        endpoint = '/c/1.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.category(1)

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_category_topics_latest(self):
        endpoint = '/c/1/l/latest.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.category_topics_latest(1)

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_category_topics_new(self):
        endpoint = '/c/1/l/new.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.category_topics_new(1)

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_category_topics_top(self):
        endpoint = '/c/1/l/top.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.category_topics_top(1)

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_category_topics_subtopics(self):
        endpoint = '/c/2/1.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.category_topics_subtopics(1, 2)

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_topic(self):
        endpoint = '/t/1.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.topic(1)

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_topics_latest(self):
        endpoint = '/latest.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.topics_latest()

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_topics_top(self):
        endpoint = '/top.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.topics_top()

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_details(self):
        endpoint = '/users/joebloggs.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.user_details()

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_activity(self):
        endpoint = '/user_actions.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        params = {'username': 'joebloggs'}
        self.client.user_activity()

        assert mock_request.called_with('GET', url, params)


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_messages(self):
        endpoint = '/topics/private-messages/joebloggs.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.user_messages()

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_notifications(self):
        endpoint = '/notifications.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        params = {'username': 'joebloggs'}
        self.client.user_notifications()

        assert mock_request.called_with('GET', url, params)


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_unread_notifications_count(self):
        res = self.client.user_unread_notifications_count()

        assert res == 0


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_user_signout(self):
        endpoint = '/admin/users/1/log_out'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.user_signout()

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_badges(self):
        endpoint = '/admin/badges.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        self.client.badges()

        assert mock_request.called_with('GET', url, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_search(self):
        endpoint = '/search.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        params = {'q': 'something', 'order': 'posts', 'ascending': 'true'}
        self.client.search('something')

        assert mock_request.called_with('GET', url, params)


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_whitelist_ip(self):
        endpoint = '/admin/logs/screened_ip_addresses.json'
        url = '{0}{1}'.format(self.domain, endpoint)
        params = {'ip_address': '1.2.3.4', 'action_name': 'do_nothing'}
        self.client._whitelist_ip('1.2.3.4')

        assert mock_request.called_with('GET', url, params)


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_update_setting(self):
        endpoint = '/admin/site_settings/setting'
        url = '{0}{1}'.format(self.domain, endpoint)
        params = {'setting': 'value'}
        self.client._update_setting('setting', 'value')

        assert mock_request.called_with('GET', url, params)
