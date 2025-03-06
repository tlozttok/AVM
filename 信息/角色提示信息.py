from core.AI元 import 角色提示生成AI元, 全局AI元池
from core.Information import 信息, 信息类型
from core.通信层 import Message, MessageRole



class 角色信息类型(信息类型):
    描述:str = "至少包含角色名"

class 角色信息(信息):
    角色:str

class 应然行为信息(信息):
    行为:str

class 角色提示信息(信息):
    角色:角色信息
    行为:应然行为信息

    def generate_content(self):
        return 全局AI元池.get_by_name("初始角色提示生成AI")[0].增加背景知识(self).process()[0].to_message(MessageRole.SYSTEM)

    def to_message(self,role:MessageRole) ->Message:
        if self.content:
            return Message(role,self.content)
        else:
            self.content=self.generate_content() #内容:前存在状态 转为 瞬时存在状态 转为 暂时存在状态
            return Message(role,self.content)
