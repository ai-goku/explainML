import json
from abc import ABCMeta
from datetime import datetime
from uuid import uuid4
from bson import json_util
import json


class Event(metaclass=ABCMeta):

    def __init__(self, name, body):
        self._id = str(uuid4())
        self._name = name
        self._body = body
        self._created_at = datetime.now()

    @property
    def name(self):
        return self._name

    @property
    def body(self):
        return self._body

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    def serialize(self):
        data = dict(
            id=self._id,
            body=self._body,
            name=self._name,
            created_at=self._created_at
        )
        return json.dumps(data, default=json_util.default)
