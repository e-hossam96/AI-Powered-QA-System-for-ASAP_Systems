from typing import Any
from .BaseModel import BaseModel
from configs import DatabaseConfig
from .data_schemas import Chunk
from pymongo import InsertOne
from motor.motor_asyncio import AsyncIOMotorDatabase


class ChunkModel(BaseModel):
    def __init__(
        self,
        db_client: AsyncIOMotorDatabase,
        vectordb_client: Any | None = None,
        embedding_client: Any | None = None,
        generation_client: Any | None = None,
    ) -> None:
        super().__init__(
            db_client, vectordb_client, embedding_client, generation_client
        )
        collection_name = DatabaseConfig.CHUNK_COLLECTION_NAME.value
        self.collection = self.db_client[collection_name]

    # async def push_chunk_to_db(self, chunk: Chunk) -> Chunk:
    #     result = await self.collection.insert_one(
    #         chunk.model_dump(by_alias=True, exclude_none=True)
    #     )
    #     chunk.id = result.inserted_id
    #     return chunk

    # async def get_all_chunks(self) -> list[Chunk]:
    #     cursor = self.collection.find({})
    #     assets = []
    #     async for record in cursor:
    #         asset = Chunk(**record)
    #         assets.append(asset)
    #     return assets

    async def clear_all_chunks(self) -> int:
        result = await self.collection.delete_many({})
        return result.deleted_count

    async def batch_push_chunks_to_db(
        self, chunks: list[Chunk], batch_size: int = 64
    ) -> int:
        num_chunks = len(chunks)
        # implement batch operations
        for i in range(0, num_chunks, batch_size):
            batch_chunks = chunks[i : i + batch_size]
            # create operations
            batch_operations = [
                InsertOne(chunk.model_dump(by_alias=True, exclude_none=True))
                for chunk in batch_chunks
            ]
            await self.collection.bulk_write(batch_operations)
        return num_chunks

    async def get_all_chunks(
        self, page_index: int = 0, page_size: int = 128
    ) -> tuple[list[Chunk], int]:
        num_records = await self.collection.count_documents({})
        num_pages = num_records // page_size
        num_pages += 1 if num_records % page_size else 0
        cursor = self.collection.find({}).skip(page_index * page_size).limit(page_size)
        chunks = []
        async for record in cursor:
            chunk = Chunk(**record)
            chunks.append(chunk)
        return chunks, num_pages
