# -*- coding: utf8 -*-
"""
pybossa-discourse
-----------------

A PyBossa plugin for Discourse integration.
"""

import os
from flask import current_app as app
from flask.ext.plugins import Plugin

__plugin__ = "PyBossaDiscourse"
__version__ = "0.1.0"


class PyBossaDiscourse(Plugin):
    """PyBossa Discourse plugin class."""


    def setup(self):
        """Setup the plugin."""
        self.setup_blueprint()


    def setup_blueprint(self):
        """Setup blueprint."""
        from .blueprint import DiscourseBlueprint
        blueprint = DiscourseBlueprint()
        app.register_blueprint(blueprint, url_prefix="/discourse")
