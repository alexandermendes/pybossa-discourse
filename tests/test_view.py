# -*- coding: utf8 -*-

import json
import pybossa_discourse
from helper import web
from default import with_context, Test
from mock import patch, MagicMock
from pybossa_discourse import view
from flask import Response


class TestView(web.Helper):


    def setUp(self):
        super(TestView, self).setUp()
        self.domain = self.flask_app.config['DISCOURSE_DOMAIN']


    @with_context
    @patch('pybossa_discourse.view.redirect')
    @patch.object(pybossa_discourse.sso.DiscourseSSO, 'signin')
    def test_index_to_sso_sign_in(self, mock_signin, mock_redirect):
        mock_redirect.return_value = Response(302)
        res = self.app.get('/discourse/index')

        assert mock_signin.called
