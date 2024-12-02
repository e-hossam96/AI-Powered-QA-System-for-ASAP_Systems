from .BaseController import BaseController


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
        return " ".join(prompt_tokens)
