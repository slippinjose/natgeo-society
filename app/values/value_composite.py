import os
import json
from flask import make_response, jsonify
from scribe.utils.services.security.encode_payload_service import EncodePayloadService


class ValueComposite(object):
    _raw_value = None

    def initialize(self, raw_value):
        self._raw_value = raw_value

    # Serializer methods for dict based value objects (initialized with {})
    def serialize_with(self, **entry):
        self._raw_value.update(entry)

    def serialize_from_value(self, value):
        self._raw_value.update(value.raw)

    def serialize_with_multiple(self, entry):
        self._raw_value.update(entry)

    # Serializer methods for array based value objects (initialized with [])
    def serialize_and_append(self, entry):
        self._raw_value.append(entry)

    def serialize_and_append_from_value(self, value):
        self._raw_value.append(value.raw)

    def serialize_and_append_from_values(self, values):
        self._raw_value += map(lambda value: value.raw, values)

    def serialize_with_nullable_value(self, key, value):
        if value:
            self.serialize_with_multiple({key: value})

    def to_dict(self):
        return dict(self._raw_value)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_list(self):
        return list(self._raw_value)

    def json_response(self, code=200):
        return make_response(jsonify(self.raw), code)

    def encoded_json(self, code=200):
        encoded_payload = EncodePayloadService(self.raw, os.environ['JWT_SECRET']).call()
        response = make_response(encoded_payload, code)
        response.headers['Content-Type'] = 'application/json'
        return response

    @property
    def raw(self):
        return self._raw_value