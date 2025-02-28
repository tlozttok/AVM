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

