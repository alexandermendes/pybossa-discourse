# -*- coding: utf8 -*-
"""Client module for pybossa-discourse."""

import socket
import uuid
import requests
from flask_discourse.exceptions import DiscourseError


class DiscourseClient(object):
    """Discourse client class for consuming the Discourse API.

    :param app: The PyBossa application
    """


    def __init__(self, app=None):
        if app:
            self.init_app(app)


    def init_app(self, app):
        discourse = app.extensions['discourse']
        self.api_key = discourse.api_key
        self.api_username = discourse.api_username
        self.domain = discourse.domain


    def _request(self, verb, endpoint, params):
        """Make an API request."""
        url = '{0}{1}'.format(self.domain, endpoint)
        params['api_key'] = self.api_key
        params['api_username'] = self.api_username

        try:
            res = requests.request(verb, url, params=params)
        except requests.RequestException as e:
            raise DiscourseError(e)

         # Some API calls return an empty response
        if res.text == " ":
            return None

        try:
            print(res.content)
            decoded = res.json()
        except ValueError as e:
            raise DiscourseError(e)

        return decoded


    def _get(self, endpoint, params=dict()):
        return self._request('GET', endpoint, params)


    def _post(self, endpoint, params=dict()):
        return self._request('POST', endpoint, params)


    def _put(self, endpoint, params=dict()):
        return self._request('PUT', endpoint, params)


    def _delete(self, endpoint, params=dict()):
        return self._request('DELETE', endpoint, params)


    def categories(self):
        """Return all categories."""
        url = '/categories.json'
        return self._get(url)


    def category(self, category_id):
        """Return all topics in a category.

        :param category_id: The ID of the category.
        """
        url = '/c/{0}.json'.format(category_id)
        return self._get(url)


    def category_topics_latest(self, category_id):
        """Return the latest topics in a category.

        :param category_id: The ID of the category.
        """
        url = '/c/{0}/l/latest.json'.format(category_id)
        return self._get(url)


    def category_topics_new(self, category_id):
        """Return the newest topics in a category.

        :param category_id: The ID of the category.
        """
        url = '/c/{0}/l/new.json'.format(category_id)
        return self._get(url)


    def category_topics_top(self, category_id):
        """Return the top topics in a category.

        :param category_id: The ID of the category.
        """
        url = '/c/{0}/l/top.json'.format(category_id)
        return self._get(url)


    def category_topics_subtopics(self, category_id, parent_category_id):
        """Return the topics in a sub-category.

        :param parent_category_id: The ID of the parent category.
        :param category_id: The ID of the category.
        """
        url = '/c/{0}/{1}.json'.format(parent_category_id, category_id)
        return self._get(url)


    def topic(self, topic_id):
        """Return a specific topic.

        :param topic_id: The ID of the topic.
        """
        url = '/t/{0}.json'.format(topic_id)
        return self._get(url)


    def topics_latest(self):
        """Return the latest topics."""
        url = '/latest.json'
        return self._get(url)


    def topics_top(self):
        """Return the top topics."""
        url = '/top.json'
        return self._get(url)


    def user_details(self, username):
        """Return a user's details.

        :param username: The user's Discourse username.
        """
        url = '/users/{0}.json'.format(username)
        return self._get(url)


    def user_username(self, email):
        """Return a user's Discourse username, creating the user if necessary.

        :param email: The user's Discourse email address.
        """
        url = '/admin/users/list/all.json'
        params = {'filter' : user.email}
        res = self._get(url, params)

        if len(res) == 0:
            self.create_user(user)

        res = self._get(url, params)
        return res[0]['username']


    def user_id(self, username):
        """Return a user's Discourse ID.

        :param username: The user's Discourse username.
        """
        details = self.user_details(username)
        user_id = details['user']['id']
        return user_id


    def user_title(self, username):
        """Return a user's title.

        :param username: The user's Discourse username.
        """
        details = self.user_details(username)
        title = details['user']['title']
        return title


    def update_user_trust_level(self, username, level):
        """Update a user's trust level.

        :param username: The user's Discourse username.
        :param level: The trust level to be set for the user.
        """
        user_id = self.user_id(user)
        url = '/admin/users/{0}/trust_level'.format(user_id)
        params = {'user_id' : user_id, 'level' : level}
        return self._put(url, params)


    def user_activity(self, username):
        """Return the user's recent activity.

        :param username: The user's Discourse username.
        """
        url = '/user_actions.json'
        params = {'username' : username}
        return self._get(url, params)


    def user_messages(self, username):
        """Return a user's private messages.

        :param username: The user's Discourse username.
        """
        url = '/topics/private-messages/{0}.json'.format(username)
        return self._get(url)


    def user_notifications(self, username):
        """Return notifications for a user.

        :param username: The user's Discourse username.
        """
        url = '/notifications.json'
        params = {'username' : username}
        return self._get(url, params)


    def user_notifications_count(self, username):
        """Return a count of unread notifications for a user.

        :param username: The user's Discourse username.
        """
        notifications = self.notifications(username)
        count = sum([1 for n in notifications['notifications']
                     if not n['read']])
        return count


    def user_notifications_markread(self, username):
        """Mark a user's notifications as read.

        :param username: The user's Discourse username.
        """
        url = '/notifications/mark-read.json'
        params = {'username' : username}
        return self._put(url, params)


    def user_signout(self, username):
        """Log out a user from Discourse.

        :param username: The user's Discourse username.
        """
        user_id = self.user_id(username)
        url = '/admin/users/{0}/log_out'.format(user_id)
        return self._post(url)


    def user_create(self, email):
        """Create a new Discourse user based on their email address.

        :param email: The user's email address.
        """
        url = '/users'
        random_name = str(uuid.uuid4().get_hex().upper()[0:15])
        random_username = str(uuid.uuid4().get_hex().upper()[0:15])
        params = {'name' : random_name,
                  'username' : random_username,
                  'email' : email,
                  'password' : 'P@ssword',
                  'active' : 'true',
                  }
        return self._post(url, params)


    def badges(self):
        """Return all badges."""
        url = '/admin/badges.json'
        return self._get(url)


    def user_badge_grant(self, username, badge_id):
        """Grant a badge to a user.

        :param username: The user's Discourse username.
        :param badge_id: The ID of the badge to be granted.
        """
        url = '/user_badges'
        params = {'username' : username, 'badge_id' : badge_id}
        return self._post(url, params)


    def search(self, query):
        """Perform a search.

        :param query: The search query.
        """
        url = '/search.json'
        params = {'q' : query, 'order' : 'posts', 'ascending' : 'true'}
        return self._get(url, params)


    def admin_server_status(self):
        """Return the server status."""
        url = '/srv/status'
        return self._get(url)


    def admin_plugins(self):
        """Return installed plugins."""
        url = '/admin/plugins.json'
        return self._get(url)


    def admin_ips_screened(self):
        """Returns screened IP addresses."""
        url="/admin/logs/screened_ip_addresses.json"
        return self._get(url)


    def admin_ips_whitelist_update(self, ip_address):
        """Ensure an IP is on the Discourse whitelist.

        :param ip_address: IP address to be added to the Discourse whitelist.
        """
        url="/admin/logs/screened_ip_addresses.json"
        params = {'ip_address': ip_address, 'action_name': 'do_nothing'}
        return self._post(url, params)


    def admin_setting_update(self, setting, new_value):
        """Update a site setting.

        :param setting: The Discourse setting to be updated.
        :param new_value: The value to be set.
        """
        url = "/admin/site_settings/{0}".format(setting)
        params = {setting: new_value}
        return self._put(url, params)