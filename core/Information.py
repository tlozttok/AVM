from core.通信层 import Message, MessageRole

class 信息持久化:
    #信息.内容:暂时存在状态 转为 持久存在状态
    raise NotImplementedError

class 信息:
    _content:str

    @property
    def content(self)->str:
        return self._content

    @content.setter
    def content(self,value:str):
        self._content=value

    def to_message(self,role:MessageRole)->Message:
        return Message(role,self.content)

class 角色提示信息(信息):
    角色:str
    行为:str

    def generate_content(self):
        # 角色提示生成器 继承 消息生成器 继承 AI元
        # self._content=角色提示生成器(self.角色,self.行为)
        raise NotImplementedError

    def to_message(self,role:MessageRole) ->Message:
        if self.content:
            return Message(role,self.content)
        else:
            self.content=self.generate_content() #内容:前存在状态 转为 瞬时存在状态 转为 暂时存在状态
            return Message(role,self.content)
