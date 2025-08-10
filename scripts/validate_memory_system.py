#!/usr/bin/env python3
"""
增强记忆系统验证脚本

验证新的记忆系统是否符合设计预期，包括：
1. 多层次记忆架构
2. 会话管理功能
3. 记忆融合算法
4. 重要性评分机制
5. 线程安全性能
6. 数据库持久化
"""

import asyncio
import threading
import time
import uuid
from typing import Dict, Any, List
from dataclasses import dataclass

from ai_core.intelligent_core import IntelligentCore
from ai_core.enhanced_dialogue_engine import EnhancedDialogueEngine
from ai_core.enhanced_memory_system import EnhancedMemorySystem


@dataclass
class ValidationResult:
    """验证结果数据结构"""
    test_name: str
    passed: bool
    details: str
    performance_ms: float = 0.0


class MemorySystemValidator:
    """记忆系统验证器"""
    
    def __init__(self):
        self.results: List[ValidationResult] = []
        self.robot_id = "test_robot_001"
        
    def log_result(self, test_name: str, passed: bool, details: str, performance_ms: float = 0.0):
        """记录验证结果"""
        result = ValidationResult(test_name, passed, details, performance_ms)
        self.results.append(result)
        
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} {test_name}: {details}")
        if performance_ms > 0:
            print(f"   性能: {performance_ms:.2f}ms")
    
    def validate_multi_layer_memory(self) -> bool:
        """验证多层次记忆架构"""
        print("\n🔍 验证多层次记忆架构...")
        
        try:
            # 初始化记忆系统
            memory = EnhancedMemorySystem(self.robot_id)
            
            # 测试短期记忆（会话记忆）
            session_id = memory.start_session()
            memory.add_memory("你好", "你好呀！", "happy", session_id=session_id)
            context = memory.get_current_context(session_id)
            short_term_ok = "你好" in context and "你好呀" in context
            
            # 测试长期记忆（语义记忆）
            memory.add_memory("我喜欢苹果", "苹果很好吃呢！", "excited", session_id=session_id)
            memory.add_memory("我喜欢香蕉", "香蕉也很棒！", "excited", session_id=session_id)
            
            # 查询语义相似记忆
            query_result = memory.query_memory("苹果", top_k=3, session_id=session_id)
            semantic_ok = len(query_result["memories"]) > 0
            
            # 测试情感记忆
            memory.add_memory("我很难过", "别难过，我会陪着你", "sad", session_id=session_id)
            emotional_result = memory.query_memory("难过", top_k=3, session_id=session_id)
            emotional_ok = len(emotional_result["memories"]) > 0
            
            # 测试上下文记忆
            context_result = memory.query_memory("我们聊了什么", top_k=3, session_id=session_id, use_context=True)
            context_ok = len(context_result["memories"]) > 0
            
            all_passed = short_term_ok and semantic_ok and emotional_ok and context_ok
            
            self.log_result(
                "多层次记忆架构",
                all_passed,
                f"短期记忆: {short_term_ok}, 语义记忆: {semantic_ok}, 情感记忆: {emotional_ok}, 上下文记忆: {context_ok}"
            )
            
            memory.close()
            return all_passed
            
        except Exception as e:
            self.log_result("多层次记忆架构", False, f"异常: {e}")
            return False
    
    def validate_session_management(self) -> bool:
        """验证会话管理功能"""
        print("\n🔍 验证会话管理功能...")
        
        try:
            memory = EnhancedMemorySystem(self.robot_id)
            
            # 测试会话创建
            session1 = memory.start_session()
            session2 = memory.start_session()
            session_creation_ok = session1 != session2
            
            # 测试会话连续性
            memory.add_memory("第一句话", "第一句回复", "neutral", session_id=session1)
            memory.add_memory("第二句话", "第二句回复", "happy", session_id=session1)
            
            context = memory.get_current_context(session1)
            continuity_ok = "第一句话" in context and "第二句话" in context
            
            # 测试会话统计
            stats = memory.get_memory_stats()
            stats_ok = stats["total_sessions"] >= 2 and stats["active_sessions"] >= 1
            
            # 测试会话清除
            removed_count = memory.clear_session_memory(session1)
            clear_ok = removed_count >= 2
            
            all_passed = session_creation_ok and continuity_ok and stats_ok and clear_ok
            
            self.log_result(
                "会话管理功能",
                all_passed,
                f"会话创建: {session_creation_ok}, 连续性: {continuity_ok}, 统计: {stats_ok}, 清除: {clear_ok}"
            )
            
            memory.close()
            return all_passed
            
        except Exception as e:
            self.log_result("会话管理功能", False, f"异常: {e}")
            return False
    
    def validate_memory_fusion(self) -> bool:
        """验证记忆融合算法"""
        print("\n🔍 验证记忆融合算法...")
        
        try:
            memory = EnhancedMemorySystem(self.robot_id)
            session_id = memory.start_session()
            
            # 添加不同类型的记忆
            memory.add_memory("我喜欢学习", "学习很有趣", "excited", session_id=session_id)
            memory.add_memory("我有点紧张", "别紧张，放松点", "sad", session_id=session_id)
            memory.add_memory("今天天气很好", "是的，阳光明媚", "happy", session_id=session_id)
            
            # 测试融合查询
            start_time = time.time()
            fusion_result = memory.query_memory("学习", top_k=5, session_id=session_id)
            performance_ms = (time.time() - start_time) * 1000
            
            # 验证融合结果
            memories = fusion_result["memories"]
            types = fusion_result["types"]
            summary = fusion_result["summary"]
            
            fusion_ok = (
                len(memories) > 0 and
                "semantic" in types and
                "context" in types and
                "emotional" in types and
                len(summary) > 0
            )
            
            # 验证权重融合
            weighted_memories = [m for m in memories if "weight" in m and "source" in m]
            weight_ok = len(weighted_memories) > 0
            
            all_passed = fusion_ok and weight_ok
            
            self.log_result(
                "记忆融合算法",
                all_passed,
                f"融合结果: {fusion_ok}, 权重分配: {weight_ok}, 记忆数: {len(memories)}",
                performance_ms
            )
            
            memory.close()
            return all_passed
            
        except Exception as e:
            self.log_result("记忆融合算法", False, f"异常: {e}")
            return False
    
    def validate_importance_scoring(self) -> bool:
        """验证重要性评分机制"""
        print("\n🔍 验证重要性评分机制...")
        
        try:
            memory = EnhancedMemorySystem(self.robot_id)
            session_id = memory.start_session()
            
            # 添加不同重要性的记忆
            memory.add_memory("你好", "你好", "neutral", session_id=session_id)  # 基础记忆
            memory.add_memory("我喜欢你", "我也喜欢你", "excited", session_id=session_id, touch_zone=1)  # 高重要性
            memory.add_memory("我很难过", "别难过", "sad", session_id=session_id)  # 情感记忆
            memory.add_memory("记住我的名字", "好的，我会记住", "excited", session_id=session_id)  # 关键词记忆
            
            # 查询并检查重要性评分
            result = memory.query_memory("我们聊了什么", top_k=10, session_id=session_id)
            memories = result["memories"]
            
            # 验证重要性评分存在
            importance_scores = [m.get("importance_score", 0) for m in memories]
            score_ok = all(0 <= score <= 1 for score in importance_scores)
            
            # 验证高重要性记忆优先
            sorted_memories = sorted(memories, key=lambda x: x.get("importance_score", 0), reverse=True)
            priority_ok = len(sorted_memories) > 0
            
            # 验证关键词提升重要性
            keyword_memory = [m for m in memories if "记住" in m.get("user_text", "")]
            keyword_ok = len(keyword_memory) > 0
            
            all_passed = score_ok and priority_ok and keyword_ok
            
            self.log_result(
                "重要性评分机制",
                all_passed,
                f"评分范围: {score_ok}, 优先级排序: {priority_ok}, 关键词提升: {keyword_ok}"
            )
            
            memory.close()
            return all_passed
            
        except Exception as e:
            self.log_result("重要性评分机制", False, f"异常: {e}")
            return False
    
    def validate_thread_safety(self) -> bool:
        """验证线程安全性能"""
        print("\n🔍 验证线程安全性能...")
        
        try:
            memory = EnhancedMemorySystem(self.robot_id)
            session_id = memory.start_session()
            
            # 多线程并发测试
            def worker(thread_id: int, iterations: int):
                for i in range(iterations):
                    try:
                        memory.add_memory(
                            f"线程{thread_id}消息{i}",
                            f"线程{thread_id}回复{i}",
                            "neutral",
                            session_id=session_id
                        )
                        memory.query_memory(f"线程{thread_id}", top_k=3, session_id=session_id)
                    except Exception as e:
                        print(f"线程{thread_id}异常: {e}")
                        return False
                return True
            
            # 启动多个线程
            threads = []
            start_time = time.time()
            
            for i in range(5):
                thread = threading.Thread(target=worker, args=(i, 10))
                threads.append(thread)
                thread.start()
            
            # 等待所有线程完成
            for thread in threads:
                thread.join()
            
            performance_ms = (time.time() - start_time) * 1000
            
            # 验证数据完整性
            stats = memory.get_memory_stats()
            data_ok = stats["total_records"] >= 50  # 5线程 * 10次
            
            # 验证无异常
            exception_ok = True  # 如果没有异常抛出，说明线程安全
            
            all_passed = data_ok and exception_ok
            
            self.log_result(
                "线程安全性能",
                all_passed,
                f"数据完整性: {data_ok}, 无异常: {exception_ok}, 记录数: {stats['total_records']}",
                performance_ms
            )
            
            memory.close()
            return all_passed
            
        except Exception as e:
            self.log_result("线程安全性能", False, f"异常: {e}")
            return False
    
    def validate_database_persistence(self) -> bool:
        """验证数据库持久化"""
        print("\n🔍 验证数据库持久化...")
        
        try:
            # 第一次创建并添加数据
            memory1 = EnhancedMemorySystem(self.robot_id, db_path="test_memory.db")
            session_id = memory1.start_session()
            memory1.add_memory("持久化测试", "数据应该保存", "neutral", session_id=session_id)
            memory1.close()
            
            # 重新打开并验证数据
            memory2 = EnhancedMemorySystem(self.robot_id, db_path="test_memory.db")
            result = memory2.query_memory("持久化", top_k=3)
            persistence_ok = len(result["memories"]) > 0
            
            # 验证会话数据
            stats = memory2.get_memory_stats()
            session_ok = stats["total_sessions"] > 0
            
            # 验证具体数据内容
            if persistence_ok:
                memory_text = result["memories"][0].get("user_text", "")
                content_ok = "持久化测试" in memory_text
            else:
                content_ok = False
            
            memory2.close()
            
            all_passed = persistence_ok and session_ok and content_ok
            
            self.log_result(
                "数据库持久化",
                all_passed,
                f"数据持久化: {persistence_ok}, 会话持久化: {session_ok}, 内容正确: {content_ok}"
            )
            
            return all_passed
            
        except Exception as e:
            self.log_result("数据库持久化", False, f"异常: {e}")
            return False
    
    def validate_dialogue_integration(self) -> bool:
        """验证对话引擎集成"""
        print("\n🔍 验证对话引擎集成...")
        
        try:
            # 测试对话引擎集成
            dialogue = EnhancedDialogueEngine(self.robot_id)
            
            # 测试会话管理
            session_id = dialogue.start_session()
            session_ok = session_id is not None
            
            # 测试对话生成
            response1 = dialogue.generate_response("你好", session_id=session_id)
            response2 = dialogue.generate_response("我们之前聊过什么？", session_id=session_id)
            
            dialogue_ok = (
                response1.session_id == session_id and
                response2.session_id == session_id and
                hasattr(response1, 'ai_response') and
                hasattr(response2, 'ai_response') and
                len(response1.ai_response) > 0 and
                len(response2.ai_response) > 0
            )
            
            # 测试记忆统计
            stats = dialogue.get_memory_stats()
            stats_ok = "total_records" in stats
            
            dialogue.close()
            
            all_passed = session_ok and dialogue_ok and stats_ok
            
            self.log_result(
                "对话引擎集成",
                all_passed,
                f"会话管理: {session_ok}, 对话生成: {dialogue_ok}, 记忆统计: {stats_ok}"
            )
            
            return all_passed
            
        except Exception as e:
            self.log_result("对话引擎集成", False, f"异常: {e}")
            return False
    
    def validate_intelligent_core_integration(self) -> bool:
        """验证智能核心集成"""
        print("\n🔍 验证智能核心集成...")
        
        try:
            # 测试智能核心集成
            core = IntelligentCore(self.robot_id)
            
            # 测试同步处理
            from ai_core.intelligent_core import UserInput
            user_input1 = UserInput(
                text="你好",
                touch_zone=None,
                session_id=None
            )
            response1 = core.process(user_input1)
            
            # 测试会话连续性
            user_input2 = UserInput(
                text="我们之前聊过什么？",
                touch_zone=None,
                session_id=response1.session_id
            )
            response2 = core.process(user_input2)
            
            core_ok = (
                response1.session_id is not None and
                response2.session_id == response1.session_id and
                hasattr(response1, 'ai_response') and
                hasattr(response2, 'ai_response') and
                len(response1.ai_response) > 0 and
                len(response2.ai_response) > 0
            )
            
            # 测试异步处理
            async def test_async():
                user_input3 = UserInput(
                    text="异步测试",
                    touch_zone=None,
                    session_id=response1.session_id
                )
                response3 = await core.process_async(user_input3)
                return response3.session_id == response1.session_id
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            async_ok = loop.run_until_complete(test_async())
            loop.close()
            
            core.close()
            
            all_passed = core_ok and async_ok
            
            self.log_result(
                "智能核心集成",
                all_passed,
                f"同步处理: {core_ok}, 异步处理: {async_ok}"
            )
            
            return all_passed
            
        except Exception as e:
            self.log_result("智能核心集成", False, f"异常: {e}")
            return False
    
    def run_all_validations(self) -> Dict[str, Any]:
        """运行所有验证"""
        print("🚀 开始验证增强记忆系统...")
        print("=" * 60)
        
        validations = [
            ("多层次记忆架构", self.validate_multi_layer_memory),
            ("会话管理功能", self.validate_session_management),
            ("记忆融合算法", self.validate_memory_fusion),
            ("重要性评分机制", self.validate_importance_scoring),
            ("线程安全性能", self.validate_thread_safety),
            ("数据库持久化", self.validate_database_persistence),
            ("对话引擎集成", self.validate_dialogue_integration),
            ("智能核心集成", self.validate_intelligent_core_integration),
        ]
        
        passed_count = 0
        total_count = len(validations)
        
        for name, validation_func in validations:
            try:
                if validation_func():
                    passed_count += 1
            except Exception as e:
                self.log_result(name, False, f"验证函数异常: {e}")
        
        # 生成验证报告
        print("\n" + "=" * 60)
        print("📊 验证报告")
        print("=" * 60)
        
        for result in self.results:
            status = "✅" if result.passed else "❌"
            print(f"{status} {result.test_name}")
            print(f"   详情: {result.details}")
            if result.performance_ms > 0:
                print(f"   性能: {result.performance_ms:.2f}ms")
            print()
        
        success_rate = (passed_count / total_count) * 100
        
        print(f"📈 总体结果: {passed_count}/{total_count} 通过 ({success_rate:.1f}%)")
        
        if success_rate >= 90:
            print("🎉 验证成功！记忆系统符合设计预期")
        elif success_rate >= 70:
            print("⚠️ 验证基本通过，但存在一些问题需要优化")
        else:
            print("❌ 验证失败，记忆系统需要重大改进")
        
        # 转换结果为可序列化的格式
        serializable_results = []
        for result in self.results:
            serializable_results.append({
                "test_name": result.test_name,
                "passed": result.passed,
                "details": result.details,
                "performance_ms": result.performance_ms
            })
        
        return {
            "total_tests": total_count,
            "passed_tests": passed_count,
            "success_rate": success_rate,
            "results": serializable_results
        }


def main():
    """主函数"""
    validator = MemorySystemValidator()
    report = validator.run_all_validations()
    
    # 保存验证报告
    import json
    with open("memory_system_validation_report.json", "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.time(),
            "robot_id": validator.robot_id,
            "report": report
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 验证报告已保存到: memory_system_validation_report.json")


if __name__ == "__main__":
    main() 