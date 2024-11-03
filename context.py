
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal

from message import Message
from tools import ToolSet
from type import MessageType, Role


class Context:
    system_prompt:str
    information:List[str]
    messages:List[Message]
    tools:ToolSet
    settings:dict #以后提取成类
    def __init__(self):
        self.system_prompt = ""
        self.information = []
        self.messages = []

    @property
    def raw_system_prompt(self):
        raw_system_prompt=self.system_prompt
        for info in self.information:
            raw_system_prompt+=f"\n{info}"
        return Message(Role.SYSTEM,MessageType.TEXT,raw_system_prompt)

    @property
    def raw_messages(self):
        return [msg.to_dict() for msg in [self.raw_system_prompt]+self.messages]

    @property
    def raw_tools_info(self):
        return self.tools.tools_info

    @property
    def completion_args(self)->dict:
        return {"messages":self.raw_messages,"tools":self.tools.tools_info,**self.settings}