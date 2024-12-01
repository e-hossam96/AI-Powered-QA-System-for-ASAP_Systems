from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseModel:
    def __init__(self, db_client: AsyncIOMotorDatabase) -> None:
        self.db_client = db_client
