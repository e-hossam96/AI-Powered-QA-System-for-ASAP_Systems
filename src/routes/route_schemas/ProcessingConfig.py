from pydantic import BaseModel


class ProcessingConfig(BaseModel):
    chunk_size: int | None = 4000
    overlap_size: int | None = 100
    batch_size: int | None = 128
    do_reset: bool | None = False
