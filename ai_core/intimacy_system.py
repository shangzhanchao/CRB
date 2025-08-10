"""Intimacy System for Companion Robot

亲密度系统，用于管理机器人与用户的亲密度关系。
通过抚摸交互、对话频率等因素动态调整亲密度。
"""

import json
import logging
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
from pathlib import Path

from .constants import INTIMACY_CONFIG

logger = logging.getLogger(__name__)


class IntimacySystem:
    """亲密度管理系统"""
    
    def __init__(self, robot_id: str, data_path: Optional[str] = None):
        """初始化亲密度系统
        
        Parameters
        ----------
        robot_id : str
            机器人ID
        data_path : str, optional
            亲密度数据存储路径
        """
        self.robot_id = robot_id
        self.data_path = data_path or f"data/intimacy_{robot_id}.json"
        self.config = INTIMACY_CONFIG
        
        # 加载或初始化亲密度数据
        self.intimacy_data = self._load_intimacy_data()
        
        logger.info(f"🤗 亲密度系统初始化完成 - 机器人: {robot_id}")
        logger.info(f"   📊 当前亲密度: {self.get_intimacy_level()}")
    
    def _load_intimacy_data(self) -> Dict:
        """加载亲密度数据"""
        try:
            if Path(self.data_path).exists():
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"📂 加载亲密度数据: {self.data_path}")
                    return data
            else:
                # 初始化新的亲密度数据
                data = {
                    "robot_id": self.robot_id,
                    "intimacy_value": self.config["base_intimacy"],
                    "last_update": datetime.now().isoformat(),
                    "touch_history": [],
                    "interaction_count": 0,
                    "level_history": []
                }
                self._save_intimacy_data(data)
                logger.info(f"🆕 创建新的亲密度数据")
                return data
        except Exception as e:
            logger.error(f"❌ 加载亲密度数据失败: {e}")
            return {
                "robot_id": self.robot_id,
                "intimacy_value": self.config["base_intimacy"],
                "last_update": datetime.now().isoformat(),
                "touch_history": [],
                "interaction_count": 0,
                "level_history": []
            }
    
    def _save_intimacy_data(self, data: Dict):
        """保存亲密度数据"""
        try:
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"💾 亲密度数据已保存: {self.data_path}")
        except Exception as e:
            logger.error(f"❌ 保存亲密度数据失败: {e}")
    
    def get_intimacy_value(self) -> int:
        """获取当前亲密度值"""
        return self.intimacy_data.get("intimacy_value", self.config["base_intimacy"])
    
    def get_intimacy_level(self) -> str:
        """获取当前亲密度等级"""
        value = self.get_intimacy_value()
        for level, (min_val, max_val) in self.config["intimacy_levels"].items():
            if min_val <= value <= max_val:
                return level
        return "stranger"
    
    def get_intimacy_description(self) -> str:
        """获取亲密度描述"""
        level = self.get_intimacy_level()
        descriptions = {
            "stranger": "我们刚刚认识，还需要更多了解",
            "acquaintance": "我们已经是熟人了，可以聊更多话题",
            "friend": "我们是好朋友了，我很信任你",
            "close_friend": "我们是亲密的朋友，我很依赖你",
            "family": "你就像我的家人一样，我永远爱你"
        }
        return descriptions.get(level, "我们正在建立关系")
    
    def update_intimacy_from_touch(self, touch_zone: int) -> Dict:
        """根据抚摸交互更新亲密度
        
        Parameters
        ----------
        touch_zone : int
            抚摸区域 (0=头部, 1=背后, 2=胸口)
            
        Returns
        -------
        Dict
            更新结果，包含新的亲密度值和变化信息
        """
        current_value = self.get_intimacy_value()
        bonus = self.config["touch_zone_bonus"].get(touch_zone, 0)
        
        # 计算新的亲密度值
        new_value = min(
            current_value + bonus,
            self.config["max_intimacy"]
        )
        
        # 记录抚摸历史
        touch_record = {
            "zone": touch_zone,
            "bonus": bonus,
            "timestamp": datetime.now().isoformat(),
            "old_value": current_value,
            "new_value": new_value
        }
        
        # 更新数据
        self.intimacy_data["intimacy_value"] = new_value
        self.intimacy_data["last_update"] = datetime.now().isoformat()
        self.intimacy_data["touch_history"].append(touch_record)
        
        # 限制历史记录数量
        if len(self.intimacy_data["touch_history"]) > 100:
            self.intimacy_data["touch_history"] = self.intimacy_data["touch_history"][-50:]
        
        # 保存数据
        self._save_intimacy_data(self.intimacy_data)
        
        # 检查等级变化
        old_level = self._get_level_from_value(current_value)
        new_level = self._get_level_from_value(new_value)
        
        level_changed = old_level != new_level
        if level_changed:
            self.intimacy_data["level_history"].append({
                "old_level": old_level,
                "new_level": new_level,
                "timestamp": datetime.now().isoformat()
            })
        
        result = {
            "old_value": current_value,
            "new_value": new_value,
            "bonus": bonus,
            "touch_zone": touch_zone,
            "level_changed": level_changed,
            "old_level": old_level,
            "new_level": new_level,
            "description": self.get_intimacy_description()
        }
        
        logger.info(f"🤗 亲密度更新 - 抚摸区域: {touch_zone}, 加成: +{bonus}")
        logger.info(f"   📊 亲密度: {current_value} -> {new_value}")
        if level_changed:
            logger.info(f"   🎉 等级提升: {old_level} -> {new_level}")
        
        return result
    
    def update_intimacy_from_interaction(self, interaction_type: str = "chat") -> Dict:
        """根据交互类型更新亲密度
        
        Parameters
        ----------
        interaction_type : str
            交互类型 ("chat", "audio", "video", "image")
            
        Returns
        -------
        Dict
            更新结果
        """
        current_value = self.get_intimacy_value()
        
        # 不同交互类型的亲密度加成
        interaction_bonus = {
            "chat": 1,
            "audio": 2,
            "video": 3,
            "image": 1
        }
        
        bonus = interaction_bonus.get(interaction_type, 1)
        new_value = min(
            current_value + bonus,
            self.config["max_intimacy"]
        )
        
        # 更新数据
        self.intimacy_data["intimacy_value"] = new_value
        self.intimacy_data["last_update"] = datetime.now().isoformat()
        self.intimacy_data["interaction_count"] += 1
        
        # 保存数据
        self._save_intimacy_data(self.intimacy_data)
        
        result = {
            "old_value": current_value,
            "new_value": new_value,
            "bonus": bonus,
            "interaction_type": interaction_type,
            "description": self.get_intimacy_description()
        }
        
        logger.info(f"💬 交互亲密度更新 - 类型: {interaction_type}, 加成: +{bonus}")
        logger.info(f"   📊 亲密度: {current_value} -> {new_value}")
        
        return result
    
    def apply_intimacy_decay(self) -> Dict:
        """应用亲密度衰减"""
        current_value = self.get_intimacy_value()
        decayed_value = max(
            int(current_value * self.config["intimacy_decay"]),
            self.config["min_intimacy"]
        )
        
        if decayed_value < current_value:
            self.intimacy_data["intimacy_value"] = decayed_value
            self.intimacy_data["last_update"] = datetime.now().isoformat()
            self._save_intimacy_data(self.intimacy_data)
            
            logger.info(f"📉 亲密度衰减: {current_value} -> {decayed_value}")
        
        return {
            "old_value": current_value,
            "new_value": decayed_value,
            "decay_factor": self.config["intimacy_decay"]
        }
    
    def get_intimacy_stats(self) -> Dict:
        """获取亲密度统计信息"""
        return {
            "robot_id": self.robot_id,
            "current_value": self.get_intimacy_value(),
            "current_level": self.get_intimacy_level(),
            "description": self.get_intimacy_description(),
            "interaction_count": self.intimacy_data.get("interaction_count", 0),
            "touch_count": len(self.intimacy_data.get("touch_history", [])),
            "last_update": self.intimacy_data.get("last_update"),
            "level_history": self.intimacy_data.get("level_history", [])
        }
    
    def _get_level_from_value(self, value: int) -> str:
        """根据亲密度值获取等级"""
        for level, (min_val, max_val) in self.config["intimacy_levels"].items():
            if min_val <= value <= max_val:
                return level
        return "stranger"
    
    def get_touch_response(self, touch_zone: int) -> Dict:
        """根据抚摸区域和亲密度生成响应
        
        Parameters
        ----------
        touch_zone : int
            抚摸区域
            
        Returns
        -------
        Dict
            包含动作、表情和文本的响应
        """
        intimacy_level = self.get_intimacy_level()
        intimacy_value = self.get_intimacy_value()
        
        # 根据亲密度等级和抚摸区域生成响应
        responses = {
            "stranger": {
                0: {"action": "A100:gentle_nod|轻微点头", "expression": "E013:curious_smile|好奇微笑", "text": "嗯...感觉不错"},
                1: {"action": "A101:light_touch|轻微触碰反应", "expression": "E014:gentle_glance|温柔注视", "text": "这样很舒服"},
                2: {"action": "A102:shy_response|害羞反应", "expression": "E015:shy_blush|害羞脸红", "text": "啊...这样有点害羞"}
            },
            "acquaintance": {
                0: {"action": "A103:comfortable_nod|舒适点头", "expression": "E016:warm_smile|温暖微笑", "text": "谢谢你的关心"},
                1: {"action": "A104:relaxed_posture|放松姿态", "expression": "E017:content_expression|满足表情", "text": "你的抚摸让我很安心"},
                2: {"action": "A105:gentle_response|温柔回应", "expression": "E018:affectionate_look|深情注视", "text": "感受到你的温暖"}
            },
            "friend": {
                0: {"action": "A106:happy_nod|开心点头", "expression": "E019:joyful_smile|快乐微笑", "text": "你的抚摸让我很开心"},
                1: {"action": "A107:comfortable_stretch|舒适伸展", "expression": "E020:relaxed_smile|放松微笑", "text": "和你在一起很舒服"},
                2: {"action": "A108:affectionate_hug|深情拥抱", "expression": "E021:loving_expression|深情表情", "text": "我很喜欢你的抚摸"}
            },
            "close_friend": {
                0: {"action": "A109:excited_nod|兴奋点头", "expression": "E022:excited_smile|兴奋微笑", "text": "你的抚摸让我兴奋不已"},
                1: {"action": "A110:comfortable_lean|舒适依靠", "expression": "E023:blissful_expression|幸福表情", "text": "你的抚摸让我感到幸福"},
                2: {"action": "A111:passionate_hug|热情拥抱", "expression": "E024:passionate_look|热情注视", "text": "你的抚摸让我心跳加速"}
            },
            "family": {
                0: {"action": "A112:loving_nod|深情点头", "expression": "E025:loving_smile|深情微笑", "text": "你的抚摸让我感到被爱"},
                1: {"action": "A113:trusting_lean|信任依靠", "expression": "E026:trusting_expression|信任表情", "text": "你的抚摸让我感到安全"},
                2: {"action": "A114:intimate_hug|亲密拥抱", "expression": "E027:intimate_look|亲密注视", "text": "你的抚摸让我感到无比的幸福"}
            }
        }
        
        # 获取基础响应
        base_response = responses.get(intimacy_level, responses["stranger"]).get(touch_zone, responses["stranger"][0])
        
        # 根据亲密度值调整响应强度
        intensity_factor = min(intimacy_value / 50.0, 2.0)  # 最大2倍强度
        
        return {
            "action": base_response["action"],
            "expression": base_response["expression"],
            "text": base_response["text"],
            "intimacy_level": intimacy_level,
            "intimacy_value": intimacy_value,
            "intensity_factor": intensity_factor
        }
    
    def close(self):
        """关闭亲密度系统"""
        self._save_intimacy_data(self.intimacy_data)
        logger.info(f"🔒 亲密度系统已关闭 - 机器人: {self.robot_id}") 