# -*- coding: utf8 -*-
"""Extensions module for pybossa-discourse."""

from pybossa_discourse.client import DiscourseClient
from pybossa_discourse.sso import DiscourseSSO

__all__ = ['discourse_client', 'discourse_sso']

discourse_client = DiscourseClient()
discourse_sso = DiscourseSSO()
