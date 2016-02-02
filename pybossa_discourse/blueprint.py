# -*- coding: utf8 -*-
"""Blueprint module for pybossa-discourse."""

import inspect
from flask import Blueprint, current_app


class DiscourseBlueprint(Blueprint):
    """Blueprint to enable Discourse API and SSO support for Flask projects.

    :param ``**kwargs``: Arbitrary keyword arguments.
    """

    def __init__(self, **kwargs):
        defaults = {'name': 'discourse', 'import_name': __name__}
        defaults.update(kwargs)

        super(DiscourseBlueprint, self).__init__(**defaults)

        # Add URLs to the blueprint
        url_map = self._build_url_map()

        for url, view_func in url_map.items():
            self.add_url_rule(url, view_func=view_func)


    def _build_url_map(self):
        """Return a URL map of all non-internal API and SSO methods."""
        discourse = current_app.extensions['discourse']
        url_map = {}

        def add_methods_to_map(inst):
            methods = inspect.getmembers(inst, predicate=inspect.ismethod)
            non_local_methods = [m for m in methods if not m[0].startswith('_')
                                 and not m[0].startswith('init')]

            for m in non_local_methods:

                # Format the URL
                url_parts = m[0].split('_')
                args = inspect.getargspec(m[1])
                args = [a for a in inspect.getargspec(m[1]).args
                        if a is not 'self']

                for arg in args:
                    arg_base = arg.split('_')[0]
                    url_arg = '<{}>'.format(arg)
                    if arg_base in url_parts:
                        url_parts.insert(url_parts.index(arg_base) + 1, url_arg)
                    else:
                        url_parts.append(url_arg)

                url = '/{}'.format('/'.join(url_parts))
                url_map[url] = m[1]

        add_methods_to_map(discourse.client)
        add_methods_to_map(discourse.sso)
        return url_map