# CRB - Companion Robot Brain
# 陪伴机器人智能大脑
# CRB - Companion Robot Brain
# 陪伴机器人智能大脑

一个基于Python的AI陪伴机器人智能大脑系统，具备记忆、人格成长和情感智能功能。

## 核心特性

- **🤖 智能对话** - 基于大模型的自然语言交互
- **🧠 语义记忆** - 向量化记忆检索，支持上下文感知对话
- **👤 人格成长** - OCEAN五维人格模型，随交互动态成长
- **😊 情感识别** - 多模态情绪感知（语音、图像、文本）
- **🎯 成长阶段** - 萌芽→启蒙→共鸣→觉醒四阶段进化
- **🤗 触摸交互** - 支持头部、背后、胸口触摸反馈
- **💾 持久记忆** - SQLite数据库存储，重启后记忆不丢失

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
# 启动HTTP服务
python service.py

# 或使用uvicorn（支持热重载）
uvicorn service:app --reload
```

### 访问界面
打开浏览器访问：`http://localhost:8000/verify`

## 系统架构

### 核心模块

| 模块 | 功能描述 |
|------|----------|
| `IntelligentCore` | 智能核心，统一调度各模块 |
| `PersonalityEngine` | 人格成长引擎，维护OCEAN五维人格 |
| `EnhancedMemorySystem` | 增强记忆系统，向量化语义记忆 |
| `EmotionPerception` | 情绪感知模块，多模态情绪识别 |
| `EnhancedDialogueEngine` | 增强对话引擎，成长式对话生成 |
| `PromptFusionEngine` | 提示词融合引擎，智能组合各种因素 |

### 数据流程

```
用户输入 → 情绪识别 → 记忆检索 → 人格成长 → 提示词融合 → 对话生成 → 输出反馈
```

## 成长阶段

| 阶段 | 触发条件 | 特征描述 |
|------|----------|----------|
| **萌芽期** | 0-3天，<5次交互 | 以咿呀声和动作为主 |
| **启蒙期** | 3-10天，<20次交互 | 模仿简单问候语 |
| **共鸣期** | 10-30天，<50次交互 | 短句对话，提出问题 |
| **觉醒期** | 30天以上 | 记忆对话，主动建议 |

## 外部服务

系统支持以下外部服务（可选）：

| 服务 | 功能 | 默认地址 |
|------|------|----------|
| **ASR** | 语音识别 | `asr.szc.com` |
| **TTS** | 语音合成 | `tts.szc.com` |
| **LLM** | 大模型推理 | `llm.szc.com` |
| **声纹识别** | 用户识别 | `voiceprint.szc.com` |

可通过环境变量自定义服务地址：
```bash
export LLM_URL="your-llm-service.com"
export TTS_URL="your-tts-service.com"
```

## API接口

### 交互接口
```bash
POST /interact
Content-Type: application/json

{
  "robot_id": "robotA",
  "text": "你好",
  "touch_zone": 0
}
```

### 响应格式
```json
{
  "text": "你好，很高兴见到你！",
  "audio": "audio_001.wav",
  "action": ["wave_hand", "smile"],
  "expression": "happy"
}
```

## 项目结构

```
CRB-main/
├── ai_core/                 # 核心AI模块
│   ├── intelligent_core.py  # 智能核心
│   ├── enhanced_dialogue_engine.py  # 增强对话引擎
│   ├── enhanced_memory_system.py   # 增强记忆系统
│   ├── personality_engine.py       # 人格引擎
│   ├── emotion_perception.py       # 情绪感知
│   └── prompt_fusion.py           # 提示词融合
├── services/                # 服务层
│   ├── session_service.py   # 会话服务
│   └── file_service.py      # 文件服务
├── data/                    # 数据文件
│   └── intimacy_robotA.json # 亲密度数据
├── service.py              # HTTP服务入口
├── requirements.txt        # 依赖列表
└── enhanced_memory.db      # 统一数据库
```

## 配置说明

### 环境变量
```bash
# 服务地址配置
LLM_URL=your-llm-service.com
TTS_URL=your-tts-service.com
ASR_URL=your-asr-service.com

# 日志级别
LOG_LEVEL=INFO
```

### 数据库
- **统一数据库**：`enhanced_memory.db` 存储所有数据
  - 会话历史记录
  - 语义记忆向量
  - 人格成长数据
  - 亲密度信息

## 开发指南

### 运行测试
```bash
python -m unittest discover -s tests
```

### 命令行演示
```bash
python demo.py --robot_id robotA --text "你好"
```

### 自定义开发
```python
from ai_core.intelligent_core import IntelligentCore, UserInput

# 创建智能核心
core = IntelligentCore(robot_id="robotA")

# 处理用户输入
user_input = UserInput(
    robot_id="robotA",
    text="你好",
    touch_zone=0
)

# 获取响应
response = core.process(user_input)
print(response.text)
```

## 技术特性

### 记忆系统
- **向量化检索**：使用sentence-transformers进行语义搜索
- **智能摘要**：自动生成对话上下文摘要
- **权重融合**：智能加权各种记忆因素
- **持久化存储**：SQLite数据库确保数据安全

### 提示词融合
- **多因子融合**：成长阶段、人格、情绪、记忆、触摸
- **智能权重**：根据重要性动态调整权重
- **优先级排序**：确保关键因素优先考虑

### 情感识别
- **多模态感知**：语音、图像、文本综合分析
- **情绪标签**：13种标准情绪状态
- **容错机制**：模型不可用时使用规则推理

## 更新日志

### 最新优化
- ✅ **数据库合并**：统一使用`enhanced_memory.db`，简化数据管理
- ✅ **记忆系统增强**：优化向量检索和智能摘要生成
- ✅ **提示词融合**：改进多因子融合算法
- ✅ **界面优化**：调整文本框高度，提升用户体验
- ✅ **依赖更新**：精简requirements.txt，移除未使用依赖

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进项目。

---

**CRB - 让AI陪伴更有温度** 🌟
