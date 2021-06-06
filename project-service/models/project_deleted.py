from pydantic import BaseModel, Field


class ProjectDeleted(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    name: str
    version: int

    def get_project_bucket(self):
        return "{project}-v{version}-{project_id}-data".format(
            project=self.name,
            project_id=self.id,
            version=self.version
        ).lower()
