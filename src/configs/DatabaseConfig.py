from enum import Enum


class DatabaseConfig(Enum):
    CHUNK_COLLECTION_NAME: str = "chunks"
    ASSET_COLLECTION_NAME: str = "assets"
