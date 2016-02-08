# -*- coding: utf8 -*-
"""
pybossa-discourse
-----------------

A PyBossa plugin for Discourse integration.
"""

import os
from flask import current_app as app
from flask.ext.plugins import Plugin
from .client import DiscourseClient
from .sso import DiscourseSSO

__plugin__ = "PyBossaDiscourse"
__version__ = "0.1.0"

DISCOURSE_SETTINGS = ('DISCOURSE_API_KEY',
                      'DISCOURSE_API_USERNAME',
                      'DISCOURSE_SECRET',
                      'DISCOURSE_DOMAIN',
                      'DISCOURSE_PYBOSSA_IP',
                      'DISCOURSE_AUTO_UPDATE_SETTINGS')


class PyBossaDiscourse(Plugin):
    """PyBossa Discourse plugin class."""


    def setup(self):
        """Setup the plugin."""

        # Check all settings are provided
        for setting in DISCOURSE_SETTINGS:
            try:
                app.config[setting]
            except KeyError:
                raise ValueError('{} setting not found.'.format(setting))

        # Application specific state
        app.extensions['discourse'] = {'client': None, 'sso': None}

        self.setup_client()
        self.setup_sso()
        self.setup_global_envar()
        self.setup_blueprint()
        if app.config['DISCOURSE_AUTO_UPDATE_SETTINGS']:
            self.setup_discourse()


    def setup_client(self):
        """Setup the Discourse client."""
        app.extensions['discourse']['client'] = DiscourseClient(app)


    def setup_sso(self):
        """Setup Discourse SSO."""
        app.extensions['discourse']['sso'] = DiscourseSSO(app)


    def setup_global_envar(self):
        """Setup global environment variable."""
        client = app.extensions['discourse']['client']
        app.jinja_env.globals.update(discourse=client)



    def setup_blueprint(self):
        """Setup blueprint."""
        from .blueprint import DiscourseBlueprint
        blueprint = DiscourseBlueprint()
        app.register_blueprint(blueprint, url_prefix="/discourse")


    def setup_discourse(self):
        """Setup Discourse site settings."""
        client = app.extensions['discourse']['client']
        pybossa_ip = app.config['DISCOURSE_PYBOSSA_IP']
        secret = app.config['DISCOURSE_SECRET']
        oauth_url = 'http://{0}/discourse/oauth-authorized'.format(pybossa_ip)
        signout_url = 'http://{0}/discourse/signout'.format(pybossa_ip)

        client._whitelist_ip(pybossa_ip)
        client._update_setting('enable_sso', 'true')
        client._update_setting('sso_url', oauth_url)
        client._update_setting('sso_secret', secret)
        client._update_setting('sso_overrides_email', 'true')
        client._update_setting('sso_overrides_username', 'true')
        client._update_setting('sso_overrides_name', 'true')
        client._update_setting('sso_overrides_avatar', 'true')
        client._update_setting('allow_uploaded_avatars', 'false')
        client._update_setting('logout_redirect', signout_url)
