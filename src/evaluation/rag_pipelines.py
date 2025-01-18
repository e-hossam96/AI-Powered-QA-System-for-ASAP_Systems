import json
import weave
from configs import OpenAIRoleConfig
from controllers import OpenAILLMController
from helpers.settings_config import Settings
from models import OpenAILLMModel, QdrantVectorModel
from models.data_schemas import Vector


class ToolCallRAGPipeline(weave.Model):
    vectordb_model: QdrantVectorModel
    embedding_model: OpenAILLMModel
    generation_model: OpenAILLMModel
    generation_controller: OpenAILLMController
    app_settings: Settings

    @weave.op()
    async def predict(
        self, query: str, chat_history: list[dict] | None = None, limit: int | None = 4
    ) -> str | None:
        prompt = self.generation_controller.process_prompt_text(
            query,
            self.app_settings.GENERATION_LLM_MAX_PROMPT_TOKENS,
            self.app_settings.GENERATION_LLM_SPECIAL_TOKENS,
        )
        messages = self.generation_controller.construct_user_query(
            prompt=prompt,
            chat_history=chat_history,
        )
        ans = await self.generation_model.generate_text(
            model_name=self.app_settings.GENERATION_LLM_MODEL_NAME,
            messages=messages,
            max_output_tokens=self.app_settings.GENERATION_LLM_MAX_OUTPUT_TOKENS,
            temperature=self.app_settings.GENERATION_LLM_TEMPERATURE,
            tools=self.generation_controller.get_tools(),
        )

        if ans is None:
            return None

        # handle function call responses
        while ans.choices[0].finish_reason == "tool_calls":
            tool_call = ans.choices[0].message.tool_calls[0].function
            tool_name = tool_call.name
            args = json.loads(tool_call.arguments)
            # get tool input parameters
            if "text" in args and tool_name == "search_knowledge_base":
                args["text"] = self.generation_controller.process_prompt_text(
                    prompt_text=query,
                    max_tokens=self.app_settings.EMBEDDING_LLM_MAX_PROMPT_TOKENS,
                    special_tokens=self.app_settings.EMBEDDING_LLM_SPECIAL_TOKENS,
                )
                vector = Vector(**args)
            else:
                return None
            # embed the text
            resp = await self.embedding_model.embed_text(
                vector.text, self.app_settings.EMBEDDING_LLM_MODEL_NAME
            )
            vector.vector = resp.data[0].embedding if resp is not None else resp
            if vector.vector is None:
                return None
            augmenttions = await self.vectordb_model.search_by_vector(vector, limit)
            if len(augmenttions) == 0:
                return None
            augmenttions = [aug.text for aug in augmenttions]
            augmenttions = self.generation_controller.process_augmentations(
                augmenttions
            )

            tool_call_result_message = {
                "role": OpenAIRoleConfig.TOOL.value,
                "content": json.dumps(
                    {
                        "text": vector.text,
                        "relevant_knowledge": augmenttions,
                    }
                ),
                "tool_call_id": ans.choices[0].message.tool_calls[0].id,
            }
            tool_messsage = ans.choices[0].message.to_dict()
            messages.extend([tool_messsage, tool_call_result_message])
            ans = await self.generation_model.generate_text(
                model_name=self.app_settings.GENERATION_LLM_MODEL_NAME,
                messages=messages,
                max_output_tokens=self.app_settings.GENERATION_LLM_MAX_OUTPUT_TOKENS,
                temperature=self.app_settings.GENERATION_LLM_TEMPERATURE,
                tools=self.generation_controller.get_tools(),
            )

        # finialize chat history and return
        messages.append(
            {
                "role": OpenAIRoleConfig.ASSISTANT.value,
                "content": ans.choices[0].message.content,
            }
        )
        messages = self.generation_controller.finalize_messages(messages)
        return {"response": messages[-1]["content"], "context": augmenttions}


class RetrieverPipeline(weave.Model):
    vectordb_model: QdrantVectorModel
    embedding_model: OpenAILLMModel
    app_settings: Settings

    @weave.op()
    async def predict(self, query: str, limit: int | None = 4) -> list[str] | None:
        vector = Vector(text=query)
        resp = await self.embedding_model.embed_text(
            vector.text, self.app_settings.EMBEDDING_LLM_MODEL_NAME
        )
        vector.vector = resp.data[0].embedding if resp is not None else resp
        if vector.vector is None:
            return None
        results = await self.vectordb_model.search_by_vector(vector, limit)
        if len(results) == 0:
            return None
        results[:] = [r.model_dump(exclude_none=True)["text"] for r in results]
        return {"context": results}
