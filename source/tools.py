
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal

from .functions import FunctionDescription
from .message import Message
from .routine import Subroutine

class ToolDescription:
    type:Literal["function"]
    function:FunctionDescription

    def to_dict(self)->dict:
        ...


class Tool(ABC):
    description:ToolDescription

    @property
    def tool_info(self)->dict:
        return self.description.to_dict()

    @abstractmethod
    def call(self,args:dict)->str:
        pass


class ToolSet:
    tools:List[Tool]
    def __init__(self):
        self.tools=[]

    @property
    def tools_info(self)->List[dict]:
        return [tool.tool_info for tool in self.tools]

    def execute(self,tool_calls:List[ChatCompletionMessageToolCall])->List[Message|Subroutine]:
        ...