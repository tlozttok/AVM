from abc import abstractmethod
from typing import List

from core.Information import 信息
from core.通信层 import Context, Setting
from 信息.角色提示信息 import 角色提示信息

class 系统元:
    """
    执行程序操作的单元
    """

class 程序提示Builder:
    raise NotImplementedError()


class AI元:
    """
    信息的储存本质上是对内容的结构化，不可避免会造成信息丢失和扭曲。对于例子少、不详细、有歧义的表述，如果ai在不同采样下回答出现各有各理的情况，那么应该将生成表述的过程进行细化
    """

    背景知识:List[信息]

    程序提示:List[信息]

    _对话内容:Context

    对话结果:List[信息]

    def __init__(self):
        self._对话内容=Context(messages=[],setting=Setting())
        self.背景知识=[]
        self.程序提示=[]
        self.对话结果=[]

    @property
    def 对话轮数(self):
        return self._对话内容.统计AI消息数()


    def 增加背景知识(self,新信息:信息):
        self.背景知识.append(新信息)

    def 设置程序提示(self,程序提示:List[信息]):
        self.程序提示=程序提示

    @abstractmethod
    def _get_system_prompt(self):
        raise NotImplementedError()

    @abstractmethod
    def _get_user_prompt(self,对话轮数):
        raise NotImplementedError()

    def _user_prompt_provider(self):
        对话轮数=self.对话轮数
        instruction=self._get_user_prompt(对话轮数)
        while instruction:
            yield instruction
            instruction=self._user_prompt_provider()
            对话轮数+=1

    @abstractmethod
    def extract_result(self):
        raise NotImplementedError()

    def process(self):
        system_prompt=self._get_system_prompt()
        self._对话内容.set_system_prompt(system_prompt)
        for instruction in self._user_prompt_provider():
            self._对话内容.append_user_prompt(instruction)
            self._对话内容.send()


class 角色化AI元(AI元):
    角色信息:角色提示信息



