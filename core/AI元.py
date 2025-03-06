from abc import abstractmethod
from typing import List

from core.Information import 信息
from core.通信层 import Context, Setting, MessageRole, Message
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
    name:str

    背景知识:List[信息]

    程序提示:List[信息]

    _对话内容:Context

    对话结果:List[信息]

    def __init__(self):
        self._对话内容=Context(messages=[],setting=Setting())
        self.背景知识=[]
        self.程序提示=[]
        self.对话结果=[]
        self.name=""

    @property
    def 对话轮数(self):
        return self._对话内容.统计AI消息数()


    def 增加背景知识(self,新信息:信息):
        self.背景知识.append(新信息)
        return self

    def 设置程序提示(self,程序提示:List[信息]):
        self.程序提示=程序提示
        return self

    @abstractmethod
    def _get_system_prompt(self):
        raise NotImplementedError()


    def _get_user_prompt(self,对话轮数):
        return self.程序提示[对话轮数].to_message(MessageRole.USER)

    def _user_prompt_provider(self):
        对话轮数=self.对话轮数
        instruction=self._get_user_prompt(对话轮数)
        while instruction:
            yield instruction
            instruction=self._get_user_prompt(对话轮数)
            对话轮数+=1

    @abstractmethod
    def extract_result(self):
        raise NotImplementedError()

    def process(self):
        system_prompt=self._get_system_prompt()
        self._对话内容.add_message(system_prompt)
        for instruction in self._user_prompt_provider():
            self._对话内容.add_message(instruction)
            self._对话内容.send()
        self.extract_result()
        return self.对话结果


class 角色提示生成AI元(AI元):
    角色信息:角色提示信息

    def _get_system_prompt(self):
        return self.角色信息.to_message(MessageRole.SYSTEM)

初始角色提示生成AI=角色提示生成AI元()#读取AI元()
初始角色提示生成AI.name="初始角色提示生成AI"


class AI元池:
    AI元s:List[AI元]
    def __init__(self):
        self.AI元s=[]

    def addAI元(self,AI:AI元):
        self.AI元s.append(AI)
        return self

    def get_by_class(self,class_name):
        result=[]
        for AI in self.AI元s:
            if isinstance(AI,class_name):
                result.append(AI)
        return result

    def get_by_name(self,name):
        result=[]
        for AI in self.AI元s:
            if AI.name==name:
                result.append(AI)
        return result

    def __getitem__(self, item):
        return self.AI元s[item]

全局AI元池=AI元池()
全局AI元池.addAI元(初始角色提示生成AI)




