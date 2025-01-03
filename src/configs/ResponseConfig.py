from enum import Enum


class ResponseConfig(Enum):
    BASE: str = "nice to meet you!"
    ASSET_UNSUPPORTED_TYPE: str = "asset type is not supported"
    ASSET_EXCEEDED_MAX_SIZE: str = "asset exceeded maximum allowed size"
    ASSET_UPLOAD_FAILED: str = "asset upload failed"
    ASSET_UPLOAD_SUCCEEDED: str = "asset upload succeeded"
    DB_NO_ASSETS: str = "no assets found in database"
    DB_NO_CHUNKS: str = "no chunks found in database"
    DB_PROCESSED_ALL_ASSETS: str = "processed all assets into chunks"
    URL_NO_CONTENT: str = "no content found in url"
    URL_CONTENT_PROCESSING_SUCCEEDED: str = "processing url content succeeded"
    EMBEDDING_FAILED: str = "failed to generate embeddings"
    VECTORDB_INDEXING_SUCCEEDED: str = "indexing vector database succeeded"
    VECTORDB_SEARCH_SUCCEEDED: str = "searching vector database succeeded"
    VECTORDB_SEARCH_FAILED: str = "searching vector database failed"
    RAG_ANS_GENERATION_FAILED: str = "rag response generation failed"
    RAG_ANS_GENERATION_SUCCEEDED: str = "rag response generation succeeded"
