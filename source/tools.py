
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
        return {"type":self.type, "function":self.function.to_dict()}


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
    tools_dict:dict[str,Tool]
    def __init__(self):
        self.tools=[]
        self.tools_dict={}

    @property
    def tools_info(self)->List[dict]:
        return [tool.tool_info for tool in self.tools]

    def execute_once(self,tool_call:ChatCompletionMessageToolCall)->Message|Subroutine:
        tool=self.tools_dict[tool_call.function.name]
        ...

    def execute(self,tool_calls:List[ChatCompletionMessageToolCall])->List[Message|Subroutine]:
        ...