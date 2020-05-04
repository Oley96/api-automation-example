import abc
import json
import jsonpath_rw
from hamcrest import assert_that

class Condition(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def match(self, response):
        return


class StatusCodeCondition(Condition):

    def match(self, response):
        assert response.status_code == self._status_code

    def __init__(self, code):
        super(StatusCodeCondition, self).__init__()
        self._status_code = code

    def __repr__(self):
        return f"status code is {self._status_code}"

status_code = StatusCodeCondition

class BodyFieldCondition(Condition):

    def match(self, response):
        json_response = response.json()
        if isinstance(json_response, str):
            json_response = json.loads(json_response)

        value = jsonpath_rw.parse(self._json_path).find(json_response)
        assert_that(value, self._matcher)

    def __init__(self, json_path, matcher):
        super(BodyFieldCondition, self).__init__()
        self._json_path = json_path
        self._matcher = matcher

    def __repr__(self):
        return f"body field {self._json_path} {self._matcher}"

body = BodyFieldCondition

class ContentTypeCondition(Condition):

    def __init__(self, content_type):
        super(ContentTypeCondition, self).__init__()
        self._content_type = content_type

    def __repr__(self):
        return f"header is {self._content_type}"

    def match(self, response):
        assert self._content_type in response.headers['Content-Type']

content_type = ContentTypeCondition