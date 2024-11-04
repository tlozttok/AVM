
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
    __last_layer_subroutine_id:List[int]=[] #看成上一层的最后一个函数与当前层的函数的距离
    client:OpenAI

    def new_subroutine_layer(self):
        self.__last_layer_subroutine_id.append(0)
    def call_subroutine(self,subroutine:Subroutine):
        self.function_stack.append((subroutine,0))
        self.context_stack.append(subroutine.get_init_context())
        self.__last_layer_subroutine_id[-1]+=1


    def tick_execution(self):
        func,op_ptr = self.function_stack[-1]
        next_routine_message=func.get_next_operate(self.context_stack[-1].messages[-1],op_ptr)
        message_proxy = func.get_next_message_proxy(self.context_stack[-1].messages[-1], op_ptr)
        if next_routine_message is not None:
            return self._process_next_routine_message(message_proxy, next_routine_message)
        else:
            return self._pop_subroutine()

    def _pop_subroutine(self):
        subroutine = self.function_stack.pop()[0]
        if isinstance(subroutine, Subroutine):
            self._add_subroutine_return_message_to_parent(subroutine)
        return

    def _add_subroutine_return_message_to_parent(self, subroutine:Subroutine):
        return_message = subroutine.get_return_message(self.context_stack.pop())
        self._parent_routine.messages.append(return_message)

    @property
    def _parent_routine(self):
        return self.context_stack[-self.__last_layer_subroutine_id[-1]]

    def _process_next_routine_message(self, message_proxy:Callable[[List[Message]],Message], next_routine_message:Message):
        self.context_stack[-1].messages.append(next_routine_message)
        response_message = self._get_model_response_message(message_proxy)
        if len(response_message.tool_calls) > 0:
            should_break = self.process_tool_call(response_message)
            if should_break:
                return
        else:
            assistant_response_message = response_message
            self.context_stack[-1].messages.append(assistant_response_message)
        return

    def _get_model_response_message(self, message_proxy:Callable[[List[Message]],Message]):
        response: ChatCompletion = self.client.chat.completions.create(**self.context_stack[-1].completion_args)
        response_messages = [Message.from_completion_choice(choice) for choice in response.choices]
        response_message = message_proxy(response_messages)
        return response_message

    def process_tool_call(self,message:Message)->bool:
        tool_calls=message.tool_calls
        results=self.context_stack[-1].tools.execute(tool_calls)
        tool_messages=[m for m in results if isinstance(m,Message)]
        subroutines=[s for s in results if isinstance(s,Subroutine)]
        if len(tool_messages)>0:
            for tool_messages in tool_messages:
                self.context_stack[-1].messages.append(tool_messages)
        if len(subroutines)>0:
            for subroutine in subroutines:
                self.call_subroutine(subroutine)
            result=True
        else:
            result=False
        return result