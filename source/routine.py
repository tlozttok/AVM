
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal

from .type import Role, MessageType
from .context import Context
from .message import Message
from .functions import FunctionParameterDescription


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



class Subroutine(Routine,ABC):
    call_id:str
    params:FunctionParameterDescription

    @abstractmethod
    def get_return_message(self)->None|Message:
        """
        对于一个子例程，结束后应该返回一个tool_call消息，做为调用它的例程期望的工具返回值
        :return:tool_call消息
        """
        pass

class TestCommonChatRoutine(Routine):


    def get_init_context(self) ->Context:
        return Context("你是一个英语翻译，用户每次会给出一个英语单词，将其翻译成中文")

    def get_next_operate(self,response:Message,op_ptr:int) ->Message:
        print(response.content)
        user_input=input()
        return Message(Role.USER,MessageType.TEXT,content=user_input)

    def get_next_message_proxy(self,response:Message,op_ptr:int) ->Callable[[List[Message]],Message]:
        def proxy(messages:List[Message])->Message:
            return messages[0]
        return proxy