
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
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
    def call(self,args:str)->Message|Subroutine:
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
        return tool.call(tool_call.function.arguments) #TODO:如果AI的回答有问题，应该通过异常处理机制回退处理步骤，因此需要在项目中建立异常体系

    def execute(self,tool_calls:List[ChatCompletionMessageToolCall])->List[Message|Subroutine]:
        result=[]
        for tool_call in tool_calls:
            result.append(self.execute_once(tool_call))
        return result