from models import AssetModel
from models.data_schemas import Asset
from controllers import AssetController
from configs import ResponseConfig
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, UploadFile, status


data_router = APIRouter(prefix="/data", tags=["data"])


@data_router.post("/push")
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


@data_router.post("/process")
async def process_asset_text_into_chunks() -> JSONResponse:
    pass


@data_router.get("/info/{collection_name}")
async def get_db_collection_info(collection_name: str) -> JSONResponse:
    pass
