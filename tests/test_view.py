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
        self.app.get('/discourse/index')
        mock_redirect.assert_called_with(self.url)

    @with_context
    @patch('pybossa_discourse.view.redirect', wraps=redirect)
    def test_registered_user_redirected_to_sso_signin(self, mock_redirect):
        self.register()
        self.signin()
        url = '{0}/session/sso?return_path=%2F'.format(self.url)
        self.app.get('/discourse/index')
        mock_redirect.assert_called_with(url)

    @with_context
    @patch('pybossa_discourse.view.redirect', wraps=redirect)
    def test_oauth_callback_redirects_anon_user_to_signin(self, mock_redirect):
        data = {'sso': 'sso', 'sig': 'sig'}
        signin_url = '/account/signin?next=%2Fdiscourse%2Foauth-authorized'
        self.app.get('/discourse/oauth-authorized', data=data)
        mock_redirect.assert_called_with(signin_url)

    @with_context
    @patch('pybossa_discourse.view.redirect', wraps=redirect)
    @patch('pybossa_discourse.view.discourse_sso')
    def test_oauth_callback_for_registered_user(self, mock_sso, mock_redirect):
        mock_sso.get_sso_login_url.return_value = "example.com"
        self.register()
        self.signin()
        data = {'sso': 'sso', 'sig': 'sig'}
        self.app.get('/discourse/oauth-authorized', data=data)
        mock_redirect.assert_called_with("example.com")

    @with_context
    @patch('pybossa_discourse.view.redirect', wraps=redirect)
    @patch('pybossa_discourse.view.discourse_client')
    def test_user_signed_out_of_discourse_and_pybossa(self, mock_client,
                                                      mock_redirect):
        self.register()
        self.signin()
        self.app.get('/discourse/signout')
        assert mock_client.user_signout.called
        mock_redirect.assert_called_with("/account/signout")
