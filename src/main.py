"""Implementation of the main FastAPI application.

In this file we will define the main fastapi app and connect it \
with the different routes of the system.
"""

from fastapi import FastAPI
from routes.base import base_router
from routes.data import data_router
from routes.index import index_router
from routes.rag import rag_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def connect_lifespan_clients(app: FastAPI):
    yield


app = FastAPI(lifespan=connect_lifespan_clients)
app.include_router(base_router)
app.include_router(data_router)
app.include_router(index_router)
app.include_router(rag_router)
