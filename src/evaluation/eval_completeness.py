import json
import weave
from models import OpenAILLMModel
from configs import OpenAIRoleConfig
from locales.eval_completeness_templates import SYSTEM_PROMPT, USER_PROMPT


@weave.op()
async def score_completeness(
    query: str, response: str, eval_model: OpenAILLMModel, **kwargs
) -> dict | None:
    messages = [
        {
            "role": OpenAIRoleConfig.SYSTEM.value,
            "content": SYSTEM_PROMPT.substitute({}),
        },
        {
            "role": OpenAIRoleConfig.USER.value,
            "content": USER_PROMPT.substitute(
                {"user_query": query, "generated_answer": response}
            ),
        },
    ]
    ans = await eval_model.generate_text(
        messages=messages,
        **kwargs,
    )
    if ans is None:
        return None
    score = json.loads(ans.choices[0].message.content)
    return score
