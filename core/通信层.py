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

    def to_dict(self):
        return {"role":self.role.value,"content":self.content}

client=openai.OpenAI(base_url="https://api.deepseek.com",api_key="sk-3edde867f5c64b77b69fe743633aa717")
client=openai.OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",api_key="sk-bfe066912d9e451ebe7b530ca15a67b8")

class Setting:
    model:str
    temperature:float
    max_tokens:int
    top_p:float
    frequency_penalty:float
    presence_penalty:float
    def __init__(self,model:str="deepseek-chat",temperature:float=0.5,max_tokens:int=4096,top_p:float=None,frequency_penalty:float=None,presence_penalty:float=None):
        self.model=model
        self.temperature=temperature
        self.max_tokens=max_tokens
        self.top_p=top_p
        self.frequency_penalty=frequency_penalty
        self.presence_penalty=presence_penalty

class Context:
    messages: List[Message]
    setting: Setting
    client:openai.OpenAI
    def __init__(self,messages:List[Message],setting:Setting):
        self.messages=messages
        self.setting=setting
        self.client=client

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
        message=[self.set_infor_prompt(infor_prompt)]+self.messages[1:]
        message=[x.to_dict() for x in message]
        response = self.client.chat.completions.create(
            model=self.setting.model,
            messages=message,
            temperature=self.setting.temperature,
            max_tokens=self.setting.max_tokens,
            top_p=self.setting.top_p,
            frequency_penalty=self.setting.frequency_penalty,
            presence_penalty=self.setting.presence_penalty,
        )
        self.messages.append(Message(MessageRole.ASSISTANT,response.choices[0].message.content))
        return response.choices[0].message.content

    def clear(self):
        self.messages=self.messages[0:1]