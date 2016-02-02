# -*- coding: utf8 -*-

import sys
import os
import pybossa_discourse as plugin


# Use the PyBossa test suite
sys.path.append(os.path.abspath("./pybossa/test"))


def setUpPackage():
    """Setup the plugin."""
    from default import flask_app
    with flask_app.app_context():
        settings = os.path.abspath('./settings_test.py')
        flask_app.config.from_pyfile(settings)
        plugin_dir = os.path.dirname(plugin.__file__)
        plugin.PyBossaDiscourse(plugin_dir).setup()
