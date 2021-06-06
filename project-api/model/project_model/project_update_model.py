from typing import Optional

from pydantic import BaseModel, Field


class ProjectUpdate(BaseModel):
    status: Optional[str] = Field(...)
