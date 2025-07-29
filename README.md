# CECR

Cognitive Engine for Companion Robot (CECR) provides a set of Python modules
for building an AI companion. The core components include:

- **PersonalityEngine**: tracks OCEAN personality traits with momentum decay.
- **SemanticMemory**: stores conversation history in a vector database.
- **EmotionPerception**: recognizes emotions from voice and face inputs.
- **DialogueEngine**: generates responses based on personality and memory.
- **IntelligentCore**: orchestrates the above modules.

These modules are located in the `ai_core` package and are designed as simple
starting points for a more advanced system.

## 简要说明

CECR 提供一系列用于构建 AI 陪伴机器人的 Python 模块，代码内含中英双语注释，方便理解和二次开发。

## Usage

Run `python demo.py` and start typing messages. The demo shows how the modules
work together to produce responses. Type `quit` to exit.

使用方法：运行 `python demo.py`，输入内容即可与示例系统交互，输入 `quit` 结束。
