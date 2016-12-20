# -*- coding: utf8 -*-
"""Extensions module for pybossa-discourse."""

from .client import DiscourseClient
from .sso import DiscourseSSO

__all__ = ['discourse_client', 'discourse_sso']

discourse_client = DiscourseClient()
discourse_sso = DiscourseSSO()
