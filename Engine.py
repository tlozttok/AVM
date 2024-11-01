
from abc import ABC, abstractmethod
from typing import List,Tuple

class Message:
    role:str
    type:str
    content:str

class Context:
    system_prompt:str
    information:List[str]
    messages:List[Message]
    def __init__(self):
        self.system_prompt = ""
        self.information = []
        self.messages = []

class Routine(ABC):
    
    @abstractmethod
    def get_init_context(self)->Context:
        pass

    @abstractmethod
    def get_next_step(self,response:Message)->Message:
        pass

class Engine:
    context:Context
    function_stack:List[Tuple[Routine,int]]
    context_stack:List


