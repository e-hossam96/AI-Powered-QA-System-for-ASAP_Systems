from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


index_router = APIRouter(prefix="/index", tags=["index"])


@index_router.post("/push")
async def push_chunks_into_vector_db() -> JSONResponse:
    pass


@index_router.post("/search")
async def search_vector_db() -> JSONResponse:
    pass


@index_router.get("/info/{collection_name}")
async def get_vector_db_collection_info(collection_name: str) -> JSONResponse:
    pass
