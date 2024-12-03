from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class Vector(BaseModel):
    vector: list[float] | None = Field(default=None, min_length=1)
    text: str = Field(..., min_length=1)
    source_name: str | None = Field(default=None, min_length=1)  # asset name
    source_id: str | None = Field(default=None)  # asset id in document db
    score: float | None = Field(default=None, gt=0.0)

    class Config:
        arbitrary_types_allowed = True
