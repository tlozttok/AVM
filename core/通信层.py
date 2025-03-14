from enum import Enum
from typing import List

import openai

class MessageRole(Enum):
    ASSISTANT="assistant"
    SYSTEM="system"
    TOOL="tool"
    USER="user"
    INFOR="infor"

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

    def 统计用户消息数(self):
        return len(list(filter(lambda x:x.role==MessageRole.USER,self.messages)))

    def set_system_prompt(self,prompt:str):
        if len(self.messages)==0:
            self.messages.append(Message(MessageRole.SYSTEM,prompt))
        else:
            self.messages[0]=Message(MessageRole.SYSTEM,prompt)

    def set_infor_prompt(self,prompt:List[str]):
        system_prompt=self.messages[0]
        return Message(MessageRole.SYSTEM,system_prompt.content+"\n".join(prompt))


    def append_user_prompt(self,prompt:str):
        self.messages.append(Message(MessageRole.USER,prompt))

    def append_assistant_prompt(self,prompt:str):
        self.messages.append(Message(MessageRole.ASSISTANT,prompt))

    def add_message(self,message:Message):
        self.messages.append(message)

    def send(self,infor_prompt:List[str])->str:
        # 发送请求
        raise NotImplementedError

    def clear(self):
        self.messages=self.messages[0:1]