"""阿里百炼大语言模型服务模块

提供阿里百炼API的调用功能，包括文本生成、对话等功能。
"""

import logging
from http import HTTPStatus
from typing import AsyncGenerator, Optional
import asyncio
from dashscope import Application

logger = logging.getLogger(__name__)

class QwenService:
    def __init__(self, app_id: str, api_key: str):
        self.app_id = app_id
        self.api_key = api_key

    async def call(self, prompt: str, session_id: Optional[str] = None, stream: bool = False) -> str:
        """
        调用百炼API，返回完整文本（非流式）
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._call_sync, prompt, session_id, stream
        )

    def _call_sync(self, prompt: str, session_id: Optional[str], stream: bool) -> str:
        """
        同步调用百炼API，返回完整文本
        """
        try:
            responses = Application.call(
                api_key=self.api_key,
                app_id=self.app_id,
                prompt=prompt,
                session_id=session_id or "default",
                stream=stream,
                incremental_output=True
            )
            text = ""
            for response in responses:
                logger.debug(f"Qwen raw response: {response}")
                if hasattr(response, "status_code") and response.status_code != HTTPStatus.OK:
                    logger.error(f"Qwen error: {getattr(response, 'message', '')}")
                    continue
                if hasattr(response, "output") and hasattr(response.output, "text"):
                    text += response.output.text or ""
            return text
        except Exception as e:
            logger.error(f"Qwen API call failed: {e}")
            return ""

    async def stream(self, prompt: str, session_id: Optional[str] = None) -> AsyncGenerator[str, None]:
        """
        异步流式调用百炼API
        """
        try:
            responses = Application.call(
                api_key=self.api_key,
                app_id=self.app_id,
                prompt=prompt,
                session_id=session_id or "default",
                stream=True,
                incremental_output=True
            )
            for response in responses:
                if hasattr(response, "status_code") and response.status_code != HTTPStatus.OK:
                    logger.error(f"Qwen error: {getattr(response, 'message', '')}")
                    continue
                if hasattr(response, "output") and hasattr(response.output, "text"):
                    yield response.output.text or ""
                await asyncio.sleep(0)
        except Exception as e:
            logger.error(f"Qwen API stream call failed: {e}")
            yield ""

# 单例工厂
_qwen_service = None

def get_qwen_service():
    global _qwen_service
    if _qwen_service is None:
        # 这里可根据实际情况读取配置
        _qwen_service = QwenService(
            app_id="03b39bdb6f0846d7a1b05b0cc37dbbe9",
            api_key="sk-5857a06baafb454fb85288170ee68dc0"
        )
    return _qwen_service


# 测试函数
async def test_qwen():
    """测试百炼API调用"""
    service = get_qwen_service()
    
    print("测试文本生成...")
    text = await service.call("你好，请介绍一下你自己")
    print(f"生成文本: {text}")
    
    print("\n测试流式输出...")
    async for chunk in service.stream("请写一首关于春天的诗"):
        print(chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(test_qwen()) 