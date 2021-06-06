from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from model.data_model.extension_enum import ContentTypeEnum
from model.py_object_id import PyObjectId


class Data(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    file_name: str = Field(...)
    project_id: PyObjectId = Field(...)
    version: int = Field(...)
    content_type: ContentTypeEnum = Field(...)
    created_at: datetime = Field(...)
    url: Optional[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}