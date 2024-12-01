from typing import Any
from .BaseModel import BaseModel
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
