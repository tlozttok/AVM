
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal


class FunctionParameterDiscription:
    name:str
    description:str
    type:str
    required:bool
    enum:List[str]


class FunctionDiscription:
    name:str
    description:str
    parameters:List[FunctionParameterDiscription]

    def to_dict(self)->dict:
        ...