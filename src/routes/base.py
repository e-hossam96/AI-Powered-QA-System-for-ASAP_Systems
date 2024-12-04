from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from configs import ResponseConfig


base_router = APIRouter(tags=["base"])


@base_router.get("/")
async def welcome() -> JSONResponse:
    resp = JSONResponse(
        content={"message": ResponseConfig.BASE.value},
        status_code=status.HTTP_200_OK,
    )
    return resp
