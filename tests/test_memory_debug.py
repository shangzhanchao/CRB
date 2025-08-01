#!/usr/bin/env python3
"""测试记忆系统的调试脚本"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_core.semantic_memory import SemanticMemory
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO)

def test_memory_system():
    """测试记忆系统的各个功能"""
    print("=== 记忆系统调试测试 ===")
    
    # 1. 初始化记忆系统
    print("\n1. 初始化记忆系统...")
    memory = SemanticMemory()
    print(f"记忆记录总数: {len(memory.records)}")
    
    # 2. 测试记忆查询
    print("\n2. 测试记忆查询...")
    test_queries = ["你好", "天气", "今天", "机器人"]
    
    for query in test_queries:
        print(f"\n查询: '{query}'")
        results = memory.query_memory(query, top_k=3)
        print(f"找到 {len(results)} 条相关记录")
        
        for i, result in enumerate(results[:3], 1):
            print(f"  {i}. 用户: {result['user_text']}")
            print(f"     AI: {result['ai_response']}")
            print(f"     情绪: {result['mood_tag']}")
            print(f"     时间: {result['time']}")
    
    # 3. 测试记忆添加
    print("\n3. 测试记忆添加...")
    test_memory = {
        "user_text": "测试记忆功能",
        "ai_response": "这是一个测试回复",
        "mood_tag": "happy",
        "user_id": "test_user"
    }
    
    memory.add_memory(**test_memory)
    print("添加测试记忆完成")
    
    # 4. 再次查询测试
    print("\n4. 再次查询测试记忆...")
    results = memory.query_memory("测试记忆功能", top_k=3)
    print(f"查询'测试记忆功能'的结果数: {len(results)}")
    
    for i, result in enumerate(results[:3], 1):
        print(f"  {i}. 用户: {result['user_text']}")
        print(f"     AI: {result['ai_response']}")
        print(f"     情绪: {result['mood_tag']}")
    
    # 5. 检查向量嵌入
    print("\n5. 测试向量嵌入...")
    test_text = "你好，机器人"
    vector = memory._embed(test_text)
    print(f"文本: '{test_text}'")
    print(f"向量维度: {len(vector)}")
    print(f"向量前5个值: {vector[:5]}")
    
    # 6. 检查数据库内容
    print("\n6. 检查数据库内容...")
    import sqlite3
    conn = sqlite3.connect('memory.db')
    cur = conn.cursor()
    
    # 检查表结构
    cur.execute("PRAGMA table_info(memory)")
    columns = cur.fetchall()
    print("数据库表结构:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # 检查记录数
    cur.execute("SELECT COUNT(*) FROM memory")
    count = cur.fetchone()[0]
    print(f"数据库记录总数: {count}")
    
    # 检查最近的记录
    cur.execute("SELECT user_text, ai_response, mood_tag FROM memory ORDER BY time DESC LIMIT 5")
    recent_records = cur.fetchall()
    print("最近的5条记录:")
    for i, record in enumerate(recent_records, 1):
        print(f"  {i}. 用户: {record[0]}, AI: {record[1]}, 情绪: {record[2]}")
    
    conn.close()

if __name__ == "__main__":
    test_memory_system() 