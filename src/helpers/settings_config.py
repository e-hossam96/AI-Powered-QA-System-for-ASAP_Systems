from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_ADMIN_USER: str
    MONGO_ADMIN_PASS: str
    UNSTRUCTURED_ALLOWED_ASSET_TYPES: list[str]
    UNSTRUCTURED_ALLOWED_ASSET_SIZE: int

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
