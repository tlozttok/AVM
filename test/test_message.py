from source.message import Message
from source.type import Role, MessageType
from test.example import *
import pytest

@pytest.fixture
def a_message():
    return Message(role=Role.USER,message_type=MessageType.TEXT,content="你好")

def test_to_dict(a_message):
    assert a_message.to_dict()=={"role":"user","content":"你好"}


def test_from_completion_choice(chat_response):
    message=Message.from_completion_choice(chat_response.choices[0])
    assert message.role==Role.ASSISTANT,message.content=="你好👋！很高兴见到你，有什么可以帮助你的吗？"
