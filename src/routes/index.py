from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from .route_schemas import VectorIndexConfig, VectorSearchConfig
from configs import ResponseConfig, VectorDistanceConfig
from models.data_schemas import Vector
from models import ChunkModel, QdrantVectorModel, OpenAILLMModel
from helpers import get_settings
from qdrant_client.models import Distance


index_router = APIRouter(prefix="/index", tags=["index"])


@index_router.post("/push")
async def push_chunks_into_vector_db(
    request: Request, index_config: VectorIndexConfig
) -> JSONResponse:
    app_settings = get_settings()
    chunk_model = ChunkModel(request.app.db_client)
    vectordb_model = QdrantVectorModel(request.app.vectordb_client)
    embedding_model = OpenAILLMModel(embedding_client=request.app.embedding_client)
    # handle collection creation
    distance_method = Distance.COSINE  # default distance
    if app_settings.VECTORDB_DISTANCE == VectorDistanceConfig.COSINE.value:
        distance_method = Distance.COSINE
    elif app_settings.VECTORDB_DISTANCE == VectorDistanceConfig.DOT.value:
        distance_method = Distance.DOT
    _ = await vectordb_model.create_collection(
        embedding_size=app_settings.EMBEDDING_LLM_EMBEDDING_SIZE,
        distance=distance_method,
        do_reset=index_config.do_reset,
    )
    # get batched chunks from db and batch push the batched into vector db
    chunks_batch, num_pages = await chunk_model.get_all_chunks()
    if num_pages == 0 or len(chunks_batch) == 0:
        return JSONResponse(
            content={"message": ResponseConfig.DB_NO_CHUNKS.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    num_vectordb_vectors, num_db_vectors = 0, 0
    for page_index in range(num_pages):
        chunks_batch, _ = await chunk_model.get_all_chunks(page_index=page_index)
        # convert chunk models to vector models
        # this is needed to communicate with the vectordb model
        vectors = [
            Vector(text=c.text, source_name=c.source_name, source_id=c.source_id)
            for c in chunks_batch
        ]
        num_db_vectors += len(vectors)
        # vectorize the texts
        for v in vectors:
            v.vector = await embedding_model.embed_text(
                text=v.text, model_name=app_settings.EMBEDDING_LLM_MODEL_NAME
            ).data[0].embedding
        # remove all vectors with no embeddings
        vectors = [v for v in vectors if v.vector is not None]
        num_vectordb_vectors += len(vectors)
        # send vectors to vectordb
        _ = await vectordb_model.batch_push(vectors)
    if num_vectordb_vectors == 0:
        return JSONResponse(
            content={"message": ResponseConfig.EMBEDDING_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return JSONResponse(
        content={"message": ResponseConfig.VECTORDB_INDEXING_SUCCEEDED.value},
        status_code=status.HTTP_200_OK,
    )


@index_router.post("/search")
async def search_vector_db(
    request: Request, search_config: VectorSearchConfig
) -> JSONResponse:
    app_settings = get_settings()
    vectordb_model = QdrantVectorModel(request.app.vectordb_client)
    embedding_model = OpenAILLMModel(embedding_client=request.app.embedding_client)
    vector = Vector(text=search_config.text)
    vector.vector = await embedding_model.embed_text(
        vector.text, app_settings.EMBEDDING_LLM_MODEL_NAME
    ).data[0].embedding
    if vector.vector is None:
        return JSONResponse(
            content={"message": ResponseConfig.EMBEDDING_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    results = await vectordb_model.search_by_vector(vector, search_config.limit)
    if len(results) == 0:
        return JSONResponse(
            content={"message": ResponseConfig.VECTORDB_SEARCH_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    results = [r.model_dump(exclude_none=True) for r in results]
    for r in results:
        r["source_id"] = r["source_id"]
    return JSONResponse(
        content={
            "message": ResponseConfig.VECTORDB_SEARCH_SUCCEEDED.value,
            "vectors": results,
        },
        status_code=status.HTTP_200_OK,
    )


@index_router.get("/info/{collection_name}")
async def get_vector_db_collection_info(collection_name: str) -> JSONResponse:
    pass
