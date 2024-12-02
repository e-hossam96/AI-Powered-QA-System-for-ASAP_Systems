from typing import Any
from qdrant_client import QdrantClient
from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseModel:
    def __init__(
        self,
        db_client: AsyncIOMotorDatabase | None = None,
        vectordb_client: QdrantClient | Any | None = None,
    ) -> None:
        self.db_client = db_client
        self.vectordb_client = vectordb_client
