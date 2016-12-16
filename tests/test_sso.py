# -*- coding: utf8 -*-

import base64
import hmac
import hashlib
import urllib
from default import with_context, Test
from pybossa_discourse.sso import DiscourseSSO
from nose.tools import assert_raises
from mock import patch, MagicMock

mock_user = MagicMock()
mock_user.email_addr.return_value = 'j@b.com'
mock_user.fullname.return_value = 'joebloggs'
mock_user.name.return_value = 'jb'
mock_user.info.return_value = None


class TestSSO(Test):

    def setUp(self):
        super(TestSSO, self).setUp()
        self.discourse_sso = DiscourseSSO(self.flask_app)
        self.nonce = "cb68251eefb5211e58c00ff1395f0c0b"
        self.payload = 'bm9uY2U9Y2I2ODI1MWVlZmI1MjExZTU4YzAwZmYxMzk1ZjBjMGI' \
                       '%3D%0A'
        self.sig = '2828aa29899722b35a2f191d34ef9b3ce695e0e6eeec47deb46d588' \
                   'd70c7cb56'

    def test_validation_fails_when_no_nonce_in_payload(self):
        pl = base64.encodestring('something')
        assert_raises(ValueError, self.discourse_sso._validate_payload, pl,
                      self.sig)

    def test_validation_fails_when_payload_does_not_match_sig(self):
        pl = base64.encodestring('nonce=1234')
        assert_raises(ValueError, self.discourse_sso._validate_payload, pl,
                      self.sig)

    def test_nonce_returned_when_parameters_valid(self):
        nonce = self.discourse_sso._validate_payload(self.payload, self.sig)
        assert nonce == self.nonce

    @patch('pybossa_discourse.sso.request')
    @patch('pybossa_discourse.sso.url_for', return_value='')
    @patch('pybossa_discourse.sso.current_user', return_value=mock_user)
    def test_expected_credentials_returned(self, mock_user, mock_url,
                                           mock_request):
        mock_user.info.return_value = False
        with patch.dict(mock_user.info, {'container': '1', 'avatar': '1.jpg'}):
            mock_root = MagicMock()
            mock_root.rstrip.return_value = ''
            mock_request = MagicMock()
            mock_request.url_root = mock_root

        expected = {'nonce': self.nonce,
                    'email': mock_user.email_addr,
                    'name': mock_user.fullname,
                    'username': mock_user.name,
                    'external_id': mock_user.id,
                    'sso_secret': self.discourse_sso.secret,
                    'avatar_force_update': 'true'}
        actual = self.discourse_sso._get_credentials(self.nonce)
        assert set(expected).issubset(set(actual))

    @patch('pybossa_discourse.sso.request')
    @patch('pybossa_discourse.sso.url_for', return_value='')
    @patch('pybossa_discourse.sso.current_user', return_value=mock_user)
    def test_url_built_with_valid_parameters(self, mock_request, mock_url,
                                             mock_user):
        url = self.discourse_sso.get_sso_login_url(self.payload, self.sig)
        assert 'sso' in url and 'sig' in url

    @patch('pybossa_discourse.sso.current_user', return_value=mock_user)
    def test_base_url_returned_to_anonymous_users(self, mock_user):
        mock_user.is_anonymous.return_value = True
        expected = self.discourse_sso.url
        actual = self.discourse_sso.get_sso_url()
        assert expected == actual

    @patch('pybossa_discourse.sso.current_user', return_value=mock_user)
    def test_sso_url_returned_to_authenticated_users(self, mock_user):
        mock_user.is_anonymous.return_value = False
        expected = '{0}/session/sso?return_path=%2F'.format(self.discourse_sso.url)
        actual = self.discourse_sso.get_sso_url()
        assert expected == actual
