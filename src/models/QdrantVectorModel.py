import os
from typing import Any
from .BaseModel import BaseModel
from .data_schemas import Vector
from configs import DatabaseConfig
from qdrant_client import AsyncQdrantClient, models


class QdrantVectorModel(BaseModel):
    def __init__(
        self,
        vectordb_client: AsyncQdrantClient,
        db_client: Any | None = None,
        embedding_client: Any | None = None,
        generation_client: Any | None = None,
    ) -> None:
        super().__init__(
            db_client, vectordb_client, embedding_client, generation_client
        )
        self.collection_name = DatabaseConfig.VECTOR_COLLECTION_NAME.value

    async def create_collection(
        self,
        embedding_size: int,
        distance: models.Distance,
        do_reset: bool = False,
        collection_name: str | None = None,
    ) -> bool:
        result = False
        if do_reset:
            _ = await self.vectordb_client.delete_collection(
                collection_name=collection_name
            )
        if collection_name is None:
            collection_name = self.collection_name
        if not await self.vectordb_client.collection_exists(
            collection_name=collection_name
        ):
            result = await self.vectordb_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size, distance=distance
                ),
            )
        return result

    async def batch_push(
        self,
        vectors: list[Vector],
        batch_size: int = 64,
        collection_name: str | None = None,
    ) -> bool:
        if collection_name is None:
            collection_name = self.collection_name
        if not await self.vectordb_client.collection_exists(
            collection_name=collection_name
        ):
            return False
        metadata = [v.model_dump(exclude_none=True) for v in vectors]
        vectors = [m.pop("vector") for m in metadata]
        self.vectordb_client.upload_collection(
            parallel=os.cpu_count(),  # full cpu power
            collection_name=collection_name,
            vectors=vectors,
            payload=metadata,
            batch_size=batch_size,
        )
        return True

    async def search_by_vector(
        self,
        vector: Vector,
        limit: int = 4,
        collection_name: str | None = None,
    ) -> list[Vector]:
        records = []
        if collection_name is None:
            collection_name = self.collection_name
        if await self.vectordb_client.collection_exists(
            collection_name=collection_name
        ):
            result = await self.vectordb_client.search(
                collection_name=collection_name,
                query_vector=vector.vector,
                limit=limit,
            )
        if result is not None:
            records.extend(
                [
                    Vector(
                        text=record.payload["text"],
                        source_name=record.payload["source_name"],
                        source_id=record.payload["source_id"],
                        score=record.score,
                    )
                    for record in result
                    if record.score > 0.0
                ]
            )
        return records
