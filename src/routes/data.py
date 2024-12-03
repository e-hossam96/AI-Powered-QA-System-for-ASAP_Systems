from models import AssetModel, ChunkModel
from models.data_schemas import Asset, Chunk
from controllers import AssetController, ChunkController
from configs import ResponseConfig
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, UploadFile, status
from .route_schemas import ProcessingConfig
from helpers import get_settings


data_router = APIRouter(prefix="/data", tags=["data"])


@data_router.post("/push/asset")
async def push_asset_to_db(
    request: Request,
    asset: UploadFile,
) -> JSONResponse:
    asset_controller = AssetController()
    # validate asset type
    is_valid = asset_controller.validate_unstructured_asset_type(asset)
    if not is_valid:
        return JSONResponse(
            content={"message": ResponseConfig.ASSET_UNSUPPORTED_TYPE.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # validate asset size
    is_valid = asset_controller.validate_unstructured_asset_size(asset)
    if not is_valid:
        return JSONResponse(
            content={"message": ResponseConfig.ASSET_EXCEEDED_MAX_SIZE.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # upload file to server storage
    asset_path, asset_name = asset_controller.get_unique_asset_path(asset.filename)
    is_written = await asset_controller.write_uploaded_unstructured_asset(
        asset, asset_path
    )
    if not is_written:
        return JSONResponse(
            content={"message": ResponseConfig.ASSET_UPLOAD_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # store asset into database
    asset_model = AssetModel(request.app.db_client)
    asset_obj = Asset(
        name=asset_name, type=asset.content_type, size=asset_path.stat().st_size
    )
    _ = await asset_model.push_asset_to_db(asset_obj)
    return JSONResponse(
        content={"message": ResponseConfig.ASSET_UPLOAD_SUCCEEDED.value},
        status_code=status.HTTP_200_OK,
    )


@data_router.post("/process/asset")
async def process_asset_text_into_chunks(
    request: Request, processing_config: ProcessingConfig
) -> JSONResponse:
    asset_model = AssetModel(request.app.db_client)
    chunk_model = ChunkModel(request.app.db_client)
    chunk_controller = ChunkController()
    if processing_config.do_reset:
        _ = await chunk_model.clear_all_chunks()
    # get all assets from db
    # should be small number relative to chunks
    assets = await asset_model.get_all_assets()
    if len(assets) == 0:
        return JSONResponse(
            content={"message": ResponseConfig.DB_NO_ASSETS.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # processing all assets and pushing them to db
    for asset in assets:
        asset_path = chunk_controller.get_asset_path(asset.name)
        asset_content = chunk_controller.get_unstructured_asset_content(asset_path)
        asset_chunks = chunk_controller.process_unstructured_asset_content(
            asset_content, processing_config.chunk_size, processing_config.overlap_size
        )
        asset_chunks = [
            Chunk(text=c.page_content, source_name=asset.name, source_id=asset.id)
            for c in asset_chunks
        ]
        _ = await chunk_model.batch_push_chunks_to_db(asset_chunks)
    return JSONResponse(
        content={"message": ResponseConfig.DB_PROCESSED_ALL_ASSETS.value},
        status_code=status.HTTP_200_OK,
    )


@data_router.post("/process/webpage")
async def process_asset_text_into_chunks(
    request: Request, processing_config: ProcessingConfig
) -> JSONResponse:
    app_settings = get_settings()
    chunk_model = ChunkModel(request.app.db_client)
    chunk_controller = ChunkController()
    if processing_config.do_reset:
        _ = await chunk_model.clear_all_chunks()
    # getting webpage contents
    webpage_content = chunk_controller.get_webpage_content(
        processing_config.asset_name_or_url,
        user_agent=app_settings.WIKIPEDIA_USER_AGENT,
        language=app_settings.WIKIPEDIA_LANGUAGE,
    )
    if webpage_content is None:
        return JSONResponse(
            content={"message": ResponseConfig.URL_NO_CONTENT.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    webpage_chunks = chunk_controller.process_unstructured_asset_content(
        webpage_content, processing_config.chunk_size, processing_config.overlap_size
    )
    webpage_chunks = [
        Chunk(
            text=c.page_content,
            source_name=processing_config.asset_name_or_url,
            source_id=processing_config.asset_name_or_url,
        )
        for c in webpage_chunks
    ]
    _ = await chunk_model.batch_push_chunks_to_db(webpage_chunks)
    return JSONResponse(
        content={"message": ResponseConfig.URL_CONTENT_PROCESSING_SUCCEEDED.value},
        status_code=status.HTTP_200_OK,
    )


@data_router.get("/info/{collection_name}")
async def get_db_collection_info(collection_name: str) -> JSONResponse:
    pass
