# -*- coding: utf8 -*-
"""Views module for pybossa-discourse."""

from flask import Blueprint, request, url_for, flash, redirect
from flask import current_app as app
from flask.ext.login import logout_user, current_user

discourse_sso = app.extensions['discourse']['sso']
discourse_client = app.extensions['discourse']['client']


def index():
    """Attempt to sign in via SSO then redirect to Discourse."""
    discourse_sso = app.extensions['discourse']['sso']
    try:
        url = discourse_sso.signin()
    except AttributeError as e:
        flash('Access Denied: {}'.format(str(e)), 'error')
        return redirect(url_for('home.home'))

    return redirect(url)


def oauth_authorized():
    """Authorise a Discourse login."""
    discourse_sso = app.extensions['discourse']['sso']
    sso = request.args.get('sso')
    sig = request.args.get('sig')

    if current_user.is_anonymous():
        next_url = url_for('discourse.oauth_authorized', sso=sso, sig=sig)
        return redirect(url_for('account.signin', next=next_url))

    try:
        url = discourse_sso.validate(sso, sig)
    except (ValueError, AttributeError) as e:
        flash('Access Denied: {0}'.format(str(e)), 'error')
        return redirect(url_for('home.home'))

    return redirect(url)


def signout():
    """Signout the current user from both PyBossa and Discourse."""
    discourse_client = app.extensions['discourse']['client']
    if not current_user.is_anonymous():
        try:
            discourse_client.log_out(current_user)
        except (ValueError, AttributeError) as e:
            msg = 'Discourse Logout Failed: {0}'.format(str(e))
            flash(msg, 'error')
        logout_user()
        flash('You are now signed out', 'success')

    return redirect(url_for('home.home'))
