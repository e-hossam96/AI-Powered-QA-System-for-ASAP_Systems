import json
import weave
from models import OpenAILLMModel
from configs import OpenAIRoleConfig
from helpers.settings_config import Settings
from locales.eval_completeness_templates import SYSTEM_PROMPT, USER_PROMPT


@weave.op()
async def score_completeness(
    query: str, response: str, app_settings: Settings, eval_model: OpenAILLMModel
) -> dict | None:
    messages = [
        {OpenAIRoleConfig.SYSTEM.value: SYSTEM_PROMPT.safe_substitute()},
        {
            OpenAIRoleConfig.USER.value: USER_PROMPT.safe_substitute(
                user_query=query, generated_answer=response
            )
        },
    ]
    ans = await eval_model.generate_text(
        model_name=app_settings.EVAL_LLM_MODEL_NAME,
        messages=messages,
        max_output_tokens=app_settings.EVAL_LLM_MAX_OUTPUT_TOKENS,
        temperature=app_settings.EVAL_LLM_TEMPERATURE,
    )
    if ans is None:
        return None
    score = json.loads(ans.choices[0].message.content)
    return score
