# -*- coding: utf8 -*-

import json
from flask import Response


STATUS = {"BadRequest": 400,
          "Unauthorized": 401,
          "Forbidden": 403,
          "NotFound": 404,
          "MethodNotAllowed": 405,
          "TypeError": 415,
          "ValueError": 415,
          "DataError": 415,
          "AttributeError": 415,
          "DBIntegrityError": 415,
          "TooManyRequests": 429,
          }


class DiscourseError(Exception):
    """Exception class for handling Discourse errors."""


    def __init__(self, e):
        super(DiscourseError, self).__init__(e)

        self.exception_cls = e.__class__.__name__

        if STATUS.get(self.exception_cls):
            self.status = STATUS[self.exception_cls]
        else:
            self.status = 500

        self.message = str(e.message)


    def to_json_response(self):
        """Return the exception as a JSON formatted response."""
        error = {'status': "failed",
                 'status_code': self.status,
                 'exception_cls': self.exception_cls,
                 'exception_msg': self.message
                 }

        return Response(json.dumps(error), status=self.status,
                        mimetype='application/json')