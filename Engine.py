
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal

from .context import Context
from .message import Message
from .routine import Routine
from .type import Role


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