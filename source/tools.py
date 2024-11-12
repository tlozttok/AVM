import json
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal


from source import routine
from .functions import FunctionDescription
from .message import Message


class ToolDescription:
    type:Literal["function"]
    function:FunctionDescription

    def __init__(self,function:FunctionDescription):
        self.type="function"
        self.function=function

    def to_dict(self)->dict:
        return {"type":self.type, "function":self.function.to_dict()}


class Tool(ABC):
    description:ToolDescription

    def __init__(self,description:ToolDescription):
        self.description=description

    @property
    def tool_info(self)->dict:
        return self.description.to_dict()

    @abstractmethod
    def call(self,args:dict)->Message|routine.Subroutine:
        pass

class ToolAdapter(Tool):
    def __init__(self,description:ToolDescription, call:Callable):
        super().__init__(description)
        self.call=call

    def call(self,args:str)->Message:
        return self.call(args)


class ToolSet:
    tools:List[Tool]
    function_tools_dict:dict[str,Tool]
    def __init__(self):
        self.tools=[]
        self.function_tools_dict={}

    def add_tool(self,tool:Tool)->None:
        self.tools.append(tool)
        self.function_tools_dict[tool.description.function.name]=tool

    @property
    def tools_info(self)->List[dict]:
        return [tool.tool_info for tool in self.tools]

    def execute_once(self,tool_call:ChatCompletionMessageToolCall)->Message|routine.Subroutine|None:
        tool=self.function_tools_dict.get(tool_call.function.name)
        if not tool:
            return None
        result=tool.call(json.loads(tool_call.function.arguments)) #TODO:如果AI的回答有问题，应该通过异常处理机制回退处理步骤，因此需要在项目中建立异常体系
        result.tool_call_id=tool_call.id
        return result

    def execute(self,tool_calls:List[ChatCompletionMessageToolCall])->List[Message|routine.Subroutine]:
        results=[]
        for tool_call in tool_calls:
            result=self.execute_once(tool_call)
            results.append(result) if result else None
        return results