
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal

from type import MessageType, Role


class Message:
    role:Role
    type:MessageType
    content:str
    tool_call:ChatCompletionMessageToolCall
    def __init__(self,role:Role,type:MessageType,*,content:str=None,tool_call:ChatCompletionMessageToolCall=None):
        self.role=role
        self.type=type
        self.content=content
        self.tool_call=tool_call

    def to_dict(self):
        #暂时忽略 type
        return {"role":self.role.value,"content":self.content}

    @staticmethod
    def from_completion_choice(choice:Choice):
        if choice.message.tool_calls is not None:
            return Message(Role(choice.message.role),MessageType.TOOL_CALL,tool_call=choice.message.tool_calls)
        if choice.message.content is not None:
            return Message(Role(choice.message.role),MessageType.TEXT,content=choice.message.content)