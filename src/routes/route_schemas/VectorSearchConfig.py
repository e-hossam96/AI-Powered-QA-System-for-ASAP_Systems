from pydantic import BaseModel


class VectorSearchConfig(BaseModel):
    text: str
    limit: int | None = 4
