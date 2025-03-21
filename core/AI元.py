import asyncio
from abc import abstractmethod
from typing import List

from core.Information import 信息, Key
from core.信息管道 import 信息管道
from core.通信层 import Context, Setting, MessageRole, Message
import json

class 系统元:
    """
    执行程序操作的单元
    """

class 程序提示Builder:
    pass


class AI元:
    """
    信息的储存本质上是对内容的结构化，不可避免会造成信息丢失和扭曲。对于例子少、不详细、有歧义的表述，如果ai在不同采样下回答出现各有各理的情况，那么应该将生成表述的过程进行细化
    """
    name:str

    _知识源:asyncio.Queue[信息]

    背景知识:List[信息]

    程序提示:asyncio.Queue[信息]

    _对话内容:Context

    输出管道:List[信息管道|asyncio.Queue[信息]]

    输出接口:asyncio.Queue[信息]

    def __init__(self,system_prompt:str):
        self._对话内容=Context(messages=[],setting=Setting(model="qwen2.5-14b-instruct-1m"))
        self.背景知识=[]
        self.name=""
        self.system_prompt=system_prompt
        self._对话内容.set_system_prompt(system_prompt)
        self._知识源=asyncio.Queue()
        self.程序提示=asyncio.Queue()
        self.输出管道=[]
        self.输出接口=asyncio.Queue()
        self.输出管道.append(self.输出接口)
        self.输入接口=asyncio.Queue()


    async def call(self, 信息:信息):
        await self.程序提示.put(信息)
        result=await self.输出接口.get()
        return result


    async def receive(self,信息:信息):
        await self._知识源.put(信息)

    @property
    def 对话轮数(self):
        return self._对话内容.统计AI消息数()

    @property
    def 半对话轮数(self):
        return self._对话内容.统计用户消息数()

    async def 添加程序提示(self,程序提示:信息):
        await self.程序提示.put(程序提示)

    @abstractmethod
    def filter(self, 信息: 信息)->bool:
        raise NotImplementedError()

    @abstractmethod
    def extract_result(self):
        raise NotImplementedError()

    @abstractmethod
    def ready_for_process(self):
        raise NotImplementedError()

    @abstractmethod
    def ready_for_output(self, result:str):
        raise NotImplementedError()

    async def change(self):
        while True:
            change1=asyncio.create_task(self._知识源.get())
            change2=asyncio.create_task(self.程序提示.get())
            done, pending = await asyncio.wait(
                [change1, change2],
                return_when=asyncio.FIRST_COMPLETED
            )

            if change1.done():
                self.背景知识.append(change1.result())

            if change2.done():
                self._对话内容.append_user_prompt(change2.result().to_string())

            for task in pending:
                task.cancel()

            if self.ready_for_process():
                await self.process()

    async def run(self):
        asyncio.create_task(self.change())

    async def process(self):
        result=self._对话内容.send([infor.to_string() for infor in self.背景知识])
        if self.ready_for_output(result):
            result=self.extract_result()
            self._对话内容.clear()
            for output in self.输出管道:
                await output.put(result)

class 角色提示生成AI(AI元):

    def ready_for_output(self, result: str):
        return self.对话轮数>0

    def ready_for_process(self):
        return self.半对话轮数>0

    def extract_result(self):
        result=self._对话内容.messages[-1].content
        result=result.replace("json","")
        result=result.replace("```","")
        result=json.loads(result)
        result_infor=[]
        for key,value in result.items():
            infor=信息(value,Key(key))
            result_infor.append(infor)
        return 信息(infor=result_infor,meta=[信息(content="角色提示词")])




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






