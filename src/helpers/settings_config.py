from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_ADMIN_USER: str
    MONGO_ADMIN_PASS: str
    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_DATABASE_NAME: str
    VECTORDB_HOST: str
    VECTORDB_PORT: int
    VECTORDB_PROVIDER: str
    VECTORDB_DISTANCE: str
    ASSET_UNSTRUCTURED_ALLOWED_TYPES: list[str]
    ASSET_UNSTRUCTURED_ALLOWED_SIZE: int
    ASSET_UNSTRUCTURED_UPLOAD_CHUNK_SIZE: int
    GENERATION_LLM_BASE_URL: str
    GENERATION_LLM_MODEL_NAME: str
    GENERATION_LLM_MAX_PROMPT_TOKENS: int
    GENERATION_LLM_MAX_OUTPUT_TOKENS: int
    GENERATION_LLM_TEMPERATURE: float
    EMBEDDING_LLM_BASE_URL: str
    EMBEDDING_LLM_MODEL_NAME: str
    EMBEDDING_LLM_EMBEDDING_SIZE: int
    OPENAI_API_KEY: str
    WIKIPEDIA_USER_AGENT: str
    WIKIPEDIA_LANGUAGE: str
    USER_AGENT: str

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
