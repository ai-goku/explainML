from enum import Enum


class ProjectStatusEnum(str, Enum):
    created = "created"
    uploaded = "uploaded"
    profiled = "profiled"
    trained = "trained"
