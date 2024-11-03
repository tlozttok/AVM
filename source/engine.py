
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

    def call_subroutine(self,subroutine:Subroutine):
        self.function_stack.append((subroutine,0))
        self.context_stack.append(subroutine.get_init_context())

    def tick_execution(self):
        func,op_ptr = self.function_stack[-1]
        next_routine_message=func.get_next_operate(self.context_stack[-1].messages[-1],op_ptr)
        if next_routine_message is not None:
            self.context_stack[-1].messages.append(next_routine_message)
            response:ChatCompletion = self.client.chat.completions.create(**self.context_stack[-1].completion_args)
            response_messages=[Message.from_completion_choice(choice) for choice in response.choices]
            message_proxy=func.get_next_message_proxy(self.context_stack[-1].messages[-1],op_ptr)
            response_message=message_proxy(response_messages)
            if len(response_message.tool_calls)>0:
                tool_return=self.process_tool_call(response_message)
                if isinstance(tool_return,Message):
                    assistant_response_message=tool_return
                elif isinstance(tool_return,Subroutine):
                    self.call_subroutine(tool_return)
                    return
                else:
                    raise Exception("This exception should never be raised")
            else:
                assistant_response_message=response_message
            self.context_stack[-1].messages.append(assistant_response_message)
            return
        else:
            subroutine=self.function_stack.pop()[0]
            if isinstance(subroutine,Subroutine):
                return_message=subroutine.get_return_message()
                self.context_stack[-1].messages.append(return_message)
            self.context_stack.pop()
            return

    def process_tool_call(self,message:Message)->Message|Subroutine:
        tool_calls=message.tool_calls
        for tool_call in tool_calls:
            ...