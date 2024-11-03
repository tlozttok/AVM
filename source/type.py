
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal


class Role(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"
    TOOL="tool"


class MessageType(Enum):
    TEXT="text"
    IMAGE="image"
    TOOL_CALL="tool_call" #必要性存疑