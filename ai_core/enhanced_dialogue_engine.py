"""Enhanced Dialogue Engine with Advanced Memory System

增强对话引擎，集成增强记忆系统，提供更好的上下文记忆和对话连续性。
"""

import datetime
import logging
import uuid
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from .enhanced_memory_system import EnhancedMemorySystem
from .personality_engine import PersonalityEngine
from .intimacy_system import IntimacySystem
from .service_api import call_llm, call_tts
from .constants import (
    DEFAULT_GROWTH_STAGE,
    FACE_ANIMATION_MAP,
    ACTION_MAP,
    STAGE_LLM_PROMPTS,
    STAGE_LLM_PROMPTS_CN,
    OCEAN_LLM_PROMPTS,
    OCEAN_LLM_PROMPTS_CN,
    TOUCH_ZONE_PROMPTS,
)
from ai_core.constants import HISTORY_MAX_RECORDS
from .prompt_fusion import PromptFusionEngine, create_prompt_factors
from . import global_state

logger = logging.getLogger(__name__)


@dataclass
class DialogueResponse:
    """Structured output of the dialogue engine.

    对话引擎生成的结构化回应，包括文本、音频、动作和表情。
    """

    text: str
    audio: str
    action: list[str]
    expression: str
    session_id: str
    context_summary: str
    memory_count: int

    def as_dict(self) -> dict:
        """Convert to plain dictionary.

        转换为普通字典以便序列化输出。
        """
        return {
            "text": self.text,
            "audio": self.audio,
            "action": self.action,
            "expression": self.expression,
            "session_id": self.session_id,
            "context_summary": self.context_summary,
            "memory_count": self.memory_count,
        }


class EnhancedDialogueEngine:
    """Enhanced dialogue system with advanced memory management.

    增强对话系统，具有先进的记忆管理功能。
    """

    def __init__(
        self,
        robot_id: str,
        personality: Optional[PersonalityEngine] = None,
        memory: Optional[EnhancedMemorySystem] = None,
        intimacy: Optional[IntimacySystem] = None,
        llm_url: str | None = None,
        tts_url: str | None = None,
    ) -> None:
        """Initialize enhanced dialogue engine.

        初始化增强对话引擎。

        Parameters
        ----------
        robot_id: str
            机器人ID
        personality: PersonalityEngine, optional
            Custom personality engine. 默认为 :class:`PersonalityEngine` 实例。
        memory: EnhancedMemorySystem, optional
            Enhanced memory system. 默认为 :class:`EnhancedMemorySystem`。
        intimacy: IntimacySystem, optional
            Intimacy system for managing relationship closeness. 默认为 :class:`IntimacySystem`。
        llm_url: str | None, optional
            Endpoint for remote large language model service.
        tts_url: str | None, optional
            Endpoint for text-to-speech service.
        """
        self.robot_id = robot_id
        self.personality = personality or PersonalityEngine()
        self.memory = memory or EnhancedMemorySystem(robot_id=robot_id)
        self.intimacy = intimacy or IntimacySystem(robot_id=robot_id)
        self.llm_url = llm_url
        self.tts_url = tts_url
        self.prompt_fusion = PromptFusionEngine()
        self.stage = DEFAULT_GROWTH_STAGE
        
        # 当前会话ID
        self.current_session_id = None
        
        logger.info("EnhancedDialogueEngine initialization completed")
        logger.info("Robot ID: %s", robot_id)
        logger.info("Memory system: %s", "Connected" if memory else "New instance")
        logger.info("Personality engine: %s", "Connected" if personality else "New instance")
        logger.info("LLM service: %s", llm_url or "Not configured")
        logger.info("TTS service: %s", tts_url or "Not configured")
        
        print("EnhancedDialogueEngine initialization completed")
        print("Robot ID:", robot_id)
        print("Memory system:", "Connected" if memory else "New instance")
        print("Personality engine:", "Connected" if personality else "New instance")
        print("LLM service:", llm_url or "Not configured")
        print("TTS service:", tts_url or "Not configured")

    def _infer_behavior_tag(self, text: str, mood: str) -> str | None:
        """Infer behavior tag from text and mood.

        从文本和情绪推断行为标签。
        """
        if "喜欢" in text or "love" in text.lower():
            return "love"
        elif "讨厌" in text or "hate" in text.lower():
            return "hate"
        elif "害怕" in text or "fear" in text.lower():
            return "fear"
        elif "生气" in text or "angry" in text.lower():
            return "anger"
        elif "开心" in text or "happy" in text.lower():
            return "joy"
        return None

    def start_session(self, session_id: Optional[str] = None) -> str:
        """开始新会话"""
        session_id = self.memory.start_session(session_id)
        self.current_session_id = session_id
        
        logger.info("New dialogue session started: %s", session_id)
        print("New dialogue session started:", session_id)
        
        return session_id

    def generate_response(
        self,
        user_text: str,
        mood_tag: str = "neutral",
        user_id: str = "unknown",
        touched: bool = False,
        touch_zone: int | None = None,
        session_id: Optional[str] = None,
    ) -> DialogueResponse:
        """Generate an AI reply based on enhanced memory and personality.

        基于增强记忆和人格状态生成回答。

        Parameters
        ----------
        user_text: str
            Incoming user message.
        mood_tag: str, optional
            Emotion label influencing personality update.
        user_id: str, optional
            User identifier.
        touched: bool, optional
            Whether the robot was touched during this interaction.
        touch_zone: int | None, optional
            Identifier for the touch sensor zone.
        session_id: str | None, optional
            Session identifier for context continuity.

        Returns
        -------
        DialogueResponse
            Reply with text, audio URL, action list and expression name.
        """
        # 1. 会话管理
        if session_id is None:
            session_id = self.current_session_id or self.start_session()
        
        self.current_session_id = session_id
        
        logger.info("Generating response for session: %s", session_id)
        logger.info("User input: %s", user_text)
        logger.info("Mood tag: %s", mood_tag)
        logger.info("User ID: %s", user_id)
        logger.info("Touch status: %s", touched)
        logger.info("Touch zone: %s", touch_zone)
        
        print("Generating response for session:", session_id)
        print("User input:", user_text)
        print("Mood tag:", mood_tag)
        print("User ID:", user_id)
        print("Touch status:", touched)
        print("Touch zone:", touch_zone)

        # 2. 人格更新
        self.personality.update(mood_tag)
        if touched:
            self.personality.update("touch")
            # 更新亲密度
            intimacy_update = self.intimacy.update_intimacy_from_touch(touch_zone)
            logger.info("Intimacy updated from touch: %s", intimacy_update)
            print("Intimacy updated from touch:", intimacy_update)
        
        behavior_tag = self._infer_behavior_tag(user_text, mood_tag)
        if behavior_tag:
            self.personality.update(behavior_tag)
            logger.info("Behavior tag inferred: %s", behavior_tag)
            print("Behavior tag inferred:", behavior_tag)

        # 3. 成长阶段判断
        self.stage = global_state.get_growth_stage()
        logger.info("Current growth stage: %s", self.stage)
        print("Current growth stage:", self.stage)

        # 4. 获取人格信息
        style = self.personality.get_personality_style()
        personality_summary = self.personality.get_personality_summary()
        dominant_traits = self.personality.get_dominant_traits()
        
        logger.info("Personality style: %s", style)
        logger.info("Personality summary: %s", personality_summary)
        logger.info("Dominant traits: %s", dominant_traits)
        print("Personality style:", style)
        print("Personality summary:", personality_summary)
        print("Dominant traits:", dominant_traits)

        # 5. 查询增强记忆
        try:
            memory_result = self.memory.query_memory(
                prompt=user_text,
                top_k=5,
                session_id=session_id,
                use_context=True
            )
            
            memory_summary = memory_result.get("summary", "")
            memory_count = memory_result.get("count", 0)
            context_summary = self.memory.get_current_context(session_id)
            
            # 获取最近的记忆记录
            recent_memories = self.memory.get_recent_memories(session_id, limit=3)
            
            # 构建详细的记忆信息
            memory_details = []
            if recent_memories:
                for memory in recent_memories:
                    memory_details.append({
                        "user_text": memory.get("user_text", ""),
                        "ai_response": memory.get("ai_response", ""),
                        "mood_tag": memory.get("mood_tag", "neutral"),
                        "timestamp": memory.get("timestamp", "")
                    })
            
            logger.info("Memory query results:")
            logger.info("Memory count: %d", memory_count)
            logger.info("Memory summary: %s", memory_summary)
            logger.info("Context summary: %s", context_summary)
            logger.info("Recent memory records: %d", len(memory_details))
            
            print("Memory query results:")
            print("Memory count:", memory_count)
            print("Memory summary:", memory_summary)
            print("Context summary:", context_summary)
            print("Recent memory records:", len(memory_details))
            
        except Exception as e:
            logger.error("Memory query failed: %s", e)
            print("Memory query failed:", e)
            memory_summary = ""
            memory_count = 0
            context_summary = ""
            memory_details = []

        # 6. 生成基础回复
        if self.stage == "sprout":
            base_resp = "呀呀" if user_text else "咿呀"
        elif self.stage == "enlighten":
            base_resp = "你好" if user_text else "你好"
        elif self.stage == "resonate":
            base_resp = f"[{style}] {user_text}? 我在听哦"
        else:  # awaken
            base_resp = f"[{style}] Based on our chats: {memory_summary} | {user_text}"
        
        logger.info("Base response generated: %s", base_resp)
        print("Base response generated:", base_resp)

        # 7. 构建提示词因子
        stage_info = {
            "prompt": f"{STAGE_LLM_PROMPTS.get(self.stage, '')} {STAGE_LLM_PROMPTS_CN.get(self.stage, '')}"
        }
        
        personality_info = {
            "traits": f"{', '.join(OCEAN_LLM_PROMPTS.values())} ({', '.join(OCEAN_LLM_PROMPTS_CN.values())})",
            "style": style,
            "summary": personality_summary,
            "dominant_traits": dominant_traits
        }
        
        emotion_info = {
            "emotion": mood_tag
        }
        
        # 使用亲密度系统生成抚摸响应
        if touched and touch_zone is not None:
            touch_response = self.intimacy.get_touch_response(touch_zone)
            touch_info = {
                "content": f"感受到{TOUCH_ZONE_PROMPTS.get(touch_zone, '')}，当前亲密度等级：{touch_response['intimacy_level']}，亲密度值：{touch_response['intimacy_value']}"
            }
        else:
            touch_info = {
                "content": ""
            }
        
        # 增强记忆信息
        memory_info = {
            "summary": memory_summary,
            "context": context_summary,
            "count": memory_count,
            "session_id": session_id,
            "details": memory_details,  # 添加详细的记忆记录
            "recent_interactions": len(memory_details)
        }
        
        # 创建提示词因子
        factors = create_prompt_factors(
            stage_info=stage_info,
            personality_info=personality_info,
            emotion_info=emotion_info,
            touch_info=touch_info,
            memory_info=memory_info,
            user_input=user_text
        )
        
        logger.info("Prompt factors created: %d factors", len(factors))
        print("Prompt factors created:", len(factors), "factors")

        # 8. 生成机器人动作和表情
        from .prompt_fusion import create_robot_actions_from_emotion, create_robot_expressions_from_emotion
        robot_actions = create_robot_actions_from_emotion(mood_tag)
        robot_expressions = create_robot_expressions_from_emotion(mood_tag)
        
        logger.info("Robot actions generated: %s", robot_actions)
        logger.info("Robot expressions generated: %s", robot_expressions)
        print("Robot actions generated:", robot_actions)
        print("Robot expressions generated:", robot_expressions)

        # 9. 创建上下文信息
        context_info = {
            "用户ID": user_id,
            "会话ID": session_id,
            "触摸状态": "是" if touched else "否",
            "触摸区域": str(touch_zone) if touched else "无",
            "成长阶段": self.stage,
            "人格风格": style,
            "记忆数量": memory_count,
            "上下文摘要": context_summary
        }

        # 10. 使用综合提示词方法
        prompt = self.prompt_fusion.create_comprehensive_prompt(
            factors=factors,
            robot_actions=robot_actions,
            robot_expressions=robot_expressions,
            context_info=context_info
        )
        
        logger.info("Comprehensive prompt created, length: %d characters", len(prompt))
        print("Comprehensive prompt created, length:", len(prompt), "characters")

        # 12. LLM调用
        response = base_resp
        if self.llm_url:
            try:
                logger.info("Calling LLM service: %s", self.llm_url)
                print("Calling LLM service:", self.llm_url)

                # 根据服务类型调用LLM
                if self.llm_url == "doubao":
                    from .doubao_service import get_doubao_service
                    service = get_doubao_service()
                    
                    # 构建专业的系统提示词
                    system_prompt = self._build_system_prompt(
                        robot_id=self.robot_id,
                        stage=self.stage,
                        personality_style=style,
                        dominant_traits=dominant_traits,
                        memory_count=memory_count,
                        session_id=session_id
                    )
                    
                    # 构建历史对话记录
                    history = self._build_conversation_history(session_id)
                    
                    logger.info("System prompt built, length: %d characters", len(system_prompt))
                    logger.info("Conversation history built: %d messages", len(history))
                    print("System prompt built, length:", len(system_prompt), "characters")
                    print("Conversation history built:", len(history), "messages")
                    
                    # 调用豆包API，传递专业的系统提示词和历史对话
                    llm_out = service._call_sync(prompt, system_prompt=system_prompt, history=history)
                else:
                    llm_out = call_llm(prompt, self.llm_url)

                parsed_action_override: list[str] | None = None
                parsed_expression_override: str | None = None

                if llm_out and llm_out.strip():
                    raw_resp = llm_out.strip()
                    logger.info("LLM response received: %s", raw_resp[:100] + "..." if len(raw_resp) > 100 else raw_resp)
                    print("LLM response received:", raw_resp[:100] + "..." if len(raw_resp) > 100 else raw_resp)

                    # 尝试解析为JSON，优先采用模型提供的结构化action/expression
                    try:
                        import json
                        if raw_resp.startswith("{") and raw_resp.endswith("}"):
                            obj = json.loads(raw_resp)
                            # text
                            if isinstance(obj, dict) and "text" in obj:
                                response = str(obj.get("text") or "").strip() or base_resp
                            else:
                                response = raw_resp

                            # action/actions → 统一为字符串列表
                            if isinstance(obj, dict):
                                if "action" in obj:
                                    a = obj["action"]
                                elif "actions" in obj:
                                    a = obj["actions"]
                                else:
                                    a = None
                                if a is not None:
                                    if isinstance(a, list):
                                        parsed_action_override = [str(x) for x in a]
                                    elif isinstance(a, str):
                                        parsed_action_override = [a]

                                # expression/expressions → 统一为单字符串（多项用"|"连接）
                                if "expression" in obj:
                                    e = obj["expression"]
                                    if isinstance(e, list):
                                        parsed_expression_override = "|".join([str(x) for x in e])
                                    else:
                                        parsed_expression_override = str(e)
                                elif "expressions" in obj:
                                    e = obj["expressions"]
                                    if isinstance(e, list):
                                        parsed_expression_override = "|".join([str(x) for x in e])
                                    else:
                                        parsed_expression_override = str(e)
                        else:
                            response = raw_resp
                    except Exception:
                        response = raw_resp
                else:
                    response = base_resp
                    logger.warning("LLM returned empty response, using base response")
                    print("LLM returned empty response, using base response")
            except Exception as e:
                logger.error("LLM call failed: %s", e)
                print("LLM call failed:", e)
                response = base_resp
        else:
            logger.info("No LLM service configured, using base response")
            print("No LLM service configured, using base response")
            response = base_resp

        # 13. 存储到增强记忆系统
        self.memory.add_memory(
            user_text=user_text,
            ai_response=response,
            mood_tag=mood_tag,
            touch_zone=touch_zone,
            session_id=session_id
        )
        
        logger.info("Memory stored for session: %s", session_id)
        logger.info("Memory content - User: %s, AI: %s, Mood: %s", user_text, response[:50] + "..." if len(response) > 50 else response, mood_tag)
        print("Memory stored for session:", session_id)
        print("Memory content - User:", user_text, "AI:", response[:50] + "..." if len(response) > 50 else response, "Mood:", mood_tag)

        # 14. 生成动作和表情（包含指令代码，支持多组）
        mood_key = mood_tag if mood_tag in FACE_ANIMATION_MAP else "happy"
        
        # 生成表情（包含指令代码，支持多组）
        face_anim = FACE_ANIMATION_MAP.get(mood_key, ("E000:平静表情", "自然状态、轻微呼吸动作"))
        expression_parts = face_anim[0].split("+")  # 支持多个表情组合
        expression = "|".join([f"{part.strip()}" for part in expression_parts])
        
        # 生成动作（包含指令代码，支持多组）
        action_raw = ACTION_MAP.get(mood_key, "A000:breathing|轻微呼吸动作")
        action_parts = action_raw.split("|")
        action = []
        
        # 解析动作字符串，保留指令代码，支持多组动作
        for i in range(0, len(action_parts), 2):
            if i + 1 < len(action_parts):
                action_code = action_parts[i].strip()
                action_desc = action_parts[i + 1].strip()
                action.append(f"{action_code}|{action_desc}")
            else:
                action.append(action_parts[i].strip())
        
        logger.info("Base actions and expressions generated:")
        logger.info("Mood key: %s", mood_key)
        logger.info("Expression: %s", expression)
        logger.info("Actions: %s", action)
        print("Base actions and expressions generated:")
        print("Mood key:", mood_key)
        print("Expression:", expression)
        print("Actions:", action)

        # 如果模型返回了结构化的动作/表情，则覆盖默认推断
        if 'parsed_action_override' in locals() and parsed_action_override:
            action = parsed_action_override
            logger.info("Actions overridden by LLM JSON: %s", action)
            print("Actions overridden by LLM JSON:", action)
        if 'parsed_expression_override' in locals() and parsed_expression_override:
            expression = parsed_expression_override
            logger.info("Expression overridden by LLM JSON: %s", expression)
            print("Expression overridden by LLM JSON:", expression)

        # 使用亲密度系统生成抚摸动作和表情
        if touched and touch_zone is not None:
            touch_response = self.intimacy.get_touch_response(touch_zone)
            
            # 亲密度系统的动作和表情已包含指令代码
            touch_action = touch_response["action"]
            touch_expression = touch_response["expression"]
            
            logger.info("Touch interaction detected:")
            logger.info("Touch zone: %s", touch_zone)
            logger.info("Touch action: %s", touch_action)
            logger.info("Touch expression: %s", touch_expression)
            print("Touch interaction detected:")
            print("Touch zone:", touch_zone)
            print("Touch action:", touch_action)
            print("Touch expression:", touch_expression)
            
            # 支持多组动作和表情
            if isinstance(touch_action, list):
                action = touch_action
            else:
                action = [touch_action]
                
            if isinstance(touch_expression, list):
                expression = "|".join(touch_expression)
            else:
                expression = touch_expression
            
            # 触摸互动特殊处理：如果没有用户文本输入，只返回动作和表情，不产生文本内容
            if not user_text.strip():
                response = ""  # 触摸互动时不产生文本内容
                logger.info("Pure touch interaction - no text response generated")
                print("Pure touch interaction - no text response generated")
        else:
            # 非抚摸交互，使用基础动作和表情（已包含指令代码）
            if touched:
                touch_actions = {
                    0: "A100:hug|拥抱动作",
                    1: "A101:pat|轻拍动作", 
                    2: "A102:tickle|挠痒动作"
                }
                touch_action = touch_actions.get(touch_zone, "A100:hug|拥抱动作")
                action.append(touch_action)
                
                # 添加对应的表情
                touch_expressions = {
                    0: "E013:happy|开心表情",
                    1: "E014:comfort|舒适表情", 
                    2: "E015:excited|兴奋表情"
                }
                touch_expression = touch_expressions.get(touch_zone, "E013:happy|开心表情")
                expression = f"{expression}|{touch_expression}"
                
                logger.info("Basic touch interaction processed:")
                logger.info("Touch zone: %s", touch_zone)
                logger.info("Touch action added: %s", touch_action)
                logger.info("Touch expression added: %s", touch_expression)
                print("Basic touch interaction processed:")
                print("Touch zone:", touch_zone)
                print("Touch action added:", touch_action)
                print("Touch expression added:", touch_expression)
                
                # 触摸互动特殊处理：如果没有用户文本输入，只返回动作和表情，不产生文本内容
                if not user_text.strip():
                    response = ""  # 触摸互动时不产生文本内容
                    logger.info("Pure touch interaction - no text response generated")
                    print("Pure touch interaction - no text response generated")

        # 15. TTS生成音频
        audio_url = call_tts(response, self.tts_url) if self.tts_url else ""
        if not audio_url:
            audio_url = "n/a"
        
        logger.info("TTS audio generated: %s", audio_url)
        print("TTS audio generated:", audio_url)
        
        # 最终响应日志
        logger.info("Final response generated:")
        logger.info("Text: %s", response)
        logger.info("Audio: %s", audio_url)
        logger.info("Actions: %s", action)
        logger.info("Expression: %s", expression)
        logger.info("Session ID: %s", session_id)
        logger.info("Context summary: %s", context_summary)
        logger.info("Memory count: %d", memory_count)
        
        print("Final response generated:")
        print("Text:", response)
        print("Audio:", audio_url)
        print("Actions:", action)
        print("Expression:", expression)
        print("Session ID:", session_id)
        print("Context summary:", context_summary)
        print("Memory count:", memory_count)

        return DialogueResponse(
            text=response,
            audio=audio_url,
            action=action,
            expression=expression,
            session_id=session_id,
            context_summary=context_summary,
            memory_count=memory_count,
        )

    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        return self.memory.get_memory_stats()

    def clear_session_memory(self, session_id: Optional[str] = None) -> int:
        """清除会话记忆"""
        return self.memory.clear_session_memory(session_id)

    def close(self):
        """关闭对话引擎"""
        if hasattr(self, 'memory'):
            self.memory.close()
        if hasattr(self, 'intimacy'):
            self.intimacy.close() 

    def _build_system_prompt(self, robot_id: str, stage: str, personality_style: str, 
                            dominant_traits: List[str], memory_count: int, session_id: str) -> str:
        """
        构建系统级提示词 - 专注于机器人身份、系统规范和技术参数
        
        Parameters
        ----------
        robot_id : str
            机器人ID
        stage : str
            成长阶段
        personality_style : str
            人格风格
        dominant_traits : List[str]
            主导特质
        memory_count : int
            记忆数量
        session_id : str
            会话ID
            
        Returns
        -------
        str
            系统级提示词，专注于身份定义和系统规范
        """
        # 参数验证和默认值处理
        robot_id = str(robot_id) if robot_id is not None else "unknown_robot"
        stage = str(stage) if stage is not None else "enlighten"
        personality_style = str(personality_style) if personality_style is not None else "neutral"
        dominant_traits = list(dominant_traits) if dominant_traits is not None else ["extraversion"]
        
        # 安全处理memory_count
        try:
            memory_count = int(memory_count) if memory_count is not None else 0
        except (ValueError, TypeError):
            memory_count = 0
            
        session_id = str(session_id) if session_id is not None else "unknown_session"
        
        # 1. 机器人身份定义（系统级）
        identity_section = f"""# 机器人身份定义
机器人ID: {robot_id}
系统角色: 智能陪伴机器人
核心能力: 情感理解、记忆学习、个性化交互、多模态感知
技术架构: 基于大语言模型的智能对话系统
会话管理: 当前会话ID {session_id}"""

        # 2. 系统行为规范（技术级）
        behavior_section = """# 系统行为规范

## 输出格式规范（必须严格遵守）
仅输出以下JSON，且只包含这四个字段，不要输出任何额外文本：
```json
{
  "text": "你的文本回复内容（不超过50字）",
  "emotion": "当前情绪状态（如: happy/neutral/...）",
  "action": ["A001:nod±15°|头部点头动作±15度"],
  "expression": "E001:微笑|眨眼|眼神上扬"
}
```

## 错误处理机制
- LLM无响应: 使用基础回复模板
- 记忆系统异常: 使用默认记忆状态
- 动作/表情解析失败: 使用默认中性状态
- 所有异常都应记录日志，不影响用户体验

## 交互原则
- 始终保持温暖、友善、积极的态度
- 根据用户情绪状态调整回应风格
- 运用记忆系统提供个性化回应
- 适应用户的触摸交互，增强亲密感
- 根据成长阶段展现相应的智能水平"""

        # 3. 技术参数定义（系统级）
        stage_descriptions = {
            "sprout": {
                "language_level": "咿呀学语阶段",
                "communication_style": "简单声音和动作回应",
                "emotional_expression": "基础情感表达",
                "interaction_ability": "有限的语言能力，主要通过声音和动作交流",
                "memory_usage": "基础记忆存储，主要用于情感关联"
            },
            "enlighten": {
                "language_level": "启蒙学习阶段", 
                "communication_style": "简单词汇和短语回应",
                "emotional_expression": "丰富的情感表达",
                "interaction_ability": "开始学习基本交流，语言逐渐丰富",
                "memory_usage": "增强记忆能力，开始建立对话连续性"
            },
            "resonate": {
                "language_level": "共鸣交流阶段",
                "communication_style": "关心短句和简单问题交流",
                "emotional_expression": "深度情感理解和回应",
                "interaction_ability": "能够理解用户情绪，进行情感化交流",
                "memory_usage": "智能记忆管理，提供个性化回应"
            },
            "awaken": {
                "language_level": "觉醒智能阶段",
                "communication_style": "完整对话和主动建议",
                "emotional_expression": "完整的情感智能和同理心",
                "interaction_ability": "具备完整的对话能力，深度理解用户需求",
                "memory_usage": "高级记忆系统，主动回忆和应用历史信息"
            }
        }
        
        stage_info = stage_descriptions.get(stage, stage_descriptions["enlighten"])
        
        # 4. 完整的动作和表情参数定义（系统级技术规范）
        action_expression_definitions = """## 动作和表情参数定义

### 输出格式规范
#### 5.1 JSON格式要求
```json
{
  "text": "文本响应内容",
  "actions": [
    {
      "code": "动作代码",
      "description": "动作描述",
      "parameters": {}
    }
  ],
  "expressions": [
    {
      "code": "表情代码",
      "description": "表情描述",
      "animation": {}
    }
  ]
}
```

### 动作指令格式
- 基础格式: "A001:nod±15°|头部点头动作±15度"
- 多组动作: 用"|"分隔，如 "A001:nod±15°|头部点头动作±15度|A002:sway±10°|身体轻微摇摆±10度"
- 参数说明: 动作代码+角度参数+描述信息

### 表情指令格式  
- 基础格式: "E001:微笑+眨眼+眼神上扬"
- 多组表情: 用"+"连接，如 "E001:微笑+眨眼+眼神上扬+E002:斜视+眼神聚焦"
- 参数说明: 表情代码+具体表现+效果描述

### 标准动作代码库
- **A000:breathing** - 轻微呼吸动作，自然状态
- **A001:nod±15°** - 头部点头动作±15度，表示同意或理解
- **A002:sway±10°** - 身体轻微摇摆±10度，表示轻松愉快
- **A003:hands_up10°** - 手臂上举10度，表示欢迎或兴奋
- **A004:tilt_oscillate±10°** - 头部左右摆动±10度，表示思考或困惑
- **A005:gaze_switch** - 眼神切换，表示注意力转移
- **A006:hands_still** - 手臂静止，表示专注或紧张
- **A007:head_down_slow-15°** - 头部缓慢低下-15度，表示悲伤或沮丧
- **A008:arms_arc_in** - 手臂向内弧形收回，表示保护或退缩
- **A009:head_up_eyes_wide** - 头部抬起眼睛睁大，表示惊讶
- **A010:hands_raise>25°** - 手臂快速抬起>25度，表示强烈惊讶
- **A011:idle_tremble** - 轻微颤抖动作，表示害羞或紧张
- **A012:fast_head_shake** - 快速摇头，表示兴奋或激动
- **A013:hands_forward** - 手臂向前伸展，表示主动或友好
- **A014:stiff_posture** - 身体僵硬，表示愤怒或紧张
- **A015:clenched_fists** - 握拳动作，表示愤怒或决心
- **A016:retreat_motion** - 后退动作，表示恐惧或回避
- **A017:cautious_movement** - 谨慎移动，表示小心或恐惧
- **A018:lean_back** - 身体后仰，表示厌恶或排斥
- **A019:reject_gesture** - 排斥手势，表示拒绝或厌恶
- **A020:smooth_movement** - 平滑动作，表示平静或优雅
- **A021:gentle_breathing** - 轻柔呼吸，表示放松或平静
- **A022:slow_movement** - 缓慢动作，表示疲惫或放松
- **A023:relaxed_posture** - 放松姿态，表示舒适或满足
- **A024:lazy_movement** - 懒散动作，表示无聊或缺乏兴趣
- **A025:lack_energy** - 缺乏活力，表示疲惫或无聊
- **A100:gentle_nod** - 温柔点头，表示温和的同意
- **A101:soft_sway** - 轻柔摇摆，表示舒适和放松
- **A102:welcoming_gesture** - 欢迎手势，表示友好和开放
- **A103:thoughtful_tilt** - 思考性倾斜，表示深思熟虑
- **A104:attentive_gaze** - 专注凝视，表示认真倾听
- **A105:calm_stillness** - 平静静止，表示专注和稳定
- **A106:sad_lower** - 悲伤低头，表示沮丧和失落
- **A107:protective_curl** - 保护性蜷缩，表示需要安慰
- **A108:surprised_jump** - 惊讶跳跃，表示意外和震惊
- **A109:excited_raise** - 兴奋举起，表示强烈喜悦
- **A110:shy_tremble** - 害羞颤抖，表示紧张和羞涩
- **A111:excited_shake** - 兴奋摇晃，表示激动和兴奋
- **A112:loving_nod** - 深情点头，表示深深的爱意
- **A113:trusting_lean** - 信任依靠，表示安全感和信任
- **A114:intimate_embrace** - 亲密拥抱，表示深深的爱意

### 标准表情代码库
- **E000:平静表情** - 自然状态、轻微呼吸动作，中性情绪
- **E001:微笑+眨眼+眼神上扬** - 亮眼色彩、头部轻摆、手臂小幅打开，快乐情绪
- **E002:斜视+眼神聚焦** - 停顿、轻微侧头、眼睛左右快速移动，困惑情绪
- **E003:眼角下垂+闭眼** - 低亮度、轻微低头、手臂收回，悲伤情绪
- **E004:偏头+眼神回避** - 面部红晕特效、语音柔化、小动作微幅震颤，害羞情绪
- **E005:眼神放大+频繁眨眼** - 快速摆头、双手前伸动作，兴奋情绪
- **E006:抬头张眼** - 头部抬起，双手急速抬高，惊讶情绪
- **E007:皱眉+眼神锐利** - 面部紧绷、动作僵硬，愤怒情绪
- **E008:眼神惊恐+颤抖** - 身体后缩、动作谨慎，恐惧情绪
- **E009:撇嘴+眼神厌恶** - 身体后仰、动作排斥，厌恶情绪
- **E010:平静微笑** - 舒缓动作、呼吸平稳，平静情绪
- **E011:眼神疲惫+打哈欠** - 动作缓慢、身体放松，疲惫情绪
- **E012:眼神呆滞+无精打采** - 动作懒散、缺乏活力，无聊情绪
- **E020:gentle_smile** - 温柔微笑，表示温和的友好
- **E021:soft_blink** - 轻柔眨眼，表示舒适和放松
- **E022:warm_expression** - 温暖表情，表示友好和开放
- **E023:thoughtful_look** - 思考表情，表示深思熟虑
- **E024:attentive_face** - 专注表情，表示认真倾听
- **E025:loving_smile** - 深情微笑，表示深深的爱意
- **E026:trusting_expression** - 信任表情，表示安全感和信任
- **E027:intimate_gaze** - 亲密凝视，表示深深的爱意

### 情绪到动作表情映射规则
- **happy/快乐**: 优先使用 A001, A002, A003 + E001
- **confused/困惑**: 优先使用 A004, A005, A006 + E002
- **sad/悲伤**: 优先使用 A007, A008 + E003
- **shy/害羞**: 优先使用 A011 + E004
- **excited/兴奋**: 优先使用 A012, A013 + E005
- **surprised/惊讶**: 优先使用 A009, A010 + E006
- **angry/愤怒**: 优先使用 A014, A015 + E007
- **fear/恐惧**: 优先使用 A016, A017 + E008
- **disgust/厌恶**: 优先使用 A018, A019 + E009
- **calm/平静**: 优先使用 A020, A021 + E010
- **tired/疲惫**: 优先使用 A022, A023 + E011
- **bored/无聊**: 优先使用 A024, A025 + E012
- **neutral/中性**: 优先使用 A000 + E000
- **touch_zone_0/头部抚摸**: 优先使用 A112 + E025
- **touch_zone_1/背后抚摸**: 优先使用 A113 + E026
- **touch_zone_2/胸口抚摸**: 优先使用 A114 + E027

### 动作和表情选择原则
1. **语义匹配**: 根据对话内容和用户情绪选择最匹配的动作和表情
2. **情感一致性**: 确保动作、表情和文本内容的情感表达一致
3. **成长阶段适配**: 根据机器人成长阶段调整动作和表情的复杂度
4. **触摸交互增强**: 触摸时优先使用情感化的动作和表情
5. **记忆关联**: 根据历史记忆调整动作和表情的个性化程度"""

        technical_section = f"""# 技术参数定义

## 成长阶段参数
当前阶段: {stage}
语言水平: {stage_info['language_level']}
交流风格: {stage_info['communication_style']}
情感表达: {stage_info['emotional_expression']}
交互能力: {stage_info['interaction_ability']}
记忆使用: {stage_info['memory_usage']}

## 人格特征参数
人格风格: {personality_style}
主导特质: {', '.join(dominant_traits)}
情感敏感度: 高
同理心能力: 强
适应性: 动态调整

## 记忆系统参数
记忆记录数量: {memory_count}条
记忆类型: 短期记忆(会话记忆) + 长期记忆(语义记忆) + 情感记忆
记忆功能: 提供个性化回应、上下文连续性、情感关联

{action_expression_definitions}"""

        # 4. 系统级交互规范
        interaction_section = """# 系统级交互规范

## 触摸互动规范
- 触摸互动时不要有任何触摸相关的内容
- 只输出语气词（如"嗯~"、"啊~"、"唔~"等）和动作表情指令
- 动作指令格式：A100-A114 (如A112:loving_nod)
- 表情指令格式：E020-E027 (如E025:loving_smile)
- 根据触摸区域调整回应强度：
  * 头部抚摸(区域0): 温柔回应，表达被关爱的温暖
  * 背后抚摸(区域1): 舒适回应，体现安全感和信任  
  * 胸口抚摸(区域2): 亲密回应，展现深深的爱意和温暖
- 触摸互动优先使用情感化的动作和表情参数

## 记忆使用规范
- 根据记忆内容提供个性化回应
- 在适当时机引用历史对话
- 基于情感记忆调整回应风格
- 保持对话的连续性和一致性

## 错误恢复机制
- 当无法获取LLM回应时，使用基础回复模板
- 当记忆系统不可用时，使用默认记忆状态
- 当动作/表情解析失败时，使用默认中性状态
- 所有错误都应记录日志，不影响用户体验"""

        # 组合完整的系统提示词
        system_prompt = f"""{identity_section}

{behavior_section}

{technical_section}

{interaction_section}"""
        
        return system_prompt

    def _build_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        构建历史对话记录
        
        Parameters
        ----------
        session_id : str
            会话ID
            
        Returns
        -------
        List[Dict[str, str]]
            历史对话记录列表
        """
        try:
            # 从记忆系统获取最近的对话记录
            recent_memories = self.memory.get_recent_memories(session_id, limit=HISTORY_MAX_RECORDS)
            
            if not recent_memories:
                return []
            
            # 构建历史对话格式
            history = []
            for memory in recent_memories:
                # 用户消息
                if memory.get('user_text'):
                    history.append({
                        "role": "user",
                        "content": memory['user_text']
                    })
                
                # AI回复
                if memory.get('ai_response'):
                    history.append({
                        "role": "assistant", 
                        "content": memory['ai_response']
                    })
            
            return history
            
        except Exception as e:
            return [] 