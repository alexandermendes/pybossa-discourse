# -*- coding: utf8 -*-
"""Jinja globals module for pybossa-discourse."""

from flask import Markup, request
from . import discourse_client


class DiscourseGlobals(object):
    """A class to implement Discourse Global variables."""

    def __init__(self, app):
        self.url = app.config['DISCOURSE_URL']
        app.jinja_env.globals.update(discourse=self)

    def comments(self):
        """Return an HTML snippet used to embed Discourse comments."""
        return Markup("""
            <div id="discourse-comments"></div>
            <script type="text/javascript">
                DiscourseEmbed = {{
                    discourseUrl: '{0}/',
                    discourseEmbedUrl: '{1}'
                }};

                window.onload = function() {{
                    let d = document.createElement('script'),
                        head = document.getElementsByTagName('head')[0],
                        body = document.getElementsByTagName('body')[0];
                    d.type = 'text/javascript';
                    d.async = true;
                    d.src = '{0}/javascripts/embed.js';
                    (head || body).appendChild(d);
                }}
            </script>
        """).format(self.url, request.base_url)

    def notifications(self):
        """Return a count of unread notifications for the current user."""
        notifications = discourse_client.user_notifications()
        if not notifications:
            return 0
        return sum([1 for n in notifications['notifications']
                    if not n['read']])
