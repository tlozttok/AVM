import asyncio
from typing import List, Tuple, Callable

from core.AI元 import AI元
from core.Information import 信息


class 信息包:
    """
    信息+描述信息的元信息
    """

class 信息管道:
    """
    作为AI元之间的连接，监测AI元的信息发送和接受，通过不断检查，进行信息发送的调控
    """
    下游AI元:List[Tuple['AI元',Callable[[信息],bool]]]

    def __init__(self):
        self.下游AI元=[]

    def add_downstream(self,AI元:AI元,filter:Callable[[信息],bool]):
        self.下游AI元.append((AI元,filter))

    async def put(self, 信息:信息):
        for AI元,filter in self.下游AI元:
            if filter(信息):
                await AI元.receive(信息)









