import weave
from pathlib import Path
from helpers import get_settings
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from controllers import OpenAILLMController
from evaluation.eval_completeness import score_completeness
from evaluation.rag_pipelines import ToolCallRAGPipeline, RAGSettings
from evaluation.utils import read_eval_data
from models import OpenAILLMModel, QdrantVectorModel

eval_router = APIRouter(prefix="/rag", tags=["rag", "evaluation"])


@eval_router.get("/evaluate")
async def evaluate(request: Request) -> JSONResponse:
    app_settings = get_settings()
    rag_settings = RAGSettings(
        GENERATION_LLM_BASE_URL=app_settings.GENERATION_LLM_BASE_URL,
        GENERATION_LLM_MODEL_NAME=app_settings.GENERATION_LLM_MODEL_NAME,
        GENERATION_LLM_SPECIAL_TOKENS=app_settings.GENERATION_LLM_SPECIAL_TOKENS,
        GENERATION_LLM_MAX_PROMPT_TOKENS=app_settings.GENERATION_LLM_MAX_PROMPT_TOKENS,
        GENERATION_LLM_MAX_OUTPUT_TOKENS=app_settings.GENERATION_LLM_MAX_OUTPUT_TOKENS,
        GENERATION_LLM_TEMPERATURE=app_settings.GENERATION_LLM_TEMPERATURE,
        EMBEDDING_LLM_BASE_URL=app_settings.EMBEDDING_LLM_BASE_URL,
        EMBEDDING_LLM_MODEL_NAME=app_settings.EMBEDDING_LLM_MODEL_NAME,
        EMBEDDING_LLM_SPECIAL_TOKENS=app_settings.EMBEDDING_LLM_SPECIAL_TOKENS,
        EMBEDDING_LLM_EMBEDDING_SIZE=app_settings.EMBEDDING_LLM_EMBEDDING_SIZE,
        EMBEDDING_LLM_MAX_PROMPT_TOKENS=app_settings.EMBEDDING_LLM_MAX_PROMPT_TOKENS,
    )
    vectordb_model = QdrantVectorModel(request.app.vectordb_client)
    embedding_model = OpenAILLMModel(embedding_client=request.app.embedding_client)
    generation_model = OpenAILLMModel(generation_client=request.app.generation_client)
    evaluation_model = OpenAILLMModel(generation_client=request.app.evaluation_client)
    generation_controller = OpenAILLMController()

    rag_pipeline = ToolCallRAGPipeline(
        vectordb_model=vectordb_model,
        embedding_model=embedding_model,
        generation_model=generation_model,
        generation_controller=generation_controller,
        rag_settings=rag_settings,
    )
    eval_dataset = read_eval_data(Path(app_settings.EVAL_DATA_PATH))

    async def scorer(query, output):
        return await score_completeness(
            query,
            output["response"],
            evaluation_model,
            model_name=app_settings.EVAL_LLM_MODEL_NAME,
            max_output_tokens=app_settings.EVAL_LLM_MAX_OUTPUT_TOKENS,
            temperature=app_settings.EVAL_LLM_TEMPERATURE,
        )

    completeness_evaluator = weave.Evaluation(
        name="Completeness-Evaluation",
        description="Evaluate completeness of LLM's generated answers compared to user query.",
        dataset=eval_dataset,
        scorers=[scorer],
    )
    try:
        scores = await completeness_evaluator.evaluate(rag_pipeline)
    except Exception as e:
        return JSONResponse(
            content={},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return JSONResponse(
        content={"scores": scores},
        status_code=status.HTTP_200_OK,
    )
