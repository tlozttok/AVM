from typing import List

from core.通信层 import Message, MessageRole

class 信息持久化:
    #信息.内容:暂时存在状态 转为 持久存在状态
    raise NotImplementedError

class 信息类型检查:
    """
    该类用于在运行时进行动态类型检查，运行前类型检查和运行时普通类型检查由python完成
    该类检查的是信息的语义类型。当AI认为类型正确时，类型就正确
    """
    raise NotImplementedError

class 鸭子包装器:
    """
    当类型通过语义检查，但python语法不正确时，用该包装器进行类型转换。这应当是一个AI元
    """

class 信息:
    pass

class 信息类型信息类型:
    pass

class 信息类型(信息):
    """
    信息类型,描述信息的特征,帮助组织信息层级结构
    信息类型同样是模糊性的,使用AI进行判断
    信息有至多一个主类型,多个副类型
    主类型表示严格的从属关系,副类型表示与接口相似的特征
    """
    描述:str
    def __init__(self,描述:str):
        self.描述=描述
        self.type.append(信息类型信息类型)


    def to_message(self,role:MessageRole)->Message:
        return Message(role,type(self).__name__+self.描述) #返回上下文无关的描述.信息类名+描述


class 信息类型信息类型(信息类型):
    描述:str="描述一个信息类型"

class 顶信息类型:
    描述:str = ""

class 底信息类型:
    描述:str = None

class 信息:
    _content:str
    type:List[信息类型] = [顶信息类型]

    @property
    def content(self)->str:
        return self._content

    @content.setter
    def content(self,value:str):
        self._content=value

    def to_message(self,role:MessageRole)->Message:
        return Message(role,self.content)


