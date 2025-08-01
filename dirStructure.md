# 项目代码结构说明

## 项目概述

CRB-main 是一个智能陪伴机器人项目，采用模块化设计，包含完整的AI对话、情绪感知、记忆管理等功能。

## 当前项目结构

```
CRB-main/
├── ai_core/                  # 核心AI模块
│   ├── __init__.py           # 模块初始化
│   ├── constants.py          # 常量定义
│   ├── dialogue_engine.py    # 对话引擎
│   ├── doubao_service.py     # 豆包服务集成
│   ├── emotion_perception.py # 情绪感知模块
│   ├── global_state.py       # 全局状态管理
│   ├── intelligent_core.py   # 智能核心调度器
│   ├── personality_engine.py # 人格引擎
│   ├── prompt_fusion.py      # 提示词融合
│   ├── qwen_service.py       # 百炼服务集成
│   ├── semantic_memory.py    # 语义记忆系统
│   ├── service_api.py        # 服务API封装
│   └── service_clients.py    # 服务客户端
├── asst/                     # 辅助工具模块
│   ├── check_growth_stage.py # 成长阶段检查
│   ├── debug_llm_call.py     # LLM调用调试
│   ├── est_growth_stage.py   # 成长阶段评估
│   ├── final_verification.py # 最终验证
│   ├── manage_growth_stage.py # 成长阶段管理
│   ├── quick_test_prompt.py  # 快速提示词测试
│   ├── show_robot_status.py  # 机器人状态显示
│   └── start_service.py      # 服务启动工具
├── ref/                      # 参考示例
│   ├── channel_qwen.py       # 百炼通道示例
│   ├── demo_qwen.py          # 百炼演示
│   └── online_doubao_client.py # 在线豆包客户端
├── tests/                    # 测试模块
│   ├── __init__.py           # 测试包初始化
│   ├── README.md             # 测试说明文档
│   ├── test_async_service.py # 异步服务测试
│   ├── test_dialogue_engine.py # 对话引擎测试
│   ├── test_doubao_integration.py # 豆包集成测试
│   ├── test_emotion_perception.py # 情绪感知测试
│   ├── test_enhanced_logging.py # 增强日志测试
│   ├── test_intelligent_core.py # 智能核心测试
│   ├── test_memory_analysis.py # 记忆分析测试
│   ├── test_memory_debug.py  # 记忆调试测试
│   ├── test_memory_fix.py    # 记忆修复测试
│   ├── test_memory_optimization.py # 记忆优化测试
│   ├── test_personality.py   # 人格测试
│   ├── test_prompt_construction.py # 提示词构建测试
│   ├── test_prompt_fusion.py # 提示词融合测试
│   ├── test_qwen_integration.py # 百炼集成测试
│   ├── test_semantic_memory.py # 语义记忆测试
│   ├── test_service_clients.py # 服务客户端测试
│   └── test_service_entry.py # 服务入口测试
├── uploads/                  # 上传文件存储
│   ├── audio_*.webm         # 音频文件
│   ├── image_*.jpg/png      # 图像文件
│   └── video_*.webm         # 视频文件
├── demo.py                   # 演示脚本
├── memory_service.py         # 记忆服务
├── service.py                # 主服务文件
├── verify_app.py             # 验证应用
├── verify.html               # 验证页面
├── requirements.txt          # 项目依赖
├── README.md                 # 项目说明
├── 新功能说明.md             # 新功能文档
├── 百炼服务使用说明.md       # 百炼服务文档
├── 项目结构说明.md           # 本文档
├── memory.db                 # SQLite记忆数据库
├── memory_backup.json        # 记忆备份文件
├── state.json                # 状态文件
└── robot_demo.log            # 演示日志
```

## 核心模块说明

### ai_core/ - 核心AI模块

#### 智能核心 (intelligent_core.py)
- **功能**: 系统调度器，协调各个模块工作
- **主要类**: `IntelligentCore`, `UserInput`
- **职责**: 处理用户输入，调用相应模块，生成响应

#### 对话引擎 (dialogue_engine.py)
- **功能**: 生成对话响应
- **主要类**: `DialogueEngine`, `DialogueResponse`
- **特点**: 支持多模态输入，融合情绪和记忆

#### 情绪感知 (emotion_perception.py)
- **功能**: 分析用户情绪状态
- **支持**: 语音情绪识别、面部表情识别、文本情绪分析
- **主要类**: `EmotionPerception`, `EmotionState`

#### 语义记忆 (semantic_memory.py)
- **功能**: 基于向量的语义记忆系统
- **存储**: SQLite数据库
- **特点**: 支持相似性搜索，记忆持久化

#### 人格引擎 (personality_engine.py)
- **功能**: 基于OCEAN模型的动态人格系统
- **维度**: 开放性、责任心、外向性、宜人性、神经质
- **特点**: 根据交互动态调整人格特征

#### 提示词融合 (prompt_fusion.py)
- **功能**: 动态构建和融合提示词
- **支持**: 多因子融合，上下文感知
- **主要类**: `PromptFusionEngine`, `PromptFactor`

#### 服务集成
- **doubao_service.py**: 豆包大模型服务集成
- **qwen_service.py**: 百炼大模型服务集成
- **service_api.py**: 统一的服务API封装

### asst/ - 辅助工具模块

#### 成长阶段管理
- **check_growth_stage.py**: 检查当前成长阶段
- **manage_growth_stage.py**: 管理成长阶段转换
- **est_growth_stage.py**: 评估成长阶段

#### 调试和测试工具
- **debug_llm_call.py**: LLM调用调试
- **quick_test_prompt.py**: 快速提示词测试
- **final_verification.py**: 最终功能验证

#### 服务管理
- **start_service.py**: 启动各种服务
- **show_robot_status.py**: 显示机器人状态

### ref/ - 参考示例

#### 服务集成示例
- **channel_qwen.py**: 百炼API通道示例
- **demo_qwen.py**: 百炼服务演示
- **online_doubao_client.py**: 在线豆包客户端示例

### tests/ - 测试模块

#### 核心功能测试
- **test_intelligent_core.py**: 智能核心测试
- **test_dialogue_engine.py**: 对话引擎测试
- **test_emotion_perception.py**: 情绪感知测试
- **test_semantic_memory.py**: 语义记忆测试

#### 服务集成测试
- **test_doubao_integration.py**: 豆包集成测试
- **test_qwen_integration.py**: 百炼集成测试
- **test_service_clients.py**: 服务客户端测试

#### 记忆系统测试
- **test_memory_analysis.py**: 记忆分析测试
- **test_memory_debug.py**: 记忆调试测试
- **test_memory_fix.py**: 记忆修复测试
- **test_memory_optimization.py**: 记忆优化测试

#### 提示词系统测试
- **test_prompt_construction.py**: 提示词构建测试
- **test_prompt_fusion.py**: 提示词融合测试

## 主要服务文件

### service.py - 主服务
- **功能**: FastAPI Web服务
- **端点**: ASR、TTS、LLM、记忆存储/查询
- **特点**: 支持文件上传，流式响应

### memory_service.py - 记忆服务
- **功能**: 独立的记忆管理服务
- **存储**: 支持文件存储和SQLite数据库
- **API**: 记忆存储和查询接口

### verify_app.py - 验证应用
- **功能**: Streamlit验证界面
- **特点**: 交互式测试各模块功能

## 数据文件

### 记忆数据
- **memory.db**: SQLite记忆数据库
- **memory_backup.json**: 记忆备份文件

### 状态文件
- **state.json**: 全局状态持久化
- **robot_demo.log**: 演示日志

### 上传文件
- **uploads/**: 用户上传的音频、图像、视频文件

## 依赖管理

### requirements.txt
```txt
# AI和机器学习库
speechbrain>=0.5.16      # 语音识别
fer>=22.4.0              # 面部表情识别
deepface>=0.0.79         # 深度人脸分析
sentence-transformers>=2.2.2  # 文本嵌入
numpy>=1.21.0            # 数值计算

# 云AI服务
dashscope>=1.13.0        # 百炼服务
openai>=1.0.0            # OpenAI服务

# Web框架
fastapi>=0.104.0         # API框架
uvicorn[standard]>=0.24.0 # ASGI服务器
streamlit>=1.28.0        # Web应用框架

# HTTP客户端
requests>=2.31.0         # HTTP请求

# 开发和测试
pytest>=7.4.0            # 测试框架
pytest-asyncio>=0.21.0   # 异步测试
```

## 运行指南

### 环境准备
```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 启动服务
```bash
# 启动主服务
python service.py

# 启动记忆服务
python memory_service.py

# 启动验证应用
streamlit run verify_app.py
```

### 运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
python tests/test_intelligent_core.py
python asst/debug_llm_call.py
```

### 使用辅助工具
```bash
# 检查成长阶段
python asst/check_growth_stage.py

# 调试LLM调用
python asst/debug_llm_call.py

# 显示机器人状态
python asst/show_robot_status.py
```

## 项目特点

### 1. 模块化设计
- 核心功能独立封装
- 清晰的模块边界
- 易于维护和扩展

### 2. 多模态支持
- 语音识别和合成
- 图像和视频处理
- 文本理解和生成

### 3. 智能记忆系统
- 语义向量存储
- 相似性搜索
- 持久化记忆

### 4. 动态人格
- OCEAN模型驱动
- 根据交互调整
- 个性化响应

### 5. 服务集成
- 支持多种AI服务
- 统一的API接口
- 容错和回退机制

## 开发规范

### 代码组织
- 按功能模块分组
- 测试文件集中管理
- 示例代码独立存放

### 文档管理
- 中文文档说明
- 详细的模块注释
- 使用示例和指南

### 版本控制
- 清晰的提交信息
- 功能分支开发
- 定期代码审查

这个项目结构现在更加清晰、规范，便于开发和维护。 