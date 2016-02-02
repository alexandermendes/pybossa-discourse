# -*- coding: utf8 -*-
"""Main module for pybossa-discourse."""

import socket
from flask_discourse.blueprint import DiscourseBlueprint
from flask_discourse.client import DiscourseClient
from flask_discourse.sso import DiscourseSSO


DISCOURSE_SETTINGS = ('DISCOURSE_API_KEY',
                      'DISCOURSE_API_USERNAME',
                      'DISCOURSE_SECRET',
                      'DISCOURSE_DOMAIN',
                      'DISCOURSE_PYBOSSA_IP',
                      'DISCOURSE_PYBOSSA_DOMAIN')


class Discourse(object):
    """Discourse class to initialise the Flask-Discourse extension.

    :param app: The PyBossa application.
    """

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)


    def init_app(self, app):
        """Initialise the extension.

        :param app: The PyBossa application.
        """

        for setting in DISCOURSE_SETTINGS:
            value = app.config.get(setting)
            if not value:
                raise ValueError('{} setting not found.'.format(setting))

            # Store settings as variables
            name = setting.replace("DISCOURSE_", "", 1).lower()
            setattr(self, name, value)
        
        app.extensions['discourse'] = self

        self.client = DiscourseClient(app)
        self.sso = DiscourseSSO(app)

        self.local_ip = app.config['PYBOSSA_IP']
        self.configure_discourse()


    def configure_discourse(self):
        """Ensure site settings in the Discourse application are correct."""
        self.client.admin_ips_whitelist_update(self.flask_ip)
        self.client.admin_setting_update('enable_sso', 'true')
        oauth_url = '{0}/discourse/oauth-authorized'.format(self.flask_ip)
        self.client.admin_setting_update('sso_url', oauth_url)
        self.client.admin_setting_update('sso_secret', self.secret)
        self.client.admin_setting_update('sso_overrides_email', 'true')
        self.client.admin_setting_update('sso_overrides_username', 'true')
        self.client.admin_setting_update('sso_overrides_name', 'true')
        self.client.admin_setting_update('sso_overrides_avatar', 'true')
        self.client.admin_setting_update('allow_uploaded_avatars', 'false')
        signout_url = '{0}/discourse/signout'.format(self.flask_ip)
        self.client.admin_setting_update('logout_redirect', signout_url)
