from typing import Any
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseModel:
    def __init__(
        self,
        db_client: AsyncIOMotorDatabase | None = None,
        vectordb_client: AsyncQdrantClient | None = None,
        embedding_client: AsyncOpenAI | None = None,
        generation_client: AsyncOpenAI | None = None,
    ) -> None:
        self.db_client = db_client
        self.vectordb_client = vectordb_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client
