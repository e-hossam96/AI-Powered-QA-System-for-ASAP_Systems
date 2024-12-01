from pydantic import BaseModel


class ProcessingConfig(BaseModel):
    asset_name: str | None = None
    chunk_size: int | None = 4000
    overlap_size: int | None = 100
    do_reset: bool | None = False
