"""记忆系统分析测试

分析记忆存储和查询的问题，找出记忆不生效的原因。
"""

import sys
import os
import logging
import json
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置详细日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from ai_core.semantic_memory import SemanticMemory
from ai_core.dialogue_engine import DialogueEngine
from ai_core.personality_engine import PersonalityEngine


def test_memory_storage():
    """测试记忆存储功能"""
    print("🔍 测试记忆存储功能")
    print("=" * 60)
    
    try:
        # 创建记忆实例
        memory = SemanticMemory()
        print(f"✅ 记忆实例创建成功")
        print(f"📊 当前记忆记录数: {len(memory.records)}")
        print(f"🗄️ 数据库路径: {memory.db_path}")
        print()
        
        # 测试添加记忆
        test_memories = [
            {
                "user_text": "你好",
                "ai_response": "你好呀！很高兴见到你！",
                "mood_tag": "happy",
                "user_id": "test_user_1"
            },
            {
                "user_text": "今天天气怎么样",
                "ai_response": "今天天气很不错呢，阳光明媚的！",
                "mood_tag": "happy", 
                "user_id": "test_user_1"
            },
            {
                "user_text": "我有点难过",
                "ai_response": "别难过，有什么事情可以和我分享吗？",
                "mood_tag": "sad",
                "user_id": "test_user_2"
            }
        ]
        
        print("📝 添加测试记忆...")
        for i, mem in enumerate(test_memories, 1):
            memory.add_memory(
                user_text=mem["user_text"],
                ai_response=mem["ai_response"],
                mood_tag=mem["mood_tag"],
                user_id=mem["user_id"]
            )
            print(f"  ✅ 记忆 {i} 添加成功")
        
        print(f"📊 添加后记忆记录数: {len(memory.records)}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 记忆存储测试失败: {e}")
        return False


def test_memory_query():
    """测试记忆查询功能"""
    print("🔍 测试记忆查询功能")
    print("=" * 60)
    
    try:
        memory = SemanticMemory()
        
        # 测试查询
        test_queries = [
            ("你好", "test_user_1"),
            ("天气", "test_user_1"), 
            ("难过", "test_user_2"),
            ("心情", None),  # 查询所有用户
        ]
        
        for query, user_id in test_queries:
            print(f"\n🔍 查询: '{query}' (用户: {user_id or '所有'})")
            results = memory.query_memory(query, top_k=3, user_id=user_id)
            
            if results:
                print(f"  📋 找到 {len(results)} 条相关记忆:")
                for i, result in enumerate(results, 1):
                    print(f"    {i}. 用户: {result['user_text']}")
                    print(f"       AI: {result['ai_response']}")
                    print(f"       情绪: {result['mood_tag']}")
                    print(f"       时间: {result['time']}")
            else:
                print("  ⚠️ 未找到相关记忆")
        
        return True
        
    except Exception as e:
        print(f"❌ 记忆查询测试失败: {e}")
        return False


def test_memory_in_dialogue():
    """测试对话引擎中的记忆使用"""
    print("🔍 测试对话引擎中的记忆使用")
    print("=" * 60)
    
    try:
        # 创建对话引擎
        personality = PersonalityEngine()
        memory = SemanticMemory()
        dialogue = DialogueEngine(
            personality=personality,
            memory=memory,
            llm_url="doubao"
        )
        
        print("✅ 对话引擎创建成功")
        print()
        
        # 模拟对话序列
        test_conversations = [
            ("你好", "user1", "happy"),
            ("今天天气怎么样", "user1", "happy"),
            ("我有点难过", "user2", "sad"),
            ("你能安慰我吗", "user2", "sad"),
            ("谢谢你的安慰", "user2", "happy"),
        ]
        
        print("🗣️ 开始模拟对话...")
        for i, (text, user_id, mood) in enumerate(test_conversations, 1):
            print(f"\n--- 对话 {i} ---")
            print(f"用户: {text}")
            print(f"用户ID: {user_id}")
            print(f"情绪: {mood}")
            
            # 生成回复
            response = dialogue.generate_response(
                user_text=text,
                mood_tag=mood,
                user_id=user_id
            )
            
            print(f"AI回复: {response.text}")
            print(f"表情: {response.expression}")
            print(f"动作: {response.action}")
            
            # 检查记忆
            print(f"📊 当前记忆记录数: {len(memory.records)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 对话引擎记忆测试失败: {e}")
        return False


def analyze_memory_effectiveness():
    """分析记忆效果"""
    print("🔍 分析记忆效果")
    print("=" * 60)
    
    try:
        memory = SemanticMemory()
        
        # 分析记忆数据
        print("📊 记忆数据分析:")
        print(f"   总记录数: {len(memory.records)}")
        
        if memory.records:
            # 按用户分组
            user_stats = {}
            mood_stats = {}
            
            for record in memory.records:
                user_id = record['user_id']
                mood = record['mood_tag']
                
                if user_id not in user_stats:
                    user_stats[user_id] = 0
                user_stats[user_id] += 1
                
                if mood not in mood_stats:
                    mood_stats[mood] = 0
                mood_stats[mood] += 1
            
            print(f"   用户数量: {len(user_stats)}")
            print(f"   情绪类型: {len(mood_stats)}")
            
            print("\n👥 用户统计:")
            for user_id, count in sorted(user_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"   {user_id}: {count} 条记录")
            
            print("\n😊 情绪统计:")
            for mood, count in sorted(mood_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"   {mood}: {count} 条记录")
        
        # 测试记忆相关性
        print("\n🔍 记忆相关性测试:")
        test_queries = ["你好", "天气", "难过", "安慰", "谢谢"]
        
        for query in test_queries:
            results = memory.query_memory(query, top_k=2)
            print(f"   '{query}': 找到 {len(results)} 条相关记忆")
            if results:
                for result in results:
                    print(f"     - {result['user_text']} -> {result['ai_response'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 记忆效果分析失败: {e}")
        return False


def test_memory_in_prompt():
    """测试记忆在提示词中的使用"""
    print("🔍 测试记忆在提示词中的使用")
    print("=" * 60)
    
    try:
        from ai_core.prompt_fusion import create_prompt_factors, PromptFusionEngine
        
        # 创建提示词融合引擎
        fusion_engine = PromptFusionEngine()
        
        # 模拟记忆信息
        memory_info = {
            "summary": "用户之前说过'你好'，AI回复'你好呀！很高兴见到你！'。用户还问过天气，AI说天气不错。",
            "count": 2
        }
        
        # 创建提示词因子
        factors = create_prompt_factors(
            stage_info={"prompt": "You are in the awaken stage. Use memories to give proactive suggestions."},
            personality_info={"style": "enthusiastic", "traits": "curious, reliable, outgoing"},
            emotion_info={"emotion": "happy"},
            memory_info=memory_info,
            user_input="你能记住我们之前的对话吗？"
        )
        
        print("📋 提示词因子:")
        for factor in factors:
            print(f"   {factor.name}: {factor.content[:50]}... (权重: {factor.weight}, 优先级: {factor.priority})")
        
        # 融合提示词
        fused_prompt = fusion_engine.fuse_prompts(factors)
        
        print("\n🔧 融合后的提示词:")
        print(fused_prompt)
        
        # 检查记忆是否包含在提示词中
        if "Memory:" in fused_prompt:
            print("\n✅ 记忆信息已包含在提示词中")
        else:
            print("\n❌ 记忆信息未包含在提示词中")
        
        return True
        
    except Exception as e:
        print(f"❌ 提示词记忆测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始记忆系统分析\n" + "="*60)
    
    # 1. 测试记忆存储
    test_memory_storage()
    
    # 2. 测试记忆查询
    test_memory_query()
    
    # 3. 测试对话引擎中的记忆
    test_memory_in_dialogue()
    
    # 4. 分析记忆效果
    analyze_memory_effectiveness()
    
    # 5. 测试记忆在提示词中的使用
    test_memory_in_prompt()
    
    print("\n" + "=" * 60)
    print("🎯 记忆系统分析完成！")
    print("\n请检查上面的输出，确认:")
    print("1. 记忆是否正确存储")
    print("2. 记忆查询是否有效")
    print("3. 记忆是否在对话中被使用")
    print("4. 记忆是否包含在提示词中")


if __name__ == "__main__":
    main() 