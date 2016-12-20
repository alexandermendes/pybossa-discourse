# -*- coding: utf8 -*-
"""
pybossa-discourse
-----------------

A PyBossa plugin for Discourse integration.
"""

import os
import json
from flask import current_app as app
from flask.ext.plugins import Plugin
from .extensions import discourse_client, discourse_sso
from .globals import DiscourseGlobals

__plugin__ = "PyBossaDiscourse"
__version__ = json.load(open(os.path.join(os.path.dirname(__file__),
                                          'info.json')))['version']

DISCOURSE_SETTINGS = ('DISCOURSE_API_KEY',
                      'DISCOURSE_API_USERNAME',
                      'DISCOURSE_SECRET',
                      'DISCOURSE_URL')


class PyBossaDiscourse(Plugin):
    """PyBossa Discourse plugin class."""

    def setup(self):
        """Setup the plugin."""
        for setting in DISCOURSE_SETTINGS:
            try:
                app.config[setting]
            except KeyError as inst:  # pragma: no cover
                msg = "PyBossa Discourse disabled"
                print type(inst)
                print inst.args
                print inst
                print msg
                log_message = '{0}: {1}'.format(msg, str(inst))
                app.logger.info(log_message)
                self.disable()
                return

        discourse_client.init_app(app)
        discourse_sso.init_app(app)
        DiscourseGlobals(app)
        self.setup_blueprint()

    def setup_blueprint(self):
        """Setup blueprint."""
        from .view import blueprint
        app.register_blueprint(blueprint, url_prefix="/discourse")
