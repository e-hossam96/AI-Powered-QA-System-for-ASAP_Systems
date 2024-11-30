from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


base_router = APIRouter(tags=["base"])


@base_router.get("/")
async def welcome() -> JSONResponse:
    resp = JSONResponse(
        content={"message": "Hello All! Nice to meet you!"},
        status_code=status.HTTP_200_OK,
    )
    return resp
