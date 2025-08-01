import asyncio

from openai import OpenAI
# doubao在线调用
async def call_dou_bao_stream(question, history_parm,agent):
    # test_function_call(question)
    if agent is None or agent == "":
        agent="你是一个强大的智能助手，擅长提供准确的信息"

    client = OpenAI(
        # api_key="6ce4cff6-c3f",
        api_key = "key",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "WebSearchPlugin",
                "description": "当需要搜索互联网内容时，调用本插件",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "需要搜索的内容",
                        },
                    },
                    "required": ["keywords"],
                },
            },
        },
    ]

    response = client.chat.completions.create(
        model="ep-20250604180101-5chxn",
        messages=[
                 {'role': 'system', 'content': agent}
             ] + history_parm + [
                 {'role': 'user', 'content': question},
                 # {'role': 'tool', 'content': None, 'tool_calls': [
                 #    {
                 #        'name': 'WebSearchPlugin',
                 #        'arguments': {
                 #            'keywords': question,
                 #        }
                 #    }
                 # ]}
             ],
        response_format={"type": "text"},
        temperature=0.3,
        # tools=tools,
        stream=True,
    )
    full_content = ""
    for idx, chunk in enumerate(response):
        chunk_message = chunk.choices[0].delta
        if not chunk_message.content:
            continue
        # print("===测试 豆包 chunk=", chunk)
        yield chunk



# 运行异步 main 函数
if __name__ == "__main__":
    async def main():
        async for response in call_dou_bao_stream("介绍下陈丹青", [],""):
            print(response)

# 使用 asyncio.run() 来运行 main 函数
    asyncio.run(main())


