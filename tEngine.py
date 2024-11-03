

from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal

class Role(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"
    TOOL="tool"

class MessageType(Enum):
    TEXT="text"
    IMAGE="image"
    TOOL_CALL="tool_call"

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

class ToolDiscription:
    type:Literal["function"]
    funcion:FunctionDiscription
    
    def to_dict(self)->dict:
        ...
    

class Tool(ABC):
    description:ToolDiscription
    def __init__(self,description:ToolDiscription):
        self.description=description

    @property
    def tool_info(self)->dict:
        return self.description.to_dict()

    @abstractmethod
    def call(self,args:dict)->str:
        pass

class ToolSet:
    tools:List[Tool]
    def __init__(self):
        self.tools=[]

    @property
    def tools_info(self)->List[dict]:
        return [tool.tool_info for tool in self.tools]


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
        if next_message.role == Role.TOOL:
            self.process_tool_call(next_message)
            return
        self.context_stack[-1].messages.append(next_message)
        
    def process_tool_call(self,message:Message):
        ...
        
        

    


