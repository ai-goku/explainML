from enum import Enum


class ProjectTypeEnum(str, Enum):
    classification = "classification"
    regression = "regression"
