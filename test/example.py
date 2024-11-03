from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import pickle
import pytest

@pytest.fixture
def chat_response():
    with open("example_data/example_response_chat.pickle", "rb") as f:
        response=pickle.load(f)
    return response

@pytest.fixture
def chat_response_message_dict():
    return {'role': 'assistant', 'content': '你好👋！很高兴见到你，有什么可以帮助你的吗？'}


if __name__=="__main__":

    ...