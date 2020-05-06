import abc
import json
from functools import partial
from jsonschema import validate
import jsonpath_rw
from hamcrest import assert_that


class Condition(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def match(self, response):
        return


class StatusCodeCondition(Condition):

    def __init__(self, code):
        super(StatusCodeCondition, self).__init__()
        self._status_code = code

    def match(self, response):
        assert response.status_code == self._status_code

    def __repr__(self):
        return f"status code is {self._status_code}"


status_code = StatusCodeCondition


class BodyFieldJsonPathCondition(Condition):

    def __init__(self, json_path, matcher):
        super(BodyFieldJsonPathCondition, self).__init__()
        self._json_path = json_path
        self._matcher = matcher

    def match(self, response):
        json_response = response.json()
        if isinstance(json_response, str):
            json_response = json.loads(json_response)

        value = jsonpath_rw.parse(self._json_path).find(json_response)
        assert_that(value, self._matcher)

    def __repr__(self):
        return f"body field {self._json_path} {self._matcher}"


body = BodyFieldJsonPathCondition


class ContentTypeCondition(Condition):

    def __init__(self, content_type):
        super(ContentTypeCondition, self).__init__()
        self._content_type = content_type

    def __repr__(self):
        return f"'{self._content_type}' content type"

    def match(self, response):
        assert self._content_type in response.headers['Content-Type']


content_type = ContentTypeCondition


class BodyFieldConditions(Condition):

    def __init__(self, callback, fields):
        super(BodyFieldConditions, self).__init__()
        self.callback = callback
        self.fields = fields

    def __repr__(self):
        return f"body fields: {self.fields}"

    def match(self, response):
        return self.callback(response, *self.fields)

    @classmethod
    def from_mapping(cls, callback, *fields):
        callback_mapping = {
            'not_fields': cls.response_does_not_have_fields,
            'fields': cls.response_has_fields,
            'only_fields': cls.response_has_only_fields,
            'field_with_value': cls.response_has_field_with_value,
            'field_contains_value': cls.response_has_field_contains_value
        }
        return cls(callback=callback_mapping[callback], fields=fields)

    @staticmethod
    def response_does_not_have_fields(response, *fields):
        json = response.json()
        unexpected_fields = [field for field in fields if json.get(field)]
        assert not unexpected_fields, f'Response contains unexpected fields: {unexpected_fields}'

    @staticmethod
    def response_has_fields(response, *fields):
        json = response.json()
        missing_fields = [field for field in fields if json.get(field) is None]
        assert not missing_fields, f'Response does not have expected fields: {missing_fields}'

    @staticmethod
    def response_has_only_fields(response, *fields):
        json = response.json()
        missing_fields = [field for field in fields if json.get(field) is None]
        assert not missing_fields, f'Response does not have expected fields: {missing_fields}'
        unexpected_fields = [key for key in json.keys() if key not in fields]
        assert not unexpected_fields, f'Response has unexpected fields: {unexpected_fields}'

    @staticmethod
    def response_has_field_with_value(response, field, value):
        actual_field_value = response.json().get(field)
        assert actual_field_value, f'Response does not have expected {field} field'
        assert value == actual_field_value, f"""
            Expected '{field}' field value don't equal to:
            {value}
            Actual '{field}' field value:
            {actual_field_value}
        """

    @staticmethod
    def response_has_field_contains_value(response, field, value):
        actual_field_value = response.json().get(field)
        assert actual_field_value, f'Response does not have expected {field} field'
        assert value in actual_field_value, f"""
            Expected '{field}' field value doesn't contain:
            {value}
            Actual '{field}' field value:
            {actual_field_value}
        """


fields = partial(BodyFieldConditions.from_mapping, 'fields')
not_fields = partial(BodyFieldConditions.from_mapping, 'not_fields')
only_fields = partial(BodyFieldConditions.from_mapping, 'only_fields')
field_with_value = partial(BodyFieldConditions.from_mapping, 'field_with_value')
field_contains_value = partial(BodyFieldConditions.from_mapping, 'field_contains_value')


class JsonSchemaCondition(Condition):

    def __init__(self, schema):
        super(JsonSchemaCondition, self).__init__()
        self._schema = schema

    def __repr__(self):
        return f"json schema validation: {self._schema}"

    def match(self, response):
        json = response.json()
        validate(instance=json, schema=self._schema)

validation_with_json_schema = JsonSchemaCondition

