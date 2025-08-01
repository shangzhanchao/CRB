from http import HTTPStatus
from datetime import datetime
import asyncio
from dashscope import Application


async def call_channel_qwen(question, agent_app_id, agent_api_key,session_id):
    responses = Application.call(
        api_key=agent_api_key,
        app_id=agent_app_id,
        prompt=question,
        session_id=session_id,
        stream=True,  # 流式输出
        incremental_output=True)  # 增量输出
    for response in responses:
        if response.status_code != HTTPStatus.OK:
            print(f'request_id={response.request_id}')
            print(f'code={response.status_code}')
            print(f'message={response.message}')
        else:
            yield response

        await asyncio.sleep(0)  # 让出控制权，避免阻塞事件循环



# 运行异步 main 函数
if __name__ == "__main__":
    async def main():
        async for response in call_channel_qwen("换绿本","appid","sk-key","123456"):
            print(datetime.now(), f"==返回内容: {response.output.text}")

# 使用 asyncio.run() 来运行 main 函数
    asyncio.run(main())
