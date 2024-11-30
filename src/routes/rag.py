from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


rag_router = APIRouter(prefix="/rag", tags=["rag"])


@rag_router.post("/query")
async def chat() -> JSONResponse:
    pass
