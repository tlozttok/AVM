from asyncio import Queue
import asyncio

from core.AI元 import 角色提示生成AI
from core.Information import 信息, Key
from core.信息管道 import 信息管道

ai1=角色提示生成AI("你是一个专业的提示词工程师，你的任务是根据用户提供的具体要求，生成符合要求的系统提示词并以JSON格式输出。请严格按照以下结构执行：\n\n{\n  \"role\": \"目标系统AI的角色定义\",\n  \"task\": \"需要完成的具体任务说明\",\n  \"output_format\": \"输出格式要求\",\n  \"constraints\": [\"限制条件列表\"],\n  \"example\": \"输出格式示例（可选）\"\n}\n\n要求：\n1. 必须包含所有指定字段\n2. 角色定义需明确身份特征\n3. 任务说明要具体可操作\n4. 输出格式必须是严格JSON\n5. 约束条件用数组形式\n6. 示例需与最终输出格式一致\n7. 使用用户指定的语言（默认中文）\n8. 不添加任何额外解释或说明")


infor=信息(key=Key("角色功能"),content="提示词工程师")

async def main():
    await ai1.run()
    result=await ai1.call(infor)
    print(result.to_string())
    print("完成")


asyncio.run(main())