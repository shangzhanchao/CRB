#!/usr/bin/env python3
"""Test script for hybrid memory system.

融合记忆系统测试脚本。
"""

import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_core.hybrid_memory import HybridMemoryManager
from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.constants import SESSION_MEMORY_LIMIT, CONTEXT_WINDOW_SIZE

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_hybrid_memory_manager():
    """测试融合记忆管理器"""
    print("🧪 开始测试融合记忆管理器")
    print("="*60)
    
    # 创建记忆管理器
    memory_manager = HybridMemoryManager("robotA")
    
    # 测试数据
    test_conversations = [
        {
            "user_text": "你好，我是小明",
            "ai_response": "你好小明！很高兴认识你！",
            "mood_tag": "happy",
            "user_id": "user1",
            "touched": False,
            "touch_zone": None,
        },
        {
            "user_text": "今天天气怎么样？",
            "ai_response": "今天天气很好，阳光明媚！",
            "mood_tag": "excited",
            "user_id": "user1",
            "touched": True,
            "touch_zone": 0,
        },
        {
            "user_text": "我喜欢和你聊天",
            "ai_response": "我也很喜欢和你聊天！你很有趣！",
            "mood_tag": "happy",
            "user_id": "user1",
            "touched": False,
            "touch_zone": None,
        },
        {
            "user_text": "你叫什么名字？",
            "ai_response": "我是小机器人，你可以叫我小助手！",
            "mood_tag": "neutral",
            "user_id": "user1",
            "touched": False,
            "touch_zone": None,
        },
        {
            "user_text": "你会做什么？",
            "ai_response": "我可以陪你聊天，回答问题，还能记住我们的对话！",
            "mood_tag": "excited",
            "user_id": "user1",
            "touched": True,
            "touch_zone": 1,
        },
    ]
    
    # 添加记忆
    print("📝 添加测试记忆...")
    for i, conv in enumerate(test_conversations, 1):
        memory_manager.add_memory(**conv)
        print(f"   ✅ 添加记忆 {i}: {conv['user_text']}")
    
    # 测试记忆查询
    print("\n🔍 测试记忆查询...")
    query_results = memory_manager.query_memory("聊天", top_k=3)
    print(f"   记忆类型: {query_results['memory_type']}")
    print(f"   会话记录数: {query_results['session_count']}")
    print(f"   语义记忆数: {query_results['semantic_count']}")
    print(f"   总记录数: {query_results['total_count']}")
    print(f"   记忆摘要: {query_results['summary']}")
    
    # 测试上下文记忆
    print("\n📖 测试上下文记忆...")
    context_memories = memory_manager.get_context_memory()
    print(f"   上下文记忆数: {len(context_memories)}")
    for i, memory in enumerate(context_memories[-3:], 1):
        print(f"   {i}. 用户: {memory.user_text}")
        print(f"      AI: {memory.ai_response}")
        print(f"      情绪: {memory.mood_tag}")
        print(f"      重要性: {memory.importance_score:.3f}")
    
    # 测试记忆统计
    print("\n📊 测试记忆统计...")
    stats = memory_manager.get_memory_stats()
    print(f"   机器人ID: {stats['robot_id']}")
    print(f"   会话记录数: {stats['session_count']}")
    print(f"   会话限制: {stats['session_limit']}")
    print(f"   上下文计数器: {stats['context_counter']}")
    
    print("\n✅ 融合记忆管理器测试完成")
    print("="*60)


def test_enhanced_dialogue_engine():
    """测试增强对话引擎"""
    print("\n🧪 开始测试增强对话引擎")
    print("="*60)
    
    # 创建增强对话引擎
    dialogue_engine = EnhancedDialogueEngine(
        robot_id="robotA",
        llm_url=None,  # 不使用LLM，只测试记忆功能
        tts_url=None,
    )
    
    # 测试对话
    test_dialogue = [
        {
            "user_text": "你好，我是小红",
            "mood_tag": "happy",
            "user_id": "user2",
            "touched": False,
            "touch_zone": None,
        },
        {
            "user_text": "今天心情怎么样？",
            "mood_tag": "excited",
            "user_id": "user2",
            "touched": True,
            "touch_zone": 0,
        },
        {
            "user_text": "你记得我们之前聊过什么吗？",
            "mood_tag": "neutral",
            "user_id": "user2",
            "touched": False,
            "touch_zone": None,
        },
    ]
    
    print("💬 测试对话生成...")
    for i, dialogue in enumerate(test_dialogue, 1):
        print(f"\n--- 对话 {i} ---")
        print(f"用户: {dialogue['user_text']}")
        print(f"情绪: {dialogue['mood_tag']}")
        print(f"触摸: {dialogue['touched']}")
        
        response = dialogue_engine.generate_response(**dialogue)
        print(f"AI回复: {response.text}")
        print(f"表情: {response.expression}")
        print(f"动作: {response.action}")
    
    # 测试记忆功能
    print("\n💾 测试记忆功能...")
    memory_stats = dialogue_engine.get_memory_stats()
    print(f"记忆统计: {memory_stats}")
    
    context_memories = dialogue_engine.get_context_memory()
    print(f"上下文记忆数: {len(context_memories)}")
    
    print("\n✅ 增强对话引擎测试完成")
    print("="*60)


def test_memory_persistence():
    """测试记忆持久化"""
    print("\n🧪 开始测试记忆持久化")
    print("="*60)
    
    # 创建第一个记忆管理器
    memory_manager1 = HybridMemoryManager("robotA")
    
    # 添加一些记忆
    test_data = [
        {
            "user_text": "这是重要的对话",
            "ai_response": "我会记住这个重要对话",
            "mood_tag": "excited",
            "user_id": "user3",
            "touched": True,
            "touch_zone": 2,
        },
        {
            "user_text": "这是普通对话",
            "ai_response": "这是普通的回复",
            "mood_tag": "neutral",
            "user_id": "user3",
            "touched": False,
            "touch_zone": None,
        },
    ]
    
    print("📝 添加测试记忆...")
    for conv in test_data:
        memory_manager1.add_memory(**conv)
    
    # 测试归档功能
    print("\n📦 测试记忆归档...")
    archived_count = memory_manager1.archive_important_memories(importance_threshold=0.7)
    print(f"归档数量: {archived_count}")
    
    # 测试清空会话记忆
    print("\n🗑️ 测试清空会话记忆...")
    cleared_count = memory_manager1.clear_session_memory()
    print(f"清除数量: {cleared_count}")
    
    print("\n✅ 记忆持久化测试完成")
    print("="*60)


def main():
    """主测试函数"""
    print("🚀 融合记忆系统测试开始")
    print("="*60)
    
    try:
        # 测试融合记忆管理器
        test_hybrid_memory_manager()
        
        # 测试增强对话引擎
        test_enhanced_dialogue_engine()
        
        # 测试记忆持久化
        test_memory_persistence()
        
        print("\n🎉 所有测试完成！")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        logger.error(f"测试错误: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 