"""提示词融合算法测试

测试新的专业提示词融合算法的各项功能。
"""

import unittest
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.prompt_fusion import (
    PromptFusionEngine,
    PromptFactor,
    RobotAction,
    RobotExpression,
    create_prompt_factors,
    create_robot_actions_from_emotion,
    create_robot_expressions_from_emotion
)


class TestPromptFusion(unittest.TestCase):
    """提示词融合算法测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.fusion_engine = PromptFusionEngine()
        
    def test_create_prompt_factors(self):
        """测试创建提示词因子"""
        factors = create_prompt_factors(
            stage_info={"prompt": "觉醒期 - 能够主动回忆过去的交互经历"},
            personality_info={"traits": "外向、友善、好奇"},
            emotion_info={"emotion": "开心"},
            touch_info={"content": "用户轻拍了机器人的头部"},
            memory_info={"summary": "用户之前提到过喜欢音乐"},
            user_input="你好，今天天气真不错！"
        )
        
        # 验证因子数量
        self.assertEqual(len(factors), 6)
        
        # 验证必需因子
        user_input_factors = [f for f in factors if f.name == "user_input"]
        self.assertEqual(len(user_input_factors), 1)
        self.assertTrue(user_input_factors[0].is_required)
        
        # 验证权重设置
        user_input_factor = user_input_factors[0]
        self.assertEqual(user_input_factor.weight, 2.0)
        self.assertEqual(user_input_factor.priority, 6)
        
    def test_create_robot_actions_from_emotion(self):
        """测试根据情绪创建机器人动作"""
        actions = create_robot_actions_from_emotion("happy")
        
        # 验证动作数量
        self.assertGreater(len(actions), 0)
        
        # 验证动作结构
        for action in actions:
            self.assertIsInstance(action, RobotAction)
            self.assertIsNotNone(action.action_code)
            self.assertIsNotNone(action.description)
            self.assertIsInstance(action.parameters, dict)
            
    def test_create_robot_expressions_from_emotion(self):
        """测试根据情绪创建机器人表情"""
        expressions = create_robot_expressions_from_emotion("sad")
        
        # 验证表情数量
        self.assertEqual(len(expressions), 1)
        
        # 验证表情结构
        expression = expressions[0]
        self.assertIsInstance(expression, RobotExpression)
        self.assertIsNotNone(expression.expression_code)
        self.assertIsNotNone(expression.description)
        self.assertIsInstance(expression.animation_params, dict)
        
    def test_create_comprehensive_prompt(self):
        """测试创建综合提示词"""
        # 创建测试因子
        factors = create_prompt_factors(
            stage_info={"prompt": "共鸣期 - 能够理解用户的情感状态"},
            personality_info={"traits": "温暖、善解人意"},
            emotion_info={"emotion": "困惑"},
            user_input="我不太明白这个概念"
        )
        
        # 创建机器人动作和表情
        robot_actions = create_robot_actions_from_emotion("confused")
        robot_expressions = create_robot_expressions_from_emotion("confused")
        
        # 创建上下文信息
        context_info = {
            "学习主题": "Python编程",
            "用户水平": "初学者"
        }
        
        # 生成提示词
        prompt = self.fusion_engine.create_comprehensive_prompt(
            factors=factors,
            robot_actions=robot_actions,
            robot_expressions=robot_expressions,
            context_info=context_info
        )
        
        # 验证提示词结构
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 100)
        
        # 验证包含关键部分
        self.assertIn("你是一个智能陪伴机器人", prompt)
        self.assertIn("## 机器人状态与能力", prompt)
        self.assertIn("## 交互上下文", prompt)
        self.assertIn("## 用户输入", prompt)
        self.assertIn("## 输出要求", prompt)
        
    def test_prompt_structure_validation(self):
        """测试提示词结构验证"""
        # 测试缺少必需因子
        factors = [
            PromptFactor(
                name="test_factor",
                content="测试内容",
                weight=1.0,
                priority=1
            )
        ]
        
        with self.assertRaises(ValueError):
            self.fusion_engine.create_comprehensive_prompt(factors)
            
    def test_emotion_based_generation(self):
        """测试基于情绪的动作和表情生成"""
        emotions = ["happy", "sad", "confused", "excited", "surprised"]
        
        for emotion in emotions:
            # 生成动作
            actions = create_robot_actions_from_emotion(emotion)
            self.assertGreater(len(actions), 0)
            
            # 生成表情
            expressions = create_robot_expressions_from_emotion(emotion)
            self.assertEqual(len(expressions), 1)
            
            # 验证动作和表情的一致性
            if emotion == "happy":
                self.assertTrue(any("nod" in action.action_code for action in actions))
            elif emotion == "sad":
                self.assertTrue(any("head_down" in action.action_code for action in actions))
                
    def test_prompt_factor_priority(self):
        """测试提示词因子优先级"""
        factors = [
            PromptFactor(name="low_priority", content="低优先级", weight=1.0, priority=1),
            PromptFactor(name="high_priority", content="高优先级", weight=1.0, priority=5),
            PromptFactor(name="user_input", content="用户输入", weight=2.0, priority=6, is_required=True)
        ]
        
        # 验证排序
        sorted_factors = sorted(factors, key=lambda x: x.priority, reverse=True)
        self.assertEqual(sorted_factors[0].name, "user_input")
        self.assertEqual(sorted_factors[1].name, "high_priority")
        self.assertEqual(sorted_factors[2].name, "low_priority")
        
    def test_json_output_format(self):
        """测试JSON输出格式"""
        # 模拟大模型输出
        expected_output = {
            "text": "你好！今天天气确实很棒呢！",
            "actions": [
                {
                    "code": "A001",
                    "description": "点头动作±15度",
                    "parameters": {"angle": 15, "duration": 1.0}
                }
            ],
            "expressions": [
                {
                    "code": "E001",
                    "description": "微笑+眨眼+眼神上扬",
                    "animation": {"intensity": 0.8, "duration": 2.0}
                }
            ]
        }
        
        # 验证JSON格式
        json_str = json.dumps(expected_output, ensure_ascii=False, indent=2)
        parsed_output = json.loads(json_str)
        
        self.assertEqual(parsed_output["text"], expected_output["text"])
        self.assertEqual(len(parsed_output["actions"]), 1)
        self.assertEqual(len(parsed_output["expressions"]), 1)
        
    def test_context_integration(self):
        """测试上下文信息集成"""
        factors = create_prompt_factors(
            stage_info={"prompt": "觉醒期"},
            personality_info={"traits": "友善"},
            user_input="测试输入"
        )
        
        context_info = {
            "时间": "下午3点",
            "地点": "客厅",
            "特殊事件": "用户生日"
        }
        
        prompt = self.fusion_engine.create_comprehensive_prompt(
            factors=factors,
            context_info=context_info
        )
        
        # 验证上下文信息被正确集成
        self.assertIn("时间：下午3点", prompt)
        self.assertIn("地点：客厅", prompt)
        self.assertIn("特殊事件：用户生日", prompt)
        
    def test_robot_action_parameters(self):
        """测试机器人动作参数"""
        action = RobotAction(
            action_code="A001",
            description="点头动作",
            parameters={"angle": 15, "duration": 1.0}
        )
        
        self.assertEqual(action.action_code, "A001")
        self.assertEqual(action.description, "点头动作")
        self.assertEqual(action.parameters["angle"], 15)
        self.assertEqual(action.parameters["duration"], 1.0)
        
    def test_robot_expression_animation(self):
        """测试机器人表情动画参数"""
        expression = RobotExpression(
            expression_code="E001",
            description="微笑表情",
            animation_params={"intensity": 0.8, "duration": 2.0}
        )
        
        self.assertEqual(expression.expression_code, "E001")
        self.assertEqual(expression.description, "微笑表情")
        self.assertEqual(expression.animation_params["intensity"], 0.8)
        self.assertEqual(expression.animation_params["duration"], 2.0)


class TestPromptFusionIntegration(unittest.TestCase):
    """提示词融合集成测试"""
    
    def test_full_integration_workflow(self):
        """测试完整的集成工作流程"""
        from ai_core.prompt_fusion import PromptFusionEngine, create_prompt_factors
        
        # 1. 创建融合引擎
        fusion_engine = PromptFusionEngine()
        
        # 2. 创建各种影响因子
        factors = create_prompt_factors(
            stage_info={"prompt": "觉醒期 - 能够主动回忆过去的交互经历"},
            personality_info={"traits": "外向、友善、好奇", "style": "语言风格温和"},
            emotion_info={"emotion": "开心"},
            touch_info={"content": "用户轻拍了机器人的头部"},
            memory_info={"summary": "用户之前提到过喜欢音乐，特别是古典音乐"},
            user_input="你好，今天天气真不错！"
        )
        
        # 3. 创建机器人动作和表情
        robot_actions = create_robot_actions_from_emotion("happy")
        robot_expressions = create_robot_expressions_from_emotion("happy")
        
        # 4. 创建上下文信息
        context_info = {
            "时间": "下午3点",
            "地点": "客厅",
            "交互历史": "这是今天的第5次交互"
        }
        
        # 5. 生成综合提示词
        comprehensive_prompt = fusion_engine.create_comprehensive_prompt(
            factors=factors,
            robot_actions=robot_actions,
            robot_expressions=robot_expressions,
            context_info=context_info
        )
        
        # 6. 验证结果
        self.assertIsInstance(comprehensive_prompt, str)
        self.assertGreater(len(comprehensive_prompt), 500)
        
        # 验证包含所有关键部分
        required_sections = [
            "你是一个智能陪伴机器人",
            "## 机器人状态与能力",
            "## 交互上下文",
            "## 用户输入",
            "## 输出要求",
            "JSON格式输出"
        ]
        
        for section in required_sections:
            self.assertIn(section, comprehensive_prompt)
            
    def test_error_handling(self):
        """测试错误处理"""
        fusion_engine = PromptFusionEngine()
        
        # 测试空因子列表
        with self.assertRaises(ValueError):
            fusion_engine.create_comprehensive_prompt([])
            
        # 测试缺少用户输入
        factors = [
            PromptFactor(name="test", content="test", weight=1.0, priority=1)
        ]
        
        with self.assertRaises(ValueError):
            fusion_engine.create_comprehensive_prompt(factors)


if __name__ == "__main__":
    # 运行测试
    unittest.main(verbosity=2) 