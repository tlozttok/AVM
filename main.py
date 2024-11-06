from source.engine import Engine
from source.routine import TestCommonChatRoutine
from openai import OpenAI

client = OpenAI(base_url="",api_key="")

engine = Engine()
engine.start_top_routine(TestCommonChatRoutine())
while True:
    engine.tick_execution()