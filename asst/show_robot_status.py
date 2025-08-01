"""显示Robot状态的脚本

用于查看robotA的详细状态信息，包括成长阶段、人格特质、记忆等。
"""

import sys
import os
import logging
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from ai_core.intelligent_core import IntelligentCore
from ai_core.constants import STAGE_ORDER, OCEAN_TRAITS


def show_robot_status(robot_id: str = "robotA"):
    """显示robot的详细状态信息"""
    
    print("🤖 Robot状态详细信息")
    print("=" * 60)
    
    # 创建智能核心
    core = IntelligentCore()
    
    # 基本信息
    print(f"🆔 Robot ID: {robot_id}")
    print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 成长阶段信息
    print("🌱 成长阶段信息")
    print("-" * 30)
    current_stage = core.dialogue.stage
    stage_index = STAGE_ORDER.index(current_stage) if current_stage in STAGE_ORDER else -1
    print(f"   当前阶段: {current_stage}")
    print(f"   阶段索引: {stage_index + 1}/{len(STAGE_ORDER)}")
    if stage_index < len(STAGE_ORDER) - 1:
        next_stage = STAGE_ORDER[stage_index + 1]
        print(f"   下一阶段: {next_stage}")
    print()
    
    # 人格特质信息
    print("🎭 人格特质信息")
    print("-" * 30)
    personality = core.dialogue.personality
    print(f"   人格风格: {personality.get_personality_style()}")
    print(f"   人格摘要: {personality.get_personality_summary()}")
    print(f"   主导特质: {', '.join(personality.get_dominant_traits())}")
    print()
    print("   📊 OCEAN人格向量:")
    for i, (trait, value) in enumerate(zip(OCEAN_TRAITS, personality.vector)):
        bar = "█" * int(abs(value) * 10) + "░" * (10 - int(abs(value) * 10))
        sign = "+" if value >= 0 else "-"
        print(f"     {trait:15}: {sign}{abs(value):.3f} {bar}")
    print()
    
    # 全局状态信息
    print("📈 全局状态信息")
    print("-" * 30)
    from ai_core import global_state
    print(f"   交互次数: {global_state.INTERACTION_COUNT}")
    print(f"   音频时长: {global_state.AUDIO_DATA_SECONDS:.1f}秒")
    print(f"   创建时间: {global_state.START_TIME}")
    print(f"   运行天数: {global_state.days_since_start()}天")
    print()
    
    # 记忆信息
    print("💾 记忆信息")
    print("-" * 30)
    memories = core.dialogue.memory.records
    print(f"   记忆总数: {len(memories)}")
    if memories:
        print(f"   最早记忆: {memories[0]['time']}")
        print(f"   最新记忆: {memories[-1]['time']}")
        print()
        print("   📋 最近5条记忆:")
        for i, memory in enumerate(memories[-5:], 1):
            print(f"     {i}. 用户: {memory['user_text']}")
            print(f"        AI: {memory['ai_response']}")
            print(f"        情绪: {memory['mood_tag']}")
            print(f"        时间: {memory['time']}")
            print()
    else:
        print("   暂无记忆记录")
    print()
    
    # 情绪统计
    if memories:
        print("😊 情绪统计")
        print("-" * 30)
        mood_counts = {}
        for memory in memories:
            mood = memory['mood_tag']
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        for mood, count in sorted(mood_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(memories)) * 100
            bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
            print(f"   {mood:10}: {count:3d} ({percentage:5.1f}%) {bar}")
        print()
    
    # 系统配置信息
    print("⚙️ 系统配置信息")
    print("-" * 30)
    print(f"   LLM服务: {core.dialogue.llm_url}")
    print(f"   TTS服务: {core.dialogue.tts_url}")
    print(f"   记忆数据库: {core.dialogue.memory.db_path}")
    print(f"   状态文件: state.json")
    print()
    
    print("=" * 60)
    print("✅ 状态信息显示完成")


def show_memory_details(robot_id: str = "robotA"):
    """显示详细的记忆信息"""
    
    print("💾 详细记忆信息")
    print("=" * 60)
    
    core = IntelligentCore()
    memories = core.dialogue.memory.records
    
    if not memories:
        print("暂无记忆记录")
        return
    
    print(f"📊 记忆统计")
    print(f"   总记录数: {len(memories)}")
    print(f"   时间跨度: {memories[0]['time']} 到 {memories[-1]['time']}")
    print()
    
    # 按用户分组显示
    user_memories = {}
    for memory in memories:
        user_id = memory['user_id']
        if user_id not in user_memories:
            user_memories[user_id] = []
        user_memories[user_id].append(memory)
    
    for user_id, user_mems in user_memories.items():
        print(f"👤 用户: {user_id} ({len(user_mems)}条记录)")
        print("-" * 40)
        
        for i, memory in enumerate(user_mems[-10:], 1):  # 显示最近10条
            print(f"   {i:2d}. [{memory['time'].strftime('%m-%d %H:%M')}] {memory['mood_tag']}")
            print(f"       用户: {memory['user_text']}")
            print(f"       AI: {memory['ai_response']}")
            if memory['touched']:
                print(f"       触摸: 区域{memory['touch_zone']}")
            print()
    
    print("=" * 60)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="显示Robot状态信息")
    parser.add_argument("--robot_id", default="robotA", help="Robot ID")
    parser.add_argument("--memory", action="store_true", help="显示详细记忆信息")
    args = parser.parse_args()
    
    if args.memory:
        show_memory_details(args.robot_id)
    else:
        show_robot_status(args.robot_id)


if __name__ == "__main__":
    main() 