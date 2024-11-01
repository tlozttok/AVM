

from openai import OpenAI 
from abc import ABC, abstractmethod
from typing import List,Tuple

class Message:
    role:str
    type:str
    content:str
    def __init__(self,role:str,type:str,content:str):
        self.role=role
        self.type=type
        self.content=content

    def to_dict(self):
        #暂时忽略 type
        return {"role":self.role,"content":self.content}

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
        return Message("system","text",raw_system_prompt)

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
    def get_next_step(self,response:Message,op_ptr:int)->Message:
        pass

class Engine:
    function_stack:List[Tuple[Routine,int]]
    context_stack:List[Context]
    client:OpenAI


    
    def tick_execution(self):
        func,op_ptr = self.function_stack[-1]
        next_message=func.get_next_step(self.context_stack[-1].messages[-1],op_ptr)
        self.context_stack[-1].messages.append(next_message)
        response = self.client.chat.completions.create(self.context_stack[-1].completion_args)
        ...

    


