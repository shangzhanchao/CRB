# CECR

Cognitive Engine for Companion Robot (CECR) provides a set of Python modules
for building an AI companion. The core components include:

- **PersonalityEngine**: tracks OCEAN personality traits with momentum decay.
- **SemanticMemory**: stores conversation history in a vector database using
  hashed embeddings for lightweight semantic search.
- **EmotionPerception**: recognizes emotions from voice and face inputs with
  simple heuristics based on file content or name.
- **DialogueEngine**: generates responses based on personality and memory and
  evolves from cold start to active interaction.
- **IntelligentCore**: orchestrates the above modules.

These modules are located in the `ai_core` package and are designed as simple
starting points for a more advanced system.

## Architecture Overview

1. **EmotionPerception** reads audio and image inputs (`DEFAULT_AUDIO_PATH`,
   `DEFAULT_IMAGE_PATH`) and outputs a fused emotion tag.
2. **DialogueEngine** uses `PersonalityEngine` and `SemanticMemory` to produce
   responses while updating interaction stages.
3. **IntelligentCore** orchestrates the pipeline: emotion perception → memory
   query → personality update → response generation.

Parameters of each module can be customized if the default settings do not
fit your scenario.

## 简要说明

CECR 提供一系列用于构建 AI 陪伴机器人的 Python 模块，代码内含中英双语注释，方便理解和二次开发。
其中示例算法使用哈希向量检索语义记忆，并根据文件名或音量等简单特征识别情绪，对话引擎会随着交互次数从模仿型逐步过渡到主动型。

## Usage

Run `python demo.py` and start typing messages. The demo shows how the modules
work together to produce responses. Default demo files `voice.wav` and
`face.png` are used when no specific paths are provided. Type `quit` to exit.

使用方法：运行 `python demo.py`，输入内容即可与示例系统交互，输入 `quit` 结束。
如未指定语音或图像文件，系统将使用默认的 `voice.wav` 与 `face.png` 进行演示。

## Testing

Unit tests are provided for each core module. Execute them with:

```bash
python -m unittest discover -s tests
```

运行以上命令即可验证各模块和整体系统的基本功能。
