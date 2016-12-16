# -*- coding: utf8 -*-
"""Jinja globals module for pybossa-discourse."""

from flask import url_for, redirect


class DiscourseGlobals(object):
    """A class to implement Discourse Global variables."""

    def __init__(self, app):
        self.url = app.config['DISCOURSE_URL']
        app.jinja_env.globals.update(discourse=self)

    def embed_comments():
        """Return an HTML snippet used to embed Discourse comments."""
        return redirect(url_for('discourse.comments', discourse_url=self.url))