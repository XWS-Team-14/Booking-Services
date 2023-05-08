from pydantic import BaseModel
from fastapi import UploadFile

class ImagePost(BaseModel):
    image_uri: str
    data: UploadFile


class ImageURI(BaseModel):
    image_uri: str
