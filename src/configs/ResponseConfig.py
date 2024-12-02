from enum import Enum


class ResponseConfig(Enum):
    ASSET_UNSUPPORTED_TYPE: str = "asset type is not supported"
    ASSET_EXCEEDED_MAX_SIZE: str = "asset exceeded maximum allowed size"
    ASSET_UPLOAD_FAILED: str = "asset upload failed"
    ASSET_UPLOAD_SUCCEEDED: str = "asset upload succeeded"
    DB_NO_ASSETS: str = "no assets found in database"
    DB_NO_CHUNKS: str = "no chunks found in database"
    DB_PROCESSED_ALL_ASSETS: str = "processed all assets into chunks"
    EMBEDDING_FAILED: str = "failed to generate embeddings"
    VECTORDB_INDEXING_SUCCEEDED: str = "indexing vector database succeeded"
