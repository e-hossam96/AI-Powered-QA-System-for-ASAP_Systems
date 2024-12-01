from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Vector(BaseModel):
    vector: list[float] = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    source_name: str = Field(..., min_length=1)  # asset name
    source_id: ObjectId  # asset id in document db

    class Config:
        arbitrary_types_allowed = True
