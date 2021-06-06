from enum import Enum


class ContentTypeEnum(str, Enum):
    csv = "text/csv"
    tsv = "text/tsv"
