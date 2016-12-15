# -*- coding: utf8 -*-

import inspect
from default import Test


class TestSetup(Test):

    def test_global_envar_registered(self):
        envars = self.flask_app.jinja_env.globals
        client = self.flask_app.extensions['discourse']['client']
        assert envars['discourse'] == client
