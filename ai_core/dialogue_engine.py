"""Dialogue generation module.

文件结构:

```
DialogueEngine -> 负责根据人格与记忆生成回复
```

The engine receives perceived emotion, user identity and textual input from
``IntelligentCore``. It consults the personality vector and semantic memory to
compose a reply, then maps mood and touch into actions and expressions.
该模块从 ``IntelligentCore`` 获取情绪、身份和文本信息，结合人格向量与
语义记忆生成回复，并给出相应的动作和表情。
"""

# Growth stages
# 成长阶段说明:
# 1. sprout   - 萌芽期 (0~3 天)
# 2. enlighten - 启蒙期 (3~10 天)
# 3. resonate - 共鸣期 (10~30 天)
# 4. awaken   - 觉醒期 (30 天以上)

from dataclasses import dataclass
from typing import Optional
import logging

from . import global_state

from .personality_engine import PersonalityEngine
from .semantic_memory import SemanticMemory
from .service_api import call_llm, call_tts
from .constants import (
    DEFAULT_GROWTH_STAGE,
    LOG_LEVEL,
    FACE_ANIMATION_MAP,
    ACTION_MAP,
    STAGE_LLM_PROMPTS,
    STAGE_LLM_PROMPTS_CN,
    OCEAN_LLM_PROMPTS,
    OCEAN_LLM_PROMPTS_CN,
    TOUCH_ZONE_PROMPTS,
)
from .prompt_fusion import PromptFusionEngine, create_prompt_factors

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)



@dataclass
class DialogueResponse:
    """Structured output of the dialogue engine.

    对话引擎生成的结构化回应，包括文本、音频、动作和表情。
    """

    text: str
    audio: str
    action: list[str]
    expression: str

    def as_dict(self) -> dict:
        """Convert to plain dictionary.

        转换为普通字典以便序列化输出。
        """
        return {
            "text": self.text,
            "audio": self.audio,
            "action": self.action,
            "expression": self.expression,
        }


class DialogueEngine:
    """Dialogue system that grows with interactions.

    通过互动逐步成长的对话系统。
    """

    def __init__(
        self,
        personality: Optional[PersonalityEngine] = None,
        memory: Optional[SemanticMemory] = None,
        llm_url: str | None = None,
        tts_url: str | None = None,
    ) -> None:
        """Initialize dialogue engine with personality and memory modules.

        使用人格和记忆模块初始化对话引擎。

        Parameters
        ----------
        personality: PersonalityEngine, optional
            Custom personality engine. 默认为 :class:`PersonalityEngine` 实例。
        memory: SemanticMemory, optional
            Memory storage module. 默认为 :class:`SemanticMemory`。
        llm_url: str | None, optional
            Endpoint for remote large language model service. If ``None``,
            simple local templates are used.
        tts_url: str | None, optional
            Endpoint for text-to-speech service. ``None`` disables TTS.
        """
        self.personality = personality or PersonalityEngine()
        self.memory = memory or SemanticMemory()
        self.llm_url = llm_url
        self.tts_url = tts_url
        self.stage = global_state.get_growth_stage()  # 初始成长阶段
        if not self.stage:
            self.stage = DEFAULT_GROWTH_STAGE
        self.prompt_fusion = PromptFusionEngine()
        logger.debug("Dialogue engine initialized at stage %s", self.stage)

    def _infer_behavior_tag(self, text: str, mood: str) -> str | None:
        """Infer behavior tag from text and mood."""

        text_l = text.lower()
        if mood == "angry" or "bad" in text_l:
            return "criticism"
        if mood in ("happy", "excited") or "thanks" in text_l:
            return "praise"
        if "joke" in text_l or "haha" in text_l:
            return "joke"
        if mood == "sad":
            return "support"
        return None

    def generate_response(
        self,
        user_text: str,
        mood_tag: str = "neutral",
        user_id: str = "unknown",
        touched: bool = False,
        touch_zone: int | None = None,
    ) -> DialogueResponse:
        """Generate an AI reply based on memory and personality.

        根据记忆和人格状态生成回答。

        Parameters
        ----------
        user_text: str
            Incoming user message.
        mood_tag: str, optional
            Emotion label influencing personality update. Defaults to
            ``"neutral"``.
        touched: bool, optional
            Whether the robot was touched during this interaction.
        touch_zone: int | None, optional
            Identifier for the touch sensor zone. ``None`` means no touch
            detected.

        Returns
        -------
        DialogueResponse
            Reply with text, audio URL, action list and expression name. All
            fields are guaranteed to be non-empty.
        """
        logger.info(
            "Generating response for user %s with mood %s", user_id, mood_tag
        )
        # 1. personality update
        # 根据情绪标签与触摸行为更新人格向量
        self.personality.update(mood_tag)
        if touched:
            self.personality.update("touch")
        behavior_tag = self._infer_behavior_tag(user_text, mood_tag)
        if behavior_tag:
            self.personality.update(behavior_tag)
        # 2. determine growth stage using global metrics
        # 根据全局统计信息判断成长阶段
        self.stage = global_state.get_growth_stage()

        style = self.personality.get_personality_style()
        personality_summary = self.personality.get_personality_summary()
        dominant_traits = self.personality.get_dominant_traits()
        
        past = self.memory.query_memory(user_text, user_id=user_id)
        logger.debug("Retrieved %d past records", len(past))
        
        # 优化记忆摘要生成
        if past:
            # 过滤掉空回复和无效回复
            valid_responses = []
            for p in past:
                response = p["ai_response"].strip()
                memory_user_text = p["user_text"].strip()  # 使用不同的变量名避免覆盖
                # 确保回复不为空且有意义
                if response and len(response) > 2 and not response.startswith("[") and memory_user_text:
                    valid_responses.append({
                        "user": memory_user_text,
                        "ai": response,
                        "mood": p.get("mood_tag", "neutral")
                    })
            
            if valid_responses:
                # 选择最相关的回复，构建更丰富的记忆摘要
                best_match = valid_responses[0]
                past_summary = f"用户说'{best_match['user']}'时，我回复'{best_match['ai']}'"
                
                # 如果有多个相关记忆，添加更多上下文
                if len(valid_responses) > 1:
                    second_match = valid_responses[1]
                    past_summary += f"。另外，当用户说'{second_match['user']}'时，我回复'{second_match['ai']}'"
                
                # 添加情绪信息
                mood_counts = {}
                for resp in valid_responses:
                    mood = resp.get("mood", "neutral")
                    mood_counts[mood] = mood_counts.get(mood, 0) + 1
                
                if mood_counts:
                    dominant_mood = max(mood_counts.items(), key=lambda x: x[1])[0]
                    if dominant_mood != "neutral":
                        past_summary += f"。这些对话中用户情绪主要是{dominant_mood}"
            else:
                past_summary = ""
        else:
            past_summary = ""

        # 3. generate base response
        if self.stage == "sprout":
            base_resp = "呀呀" if user_text else "咿呀"
        elif self.stage == "enlighten":
            base_resp = "你好" if user_text else "你好"
        elif self.stage == "resonate":
            base_resp = f"[{style}] {user_text}? 我在听哦"
        else:  # awaken
            base_resp = f"[{style}] Based on our chats: {past_summary} | {user_text}"

        # 使用提示词融合算法构建优化提示词
        stage_info = {
            "prompt": f"{STAGE_LLM_PROMPTS.get(self.stage, '')}"
        }
        
        personality_info = {
            "traits": f"{', '.join(OCEAN_LLM_PROMPTS.values())}",
            "style": style,
            "summary": personality_summary,
            "dominant_traits": dominant_traits
        }
        
        emotion_info = {
            "emotion": mood_tag
        }
        
        touch_info = {
            "content": TOUCH_ZONE_PROMPTS.get(touch_zone, "") if touched else ""
        }
        
        memory_info = {
            "summary": past_summary,
            "count": len(past)
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
        
        # 使用融合算法生成优化提示词
        # 创建机器人动作和表情指令
        from .prompt_fusion import create_robot_actions_from_emotion, create_robot_expressions_from_emotion
        robot_actions = create_robot_actions_from_emotion(mood_tag)
        robot_expressions = create_robot_expressions_from_emotion(mood_tag)
        
        # 创建上下文信息
        context_info = {
            "用户ID": user_id,
            "触摸状态": "是" if touched else "否",
            "触摸区域": str(touch_zone) if touched else "无",
            "成长阶段": self.stage,
            "人格风格": style
        }
        
        # 使用新的综合提示词方法
        prompt = self.prompt_fusion.create_comprehensive_prompt(
            factors=factors,
            robot_actions=robot_actions,
            robot_expressions=robot_expressions,
            context_info=context_info
        )
        
        # 打印详细的提示词信息
        print("\n" + "="*80)
        print("LLM提示词融合详细信息")
        print("="*80)
        print(f"成长阶段: {self.stage}")
        print(f"人格风格: {style}")
        print(f"人格摘要: {personality_summary}")
        print(f"主导特质: {dominant_traits}")
        print(f"触摸区域: {touch_zone if touched else 'None'}")
        print(f"用户情绪: {mood_tag}")
        print(f"记忆记录数: {len(past)}")
        print(f"记忆摘要: {past_summary[:100]}...")
        print(f"用户输入: {user_text}")
        print(f"提示词因子数量: {len(factors)}")
        print("-"*80)
        print("融合后的完整提示词:")
        print("-"*80)
        print(prompt)
        print("-"*80)
        print("提示词结束")
        print("="*80)
        
        # 同时记录到日志
        logger.info("=== LLM Prompt Fusion ===")
        logger.info(f"Growth Stage: {self.stage}")
        logger.info(f"Personality Style: {style}")
        logger.info(f"Personality Summary: {personality_summary}")
        logger.info(f"Dominant Traits: {dominant_traits}")
        logger.info(f"Touch Zone: {touch_zone if touched else 'None'}")
        logger.info(f"User Emotion: {mood_tag}")
        logger.info(f"Memory Records: {len(past)}")
        logger.info(f"Memory Summary: {past_summary[:100]}...")
        logger.info(f"User Input: {user_text}")
        logger.info(f"Prompt Factors Count: {len(factors)}")
        logger.info("--- Fused Prompt ---")
        logger.info(prompt)
        logger.info("=== End Prompt Fusion ===")

        response = base_resp
        if self.llm_url:
            try:
                print("\n" + "="*80)
                print("LLM调用详细信息")
                print("="*80)
                print(f"服务类型: {self.llm_url}")
                print(f"用户输入: {user_text}")
                print(f"情绪状态: {mood_tag}")
                print(f"用户ID: {user_id}")
                print(f"触摸状态: {touched}")
                print(f"触摸区域: {touch_zone if touched else 'None'}")
                print(f"成长阶段: {self.stage}")
                print(f"人格风格: {style}")
                print(f"人格摘要: {personality_summary}")
                print(f"主导特质: {', '.join(dominant_traits)}")
                print(f"记忆记录数: {len(past)}")
                print(f"记忆摘要: {past_summary[:100]}...")
                print("-" * 80)
                print("发送给LLM的完整提示词:")
                print("-" * 80)
                print(prompt)
                print("-" * 80)
                
                # 同时记录到日志
                logger.info("=" * 80)
                logger.info("LLM调用详细信息")
                logger.info("=" * 80)
                logger.info(f"服务类型: {self.llm_url}")
                logger.info(f"用户输入: {user_text}")
                logger.info(f"情绪状态: {mood_tag}")
                logger.info(f"用户ID: {user_id}")
                logger.info(f"触摸状态: {touched}")
                logger.info(f"触摸区域: {touch_zone if touched else 'None'}")
                logger.info(f"成长阶段: {self.stage}")
                logger.info(f"人格风格: {style}")
                logger.info(f"人格摘要: {personality_summary}")
                logger.info(f"主导特质: {', '.join(dominant_traits)}")
                logger.info(f"记忆记录数: {len(past)}")
                logger.info(f"记忆摘要: {past_summary[:100]}...")
                logger.info("-" * 80)
                logger.info("优化后的提示词:")
                logger.info(prompt)
                
                # 如果是百炼服务，使用异步调用
                if self.llm_url == "qwen" or self.llm_url == "qwen-service":
                    import asyncio
                    from .service_api import async_call_llm
                    print("🚀 调用百炼API...")
                    logger.info("🚀 调用百炼API...")
                    # 检查是否已经在事件循环中
                    try:
                        loop = asyncio.get_running_loop()
                        # 如果已经在事件循环中，使用create_task
                        task = loop.create_task(async_call_llm(prompt, self.llm_url))
                        llm_out = task.result()
                    except RuntimeError:
                        # 如果没有运行的事件循环，使用run
                        llm_out = asyncio.run(async_call_llm(prompt, self.llm_url))
                elif self.llm_url == "doubao":
                    # 豆包服务需要系统提示词
                    system_prompt = f"""你是一个智能机器人助手，具有以下特点：
1. 成长阶段：{self.stage}
2. 人格特质：{personality_summary}
3. 主导特质：{', '.join(dominant_traits)}
4. 当前风格：{style}

### 输出格式规范
请严格按照以下JSON格式输出回复：
{{
    "text": "你的文本回复内容",
    "emotion": "当前情绪状态",
    "action": "相关动作",
    "expression": "表情描述"
}}

请根据用户输入和上下文生成自然、友好的回复，并确保输出格式符合上述JSON规范。"""
                    print("🚀 调用豆包API...")
                    print(f"📋 系统提示词: {system_prompt}")
                    logger.info("🚀 调用豆包API...")
                    logger.info(f"📋 系统提示词: {system_prompt}")
                    from .doubao_service import get_doubao_service
                    service = get_doubao_service()
                    llm_out = service._call_sync(prompt, system_prompt=system_prompt, history=None)
                else:
                    print(f"🚀 调用其他API: {self.llm_url}")
                    logger.info(f"🚀 调用其他API: {self.llm_url}")
                    llm_out = call_llm(prompt, self.llm_url)
                
                print("\n" + "="*80)
                print("📤 LLM原始输出:")
                print("="*80)
                print(llm_out)
                print("="*80)
                logger.info(f"📤 LLM原始输出: {llm_out}")
                
                if llm_out and llm_out.strip():
                    # 尝试解析LLM返回的JSON格式
                    raw_response = llm_out.strip()
                    print(f"📤 LLM原始输出: {raw_response}")
                    logger.info(f"📤 LLM原始输出: {raw_response}")
                    
                    # 尝试解析JSON格式的响应
                    try:
                        import json
                        # 检查是否包含JSON格式
                        if raw_response.strip().startswith('{') and raw_response.strip().endswith('}'):
                            parsed_response = json.loads(raw_response)
                            if isinstance(parsed_response, dict):
                                # 提取text字段
                                if 'text' in parsed_response:
                                    response = parsed_response['text']
                                    print(f"✅ 成功解析JSON格式响应: {response}")
                                    logger.info(f"✅ 成功解析JSON格式响应: {response}")
                                    
                                    # 保存解析出的其他字段，供后续使用
                                    if 'emotion' in parsed_response:
                                        self._parsed_emotion = parsed_response['emotion']
                                        print(f"📊 解析出情绪: {parsed_response['emotion']}")
                                    if 'action' in parsed_response:
                                        self._parsed_action = parsed_response['action']
                                        print(f"🤸 解析出动作: {parsed_response['action']}")
                                    if 'expression' in parsed_response:
                                        self._parsed_expression = parsed_response['expression']
                                        print(f"🎭 解析出表情: {parsed_response['expression']}")
                                else:
                                    response = raw_response
                                    print("⚠️ JSON格式不包含text字段，使用原始响应")
                                    logger.warning("⚠️ JSON格式不包含text字段，使用原始响应")
                            else:
                                response = raw_response
                                print("⚠️ 解析的JSON不是字典格式，使用原始响应")
                                logger.warning("⚠️ 解析的JSON不是字典格式，使用原始响应")
                        else:
                            response = raw_response
                            print("✅ 使用原始文本响应")
                            logger.info("✅ 使用原始文本响应")
                    except json.JSONDecodeError:
                        response = raw_response
                        print("⚠️ JSON解析失败，使用原始响应")
                        logger.warning("⚠️ JSON解析失败，使用原始响应")
                    except Exception as e:
                        response = raw_response
                        print(f"⚠️ 响应处理异常: {e}，使用原始响应")
                        logger.warning(f"⚠️ 响应处理异常: {e}，使用原始响应")
                else:
                    print("⚠️ LLM返回空响应，使用基础回复")
                    logger.warning("⚠️ LLM返回空响应，使用基础回复")
            except Exception as e:
                print(f"❌ LLM调用失败: {e}, 使用基础回复")
                logger.error(f"❌ LLM调用失败: {e}, 使用基础回复")
                response = base_resp
        else:
            print("⚠️ 未配置LLM URL，使用基础回复")
            logger.warning("⚠️ 未配置LLM URL，使用基础回复")

        # 4. store this interaction in memory
        self.memory.add_memory(
            user_text,
            response,
            mood_tag,
            user_id,
            touched,
            touch_zone,
        )
        logger.debug("Memory stored for user %s", user_id)

        # 5. derive action and expression from mood
        mood_key = mood_tag if mood_tag in FACE_ANIMATION_MAP else "happy"
        face_anim = FACE_ANIMATION_MAP.get(mood_key, ("E000:平静表情", "自然状态、轻微呼吸动作"))
        expression = f"{face_anim[0]} | {face_anim[1]}".strip()

        # 获取动作列表，格式：动作编号+动作+角度+说明
        action_raw = ACTION_MAP.get(mood_key, "A000:breathing|轻微呼吸动作")
        action_parts = action_raw.split("|")
        action = []
        
        # 将动作字符串解析为结构化动作列表
        for i in range(0, len(action_parts), 2):
            if i + 1 < len(action_parts):
                action_code = action_parts[i].strip()
                action_desc = action_parts[i + 1].strip()
                action.append(f"{action_code}|{action_desc}")
            else:
                action.append(action_parts[i].strip())
        
        if touched:
            # 添加触摸动作
            touch_actions = {
                0: "A100:hug|拥抱动作",
                1: "A101:pat|轻拍动作", 
                2: "A102:tickle|挠痒动作"
            }
            touch_action = touch_actions.get(touch_zone, "A100:hug|拥抱动作")
            action.append(touch_action)
        
        print("\n" + "="*80)
        print("🎭 表情输出:")
        print("="*80)
        print(expression)
        print("="*80)
        print("\n" + "="*80)
        print("🤸 动作输出:")
        print("="*80)
        print(action)
        print("="*80)
        
        logger.info("🎭 表情输出: %s", expression)
        logger.info("🤸 动作输出: %s", action)

        # TTS generates an audio URL when service is provided
        audio_url = call_tts(response, self.tts_url) if self.tts_url else ""
        if not audio_url:
            audio_url = "n/a"  # 保证音频字段不为空

        print("\n" + "="*80)
        print("🎯 最终生成的回复:")
        print("="*80)
        print(response)
        print("="*80)
        logger.info("Generated response: %s", response)

        return DialogueResponse(
            text=response,
            audio=audio_url,
            action=action,
            expression=expression,
        )