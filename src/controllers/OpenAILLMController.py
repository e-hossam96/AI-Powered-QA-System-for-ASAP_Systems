from .BaseController import BaseController
from locales import rag_templates
from configs import OpenAIRoleConfig


class OpenAILLMController(BaseController):
    def __init__(self) -> None:
        super().__init__()

    def process_prompt_text(
        self,
        prompt_text: str,
        max_tokens: int = 1024,
        special_tokens: list[str] | None = None,
    ):
        prompt_tokens = prompt_text.split()
        if special_tokens is not None:
            for st in special_tokens:
                while st in prompt_tokens:
                    prompt_tokens.remove(st)
        prompt_tokens = prompt_tokens[:max_tokens]
        return " ".join(prompt_tokens).strip()

    def construct_rag_messages(
        self,
        prompt: str,
        augmentations: list[str] | None,
        chat_history: list[dict] | None = None,
    ) -> list[dict]:
        if chat_history is None:
            system_msg = rag_templates.system_prompt.substitute({})
            chat_history = [
                {"role": OpenAIRoleConfig.SYSTEM.value, "content": system_msg}
            ]
        if augmentations is None:
            chat_history.append(
                {
                    "role": OpenAIRoleConfig.USER.value,
                    "content": f"{prompt}",
                }
            )
        else:
            augmentations = [
                rag_templates.document_prompt.substitute(
                    {"doc_num": i + 1, "chunk_text": aug}
                )
                for i, aug in enumerate(augmentations)
            ]
            augmentations = "\n".join(augmentations)
            prompt = rag_templates.footer_prompt.substitute({"user_query": prompt})
            chat_history.append(
                {
                    "role": OpenAIRoleConfig.USER.value,
                    "content": f"{augmentations}\n\n{prompt}",
                }
            )
        return chat_history

    def process_augmentations(self, augmentations: list[str]) -> str:
        augmentations = [
            rag_templates.document_prompt.substitute(
                {"doc_num": i + 1, "chunk_text": aug}
            )
            for i, aug in enumerate(augmentations)
        ]
        augmentations = "\n".join(augmentations)
        return augmentations
