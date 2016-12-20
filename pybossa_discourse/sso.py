# -*- coding: utf8 -*-
"""SSO module for pybossa-discourse."""

from flask.ext.login import current_user
from flask import request, url_for
import urllib
import base64
import hmac
import hashlib


class DiscourseSSO(object):
    """A class for handling Discourse SSO.

    :param app: The PyBossa application.
    """

    def __init__(self, app=None):
        if app is not None:  # pragma: no cover
            self.init_app(app)

    def init_app(self, app):
        """Configure"""
        self.secret = app.config['DISCOURSE_SECRET']
        self.url = app.config['DISCOURSE_URL']

    def _validate_payload(self, payload, sig):
        """Validate an SSO payload."""
        payload = urllib.unquote(payload)
        decoded = base64.decodestring(payload)

        if not payload or not sig or 'nonce' not in decoded:
            raise ValueError('Invalid parameters')

        h = hmac.new(self.secret, payload, digestmod=hashlib.sha256)
        this_sig = h.hexdigest()

        if this_sig != sig:
            raise ValueError('Payload does not match signature')

        nonce = decoded.split('=')[1].split('&')[0]
        return nonce

    def _build_return_query(self, credentials):
        """Construct the return query string."""
        return_payload = base64.encodestring(urllib.urlencode(credentials))
        h = hmac.new(self.secret, return_payload, digestmod=hashlib.sha256)
        query_string = urllib.urlencode({'sso': return_payload,
                                         'sig': h.hexdigest()})
        return query_string

    def _get_avatar_url(self):
        """Return the avatar URL for the current user."""
        container = current_user.info.get('container', None)
        avatar = current_user.info.get('avatar', None)
        if not container or not avatar:
            return None
        root = request.url_root.rstrip('/')
        filename = '{0}/{1}'.format(container, avatar)
        file_url = url_for('uploads.uploaded_file', filename=filename)
        avatar_url = '{0}{1}'.format(root, file_url)
        return avatar_url

    def _get_credentials(self, nonce):
        """Return credentials for the current user."""
        credentials = {'nonce': nonce,
                       'email': current_user.email_addr,
                       'name': current_user.fullname,
                       'username': current_user.name,
                       'external_id': current_user.id,
                       'sso_secret': self.secret
                       }
        avatar_url = self._get_avatar_url()
        if avatar_url:
            credentials.update({'avatar_url': avatar_url,
                                'avatar_force_update': 'true'})
        return credentials

    def get_sso_login_url(self, payload, sig):
        """Validate payload and return SSO url.

        :param payload: The inbound payload.
        :param sig: The signature.
        """
        nonce = self._validate_payload(payload, sig)
        credentials = self._get_credentials(nonce)
        payload = self._build_return_query(credentials)
        url = '{0}/session/sso_login?{1}'.format(self.url, payload)
        return url

    def get_sso_url(self):
        """Return SSO URL, or the Discourse base URL if anonymous user."""
        if current_user.is_anonymous():
            return self.url
        return '{0}/session/sso?return_path=%2F'.format(self.url)
