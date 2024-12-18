import weave
from typing import Any
from openai import AsyncOpenAI
from .BaseModel import BaseModel
from openai.types.chat import ChatCompletion
from openai.types.create_embedding_response import CreateEmbeddingResponse


class OpenAILLMModel(BaseModel):
    def __init__(
        self,
        db_client: Any | None = None,
        vectordb_client: Any | None = None,
        embedding_client: AsyncOpenAI | None = None,
        generation_client: AsyncOpenAI | None = None,
    ) -> None:
        super().__init__(
            db_client, vectordb_client, embedding_client, generation_client
        )

    @weave.op()
    async def generate_text(
        self,
        model_name: str,
        messages: list[dict],
        max_output_tokens: int = 512,
        temperature: float = 0.01,
        tools: list[dict] | None = None,
    ) -> ChatCompletion | None:
        # ensure client is set
        if self.generation_client is None:
            return None
        # ensure messages is a populated list
        if not isinstance(messages, list) or len(messages) == 0:
            return None
        # send prompt to chat endpoint
        resp = await self.generation_client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_output_tokens,
            temperature=temperature,
            tools=tools,
        )
        # validate response
        if (
            resp is None
            or resp.choices is None
            or len(resp.choices) == 0
            or resp.choices[0].message is None
        ):
            return None
        return resp

    @weave.op()
    async def embed_text(
        self, text: str, model_name: str
    ) -> CreateEmbeddingResponse | None:
        # ensure client is set
        if self.embedding_client is None:
            return None
        # send text to embedding endpoint
        resp = await self.embedding_client.embeddings.create(
            model=model_name, input=text
        )
        if (
            resp is None
            or resp.data is None
            or len(resp.data) == 0
            or resp.data[0].embedding is None
        ):
            return None
        return resp
