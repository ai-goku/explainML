from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: str = Field(alias="_id")
    name: str = Field(...)
    version: int = Field(...)
    description: str = Field(...)
    status: str = Field(...)
    project_type: str = Field(...)
    parent_project: Optional[str] = None
    user_id: str = Field(...)
    created_date: datetime = Field(...)

    def get_project_bucket(self):
        return "{project}-v{version}-{project_id}-data".format(
            project=self.name,
            project_id=self.id,
            version=self.version
        ).lower()