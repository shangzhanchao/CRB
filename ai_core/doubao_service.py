"""豆包服务模块

实现豆包API的调用功能，作为百炼API的替代方案。
"""

import logging
import asyncio
from typing import AsyncGenerator, Optional, List, Dict, Any
from openai import OpenAI

logger = logging.getLogger(__name__)

class DoubaoService:
    """豆包服务类"""
    
    def __init__(self, api_key: str = "4b76f73c-key", 
                 base_url: str = "https://ark.cn-beijing.volces.com/api/v3",
                 model: str = "ep-20250604180101-5chxn"):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
    
    def _call_sync(self, prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None) -> str:
        """
        同步调用豆包API，返回完整文本
        """
        try:
            messages = []
            
            # 添加系统提示词
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({"role": "system", "content": "你是一个强大的智能助手，擅长提供准确的信息"})
            
            # 添加历史对话
            if history:
                messages.extend(history)
            
            # 添加用户消息
            messages.append({"role": "user", "content": prompt})
            
            logger.debug(f"豆包API调用参数: model={self.model}, messages={messages}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "text"},
                temperature=0.3,
                stream=False
            )
            
            if response.choices and response.choices[0].message:
                text = response.choices[0].message.content
                logger.debug(f"豆包API返回: {text}")
                return text or ""
            else:
                logger.warning("豆包API返回空内容")
                return ""
                
        except Exception as e:
            logger.error(f"豆包API调用失败: {e}")
            return ""
    
    async def call(self, prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None) -> str:
        """
        异步调用豆包API，返回完整文本
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._call_sync, prompt, system_prompt, history
        )
    
    async def stream(self, prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """
        异步流式调用豆包API
        """
        try:
            messages = []
            
            # 添加系统提示词
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            else:
                messages.append({"role": "system", "content": "你是一个强大的智能助手，擅长提供准确的信息"})
            
            # 添加历史对话
            if history:
                messages.extend(history)
            
            # 添加用户消息
            messages.append({"role": "user", "content": prompt})
            
            logger.debug(f"豆包API流式调用参数: model={self.model}, messages={messages}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "text"},
                temperature=0.3,
                stream=True
            )
            
            for chunk in response:
                chunk_message = chunk.choices[0].delta
                if not chunk_message.content:
                    continue
                
                content = chunk_message.content
                logger.debug(f"豆包流式返回: {content}")
                yield content
                
                await asyncio.sleep(0)
                
        except Exception as e:
            logger.error(f"豆包API流式调用失败: {e}")
            yield ""


# 全局豆包服务实例
_doubao_service = None

def get_doubao_service():
    """获取豆包服务实例"""
    global _doubao_service
    if _doubao_service is None:
        _doubao_service = DoubaoService()
    return _doubao_service


# 兼容性函数
def call_doubao_llm(prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None) -> str:
    """调用豆包LLM（同步）"""
    service = get_doubao_service()
    return service._call_sync(prompt, system_prompt, history)


async def call_doubao_stream(prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None):
    """调用豆包LLM（流式）"""
    service = get_doubao_service()
    return service.stream(prompt, system_prompt, history) 
