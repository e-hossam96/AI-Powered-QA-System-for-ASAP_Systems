from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from .route_schemas import RagQueryConfig
from configs import ResponseConfig, OpenAIRoleConfig
from models.data_schemas import Vector
from models import QdrantVectorModel, OpenAILLMModel
from controllers import OpenAILLMController
from helpers import get_settings


rag_router = APIRouter(prefix="/rag", tags=["rag"])

# one tool to search the vector db
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "the text used to search knowledge base",
                    },
                },
                "required": ["text"],
                "additionalProperties": False,
            },
        },
    }
]


@rag_router.post("/query")
async def chat(request: Request, rag_config: RagQueryConfig) -> JSONResponse:
    # almost same as search index at start
    app_settings = get_settings()
    vectordb_model = QdrantVectorModel(request.app.vectordb_client)
    embedding_model = OpenAILLMModel(embedding_client=request.app.embedding_client)
    generation_model = OpenAILLMModel(generation_client=request.app.generation_client)
    generation_controller = OpenAILLMController()
    vector = Vector(text=rag_config.text)
    vector.vector = await embedding_model.embed_text(
        vector.text, app_settings.EMBEDDING_LLM_MODEL_NAME
    )
    if vector.vector is None:
        return JSONResponse(
            content={"message": ResponseConfig.EMBEDDING_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    augmenttions = await vectordb_model.search_by_vector(vector, rag_config.limit)
    if len(augmenttions) == 0:
        return JSONResponse(
            content={"message": ResponseConfig.VECTORDB_SEARCH_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    augmenttions = [aug.text for aug in augmenttions]
    prompt = generation_controller.process_prompt_text(
        vector.text, app_settings.GENERATION_LLM_MAX_PROMPT_TOKENS
    )
    messages = generation_controller.construct_rag_messages(
        prompt, augmenttions, rag_config.chat_history
    )
    ans = await generation_model.generate_text(
        model_name=app_settings.GENERATION_LLM_MODEL_NAME,
        messages=messages,
        max_output_tokens=app_settings.GENERATION_LLM_MAX_OUTPUT_TOKENS,
        temperature=app_settings.GENERATION_LLM_TEMPERATURE,
    )
    if ans is None:
        return JSONResponse(
            content={"message": ResponseConfig.RAG_ANS_GENERATION_FAILED.value},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    messages.append({"role": OpenAIRoleConfig.ASSISTANT.value, "content": ans})
    return JSONResponse(
        content={
            "message": ResponseConfig.RAG_ANS_GENERATION_SUCCEEDED.value,
            "response": ans,
            "chat_history": messages,
        },
        status_code=status.HTTP_200_OK,
    )
