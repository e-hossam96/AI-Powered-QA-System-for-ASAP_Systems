from typing import Any
from openai import AsyncOpenAI
from .BaseModel import BaseModel


class OpenAILLMModel(BaseModel):
    def __init__(
        self,
        db_client: Any | None = None,
        vectordb_client: Any | None = None,
        embedding_client: AsyncOpenAI | None = None,
        generation_client: AsyncOpenAI | None = None,
    ) -> None:
        super().__init__(
            db_client, vectordb_client, embedding_client, generation_client
        )
