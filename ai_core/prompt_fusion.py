"""提示词融合算法

将各种影响因子（成长阶段、人格特质、情绪、触摸、记忆等）智能融合为一个优化的提示词。
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PromptFactor:
    """提示词因子"""
    name: str
    content: str
    weight: float = 1.0
    priority: int = 0
    is_required: bool = False


class PromptFusionEngine:
    """提示词融合引擎"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def fuse_prompts(self, factors: List[PromptFactor]) -> str:
        """融合多个提示词因子
        
        Parameters
        ----------
        factors : List[PromptFactor]
            提示词因子列表
            
        Returns
        -------
        str
            融合后的优化提示词
        """
        self.logger.debug("开始提示词融合...")
        self.logger.debug(f"输入因子数量: {len(factors)}")
        
        # 1. 验证必需因子
        self._validate_required_factors(factors)
        
        # 2. 按优先级排序
        sorted_factors = sorted(factors, key=lambda x: x.priority, reverse=True)
        
        # 3. 构建融合策略
        fusion_strategy = self._build_fusion_strategy(sorted_factors)
        
        # 4. 执行融合
        fused_prompt = self._execute_fusion(sorted_factors, fusion_strategy)
        
        # 5. 后处理优化
        optimized_prompt = self._post_process(fused_prompt)
        
        self.logger.debug(f"融合完成，最终提示词长度: {len(optimized_prompt)}")
        self.logger.debug(f"最终提示词: {optimized_prompt}")
        
        return optimized_prompt
    
    def _validate_required_factors(self, factors: List[PromptFactor]) -> None:
        """验证必需因子是否存在"""
        required_factors = [f for f in factors if f.is_required]
        missing_required = []
        
        # 检查用户输入是否必需
        user_input_found = any(f.name == "user_input" for f in factors)
        if not user_input_found:
            missing_required.append("user_input")
        
        if missing_required:
            raise ValueError(f"缺少必需因子: {missing_required}")
    
    def _build_fusion_strategy(self, factors: List[PromptFactor]) -> Dict[str, any]:
        """构建融合策略"""
        strategy = {
            "stage_weight": 1.5,      # 成长阶段权重
            "personality_weight": 1.2, # 人格特质权重
            "emotion_weight": 1.0,     # 情绪权重
            "touch_weight": 0.8,       # 触摸权重
            "memory_weight": 0.6,      # 记忆权重
            "max_length": 2000,        # 最大长度
            "separator": " | ",        # 分隔符
        }
        
        # 根据因子数量调整策略
        if len(factors) > 8:
            strategy["separator"] = "\n"
            strategy["max_length"] = 1500
        
        return strategy
    
    def _execute_fusion(self, factors: List[PromptFactor], strategy: Dict) -> str:
        """执行融合算法"""
        self.logger.debug("执行融合算法...")
        
        # 按类别分组
        grouped_factors = self._group_factors(factors)
        
        # 构建各部分
        parts = []
        
        # 1. 成长阶段部分（最高优先级）
        if "stage" in grouped_factors:
            stage_part = self._build_stage_section(grouped_factors["stage"], strategy)
            if stage_part:
                parts.append(stage_part)
        
        # 2. 人格特质部分
        if "personality" in grouped_factors:
            personality_part = self._build_personality_section(grouped_factors["personality"], strategy)
            if personality_part:
                parts.append(personality_part)
        
        # 3. 交互信息部分
        interaction_part = self._build_interaction_section(grouped_factors, strategy)
        if interaction_part:
            parts.append(interaction_part)
        
        # 4. 用户输入部分（必需）
        if "user_input" in grouped_factors:
            user_part = self._build_user_section(grouped_factors["user_input"], strategy)
            if user_part:
                parts.append(user_part)
        
        # 5. 记忆部分（可选）
        if "memory" in grouped_factors:
            memory_part = self._build_memory_section(grouped_factors["memory"], strategy)
            if memory_part:
                parts.append(memory_part)
        
        # 组合所有部分
        fused_prompt = strategy["separator"].join(parts)
        
        self.logger.debug(f"融合后提示词长度: {len(fused_prompt)}")
        return fused_prompt
    
    def _group_factors(self, factors: List[PromptFactor]) -> Dict[str, List[PromptFactor]]:
        """按类别分组因子"""
        groups = {
            "stage": [],
            "personality": [],
            "emotion": [],
            "touch": [],
            "memory": [],
            "user_input": [],
            "other": []
        }
        
        for factor in factors:
            if "stage" in factor.name.lower():
                groups["stage"].append(factor)
            elif "personality" in factor.name.lower() or "trait" in factor.name.lower():
                groups["personality"].append(factor)
            elif "emotion" in factor.name.lower() or "mood" in factor.name.lower():
                groups["emotion"].append(factor)
            elif "touch" in factor.name.lower():
                groups["touch"].append(factor)
            elif "memory" in factor.name.lower() or "past" in factor.name.lower():
                groups["memory"].append(factor)
            elif "user" in factor.name.lower() or "input" in factor.name.lower():
                groups["user_input"].append(factor)
            else:
                groups["other"].append(factor)
        
        return groups
    
    def _build_stage_section(self, stage_factors: List[PromptFactor], strategy: Dict) -> str:
        """构建成长阶段部分"""
        if not stage_factors:
            return ""
        
        # 取权重最高的阶段因子
        best_stage = max(stage_factors, key=lambda x: x.weight)
        
        # 构建双语提示
        stage_parts = []
        if "stage" in best_stage.content.lower():
            stage_parts.append(f"Stage: {best_stage.content}")
        if "阶段" in best_stage.content or "期" in best_stage.content:
            stage_parts.append(f"阶段: {best_stage.content}")
        
        return " | ".join(stage_parts)
    
    def _build_personality_section(self, personality_factors: List[PromptFactor], strategy: Dict) -> str:
        """构建人格特质部分"""
        if not personality_factors:
            return ""
        
        # 按权重排序
        sorted_personality = sorted(personality_factors, key=lambda x: x.weight, reverse=True)
        
        personality_parts = []
        trait_parts = []
        style_parts = []
        
        for factor in sorted_personality:
            if "trait" in factor.name.lower():
                trait_parts.append(factor.content)
            elif "style" in factor.name.lower():
                style_parts.append(factor.content)
            else:
                personality_parts.append(factor.content)
        
        # 组合人格信息
        combined_parts = []
        if personality_parts:
            combined_parts.append(f"Personality: {' | '.join(personality_parts)}")
        if trait_parts:
            combined_parts.append(f"Traits: {', '.join(trait_parts)}")
        if style_parts:
            combined_parts.append(f"Style: {' | '.join(style_parts)}")
        
        return " | ".join(combined_parts)
    
    def _build_interaction_section(self, grouped_factors: Dict, strategy: Dict) -> str:
        """构建交互信息部分"""
        interaction_parts = []
        
        # 情绪信息
        if "emotion" in grouped_factors and grouped_factors["emotion"]:
            emotion_factor = max(grouped_factors["emotion"], key=lambda x: x.weight)
            if emotion_factor.content and emotion_factor.content != "neutral":
                interaction_parts.append(f"User emotion: {emotion_factor.content}")
        
        # 触摸信息
        if "touch" in grouped_factors and grouped_factors["touch"]:
            touch_factor = max(grouped_factors["touch"], key=lambda x: x.weight)
            if touch_factor.content:
                interaction_parts.append(f"Touch: {touch_factor.content}")
        
        return " | ".join(interaction_parts)
    
    def _build_user_section(self, user_factors: List[PromptFactor], strategy: Dict) -> str:
        """构建用户输入部分"""
        if not user_factors:
            return ""
        
        # 取最重要的用户输入
        best_user = max(user_factors, key=lambda x: x.weight)
        return f"User: {best_user.content}"
    
    def _build_memory_section(self, memory_factors: List[PromptFactor], strategy: Dict) -> str:
        """构建记忆部分"""
        if not memory_factors:
            return ""
        
        # 合并所有记忆信息
        memory_contents = [f.content for f in memory_factors if f.content.strip()]
        if memory_contents:
            # 限制记忆长度
            memory_text = " ".join(memory_contents)
            if len(memory_text) > 200:
                memory_text = memory_text[:200] + "..."
            return f"Memory: {memory_text}"
        
        return ""
    
    def _post_process(self, prompt: str) -> str:
        """后处理优化"""
        # 1. 移除重复内容
        prompt = self._remove_duplicates(prompt)
        
        # 2. 优化分隔符
        prompt = self._optimize_separators(prompt)
        
        # 3. 截断过长内容
        if len(prompt) > 2000:
            prompt = prompt[:2000] + "..."
        
        # 4. 清理空白
        prompt = " ".join(prompt.split())
        
        return prompt
    
    def _remove_duplicates(self, prompt: str) -> str:
        """移除重复内容"""
        parts = prompt.split(" | ")
        seen = set()
        unique_parts = []
        
        for part in parts:
            # 提取关键信息
            key = part.split(":")[0] if ":" in part else part
            if key not in seen:
                seen.add(key)
                unique_parts.append(part)
        
        return " | ".join(unique_parts)
    
    def _optimize_separators(self, prompt: str) -> str:
        """优化分隔符"""
        # 替换多余的分隔符
        prompt = prompt.replace(" |  | ", " | ")
        prompt = prompt.replace(" | | ", " | ")
        
        # 清理开头和结尾的分隔符
        prompt = prompt.strip(" |")
        
        return prompt


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
    
    # 成长阶段因子
    if stage_info:
        factors.append(PromptFactor(
            name="growth_stage",
            content=stage_info.get("prompt", ""),
            weight=1.5,
            priority=5,
            is_required=True
        ))
    
    # 人格特质因子
    if personality_info:
        if "traits" in personality_info:
            factors.append(PromptFactor(
                name="personality_traits",
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
    
    # 情绪因子
    if emotion_info and emotion_info.get("emotion") != "neutral":
        factors.append(PromptFactor(
            name="user_emotion",
            content=emotion_info["emotion"],
            weight=1.0,
            priority=3
        ))
    
    # 触摸因子
    if touch_info and touch_info.get("content"):
        factors.append(PromptFactor(
            name="touch_interaction",
            content=touch_info["content"],
            weight=0.8,
            priority=2
        ))
    
    # 记忆因子
    if memory_info:
        # 如果有记忆摘要，创建记忆因子
        if memory_info.get("summary"):
            factors.append(PromptFactor(
                name="memory_summary",
                content=memory_info["summary"],
                weight=0.6,
                priority=1
            ))
        # 如果有记忆记录但无摘要，创建基础记忆因子
        elif memory_info.get("count", 0) > 0:
            factors.append(PromptFactor(
                name="memory_summary",
                content=f"我有{memory_info['count']}条相关记忆记录",
                weight=0.4,
                priority=1
            ))
    
    # 用户输入因子（必需）
    if user_input:
        factors.append(PromptFactor(
            name="user_input",
            content=user_input,
            weight=2.0,
            priority=6,
            is_required=True
        ))
    
    return factors 