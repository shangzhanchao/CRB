"""豆包服务模块

实现豆包API的调用功能，提供统一的模型调用接口。
"""

import asyncio
import logging
import re
from typing import AsyncGenerator, Optional, List, Dict, Any
from openai import OpenAI
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class DoubaoService:
    """豆包服务类"""
    
    def __init__(self, api_key: str = "4b76f73c-", 
                 base_url: str = "https://ark.cn-beijing.volces.com/api/v3",
                 model: str = "ep-202506xn"):
        # 参数校验
        self._validate_parameters(api_key, base_url, model)
        
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        
        logger.info("DoubaoService initialization completed")
        logger.info("API Key: %s", api_key[:8] + "..." if len(api_key) > 8 else api_key)
        logger.info("Base URL: %s", base_url)
        logger.info("Model: %s", model)
        
        print("DoubaoService initialization completed")
        print("API Key:", api_key[:8] + "..." if len(api_key) > 8 else api_key)
        print("Base URL:", base_url)
        print("Model:", model)
    
    def _validate_parameters(self, api_key: str, base_url: str, model: str):
        """验证初始化参数"""
        # 验证API Key
        if not api_key or not api_key.strip():
            raise ValueError("API Key cannot be empty")
        
        # 验证API Key格式（豆包API Key通常是UUID格式）
        api_key_pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
        if not re.match(api_key_pattern, api_key):
            raise ValueError("API Key format is invalid (expected UUID format)")
        
        # 验证Base URL
        if not base_url or not base_url.strip():
            raise ValueError("Base URL cannot be empty")
        
        try:
            parsed_url = urlparse(base_url)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid URL format")
            
            # 验证协议必须是http或https
            if parsed_url.scheme not in ['http', 'https']:
                raise ValueError("Base URL must use HTTP or HTTPS protocol")
        except Exception as e:
            raise ValueError(f"Invalid Base URL: {e}")
        
        # 验证Model
        if not model or not model.strip():
            raise ValueError("Model name cannot be empty")
        
        # 验证Model格式（豆包模型通常是ep-开头的格式）
        if not model.startswith("ep-"):
            raise ValueError("Model name format is invalid (expected 'ep-' prefix)")
        
        logger.info("Parameter validation passed")
        print("Parameter validation passed")

    def _call_sync(self, prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None) -> str:
        """
        同步调用豆包API，返回完整文本
        
        Parameters
        ----------
        prompt : str
            用户输入的提示词
        system_prompt : str, optional
            系统提示词
        history : List[Dict[str, Any]], optional
            历史对话记录
            
        Returns
        -------
        str
            模型返回的文本内容
        """
        import time
        start_time = time.time()
        
        logger.info("DoubaoService _call_sync started")
        logger.info("Prompt length: %d characters", len(prompt))
        logger.info("System prompt provided: %s", system_prompt is not None and len(system_prompt) > 0)
        logger.info("History provided: %s", history is not None and len(history) > 0)
        
        print("DoubaoService _call_sync started")
        print("Prompt length:", len(prompt), "characters")
        print("System prompt provided:", system_prompt is not None and len(system_prompt) > 0)
        print("History provided:", history is not None and len(history) > 0)
        
        # 打印完整的prompt和system_prompt参数内容
        print("=== PROMPT CONTENT ===")
        print(prompt)
        print("=== END PROMPT ===")
        
        if system_prompt:
            print("=== SYSTEM PROMPT CONTENT ===")
            print(system_prompt)
            print("=== END SYSTEM PROMPT ===")
        else:
            print("=== SYSTEM PROMPT CONTENT ===")
            print("None or empty")
            print("=== END SYSTEM PROMPT ===")
        
        try:
            messages = []
            
            # 添加系统提示词 - 修复：只有当system_prompt不为None且不为空字符串时才添加
            if system_prompt and system_prompt.strip():
                messages.append({"role": "system", "content": system_prompt})
                logger.info("System prompt added to messages")
                print("System prompt added to messages")
            elif system_prompt is None:  # 只有明确为None时才使用默认提示词
                default_system = """你是一个强大的智能助手，擅长提供准确的信息。

### 输出格式规范
请严格按照以下JSON格式输出回复：
{
    "text": "你的文本回复内容",
    "emotion": "当前情绪状态",
    "action": "相关动作",
    "expression": "表情描述"
}"""
                messages.append({"role": "system", "content": default_system})
                logger.info("Default system prompt added to messages")
                print("Default system prompt added to messages")
            
            # 添加历史对话
            if history and isinstance(history, list):
                # 验证历史记录格式
                valid_history = []
                for msg in history:
                    if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                        if msg['role'] in ['user', 'assistant', 'system']:
                            # 确保content不为空
                            if msg['content'] and msg['content'].strip():
                                valid_history.append(msg)
                
                if valid_history:
                    messages.extend(valid_history)
                    logger.info("History messages added: %d messages", len(valid_history))
                    print("History messages added:", len(valid_history), "messages")
                    print("History content preview:")
                    for i, msg in enumerate(valid_history[-3:], 1):  # 只显示最后3条
                        content_preview = msg.get('content', '')[:100]
                        print(f"  {i}. {msg.get('role', 'unknown')}: {content_preview}...")
                else:
                    logger.warning("No valid history messages found in provided history")
                    print("No valid history messages found in provided history")
                    if history:
                        print("Invalid history format:", type(history))
                        print("History content:", history)
            elif history:
                logger.warning("History is not a list: %s", type(history))
                print("History is not a list:", type(history))
                print("History content:", history)
            
            # 添加用户消息
            messages.append({"role": "user", "content": prompt})
            logger.info("User message added to messages")
            print("User message added to messages")
            
            logger.info("Total messages prepared: %d", len(messages))
            print("Total messages prepared:", len(messages))
            
            # 构建API调用参数
            api_params = {
                "model": self.model,
                "messages": messages,
                "response_format": {"type": "text"},
                "temperature": 0.3,
                "stream": False
            }
            
            logger.info("API parameters prepared:")
            logger.info("Model: %s", self.model)
            logger.info("Temperature: %s", 0.3)
            logger.info("Stream: %s", False)
            print("API parameters prepared:")
            print("Model:", self.model)
            print("Temperature:", 0.3)
            print("Stream:", False)
            
            # 调用API
            logger.info("Calling Doubao API...")
            print("Calling Doubao API...")
            response = self.client.chat.completions.create(**api_params)
            
            logger.info("Doubao API call completed")
            print("Doubao API call completed")
            
            if response.choices and response.choices[0].message:
                text = response.choices[0].message.content
                response_text = text or ""
                
                end_time = time.time()
                duration = end_time - start_time
                
                logger.info("Doubao API response received:")
                logger.info("Response length: %d characters", len(response_text))
                logger.info("Response time: %.2f seconds", duration)
                logger.info("Response preview: %s", response_text[:100] + "..." if len(response_text) > 100 else response_text)
                
                print("Doubao API response received:")
                print("Response length:", len(response_text), "characters")
                print("Response time:", "%.2f" % duration, "seconds")
                print("Response preview:", response_text[:100] + "..." if len(response_text) > 100 else response_text)
                
                # 打印完整的大模型返回信息
                print("=== LLM RESPONSE CONTENT ===")
                print(response_text)
                print("=== END LLM RESPONSE ===")
                
                return response_text
            else:
                logger.warning("Doubao API returned empty response")
                print("Doubao API returned empty response")
                return ""
                
        except Exception as e:
            error_msg = f"Doubao API call failed: {e}"
            logger.error(error_msg)
            print(error_msg)
            
            # 根据错误类型提供更具体的错误信息
            if "authentication" in str(e).lower() or "unauthorized" in str(e).lower():
                print("Error: Authentication failed. Please check your API key.")
            elif "not found" in str(e).lower() or "404" in str(e):
                print("Error: Model or endpoint not found. Please check the model name and base URL.")
            elif "rate limit" in str(e).lower():
                print("Error: Rate limit exceeded. Please wait before making another request.")
            elif "timeout" in str(e).lower():
                print("Error: Request timeout. Please check your network connection.")
            else:
                print("Error: Unknown error occurred during API call.")
            
            return ""
    
    async def call(self, prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None) -> str:
        """
        异步调用豆包API，返回完整文本
        
        Parameters
        ----------
        prompt : str
            用户输入的提示词
        system_prompt : str, optional
            系统提示词
        history : List[Dict[str, Any]], optional
            历史对话记录
            
        Returns
        -------
        str
            模型返回的文本内容
        """
        logger.info("DoubaoService async call started")
        print("DoubaoService async call started")
        
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, self._call_sync, prompt, system_prompt, history
        )
        
        logger.info("DoubaoService async call completed")
        print("DoubaoService async call completed")
        
        return result
    
    async def stream(self, prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None) -> AsyncGenerator[str, None]:
        """
        异步流式调用豆包API
        
        Parameters
        ----------
        prompt : str
            用户输入的提示词
        system_prompt : str, optional
            系统提示词
        history : List[Dict[str, Any]], optional
            历史对话记录
            
        Yields
        ------
        str
            流式返回的文本片段
        """
        try:
            logger.info("DoubaoService stream call started")
            print("DoubaoService stream call started")
            
            # 打印完整的prompt和system_prompt参数内容
            print("=== STREAM PROMPT CONTENT ===")
            print(prompt)
            print("=== END STREAM PROMPT ===")
            
            if system_prompt:
                print("=== STREAM SYSTEM PROMPT CONTENT ===")
                print(system_prompt)
                print("=== END STREAM SYSTEM PROMPT ===")
            else:
                print("=== STREAM SYSTEM PROMPT CONTENT ===")
                print("None or empty")
                print("=== END STREAM SYSTEM PROMPT ===")
            
            messages = []
            
            # 添加系统提示词 - 修复：只有当system_prompt不为None且不为空字符串时才添加
            if system_prompt and system_prompt.strip():
                messages.append({"role": "system", "content": system_prompt})
                logger.info("System prompt added to stream messages")
                print("System prompt added to stream messages")
            elif system_prompt is None:  # 只有明确为None时才使用默认提示词
                default_system = "你是一个强大的智能助手，擅长提供准确的信息"
                messages.append({"role": "system", "content": default_system})
                logger.info("Default system prompt added to stream messages")
                print("Default system prompt added to stream messages")
            
            # 添加历史对话
            if history:
                messages.extend(history)
                logger.info("History messages added to stream: %d messages", len(history))
                print("History messages added to stream:", len(history), "messages")
            
            # 添加用户消息
            messages.append({"role": "user", "content": prompt})
            logger.info("User message added to stream messages")
            print("User message added to stream messages")
            
            # 构建API调用参数
            api_params = {
                "model": self.model,
                "messages": messages,
                "response_format": {"type": "text"},
                "temperature": 0.3,
                "stream": True
            }
            
            logger.info("Stream API parameters prepared")
            print("Stream API parameters prepared")
            
            # 调用API
            logger.info("Calling Doubao stream API...")
            print("Calling Doubao stream API...")
            response = self.client.chat.completions.create(**api_params)
            
            chunk_count = 0
            for chunk in response:
                chunk_message = chunk.choices[0].delta
                if not chunk_message.content:
                    continue
                
                content = chunk_message.content
                chunk_count += 1
                yield content
                
                await asyncio.sleep(0)
            
            logger.info("Doubao stream API completed: %d chunks received", chunk_count)
            print("Doubao stream API completed:", chunk_count, "chunks received")
                
        except Exception as e:
            logger.error("Doubao stream API call failed: %s", e)
            print("Doubao stream API call failed:", e)
            yield ""


# 全局豆包服务实例
_doubao_service = None

def get_doubao_service():
    """获取豆包服务实例"""
    global _doubao_service
    if _doubao_service is None:
        logger.info("Creating new DoubaoService instance")
        print("Creating new DoubaoService instance")
        _doubao_service = DoubaoService()
    else:
        logger.info("Returning existing DoubaoService instance")
        print("Returning existing DoubaoService instance")
    return _doubao_service


# 兼容性函数
def call_doubao_llm(prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None) -> str:
    """调用豆包LLM（同步）"""
    logger.info("call_doubao_llm compatibility function called")
    print("call_doubao_llm compatibility function called")
    service = get_doubao_service()
    return service._call_sync(prompt, system_prompt, history)


async def call_doubao_stream(prompt: str, system_prompt: str = None, history: List[Dict[str, Any]] = None):
    """调用豆包LLM（流式）"""
    logger.info("call_doubao_stream compatibility function called")
    print("call_doubao_stream compatibility function called")
    service = get_doubao_service()
    return service.stream(prompt, system_prompt, history) 