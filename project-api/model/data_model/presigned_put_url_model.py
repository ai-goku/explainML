from pydantic import BaseModel


class PresignedPutURLResponse(BaseModel):
    url: str
    api: str
