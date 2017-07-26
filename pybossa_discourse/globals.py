# -*- coding: utf8 -*-
"""Jinja globals module for pybossa-discourse."""

from flask import Markup, request, abort, url_for
from pybossa.core import project_repo
from . import discourse_client


class DiscourseGlobals(object):
    """A class to implement Discourse Global variables."""

    def __init__(self, app):
        self.url = app.config['DISCOURSE_URL']
        self.api = discourse_client
        app.jinja_env.globals.update(discourse=self)

    def _comment_feed_markup(self, embed_url):
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
        """).format(self.url, embed_url)

    def category_comments(self, category_id):
        """Embed Discourse comments for a particular category."""
        category = project_repo.get_category(category_id)
        if not category:
            abort(404)
        embed_url = url_for('project.project_cat_index',
                            category=category.short_name, _external=True)
        return self._comment_feed_markup(embed_url)

    def comments(self, embedUrl=None):
        """Return an HTML snippet used to embed Discourse comments."""
        if not embedUrl:
            embedUrl = request.base_url
        return self._comment_feed_markup(embedUrl)

    def notifications(self):
        """Return a count of unread notifications for the current user."""
        notifications = discourse_client.user_notifications()
        if not notifications:
            return 0
        return sum([1 for n in notifications if not n['read']])
