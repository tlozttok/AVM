

from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable

class Role(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"

class MessageType(Enum):
    TEXT="text"
    IMAGE="image"

class Message:
    role:Role
    type:MessageType
    content:str
    def __init__(self,role:Role,type:MessageType,content:str):
        self.role=role
        self.type=type
        self.content=content

    def to_dict(self):
        #暂时忽略 type
        return {"role":self.role.value,"content":self.content}
    
    @staticmethod
    def from_completion_choice(choice:Choice):
        return Message(MessageType(choice.message.role),MessageType.TEXT,choice.message.content)

class Context:
    system_prompt:str
    information:List[str]
    messages:List[Message]
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
    def completion_args(self)->dict:
        return {"messages":self.raw_messages,**self.settings}

class Routine(ABC):
    
    @abstractmethod
    def get_init_context(self)->Context:
        pass

    @abstractmethod
    def get_next_operate(self,response:Message,op_ptr:int)->Message:
        pass

    @abstractmethod
    def get_next_message_proxy(self,response:Message,op_ptr:int)->Callable[[List[Message]],Message]:
        pass

class Engine:
    function_stack:List[Tuple[Routine,int]]
    context_stack:List[Context]
    client:OpenAI


    
    def tick_execution(self):
        func,op_ptr = self.function_stack[-1]
        next_message=func.get_next_operate(self.context_stack[-1].messages[-1],op_ptr)
        self.context_stack[-1].messages.append(next_message)
        response:ChatCompletion = self.client.chat.completions.create(self.context_stack[-1].completion_args)
        response_messages=[Message.from_completion_choice(choice) for choice in response.choices]
        message_proxy=func.get_next_message_proxy(next_message,op_ptr)
        next_message=message_proxy(response_messages)
        self.context_stack[-1].messages.append(next_message)
        
    def process_tool_call(self):
        ...
        
        

    


