from typing import Any
from .BaseModel import BaseModel
from configs import DatabaseConfig
from .data_schemas import Asset
from motor.motor_asyncio import AsyncIOMotorDatabase


class AssetModel(BaseModel):
    def __init__(
        self,
        db_client: AsyncIOMotorDatabase,
        vectordb_client: Any | None = None,
    ) -> None:
        super().__init__(db_client, vectordb_client)
        collection_name = DatabaseConfig.ASSET_COLLECTION_NAME.value
        self.collection = self.db_client[collection_name]

    async def push_asset_to_db(self, asset: Asset) -> Asset:
        result = await self.collection.insert_one(
            asset.model_dump(by_alias=True, exclude_none=True)
        )
        asset.id = result.inserted_id
        return asset

    # async def get_asset_by_name(self, name: str) -> Asset | None:
    #     record = await self.collection.find_one(filter={"name": name})
    #     if record:
    #         record = Asset(**record)
    #     return record

    async def get_all_assets(self) -> list[Asset]:
        cursor = self.collection.find({})
        assets = []
        async for record in cursor:
            asset = Asset(**record)
            assets.append(asset)
        return assets
