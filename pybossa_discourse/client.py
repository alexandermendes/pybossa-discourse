# -*- coding: utf8 -*-
"""Client module for consuming with the Discourse API."""

import socket
import uuid
import requests
from flask_discourse.exceptions import DiscourseError


class DiscourseClient(object):
    """Discourse client class for consuming the Discourse API."""


    def __init__(self, app=None):
        """Initialise."""
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

        Parameters
        ----------
        category_id : int
            The ID of the category.
        """
        url = '/c/{0}.json'.format(category_id)
        return self._get(url)


    def category_topics_latest(self, category_id):
        """Return the latest topics in a category.

        Parameters
        ----------
        category_id : int
            The ID of the category.
        """
        url = '/c/{0}/l/latest.json'.format(category_id)
        return self._get(url)


    def category_topics_new(self, category_id):
        """Return the newest topics in a category.

        Parameters
        ----------
        category_id : int
            The ID of the category.
        """
        url = '/c/{0}/l/new.json'.format(category_id)
        return self._get(url)


    def category_topics_top(self, category_id):
        """Return the top topics in a category.

        Parameters
        ----------
        category_id : int
            The ID of the category.
        """
        url = '/c/{0}/l/top.json'.format(category_id)
        return self._get(url)


    def category_topics_subtopics(self, category_id, parent_category_id):
        """Return the topics in a sub-category.

        Parameters
        ----------
        parent_category_id : int
            The ID of the parent category.
        category_id : int
            The ID of the sub-category.
        """
        url = '/c/{0}/{1}.json'.format(parent_category_id, category_id)
        return self._get(url)

    
    def topic(self, topic_id):
        """Return a specific topic.

        Parameters
        ----------
        topic_id : int
            The ID of the topic.
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


    def user_details(self, user):
        """Return a user's details.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        url = '/users/{0}.json'.format(user)
        return self._get(url)


    def user_username(self, email):
        """Return a user's Discourse username, creating the user if necessary.

        Parameters
        ----------
        email : str
            The user's Discourse email address.
        """
        url = '/admin/users/list/all.json'
        params = {'filter' : user.email}
        res = self._get(url, params)

        if len(res) == 0:
            self.create_user(user)

        res = self._get(url, params)
        return res[0]['username']


    def user_id(self, user):
        """Return a user's Discourse ID.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        details = self.user_details(user)
        user_id = details['user']['id']
        return user_id


    def user_title(self, user):
        """Return a user's title.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        details = self.user_details(user)
        title = details['user']['title']
        return title


    def update_user_trust_level(self, user, level):
        """Update a user's trust level.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        level : int
            The trust level to be set for the user.
        """
        user_id = self.user_id(user)
        url = '/admin/users/{0}/trust_level'.format(user_id)
        params = {'user_id' : user_id, 'level' : level}
        return self._put(url, params)


    def user_activity(self, user):
        """Return the user's recent activity.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        url = '/user_actions.json'
        params = {'username' : user}
        return self._get(url, params)


    def user_messages(self, user):
        """Return a user's private messages.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        url = '/topics/private-messages/{0}.json'.format(user)
        return self._get(url)


    def user_notifications(self, user):
        """Return notifications for a user.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        url = '/notifications.json'
        params = {'username' : user}
        return self._get(url, params)


    def user_notifications_count(self, user):
        """Return a count of unread notifications for a user.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        notifications = self.notifications(user)
        count = sum([1 for n in notifications['notifications']
                     if not n['read']])
        return count


    def user_notifications_markread(self, user):
        """Mark a user's notifications as read.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        url = '/notifications/mark-read.json'
        params = {'username' : user}
        return self._put(url, params)


    def user_signout(self, user):
        """Log out a user from Discourse.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        """
        user_id = self.user_id(user)
        url = '/admin/users/{0}/log_out'.format(user_id)
        return self._post(url)


    def user_create(self, email):
        """Create a new Discourse user based on their email address.

        Parameters
        ----------
        email : str
            The user's email address.
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


    def user_badge_grant(self, user, badge_id):
        """Grant a badge to a user.

        Parameters
        ----------
        user : str
            The user's Discourse username.
        badge_id : int
            The ID of the badge to be granted.
        """
        url = '/user_badges'
        params = {'username' : user, 'badge_id' : badge_id}
        return self._post(url, params)


    def search(self, query):
        """Search for a given query.

        Parameters
        ----------
        query : str
            The query to search for.
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

        Parameters
        ----------
        ip_address : str
            The IP address to be added to the Discourse whitelist.
        """
        url="/admin/logs/screened_ip_addresses.json"
        params = {'ip_address': ip_address, 'action_name': 'do_nothing'}
        return self._post(url, params)


    def admin_setting_update(self, setting, new_value):
        """Update a site setting.

        Parameters
        ----------
        setting : str
            The Discourse setting to be updated.
        new_value : str
            The value to be set.
        """
        url = "/admin/site_settings/{0}".format(setting)
        params = {setting: new_value}
        return self._put(url, params)