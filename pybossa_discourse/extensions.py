# -*- coding: utf8 -*-

from .sso import DiscourseSSO
from .client import DiscourseClient

__all__['discourse_sso', 'discourse_client']

discourse_sso = DiscourseSSO()
discourse_client = DiscourseClient()
