from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from model.project_model.project_type_enum import ProjectTypeEnum


class ProjectCreate(BaseModel):
    name: str = Field(...)
    project_type: Optional[ProjectTypeEnum] = Field(...)
    description: str = Field(...)
    user_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "project_model": {
                "name": "Cat vs Dog Classifier",
                "project_type": "classification",
                "user_id": "-1"
            }
        }