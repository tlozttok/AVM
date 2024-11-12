import json

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import pickle
import pytest
from scipy.special import result

from source.functions import FunctionDescription, FunctionParameterDescription
from source.message import Message
from source.tools import ToolSet, Tool, ToolAdapter, ToolDescription
from source.type import Role, MessageType


@pytest.fixture
def chat_response():
    with open("example_data/example_response_chat.pickle", "rb") as f:
        response=pickle.load(f)
    return response

@pytest.fixture
def chat_response_message_dict():
    return {'role': 'assistant', 'content': '你好👋！很高兴见到你，有什么可以帮助你的吗？'}

@pytest.fixture
def tool_eval():
    eval_tool=ToolSet()
    function_parameters=[
        FunctionParameterDescription("code","要计算的python代码，会使用eval()来执行",required=True,type="string")
    ]
    function_description=FunctionDescription("代码执行","执行python代码,用于进行数值计算",function_parameters)
    tool_description=ToolDescription(function_description)
    def eval_code(code:str)->Message:
        result={"result":eval(code)}
        return Message(Role.TOOL,MessageType.TOOL_CALL,content=json.dumps(result))
    the_tool=ToolAdapter(tool_description,eval_code)
    eval_tool.add_tool(the_tool)
    return eval_tool


if __name__=="__main__":

    ...