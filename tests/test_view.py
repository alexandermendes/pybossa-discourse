# -*- coding: utf8 -*-

from flask import redirect, url_for
from helper import web
from default import with_context
from mock import patch


class TestView(web.Helper):

    def setUp(self):
        super(TestView, self).setUp()
        self.url = self.flask_app.config['DISCOURSE_URL']

    @with_context
    @patch('pybossa_discourse.view.redirect', wraps=redirect)
    def test_anon_user_redirected_to_discourse_homepage(self, mock_redirect):
        mock_redirect.return_value = "OK"
        self.app.get('/discourse/index', follow_redirects=True)
        mock_redirect.assert_called_with(self.url)

    @with_context
    @patch('pybossa_discourse.view.redirect', wraps=redirect)
    def test_registered_user_redirected_to_sso_signin(self, mock_redirect):
        mock_redirect.return_value = "OK"
        self.register()
        self.signin()
        url = '{0}/session/sso?return_path=%2F'.format(self.url)
        self.app.get('/discourse/index', follow_redirects=True)
        mock_redirect.assert_called_with(url)
