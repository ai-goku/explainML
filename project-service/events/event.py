import json
from abc import ABCMeta
from datetime import datetime
from uuid import uuid4


class Event(metaclass=ABCMeta):

    def __init__(self, name, body, id=None, created_at=None):
        self._id = str(uuid4()) if not id else id
        self._name = name
        self._body = body
        self._created_at = datetime.now() if not created_at else created_at

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
        return json.dumps(data)

    def __str__(self):
        return f'Event(' \
               f'id={self._id},' \
               f' name={self._name}' \
               f' body={self._body}'\
               f' created_at={self._created_at}'