from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


data_router = APIRouter(prefix="/data", tags=["data"])


@data_router.post("/push")
async def push_asset_to_db() -> JSONResponse:
    pass


@data_router.post("/process")
async def process_asset_text_into_chunks() -> JSONResponse:
    pass


@data_router.get("/info/{collection_name}")
async def get_db_collection_info(collection_name: str) -> JSONResponse:
    pass
