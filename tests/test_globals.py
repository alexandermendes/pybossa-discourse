# -*- coding: utf8 -*-

from flask import redirect, url_for
from helper import web
from default import with_context, flask_app
from mock import patch
from pybossa_discourse.globals import DiscourseGlobals


class TestGlobals(web.Helper):

    def setUp(self):
        super(TestGlobals, self).setUp()
        self.url = self.flask_app.config['DISCOURSE_URL']

    @with_context
    def test_embedded_comments(self):
        with self.flask_app.test_request_context('/'):
            d = DiscourseGlobals(self.flask_app)
            print d.comments()
            assert 1 == 2
