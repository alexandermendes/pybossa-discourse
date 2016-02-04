# -*- coding: utf8 -*-
"""Blueprint module for pybossa-discourse."""

from flask import Blueprint
from .view import index, oauth_authorized, signout


class DiscourseBlueprint(Blueprint):
    """Blueprint to support SSO.

    :param ``**kwargs``: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        defaults = {'name': 'discourse', 'import_name': __name__}
        defaults.update(kwargs)

        super(DiscourseBlueprint, self).__init__(**defaults)

        self.add_url_rule('/index', view_func=index)
        self.add_url_rule('/oauth-authorized', view_func=oauth_authorized)
        self.add_url_rule('/signout', view_func=signout)
