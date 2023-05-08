from pydantic import UUID4, BaseModel


class ImagePost(BaseModel):
    image_uri: str
    data: bytes


class ImageDelete(BaseModel):
    image_uri: str
