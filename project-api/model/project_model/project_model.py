from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from model.project_model.project_status_enum import ProjectStatusEnum
from model.project_model.project_type_enum import ProjectTypeEnum
from model.py_object_id import PyObjectId


class Project(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    version: int = Field(...)
    description: str = Field(...)
    status: Optional[ProjectStatusEnum] = Field(...)
    project_type: Optional[ProjectTypeEnum] = Field(...)
    parent_project: Optional[PyObjectId] = Field(...)
    user_id: str = Field(...)
    created_date: datetime = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "project_model": {
                "name": "Cat vs Dog Classifier",
                "version": 1,
                "user_id": "-1"
            }
        }

    def get_project_bucket(self):
        return "{project}-v{version}-{project_id}-data".format(
            project=self.name,
            project_id=self.id,
            version=self.version
        ).lower()