from typing import Any
from .BaseModel import BaseModel
from data_schemas import Vector
from bson.objectid import ObjectId
from qdrant_client import QdrantClient, models


class QdrantVectorModel(BaseModel):
    def __init__(
        self,
        vectordb_client: QdrantClient,
        db_client: Any | None = None,
    ) -> None:
        super().__init__(db_client, vectordb_client)

    def create_collection(
        self,
        collection_name: str,
        embedding_size: int,
        distance: models.Distance,
        do_reset: bool = False,
    ) -> bool:
        result = False
        if do_reset:
            _ = self.vectordb_client.delete_collection(collection_name=collection_name)
        if not self.vectordb_client.collection_exists(collection_name=collection_name):
            result = self.vectordb_client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size, distance=distance
                ),
            )
        return result

    def batch_push(
        self,
        collection_name: str,
        vectors: list[Vector],
        batch_size: int = 64,
    ) -> bool:
        if not self.vectordb_client.collection_exists(collection_name=collection_name):
            return False
        metadata = [v.model_dump(mode="json", exclude_none=True) for v in vectors]
        vectors = [m.pop("vector") for m in metadata]
        self.vectordb_client.upload_collection(
            collection_name=collection_name,
            vectors=vectors,
            payload=metadata,
            batch_size=batch_size,
        )
        return True

    def search_by_vector(
        self, collection_name: str, vector: Vector, limit: int = 4
    ) -> list[Vector]:
        records = []
        if self.vectordb_client.collection_exists(collection_name=collection_name):
            result = self.vectordb_client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=limit,
            )
        if result is not None:
            records.extend(
                [
                    Vector(
                        text=record.payload["text"],
                        source_name=record.payload["source_name"],
                        source_id=ObjectId(record.payload["source_id"]),
                        score=record.score,
                    )
                    for record in result
                ]
            )
        return records
