# -*- coding: utf8 -*-
"""Views module for pybossa-discourse."""

from flask import Blueprint, request, url_for, flash, redirect, abort
from flask.ext.login import current_user
from . import discourse_sso, discourse_client


blueprint = Blueprint('discourse', __name__)


@blueprint.route('/index')
def index():
    """Initiate SSO signin, if the current user is not anonymous."""
    url = discourse_sso.get_sso_url()
    return redirect(url)


@blueprint.route('/oauth-authorized')
def oauth_authorized():
    """Authorise a Discourse login."""
    sso = request.args.get('sso')
    sig = request.args.get('sig')

    if current_user.is_anonymous():
        next_url = url_for('discourse.oauth_authorized', sso=sso, sig=sig)
        return redirect(url_for('account.signin', next=next_url))

    try:
        url = discourse_sso.get_sso_login_url(sso, sig)
    except (ValueError, AttributeError) as e:  # pragma: no cover
        flash('Access Denied: {0}'.format(str(e)), 'error')
        return redirect(url_for('home.home'))
    return redirect(url)


@blueprint.route('/signout')
def signout():
    """Signout the current user from both PyBossa and Discourse."""
    if not current_user.is_anonymous():
        try:
            discourse_client.user_signout()
        except (ValueError, AttributeError) as e:  # pragma: no cover
            flash('Discourse Logout Failed: {0}'.format(str(e)), 'error')
    return redirect(url_for('account.signout'))
