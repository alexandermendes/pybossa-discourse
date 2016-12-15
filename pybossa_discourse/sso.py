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

    def _build_return_payload(self, nonce):
        """Construct the return url."""
        credentials = self._get_credentials(nonce)
        return_payload = base64.encodestring(urllib.urlencode(credentials))
        h = hmac.new(self.secret, return_payload, digestmod=hashlib.sha256)
        query_string = urllib.urlencode({'sso': return_payload,
                                         'sig': h.hexdigest()})
        return query_string

    def _get_credentials(self, nonce):
        """Return credentials for the current user."""
        credentials = {'nonce': nonce,
                       'email': current_user.email_addr,
                       'name': current_user.fullname,
                       'username': current_user.name,
                       'external_id': current_user.id,
                       'sso_secret': self.secret
                       }

        # Add the avatar URL
        info = current_user.info
        if info.get('container') and info.get('avatar'):
            root = request.url_root.rstrip('/')
            filename = '{0}/{1}'.format(info['container'], info['avatar'])
            file_url = url_for('uploads.uploaded_file', filename=filename)
            avatar_details = {'avatar_url': '{0}{1}'.format(root, file_url),
                              'avatar_force_update': 'true'
                              }
            credentials.update(avatar_details)
        return credentials

    def validate(self, payload, sig):
        """Validate payload and return SSO url.

        :param payload: The inbound payload.
        :param sig: The signature.
        """
        nonce = self._validate_payload(payload, sig)
        payload = self._build_return_payload(nonce)
        url = '{0}/session/sso_login?{1}'.format(self.url, payload)
        return url

    def get_sso_url(self):
        """Return Discourse SSO URL, if the current user is not anonymous.

        :returns: Discourse SSO URL, or Discourse base URL if the current user
        is anonymous.
        """
        if current_user.is_anonymous():
            return self.url
        return '{0}/session/sso?return_path=%2F'.format(self.url)
