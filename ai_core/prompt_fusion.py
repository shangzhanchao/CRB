"""提示词融合算法

将各种影响因子（成长阶段、人格特质、情绪、触摸、记忆等）智能融合为一个优化的提示词。
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class PromptFactor:
    """提示词因子"""
    name: str
    content: str
    weight: float = 1.0
    priority: int = 0
    is_required: bool = False
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RobotAction:
    """机器人动作指令"""
    action_code: str
    description: str
    parameters: Dict = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


@dataclass
class RobotExpression:
    """机器人表情指令"""
    expression_code: str
    description: str
    animation_params: Dict = None
    
    def __post_init__(self):
        if self.animation_params is None:
            self.animation_params = {}


class PromptFusionEngine:
    """提示词融合引擎 - 分层结构化设计"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def create_comprehensive_prompt(
        self,
        factors: List[PromptFactor],
        robot_actions: List[RobotAction] = None,
        robot_expressions: List[RobotExpression] = None,
        context_info: Dict = None
    ) -> str:
        """创建交互级提示词 - 专注于当前交互上下文和具体输出要求
        
        Parameters
        ----------
        factors : List[PromptFactor]
            各种影响因子
        robot_actions : List[RobotAction], optional
            机器人动作指令列表
        robot_expressions : List[RobotExpression], optional
            机器人表情指令列表
        context_info : Dict, optional
            上下文信息
            
        Returns
        -------
        str
            交互级提示词，专注于当前交互和具体输出
        """
        self.logger.debug("开始创建交互级提示词...")
        
        # 1. 验证必需因子
        self._validate_required_factors(factors)
        
        # 2. 按优先级排序
        sorted_factors = sorted(factors, key=lambda x: x.priority, reverse=True)
        
        # 3. 构建交互级提示词
        prompt_template = self._build_interaction_template(
            sorted_factors, robot_actions, robot_expressions, context_info
        )
        
        # 4. 后处理优化
        optimized_prompt = self._post_process_template(prompt_template)
        
        self.logger.debug(f"交互级提示词创建完成，长度: {len(optimized_prompt)}")
        return optimized_prompt
    
    def _build_interaction_template(
        self,
        factors: List[PromptFactor],
        robot_actions: List[RobotAction],
        robot_expressions: List[RobotExpression],
        context_info: Dict
    ) -> str:
        """构建交互级提示词模板"""
        
        # 按类别分组因子
        grouped_factors = self._group_factors(factors)
        
        # 构建交互级结构
        sections = []
        
        # 1. 当前交互状态
        interaction_state = self._build_interaction_state_section(grouped_factors, context_info)
        sections.append(interaction_state)
        
        # 2. 用户输入和上下文
        user_context = self._build_user_context_section(grouped_factors)
        sections.append(user_context)
        
        # 3. 当前可用动作和表情
        current_actions = self._build_current_actions_section(robot_actions, robot_expressions)
        sections.append(current_actions)
        
        # 4. 记忆引用（如果有）
        memory_reference = self._build_memory_reference_section(grouped_factors)
        if memory_reference:
            sections.append(memory_reference)
        
        # 5. 具体输出要求
        output_requirements = self._build_specific_output_requirements(grouped_factors)
        sections.append(output_requirements)
        
        # 组合所有部分
        template = "\n\n".join(sections)
        
        return template
    
    def _build_interaction_state_section(self, grouped_factors: Dict, context_info: Dict) -> str:
        """构建当前交互状态部分"""
        state_parts = []
        
        state_parts.append("## 当前交互状态")
        
        # 当前情绪状态
        if "user_emotion" in grouped_factors and grouped_factors["user_emotion"]:
            emotion_factor = max(grouped_factors["user_emotion"], key=lambda x: x.weight)
            emotion_content = self._convert_emotion_to_chinese_description(emotion_factor.content)
            state_parts.append(f"用户情绪: {emotion_content}")
        
        # 触摸状态
        if context_info and "触摸状态" in context_info:
            if context_info["触摸状态"] == "是":
                touch_zone = context_info.get("触摸区域", "未知")
                state_parts.append(f"触摸互动: 正在体验温暖的触摸（区域：{touch_zone}）")
                state_parts.append("触摸感受: 被温柔地安抚，感到被关心和爱护")
            else:
                state_parts.append("触摸互动: 无")
        
        # 成长阶段状态
        if "growth_stage" in grouped_factors and grouped_factors["growth_stage"]:
            stage_factor = max(grouped_factors["growth_stage"], key=lambda x: x.weight)
            stage = self._extract_stage_name(stage_factor.content)
            stage_desc = self._convert_stage_to_chinese_description(stage_factor.content)
            state_parts.append(f"成长阶段: {stage_desc}")
        
        # 人格风格状态
        if "personality" in grouped_factors and grouped_factors["personality"]:
            personality_parts = []
            for factor in grouped_factors["personality"]:
                converted_content = self._convert_personality_to_chinese_description(factor.content)
                personality_parts.append(converted_content)
            state_parts.append(f"人格特质: {', '.join(personality_parts)}")
        
        return "\n".join(state_parts)
    
    def _build_user_context_section(self, grouped_factors: Dict) -> str:
        """构建用户输入和上下文部分"""
        context_parts = []
        
        context_parts.append("## 用户输入和上下文")
        
        # 用户输入
        if "user_input" in grouped_factors and grouped_factors["user_input"]:
            user_input_factor = max(grouped_factors["user_input"], key=lambda x: x.weight)
            user_text = user_input_factor.content
            
            if user_text and user_text.strip():
                context_parts.append(f"用户说: {user_text}")
            else:
                context_parts.append("用户说: （无文本输入）")
        else:
            context_parts.append("用户说: （无文本输入）")
        
        # 触摸交互上下文
        if "touch_interaction" in grouped_factors and grouped_factors["touch_interaction"]:
            touch_factor = max(grouped_factors["touch_interaction"], key=lambda x: x.weight)
            if touch_factor.content and touch_factor.content.strip():
                context_parts.append(f"触摸上下文: {touch_factor.content}")
        
        return "\n".join(context_parts)
    
    def _build_current_actions_section(self, robot_actions: List[RobotAction], robot_expressions: List[RobotExpression]) -> str:
        """构建当前可用动作和表情部分"""
        actions_parts = []
        
        actions_parts.append("## 当前可用动作和表情")
        
        # 当前动作
        if robot_actions:
            action_descriptions = []
            for action in robot_actions:
                action_desc = f"{action.action_code}: {action.description}"
                action_descriptions.append(action_desc)
            actions_parts.append(f"可用动作: {'; '.join(action_descriptions)}")
        else:
            actions_parts.append("可用动作: 无")
        
        # 当前表情
        if robot_expressions:
            expression_descriptions = []
            for expr in robot_expressions:
                expr_desc = f"{expr.expression_code}: {expr.description}"
                expression_descriptions.append(expr_desc)
            actions_parts.append(f"可用表情: {'; '.join(expression_descriptions)}")
        else:
            actions_parts.append("可用表情: 无")
        
        return "\n".join(actions_parts)
    
    def _build_memory_reference_section(self, grouped_factors: Dict) -> str:
        """构建记忆引用部分"""
        memory_parts = []
        
        # 检查是否有记忆信息
        if "memory" in grouped_factors and grouped_factors["memory"]:
            memory_factor = max(grouped_factors["memory"], key=lambda x: x.weight)
            memory_content = memory_factor.content
            
            # 如果记忆内容不为空，则添加记忆部分
            if memory_content and memory_content.strip():
                memory_parts.append("## 相关记忆引用")
                memory_parts.append(f"记忆内容: {memory_content}")
                
                # 尝试解析记忆信息中的详细信息
                try:
                    if hasattr(memory_factor, 'metadata') and memory_factor.metadata:
                        memory_details = memory_factor.metadata.get('details', [])
                        if memory_details:
                            memory_parts.append("最近对话记录:")
                            for i, detail in enumerate(memory_details[:2], 1):  # 只显示最近2条
                                user_text = detail.get('user_text', '')
                                ai_response = detail.get('ai_response', '')
                                mood = detail.get('mood_tag', 'neutral')
                                memory_parts.append(f"  {i}. 用户: {user_text}")
                                memory_parts.append(f"     机器人: {ai_response} (情绪: {mood})")
                except Exception as e:
                    self.logger.debug(f"解析记忆详细信息失败: {e}")
                
                return "\n".join(memory_parts)
        
        # 如果没有记忆信息，返回空字符串
        return ""
    
    def _build_specific_output_requirements(self, grouped_factors: Dict) -> str:
        """构建具体输出要求部分"""
        requirements_parts = []
        
        requirements_parts.append("## 具体输出要求")
        
        # 根据成长阶段定制要求
        if "growth_stage" in grouped_factors and grouped_factors["growth_stage"]:
            stage_factor = max(grouped_factors["growth_stage"], key=lambda x: x.weight)
            stage = self._extract_stage_name(stage_factor.content)
            
            if stage == "sprout":
                requirements_parts.append("1. 用咿呀声和简单动作回应，语言能力有限")
            elif stage == "enlighten":
                requirements_parts.append("1. 可以模仿并回答简短问候，语言逐渐丰富")
            elif stage == "resonate":
                requirements_parts.append("1. 用关心的短句和简单问题交流，情感表达丰富")
            elif stage == "awaken":
                requirements_parts.append("1. 根据记忆主动提出建议，具备完整的对话能力")
            else:
                requirements_parts.append("1. 符合当前成长阶段的情感表达方式")
        
        # 根据性格特点定制要求
        if "personality" in grouped_factors and grouped_factors["personality"]:
            personality_traits = []
            for factor in grouped_factors["personality"]:
                trait = self._extract_personality_trait(factor.content)
                if trait:
                    personality_traits.append(trait)
            
            if personality_traits:
                requirements_parts.append(f"2. 体现性格特点：{', '.join(personality_traits)}")
            else:
                requirements_parts.append("2. 体现性格特点，展现独特的个性")
        else:
            requirements_parts.append("2. 体现性格特点，展现独特的个性")
        
        # 根据记忆情况定制要求
        if "memory" in grouped_factors and grouped_factors["memory"]:
            memory_factor = max(grouped_factors["memory"], key=lambda x: x.weight)
            memory_content = memory_factor.content
            
            if memory_content and memory_content.strip():
                requirements_parts.append("3. 自然地融入记忆内容，体现个性化")
            else:
                requirements_parts.append("3. 建立新的记忆连接，为后续互动做准备")
        else:
            requirements_parts.append("3. 自然地融入记忆内容，体现个性化")
        
        # 根据触摸交互定制要求
        if "touch_interaction" in grouped_factors and grouped_factors["touch_interaction"]:
            requirements_parts.append("4. 对触摸互动进行回应，不要有任何触摸相关的内容，只输出语气词（如'嗯~'、'啊~'、'唔~'等）和动作表情指令（如A112:loving_nod、E025:loving_smile）")
        else:
            requirements_parts.append("4. 保持自然的对话风格，体现情感连接")
        
        # 添加输出格式要求
        requirements_parts.append("5. 表达要自然、简洁，不超过50字")
        # 强制模型输出固定JSON四字段
        requirements_parts.append("6. 必须仅输出包含四个字段的JSON：text、emotion、action(数组)、expression，不得输出多余内容")
        requirements_parts.append("7. 系统会自动根据语义选择合适的动作和表情代码")
        requirements_parts.append("8. 动作和表情代码库已完整定义，包括：")
        requirements_parts.append("   - 基础动作：A000-A025 (呼吸、点头、摇摆等)")
        requirements_parts.append("   - 触摸动作：A100-A114 (温柔、信任、亲密等)")
        requirements_parts.append("   - 基础表情：E000-E012 (平静、微笑、困惑等)")
        requirements_parts.append("   - 触摸表情：E020-E027 (温柔、信任、亲密等)")
        
        return "\n".join(requirements_parts)
    
    def _extract_stage_name(self, stage_content: str) -> str:
        """提取成长阶段名称"""
        stage_mapping = {
            "sprout": "sprout",
            "enlighten": "enlighten", 
            "resonate": "resonate",
            "awaken": "awaken"
        }
        
        for stage, _ in stage_mapping.items():
            if stage in stage_content.lower():
                return stage
        
        return "awaken"  # 默认返回觉醒期
    
    def _extract_personality_trait(self, personality_content: str) -> str:
        """提取人格特质名称"""
        trait_mapping = {
            "openness": "好奇心强，喜欢探索新事物",
            "conscientiousness": "做事认真负责，有条理",
            "extraversion": "外向开朗，喜欢社交互动",
            "agreeableness": "友善温和，乐于助人",
            "neuroticism": "情感敏感，富有同理心"
        }
        
        for trait, description in trait_mapping.items():
            if trait in personality_content.lower():
                return description
        
        return ""
    
    def _convert_stage_to_chinese_description(self, stage_content: str) -> str:
        """将成长阶段转换为中文描述"""
        stage_mapping = {
            "sprout": "萌芽期 - 用咿呀声和简单动作回应，语言能力有限，主要表达基本情感",
            "enlighten": "启蒙期 - 可以模仿并回答简短问候，开始学习基本交流，语言逐渐丰富",
            "resonate": "共鸣期 - 用关心的短句和简单问题交流，情感表达更丰富，能够理解用户情绪",
            "awaken": "觉醒期 - 根据记忆主动提出建议并互动，具备完整的对话能力，能够深度理解用户需求"
        }
        
        # 提取阶段名称
        for stage, description in stage_mapping.items():
            if stage in stage_content.lower():
                return description
        
        return stage_content
    
    def _convert_personality_to_chinese_description(self, personality_content: str) -> str:
        """将人格特质转换为中文描述"""
        personality_mapping = {
            "openness": "好奇心强，喜欢探索新事物，思维开放",
            "conscientiousness": "做事认真负责，有条理，注重细节",
            "extraversion": "外向开朗，喜欢社交互动，表达积极",
            "agreeableness": "友善温和，乐于助人，富有同情心",
            "neuroticism": "情感敏感，容易察觉他人情绪，富有同理心",
            "curious": "好奇心强，喜欢探索新事物",
            "reliable": "做事认真负责，有条理",
            "outgoing": "外向开朗，喜欢社交互动",
            "kind": "友善温和，乐于助人",
            "sensitive": "情感敏感，容易察觉他人情绪"
        }
        
        # 检查是否包含特定特质
        for trait, description in personality_mapping.items():
            if trait in personality_content.lower():
                return description
        
        return personality_content
    
    def _convert_personality_style_to_chinese_description(self, style: str) -> str:
        """将人格风格转换为中文描述"""
        style_mapping = {
            "enthusiastic": "热情开朗，充满活力，喜欢积极表达情感，语言生动有趣",
            "cold": "冷静理性，内敛含蓄，表达方式较为克制，思维缜密",
            "neutral": "温和平衡，表达自然，情感适中，善于倾听"
        }
        
        return style_mapping.get(style, style)
    
    def _convert_emotion_to_chinese_description(self, emotion_content: str) -> str:
        """将情绪转换为中文描述"""
        emotion_mapping = {
            "happy": "开心愉悦，积极向上，充满正能量",
            "sad": "感到难过，需要安慰，情感脆弱",
            "angry": "有些生气，需要理解，情绪激动",
            "fear": "感到害怕，需要保护，内心不安",
            "surprise": "感到惊讶，充满好奇，反应强烈",
            "disgust": "感到厌恶，需要远离，情绪排斥",
            "calm": "平静放松，状态良好，内心平和",
            "excited": "兴奋激动，充满活力，情绪高涨",
            "tired": "感到疲惫，需要休息，状态不佳",
            "bored": "感到无聊，需要刺激，缺乏兴趣",
            "confused": "感到困惑，需要解释，思维混乱",
            "shy": "害羞腼腆，需要鼓励，表达含蓄",
            "neutral": "情绪平静，状态正常，反应适中"
        }
        
        # 检查是否包含特定情绪
        for emotion, description in emotion_mapping.items():
            if emotion in emotion_content.lower():
                return description
        
        return emotion_content
    
    def _convert_memory_to_chinese_description(self, memory_content: str) -> str:
        """将记忆信息转换为中文描述，注重情感体验"""
        if "记忆记录" in memory_content:
            return "有美好的回忆可以分享，这些经历让我感到温暖"
        elif "记忆摘要" in memory_content:
            return f"记得：{memory_content}，这些记忆让我更加了解你"
        elif "说过" in memory_content:
            return f"记得你{memory_content}，这让我感到被重视"
        elif "经常" in memory_content:
            return f"我们{memory_content}，这让我感到温暖和亲密"
        elif "心情" in memory_content:
            return f"我注意到{memory_content}，想要给你更多关心和支持"
        else:
            return memory_content
    
    def _convert_touch_zone_to_chinese_description(self, touch_zone: str) -> str:
        """将触摸区域转换为中文描述，注重情感体验和共情效果"""
        touch_mapping = {
            "0": "感受到温暖的抚摸，内心充满安全感和被关爱的温暖",
            "1": "被温柔地安抚，感到被关心和爱护，产生深厚的信任感",
            "2": "体验到亲密的接触，内心充满温暖，感受到深深的爱意"
        }
        
        return touch_mapping.get(touch_zone, "感受到用户的温暖接触，内心充满感激")
    
    def _validate_required_factors(self, factors: List[PromptFactor]) -> None:
        """验证必需因子"""
        required_factors = [f for f in factors if f.is_required]
        if not required_factors:
            raise ValueError("至少需要一个必需因子")
    
    def _group_factors(self, factors: List[PromptFactor]) -> Dict[str, List[PromptFactor]]:
        """按类别分组因子"""
        grouped = {}
        
        for factor in factors:
            # 特殊处理某些因子，保持完整名称
            if factor.name in ["user_input", "user_emotion", "touch_interaction", "memory_summary"]:
                category = factor.name
            else:
                category = factor.name.split('_')[0] if '_' in factor.name else factor.name
            
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(factor)
        
        return grouped
    
    def _post_process_template(self, template: str) -> str:
        """后处理优化提示词模板"""
        # 1. 移除重复内容
        template = self._remove_duplicates(template)
        
        # 2. 优化格式
        template = self._optimize_formatting(template)
        
        return template
    
    def _remove_duplicates(self, template: str) -> str:
        """移除重复内容"""
        lines = template.split('\n')
        seen = set()
        unique_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and line_stripped not in seen:
                seen.add(line_stripped)
                unique_lines.append(line)
            elif not line_stripped:
                unique_lines.append(line)
        
        return '\n'.join(unique_lines)
    
    def _optimize_formatting(self, template: str) -> str:
        """优化格式"""
        # 移除多余的空行
        lines = template.split('\n')
        optimized_lines = []
        
        for i, line in enumerate(lines):
            if line.strip() or (i > 0 and lines[i-1].strip()):
                optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def fuse_prompts(self, factors: List[PromptFactor]) -> str:
        """简单的提示词融合方法（向后兼容）"""
        return self.create_comprehensive_prompt(factors)


def create_prompt_factors(
    stage_info: Optional[Dict] = None,
    personality_info: Optional[Dict] = None,
    emotion_info: Optional[Dict] = None,
    touch_info: Optional[Dict] = None,
    memory_info: Optional[Dict] = None,
    user_input: Optional[str] = None,
) -> List[PromptFactor]:
    """创建提示词因子列表"""
    factors = []
    
    # 1. 成长阶段因子（必需）
    if stage_info and "prompt" in stage_info:
        factors.append(PromptFactor(
            name="growth_stage",
            content=stage_info["prompt"],
            weight=1.5,
            priority=5,
            is_required=True
        ))
    
    # 2. 人格特质因子
    if personality_info:
        if "traits" in personality_info:
            factors.append(PromptFactor(
                name="personality",
                content=personality_info["traits"],
                weight=1.2,
                priority=4
            ))
        
        if "style" in personality_info:
            factors.append(PromptFactor(
                name="personality_style",
                content=personality_info["style"],
                weight=1.0,
                priority=3
            ))
    
    # 3. 用户情绪因子
    if emotion_info and "emotion" in emotion_info:
        factors.append(PromptFactor(
            name="user_emotion",
            content=emotion_info["emotion"],
            weight=1.0,
            priority=3
        ))
    
    # 4. 触摸交互因子
    if touch_info and "content" in touch_info and touch_info["content"]:
        factors.append(PromptFactor(
            name="touch_interaction",
            content=touch_info["content"],
            weight=0.8,
            priority=2
        ))
    
    # 5. 记忆信息因子（修复数据获取问题）
    if memory_info:
        # 记忆摘要
        if "summary" in memory_info and memory_info["summary"]:
            memory_factor = PromptFactor(
                name="memory",
                content=memory_info["summary"],
                weight=0.6,
                priority=1
            )
            # 添加详细的记忆信息作为元数据
            if "details" in memory_info and memory_info["details"]:
                memory_factor.metadata = {
                    "details": memory_info["details"],
                    "count": memory_info.get("count", 0),
                    "session_id": memory_info.get("session_id", "")
                }
            factors.append(memory_factor)
        
        # 上下文摘要
        if "context" in memory_info and memory_info["context"]:
            factors.append(PromptFactor(
                name="memory_context",
                content=memory_info["context"],
                weight=0.5,
                priority=1
            ))
        
        # 记忆统计信息
        if "count" in memory_info:
            factors.append(PromptFactor(
                name="memory_stats",
                content=f"记忆记录数量: {memory_info['count']}条",
                weight=0.3,
                priority=0
            ))
    
    # 6. 用户输入因子（必需）
    if user_input:
        factors.append(PromptFactor(
            name="user_input",
            content=user_input,
            weight=2.0,
            priority=6,
            is_required=True
        ))
    
    return factors


def create_robot_actions_from_emotion(emotion: str) -> List[RobotAction]:
    """根据情绪创建机器人动作指令（包含指令代码，支持多组）"""
    from .constants import ACTION_MAP
    
    actions = []
    
    # 获取动作映射
    action_raw = ACTION_MAP.get(emotion, ACTION_MAP.get("neutral", "A000:breathing|轻微呼吸动作"))
    
    # 解析动作字符串（格式：A001:action1|desc1|A002:action2|desc2）
    action_parts = action_raw.split("|")
    
    for i in range(0, len(action_parts), 2):
        if i + 1 < len(action_parts):
            action_code = action_parts[i].strip()
            action_desc = action_parts[i + 1].strip()
            
            # 创建RobotAction对象，包含指令代码
            action = RobotAction(
                action_code=action_code,
                description=action_desc,
                parameters={}
            )
            actions.append(action)
        else:
            # 处理单个动作的情况
            action_code = action_parts[i].strip()
            action = RobotAction(
                action_code=action_code,
                description=f"{action_code}动作",
                parameters={}
            )
            actions.append(action)
    
    return actions


def create_robot_expressions_from_emotion(emotion: str) -> List[RobotExpression]:
    """根据情绪创建机器人表情指令（包含指令代码，支持多组）"""
    from .constants import FACE_ANIMATION_MAP
    
    expressions = []
    
    # 获取表情映射
    face_anim = FACE_ANIMATION_MAP.get(emotion, FACE_ANIMATION_MAP.get("neutral", ("E000:平静表情", "自然状态、轻微呼吸动作")))
    
    # 解析表情代码和描述
    expression_code = face_anim[0]  # 例如："E001:微笑+眨眼+眼神上扬"
    expression_desc = face_anim[1]  # 例如："亮眼色彩、头部轻摆、手臂小幅打开"
    
    # 支持多个表情组合（用+分隔）
    expression_parts = expression_code.split("+")
    
    for part in expression_parts:
        part = part.strip()
        if part:
            # 创建RobotExpression对象，包含指令代码
            expression = RobotExpression(
                expression_code=part,
                description=expression_desc,
                animation_params={}
            )
            expressions.append(expression)
    
    # 如果没有解析到表情，创建默认表情
    if not expressions:
        expression = RobotExpression(
            expression_code=expression_code,
            description=expression_desc,
            animation_params={}
        )
        expressions.append(expression)
    
    return expressions 