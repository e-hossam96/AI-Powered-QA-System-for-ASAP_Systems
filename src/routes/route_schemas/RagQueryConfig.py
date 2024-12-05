from typing import Any
from pydantic import BaseModel


class RagQueryConfig(BaseModel):
    text: str
    limit: int | None = 4
    chat_history: list[dict[str, Any]] | None = None
