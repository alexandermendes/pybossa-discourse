# -*- coding: utf8 -*-

import socket
from flask_discourse.blueprint import DiscourseBlueprint
from flask_discourse.client import DiscourseClient
from flask_discourse.sso import DiscourseSSO


DISCOURSE_SETTINGS = ('DISCOURSE_API_KEY',
                      'DISCOURSE_API_USERNAME',
                      'DISCOURSE_SECRET',
                      'DISCOURSE_DOMAIN')


class Discourse(object):
    """Discourse class to initialise the Flask-Discourse extension.

    Args:
        app : The Flask application.
    """

    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)


    def init_app(self, app):
        """Initialise the extension.

        Args:
            app : The Flask application.
        """
        app.extensions['discourse'] = self

        for setting in DISCOURSE_SETTINGS:
            value = app.config.get(setting)
            if not value:
                raise ValueError('{} setting not found.'.format(setting))

            # Store settings as variables
            name = setting.replace("DISCOURSE_", "", 1).lower()
            setattr(self, name, value)

        self.client = DiscourseClient(app)
        self.sso = DiscourseSSO(app)

        self.local_ip = self.get_ip()
        self.register_blueprint(app)
        self.configure_discourse()


    def register_blueprint(self, app, *args, **kwargs):
        """Register the Discourse blueprint.

        Args:
            app : The Flask application.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        blueprint = DiscourseBlueprint()
        app.register_blueprint(blueprint, *args, **kwargs)


    def get_ip(self):
        """Return the IP address of the Flask application.

        Returns:
            The IP address where the Flask application is hosted.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip


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
