from typing import Any

from .message import Message
from abc import ABC, abstractmethod

class Process:

    @abstractmethod
    def start(self,message:Message,*args,**kwargs):
        pass

    @abstractmethod
    def is_end(self)->bool:
        pass

    @abstractmethod
    def get_result(self)->Message|Any:
        pass