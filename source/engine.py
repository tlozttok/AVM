
from enum import Enum
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion,Choice
from openai.types.chat.chat_completion_message import ChatCompletionMessageToolCall
from abc import ABC, abstractmethod
from typing import List,Tuple,Callable,Literal

from .routine import Subroutine
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
        next_routine_message=func.get_next_operate(self.context_stack[-1].messages[-1],op_ptr)
        if next_routine_message is not None:
            self.context_stack[-1].messages.append(next_routine_message)
            response:ChatCompletion = self.client.chat.completions.create(**self.context_stack[-1].completion_args)
            response_messages=[Message.from_completion_choice(choice) for choice in response.choices]
            message_proxy=func.get_next_message_proxy(self.context_stack[-1].messages[-1],op_ptr)
            response_message=message_proxy(response_messages)
            if response_message.role == Role.TOOL:
                assistant_response_message=self.process_tool_call(response_message)
            else:
                assistant_response_message=response_message
            self.context_stack[-1].messages.append(assistant_response_message)
        else:
            subroutine=self.function_stack.pop()[0]
            if isinstance(subroutine,Subroutine):
                return_message=subroutine.get_return_message()
                self.context_stack[-1].messages.append(return_message)
            self.context_stack.pop()

    def process_tool_call(self,message:Message)->Message:
        ...