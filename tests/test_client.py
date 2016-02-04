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
    def test_discourse_categories(self):
        endpoint = '/categories.json'
        self.client.discourse_categories()

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_category(self):
        endpoint = '/c/1.json'
        self.client.discourse_category(1)

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_category_topics_latest(self):
        endpoint = '/c/1/l/latest.json'
        self.client.discourse_category_topics_latest(1)

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_category_topics_new(self):
        endpoint = '/c/1/l/new.json'
        self.client.discourse_category_topics_new(1)

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_category_topics_top(self):
        endpoint = '/c/1/l/top.json'
        self.client.discourse_category_topics_top(1)

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_category_topics_subtopics(self):
        endpoint = '/c/2/1.json'
        self.client.discourse_category_topics_subtopics(1, 2)

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_topic(self):
        endpoint = '/t/1.json'
        self.client.discourse_topic(1)

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_topics_latest(self):
        endpoint = '/latest.json'
        self.client.discourse_topics_latest()

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_topics_top(self):
        endpoint = '/top.json'
        self.client.discourse_topics_top()

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_user_details(self):
        endpoint = '/users/joebloggs.json'
        self.client.discourse_user_details()

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_user_activity(self):
        endpoint = '/user_actions.json'
        params = {'username': 'joebloggs'}
        self.client.discourse_user_activity()

        assert mock_request.called_with('GET', endpoint, params)


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_user_messages(self):
        endpoint = '/topics/private-messages/joebloggs.json'
        self.client.discourse_user_messages()

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_user_notifications(self):
        endpoint = '/notifications.json'
        params = {'username': 'joebloggs'}
        self.client.discourse_user_notifications()

        assert mock_request.called_with('GET', endpoint, params)


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_user_unread_notifications_count(self):
        res = self.client.discourse_user_unread_notifications_count()

        assert res == 0


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_user_signout(self):
        endpoint = '/admin/users/1/log_out'
        self.client.discourse_user_signout()

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_badges(self):
        endpoint = '/admin/badges.json'
        self.client.discourse_badges()

        assert mock_request.called_with('GET', endpoint, dict())


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_discourse_search(self):
        endpoint = '/search.json'
        params = {'q': 'something', 'order': 'posts', 'ascending': 'true'}
        self.client.discourse_search('something')

        assert mock_request.called_with('GET', endpoint, params)


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_whitelist_ip(self):
        endpoint = '/admin/logs/screened_ip_addresses.json'
        params = {'ip_address': '1.2.3.4', 'action_name': 'do_nothing'}
        self.client._whitelist_ip('1.2.3.4')

        assert mock_request.called_with('GET', endpoint, params)


    @patch('pybossa_discourse.client.current_user', new=mock_user)
    @patch('pybossa_discourse.client.requests.request', new=mock_request)
    def test_update_setting(self):
        endpoint = '/admin/site_settings/setting'
        params = {'setting': 'value'}
        self.client._update_setting('setting', 'value')

        assert mock_request.called_with('GET', endpoint, params)
