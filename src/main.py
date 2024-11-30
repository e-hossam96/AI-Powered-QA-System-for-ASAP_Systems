"""Implementation of the main FastAPI application.

In this file we will define the main fastapi app and connect it \
with the different routes of the system.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def connect_lifespan_clients(app: FastAPI):
    pass


app = FastAPI(lifespan=connect_lifespan_clients)
