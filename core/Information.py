from typing import List

from core.通信层 import Message, MessageRole

class 信息持久化:
    #信息.内容:暂时存在状态 转为 持久存在状态
    pass

class 信息类型检查:
    """
    该类用于在运行时进行动态类型检查，运行前类型检查和运行时普通类型检查由python完成
    该类检查的是信息的语义类型。当AI认为类型正确时，类型就正确
    """
    pass

class 鸭子包装器:
    """
    当类型通过语义检查，但python语法不正确时，用该包装器进行类型转换。这应当是一个AI元
    """
    pass

class 信息:
    """
    除了给定结构的静态类型信息，还可以使用通过在文本内容中加入修饰和标识的方式形成动态类型标识
    如果有动态类型标识结构重复出现，将其自动代码化为静态（类似短期记忆转换为长期记忆）
    """
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

class Key:
    key:str
    def __init__(self,key:str):
        self.key=key

    def __str__(self):
        return self.key

class 信息:
    _content:str
    key:Key
    infor:List[信息]
    meta:List[信息]

    def __init__(self, content:str=None, key:Key=None, infor=None, meta:List[信息]=None):
        self.key=key
        self.content=content
        self.infor=infor
        self.meta=meta

    @property
    def content(self)->str:
        return self._content

    @content.setter
    def content(self,value:str):
        self._content=value

    def __str__(self) -> str:
        parts = []
        # 处理 key
        if self.key is not None:
            parts.append(f"{self.key}:")
        # 处理 content，假设实际属性是 content（根据 __init__）
        if self.content is not None:
            parts.append(f"{self.content},")
        # 处理 infor，递归转换每个元素
        if self.infor:
            infor_str = '\n'.join(str(item) for item in self.infor)
            parts.append(f"此外：\n{infor_str}")
        return f"{', '.join(parts)}"

    def to_string(self)->str:
        return str(self)

    def to_message(self,role:MessageRole)->Message:
        return Message(role,self.content)


