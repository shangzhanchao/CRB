# 测试文件说明

本文件夹包含项目的所有测试文件，用于验证系统功能和调试问题。

## 文件结构

### 核心功能测试
- `debug_llm_call.py` - 调试LLM调用问题，验证百炼API集成
- `test_prompt_fusion.py` - 测试提示词融合算法
- `quick_test_prompt.py` - 快速测试提示词构建
- `test_prompt_construction.py` - 详细测试提示词构建和LLM调用

### 成长阶段管理
- `check_growth_stage.py` - 检查机器人成长阶段
- `manage_growth_stage.py` - 手动管理成长阶段
- `est_growth_stage.py` - 成长阶段测试

### 服务功能测试
- `test_memory_fix.py` - 测试记忆服务修复
- `start_service.py` - 验证服务启动
- `final_verification.py` - 最终功能验证

### 原有测试文件
- `test_qwen_integration.py` - 百炼集成测试
- `test_async_service.py` - 异步服务测试
- `test_dialogue_engine.py` - 对话引擎测试
- `test_emotion_perception.py` - 情绪感知测试
- `test_intelligent_core.py` - 智能核心测试
- `test_personality.py` - 人格测试
- `test_semantic_memory.py` - 语义记忆测试
- `test_service_clients.py` - 服务客户端测试
- `test_service_entry.py` - 服务入口测试

## 运行测试

### 单个测试
```bash
# 调试LLM调用
python tests/debug_llm_call.py

# 检查成长阶段
python tests/check_growth_stage.py

# 管理成长阶段
python tests/manage_growth_stage.py

# 快速测试提示词
python tests/quick_test_prompt.py
```

### 批量测试
```bash
# 运行所有测试（需要pytest）
pytest tests/

# 运行特定类型的测试
pytest tests/test_*.py
```

## 注意事项

1. 所有测试文件都已更新路径，可以正确导入项目模块
2. 测试文件使用相对路径访问项目根目录的文件（如 `state.json`）
3. 部分测试需要服务运行，请先启动 `python service.py`
4. 调试类测试会输出详细日志，便于排查问题

## 测试分类

### 功能验证测试
- 验证系统核心功能是否正常工作
- 检查API调用是否成功
- 确认数据处理流程正确

### 调试测试
- 排查特定问题（如LLM调用失败）
- 输出详细日志信息
- 帮助定位问题根源

### 集成测试
- 测试多个模块的协作
- 验证端到端功能
- 确保系统整体稳定

### 性能测试
- 测试系统响应时间
- 验证并发处理能力
- 检查资源使用情况 