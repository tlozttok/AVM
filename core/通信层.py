from enum import Enum
from typing import List

import openai

class MessageRole(Enum):
    ASSISTANT="assistant"
    SYSTEM="system"
    TOOL="tool"
    USER="user"

class Message:
    role:MessageRole
    content:str
    def __init__(self,role:MessageRole,content:str):
        self.role=role
        self.content=content

class Setting:
    model:str
    temperature:float
    max_tokens:int
    top_p:float
    frequency_penalty:float
    presence_penalty:float

class Context:
    messages: List[Message]
    setting: Setting
    def __init__(self,messages:List[Message],setting:Setting):
        self.messages=messages
        self.setting=setting

    def 统计AI消息数(self):
        return len(list(filter(lambda x:x.role==MessageRole.ASSISTANT,self.messages)))

    def set_system_prompt(self,prompt:str):
        self.messages.insert(0,Message(MessageRole.SYSTEM,prompt))

    def append_user_prompt(self,prompt:str):
        self.messages.append(Message(MessageRole.USER,prompt))

    def append_assistant_prompt(self,prompt:str):
        self.messages.append(Message(MessageRole.ASSISTANT,prompt))

    def send(self):
        # 发送请求
        raise NotImplementedError