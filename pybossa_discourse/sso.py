# -*- coding: utf8 -*-
"""SSO module for Flask-Discourse."""

from flask.ext.login import current_user
from flask import request, url_for, flash, abort
from urllib import urlencode
import base64
import hmac
import hashlib


class DiscourseSSO(object):
    """DiscourseSSO class for handling Discourse single sign-on."""


    def __init__(self, app):
        """Configuration."""
        discourse = app.extensions['discourse']
        self.secret = discourse.secret
        self.domain = discourse.domain


    def _validate_payload(self, payload, sig):
        """Validate an SSO payload."""
        decoded = base64.decodestring(payload)

        if not payload or not sig or 'nonce' not in decoded:
            raise ValueError('Invalid parameters')

        h = hmac.new(self.secret, payload, digestmod=hashlib.sha256)
        this_sig = h.hexdigest()

        if this_sig != sig:
            raise ValueError('Payload does not match signature')

        nonce = decoded.split('=')[1].split('&')[0]

        return nonce


    def _build_return_url(self, nonce):
        """Construct the return url."""
        credentials = self._get_credentials(nonce)
        return_payload = base64.encodestring(urlencode(credentials))
        h = hmac.new(self.secret, return_payload, digestmod=hashlib.sha256)
        query_string = urlencode({'sso': return_payload, 'sig': h.hexdigest()})

        return query_string


    def _get_credentials(self):
        credentials = {
            'nonce': nonce,
            'email': current_user.email,
            'name': current_user.fullname,
            'username': current_user.name,
            'external_id': current_user.id,
            'sso_secret': self.secret
            }

        # Add the URL of the avatar, if any
        info = current_user.info
        if (info and 'container' in info and 'avatar' in info):
            root = request.url_root.rstrip('/')
            filename = '{0}/{1}'.format(current_user.info['container'],
                                        current_user.info['avatar'])

            file_url = url_for('uploads.uploaded_file', filename=filename)
            avatar_details = {'avatar_url': '{0}{1}'.format(root, file_url),
                              'avatar_force_update': 'true'
                              }
            credentials.update(avatar_details)
        
        return credentials


    def validate(self, payload, sig):
        """Validate payload and return SSO url.

        Parameters
        ----------
        payload : str
            The inbound payload.
        sig : str
            The signature.

        Returns
        -------
            The SSO login URL.
        """
        nonce = self._validate_payload(payload, sig)
        payload = self._build_return_url(nonce)
        url = '{0}/session/sso_login?{1}'.format(self.domain, payload)

        return url


    def signin(self):
        """Signin to Discourse via SSO, if the current user is not anonymous.

        Returns
        -------
        str
            The Discourse SSO URL if the current user is not anonymous and the
            root Discourse URL otherwise.
        """
        if current_user.is_anonymous():
            return redirect(self.domain)

        url = '{0}/session/sso?return_path=%2F'.format(self.domain)
        return redirect(url)