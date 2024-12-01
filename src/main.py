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
from motor.motor_asyncio import AsyncIOMotorClient
from helpers import get_settings, Settings


def connect_mongo_client(
    app: FastAPI,
    app_settinigs,
) -> FastAPI:
    # get mongo connection and db client
    app.db_connection = AsyncIOMotorClient(host=app_settinigs.MONGODB_URL)
    app.db_client = app.db_connection[app_settinigs.MONGODB_DATABASE_NAME]
    return app


@asynccontextmanager
async def connect_lifespan_clients(app: FastAPI):
    settings = get_settings()
    app = connect_mongo_client(app, settings)
    yield
    app.db_connection.close()


app = FastAPI(lifespan=connect_lifespan_clients)
app.include_router(base_router)
app.include_router(data_router)
app.include_router(index_router)
app.include_router(rag_router)
