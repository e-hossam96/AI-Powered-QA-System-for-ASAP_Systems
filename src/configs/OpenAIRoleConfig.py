from enum import Enum


class OpenAIRoleConfig(Enum):
    SYSTEM: str = "system"
    USER: str = "user"
    ASSISTANT: str = "assistant"
    TOOL: str = "tool"
