from typing import List

from core.Information import 信息
from core.通信层 import Context

class 程序提示Builder:
    raise NotImplementedError()


class AI元:
    背景知识:List[信息]

    程序提示:List[信息]

    _对话内容:Context

    对话结果:List[信息]


    def 增加背景知识(self,新信息:信息):
        self.背景知识.append(新信息)

    def 设置程序提示(self,程序提示:List[信息]):
        self.程序提示=程序提示

    def 
