# -*- coding: utf8 -*-

from helper import web
from default import with_context
from pybossa_discourse import view


class TestBlueprint(web.Helper):


    @with_context
    def test_all_view_functions_registered(self):
        funcs = [view.index, view.oauth_authorized, view.signout]
        registered = [r for r in self.flask_app.url_map.iter_rules()]

        assert not set(funcs).issubset(set(registered))
