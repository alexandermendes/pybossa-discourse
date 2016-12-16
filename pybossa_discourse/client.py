# -*- coding: utf8 -*-
"""Discourse client module for pybossa-discourse."""

import uuid
import requests
from flask.ext.login import current_user
from pybossa.error import ErrorStatus


class DiscourseClient(object):
    """A class to interact with the Discourse API.

    :param app: The PyBossa application.
    """

    def __init__(self, app=None):
        if app is not None:  # pragma: no cover
            self.init_app(app)

    def init_app(self, app):
        self.url = app.config['DISCOURSE_URL']
        self.api_key = app.config['DISCOURSE_API_KEY']
        self.api_username = app.config['DISCOURSE_API_USERNAME']
        self.error_status = ErrorStatus()

    def _request(self, verb, endpoint, params):
        """Make a request."""
        url = '{0}{1}'.format(self.url, endpoint)
        params['api_key'] = self.api_key
        params['api_username'] = self.api_username

        try:
            res = requests.request(verb, url, params=params)
        except requests.RequestException as e:  # pragma: no cover
            return []

        try:
            return res.json()
        except ValueError as e:  # pragma: no cover
            return []

    def _get(self, endpoint, params=dict()):
        """Make a GET request."""
        return self._request('GET', endpoint, params)

    def _post(self, endpoint, params=dict()):
        """Make a POST request."""
        return self._request('POST', endpoint, params)

    def _put(self, endpoint, params=dict()):
        """Make a PUT request."""
        return self._request('PUT', endpoint, params)

    def _create_user(self):
        """Create a new Discourse user based on the current users email."""
        endpoint = '/users'
        random_name = str(uuid.uuid4().get_hex().upper()[0:15])
        random_username = str(uuid.uuid4().get_hex().upper()[0:15])
        params = {'name': random_name,
                  'username': random_username,
                  'email': current_user.email_addr,
                  'password': 'P@ssword',
                  'active': 'true',
                  }
        return self._post(endpoint, params)

    def _get_username(self):
        """Return the current user's Discourse username.

        A new Discourse user will be created first, if necessary.
        """
        if current_user.is_anonymous():
            return None

        endpoint = '/admin/users/list/all.json'
        params = {'filter': current_user.email_addr}
        res = self._get(endpoint, params)

        # Attempt to create a new user
        if len(res) == 0:
            self._create_user()
            res = self._get(endpoint, params)

        return res[0]['username'] if len(res) != 0 else None

    def categories(self):
        """Return all categories."""
        endpoint = '/categories.json'
        res = self._get(endpoint)
        return res.category_list.categories

    def category(self, category_id):
        """Return all topics in a category.

        :param category_id: The ID of the category.
        """
        endpoint = '/c/{0}.json'.format(category_id)
        res = self._get(endpoint)
        return res.topic_list.topics

    def subtopics(self, category_id, p_category_id):
        """Return the topics in a sub-category.

        :param p_category_id: The ID of the parent category.
        :param category_id: The ID of the category.
        """
        endpoint = '/c/{0}/{1}.json'.format(p_category_id, category_id)
        res = self._get(endpoint)
        return res.topic_list.topics

    def topic(self, topic_id):
        """Return a specific topic.

        :param topic_id: The ID of the topic.
        """
        endpoint = '/t/{0}.json'.format(topic_id)
        return self._get(endpoint)

    def new_topics(self, category_id=None):
        """Return the newest topics in a category.

        :param category_id: Optional category ID by which to filter topics.
        """
        endpoint = '/new.json'
        if category_id:
            endpoint = '/c/{0}/l{1}'.format(category_id, endpoint)
        res = self._get(endpoint)
        return res.topic_list.topics

    def latest_topics(self, category_id=None):
        """Return the latest topics.

        :param category_id: Optional category ID by which to filter topics.
        """
        endpoint = '/latest.json'
        if category_id:
            endpoint = '/c/{0}/l{1}'.format(category_id, endpoint)
        res = self._get(endpoint)
        return res.topic_list.topics

    def top_topics(self, category_id=None):
        """Return the top topics.

        :param category_id: Optional category ID by which to filter topics.
        """
        endpoint = '/top.json'
        if category_id:
            endpoint = '/c/{0}/l{1}'.format(category_id, endpoint)
        res = self._get(endpoint)
        return res.topic_list.topics

    def user_details(self):
        """Return the current user's details."""
        username = self._get_username()
        if not username:
            return []

        endpoint = '/users/{0}.json'.format(username)
        return self._get(endpoint)

    def user_activity(self):
        """Return the current user's recent activity.

        :param username: The user's Discourse username.
        """
        username = self._get_username()
        if not username:
            return []

        endpoint = '/user_actions.json'
        params = {'username': username}
        res = self._get(endpoint, params)
        return res.user_actions

    def user_notifications(self):
        """Return the current user's notifications."""
        username = self._get_username()
        if not username:
            return []

        endpoint = '/notifications.json'
        params = {'username': username}
        res = self._get(endpoint, params)
        return res.notifications

    def user_signout(self):
        """Sign out the current user from Discourse."""
        details = self.user_details()
        if not details:
            return None

        user_id = details['user']['id']
        endpoint = '/admin/users/{0}/log_out'.format(user_id)
        return self._post(endpoint)

    def badges(self):
        """Return all badges."""
        endpoint = '/admin/badges.json'
        return self._get(endpoint)

    def search(self, query):
        """Perform a search.

        :param query: The search query.
        """
        endpoint = '/search.json'
        params = {'q': query, 'order': 'posts', 'ascending': 'true'}
        return self._get(endpoint, params)
