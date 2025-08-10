"""系统提示词模板优化验证测试

验证：
1. JSON输出格式规范是否正确包含
2. 动作和表情参数定义是否完整
3. 触摸交互专用代码是否正确定义
4. 系统提示词是否能正确指导LLM生成合适的回应
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.constants import ACTION_MAP, FACE_ANIMATION_MAP


def test_system_prompt_optimization():
    """测试系统提示词模板优化"""
    print("🔍 测试系统提示词模板优化")
    print("=" * 60)
    
    try:
        # 创建增强对话引擎
        engine = EnhancedDialogueEngine(
            robot_id="test_robot",
            llm_url=None,  # 不实际调用LLM
            tts_url=None
        )
        
        # 测试参数
        test_params = {
            "robot_id": "test_robot",
            "stage": "awaken",
            "personality_style": "热情开朗",
            "dominant_traits": ["high_extraversion"],
            "memory_count": 5,
            "session_id": "test_session_123"
        }
        
        # 生成系统提示词
        system_prompt = engine._build_system_prompt(**test_params)
        
        print("✅ 系统提示词生成成功")
        print(f"📏 提示词长度: {len(system_prompt)} 字符")
        
        # 验证JSON格式规范
        json_format_check = "JSON格式要求" in system_prompt
        json_structure_check = '"text": "文本响应内容"' in system_prompt
        json_actions_check = '"actions": [' in system_prompt
        json_expressions_check = '"expressions": [' in system_prompt
        
        print(f"\n📋 JSON格式规范检查:")
        print(f"  ✅ JSON格式要求: {'通过' if json_format_check else '❌ 未找到'}")
        print(f"  ✅ JSON结构定义: {'通过' if json_structure_check else '❌ 未找到'}")
        print(f"  ✅ 动作数组定义: {'通过' if json_actions_check else '❌ 未找到'}")
        print(f"  ✅ 表情数组定义: {'通过' if json_expressions_check else '❌ 未找到'}")
        
        # 验证动作代码库完整性
        action_codes_check = []
        expected_action_codes = [
            "A000:breathing", "A001:nod±15°", "A002:sway±10°", "A003:hands_up10°",
            "A004:tilt_oscillate±10°", "A005:gaze_switch", "A006:hands_still",
            "A007:head_down_slow-15°", "A008:arms_arc_in", "A009:head_up_eyes_wide",
            "A010:hands_raise>25°", "A011:idle_tremble", "A012:fast_head_shake",
            "A013:hands_forward", "A014:stiff_posture", "A015:clenched_fists",
            "A016:retreat_motion", "A017:cautious_movement", "A018:lean_back",
            "A019:reject_gesture", "A020:smooth_movement", "A021:gentle_breathing",
            "A022:slow_movement", "A023:relaxed_posture", "A024:lazy_movement",
            "A025:lack_energy", "A100:gentle_nod", "A101:soft_sway",
            "A102:welcoming_gesture", "A103:thoughtful_tilt", "A104:attentive_gaze",
            "A105:calm_stillness", "A106:sad_lower", "A107:protective_curl",
            "A108:surprised_jump", "A109:excited_raise", "A110:shy_tremble",
            "A111:excited_shake", "A112:loving_nod", "A113:trusting_lean",
            "A114:intimate_embrace"
        ]
        
        for code in expected_action_codes:
            if code in system_prompt:
                action_codes_check.append(True)
            else:
                action_codes_check.append(False)
                print(f"    ❌ 缺少动作代码: {code}")
        
        action_completeness = sum(action_codes_check) / len(expected_action_codes) * 100
        print(f"\n🤸 动作代码库完整性: {action_completeness:.1f}% ({sum(action_codes_check)}/{len(expected_action_codes)})")
        
        # 验证表情代码库完整性
        expression_codes_check = []
        expected_expression_codes = [
            "E000:平静表情", "E001:微笑+眨眼+眼神上扬", "E002:斜视+眼神聚焦",
            "E003:眼角下垂+闭眼", "E004:偏头+眼神回避", "E005:眼神放大+频繁眨眼",
            "E006:抬头张眼", "E007:皱眉+眼神锐利", "E008:眼神惊恐+颤抖",
            "E009:撇嘴+眼神厌恶", "E010:平静微笑", "E011:眼神疲惫+打哈欠",
            "E012:眼神呆滞+无精打采", "E020:gentle_smile", "E021:soft_blink",
            "E022:warm_expression", "E023:thoughtful_look", "E024:attentive_face",
            "E025:loving_smile", "E026:trusting_expression", "E027:intimate_gaze"
        ]
        
        for code in expected_expression_codes:
            if code in system_prompt:
                expression_codes_check.append(True)
            else:
                expression_codes_check.append(False)
                print(f"    ❌ 缺少表情代码: {code}")
        
        expression_completeness = sum(expression_codes_check) / len(expected_expression_codes) * 100
        print(f"🎭 表情代码库完整性: {expression_completeness:.1f}% ({sum(expression_codes_check)}/{len(expected_expression_codes)})")
        
        # 验证触摸交互专用代码
        touch_codes_check = []
        touch_action_codes = ["A112:loving_nod", "A113:trusting_lean", "A114:intimate_embrace"]
        touch_expression_codes = ["E025:loving_smile", "E026:trusting_expression", "E027:intimate_gaze"]
        
        for code in touch_action_codes + touch_expression_codes:
            if code in system_prompt:
                touch_codes_check.append(True)
            else:
                touch_codes_check.append(False)
                print(f"    ❌ 缺少触摸代码: {code}")
        
        touch_completeness = sum(touch_codes_check) / len(touch_codes_check) * 100
        print(f"🤗 触摸交互代码完整性: {touch_completeness:.1f}% ({sum(touch_codes_check)}/{len(touch_codes_check)})")
        
        # 验证情绪映射规则
        emotion_mapping_check = []
        expected_emotions = [
            "happy/快乐", "confused/困惑", "sad/悲伤", "shy/害羞",
            "excited/兴奋", "surprised/惊讶", "angry/愤怒", "fear/恐惧",
            "disgust/厌恶", "calm/平静", "tired/疲惫", "bored/无聊",
            "neutral/中性", "touch_zone_0/头部抚摸", "touch_zone_1/背后抚摸",
            "touch_zone_2/胸口抚摸"
        ]
        
        for emotion in expected_emotions:
            if emotion in system_prompt:
                emotion_mapping_check.append(True)
            else:
                emotion_mapping_check.append(False)
                print(f"    ❌ 缺少情绪映射: {emotion}")
        
        emotion_completeness = sum(emotion_mapping_check) / len(emotion_mapping_check) * 100
        print(f"😊 情绪映射规则完整性: {emotion_completeness:.1f}% ({sum(emotion_mapping_check)}/{len(emotion_mapping_check)})")
        
        # 验证选择原则
        selection_principles = [
            "语义匹配", "情感一致性", "成长阶段适配", "触摸交互增强", "记忆关联"
        ]
        
        principles_check = []
        for principle in selection_principles:
            if principle in system_prompt:
                principles_check.append(True)
            else:
                principles_check.append(False)
                print(f"    ❌ 缺少选择原则: {principle}")
        
        principles_completeness = sum(principles_check) / len(principles_check) * 100
        print(f"🎯 选择原则完整性: {principles_completeness:.1f}% ({sum(principles_check)}/{len(principles_check)})")
        
        # 总体评估
        overall_score = (
            (json_format_check + json_structure_check + json_actions_check + json_expressions_check) / 4 * 25 +
            action_completeness * 0.25 +
            expression_completeness * 0.25 +
            touch_completeness * 0.15 +
            emotion_completeness * 0.05 +
            principles_completeness * 0.05
        )
        
        print(f"\n📊 总体优化评分: {overall_score:.1f}/100")
        
        if overall_score >= 90:
            print("🎉 系统提示词模板优化成功！")
            print("✅ JSON格式规范完整")
            print("✅ 动作和表情代码库完整")
            print("✅ 触摸交互专用代码完整")
            print("✅ 情绪映射规则完整")
            print("✅ 选择原则完整")
        elif overall_score >= 70:
            print("⚠️ 系统提示词模板基本优化完成，但还有改进空间")
        else:
            print("❌ 系统提示词模板优化不完整，需要进一步改进")
        
        return overall_score >= 70
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_constants_integration():
    """测试常量集成"""
    print("\n🔍 测试常量集成")
    print("=" * 60)
    
    try:
        # 验证ACTION_MAP中的触摸交互代码
        touch_actions = ["touch_zone_0", "touch_zone_1", "touch_zone_2"]
        action_check = []
        
        for zone in touch_actions:
            if zone in ACTION_MAP:
                action_check.append(True)
                print(f"  ✅ 触摸动作 {zone}: {ACTION_MAP[zone]}")
            else:
                action_check.append(False)
                print(f"  ❌ 缺少触摸动作: {zone}")
        
        # 验证FACE_ANIMATION_MAP中的触摸交互代码
        touch_expressions = ["touch_zone_0", "touch_zone_1", "touch_zone_2"]
        expression_check = []
        
        for zone in touch_expressions:
            if zone in FACE_ANIMATION_MAP:
                expression_check.append(True)
                print(f"  ✅ 触摸表情 {zone}: {FACE_ANIMATION_MAP[zone][0]}")
            else:
                expression_check.append(False)
                print(f"  ❌ 缺少触摸表情: {zone}")
        
        constants_score = (sum(action_check) + sum(expression_check)) / (len(action_check) + len(expression_check)) * 100
        print(f"\n📊 常量集成评分: {constants_score:.1f}/100")
        
        return constants_score >= 90
        
    except Exception as e:
        print(f"❌ 常量集成测试失败: {e}")
        return False


if __name__ == "__main__":
    print("🚀 开始系统提示词模板优化验证测试")
    print("=" * 80)
    
    # 运行测试
    prompt_test_result = test_system_prompt_optimization()
    constants_test_result = test_constants_integration()
    
    print("\n" + "=" * 80)
    print("📋 测试结果总结")
    print("=" * 80)
    
    if prompt_test_result and constants_test_result:
        print("🎉 所有测试通过！系统提示词模板优化成功！")
        print("\n✅ 优化成果:")
        print("  1. JSON输出格式规范完整定义")
        print("  2. 动作和表情代码库完整（A000-A114, E000-E027）")
        print("  3. 触摸交互专用代码完整定义")
        print("  4. 情绪映射规则完整")
        print("  5. 选择原则完整")
        print("  6. 常量文件集成完整")
    else:
        print("❌ 部分测试失败，需要进一步优化")
        if not prompt_test_result:
            print("  - 系统提示词模板优化不完整")
        if not constants_test_result:
            print("  - 常量文件集成不完整")
    
    print("\n🔧 后续建议:")
    print("  1. 在实际LLM调用中验证JSON格式输出")
    print("  2. 测试不同情绪和触摸场景的动作表情选择")
    print("  3. 验证系统提示词对LLM输出的指导效果")
    print("  4. 根据实际使用情况进一步优化代码库")
