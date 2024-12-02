from pydantic import BaseModel


class VectorIndexConfig(BaseModel):
    do_reset: bool | None = False
