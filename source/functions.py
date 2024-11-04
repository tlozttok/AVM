
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal


class FunctionParameterDescription:
    name:str
    description:str
    type:str
    required:bool
    enum:List[str]

    def to_dict(self)->dict:
        result= {"description": self.description, "type": self.type}
        if self.enum:
            result["enum"]=self.enum
        return result


class FunctionDescription:
    name:str
    description:str
    parameters:List[FunctionParameterDescription]

    def to_dict(self)->dict:
        result= {"name": self.name, "description": self.description,
                 "parameters": {"type": "object", "properties": {}, "required": []}}
        for param in self.parameters:
            result["parameters"]["properties"][param.name]=param.to_dict()
            if param.required:
                result["parameters"]["required"].append(param.name)
        return result