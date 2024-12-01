from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_ADMIN_USER: str
    MONGO_ADMIN_PASS: str
    MONGODB_URL: str
    MONGODB_DATABASE_NAME: str
    ASSET_UNSTRUCTURED_ALLOWED_TYPES: list[str]
    ASSET_UNSTRUCTURED_ALLOWED_SIZE: int
    ASSET_UNSTRUCTURED_UPLOAD_CHUNK_SIZE: int

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
