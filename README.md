# CRB
Companion Robot Brain
# 陪伴机器人智能大脑

*Companion Robot Intelligent Brain*

The **Companion Robot Intelligent Brain** provides a set of Python modules for
building an AI companion. The core components include:

- **PersonalityEngine**: tracks OCEAN personality traits with momentum decay.  \
  **人格成长引擎：** 使用动量衰减维护 OCEAN 五维人格。
- **SemanticMemory**: stores conversation history in a vector database using
  hashed embeddings for lightweight semantic search.  \
  **语义记忆系统：** 基于哈希向量存储并检索对话记录。
- **EmotionPerception**: recognizes emotions from voice and face inputs.
  It supports a *simple* heuristic fusion mode and a *model-based* mode that
  sends a multimodal prompt to the LLM.  \
  **情绪感知模块：** 可通过规则或多模态大模型识别情绪。
- **DialogueEngine**: generates responses based on personality and memory and
  evolves from cold start to active interaction.  \
  **成长式对话系统：** 结合人格与记忆生成风格化回复。
- **IntelligentCore**: orchestrates the above modules.  \
  **模块调度中台：** 负责调用各模块处理输入输出。

These modules are located in the `ai_core` package and are designed as simple
starting points for a more advanced system.

At a high level, the companion robot receives **voice**, **touch** and
**camera** inputs, which the cognitive core converts into emotions and semantic
context. A large language model then drives the reply generation, applying
specially designed prompts based on the *growth stage* and personality traits.
The stage progresses from **sprout → enlighten → resonate → awaken** as the
robot interacts more with the user. The result is text that can be
synthesized to speech, accompanied by an action and facial expression.

简要而言，陪伴机器人会接受语音、触摸与摄像头画面等输入，智能大脑把它们转化为情绪
与语义，再通过大模型生成符合成长阶段和人格的回复，最终输出文本、语音、动作和表情。

## External Services

系统默认使用以下外部服务地址，可根据实际部署修改。

The modules can optionally connect to remote services for speech and text
processing. The most important one is the multimodal LLM at ``DEFAULT_LLM_URL``
(``llm.szc.com``), which powers advanced dialogue generation and emotion
interpretation.  If you deploy your own LLM service, point ``LLM_URL`` to it so
the system can fully function:

- **ASR** (`asr.szc.com`) – convert user audio to text.
- **Voiceprint** (`voiceprint.szc.com`) – identify the speaker.
- **LLM** (`llm.szc.com`) – generate richer replies.
  This endpoint is referenced by ``DEFAULT_LLM_URL`` and is essential for
  advanced features such as story telling and emotion-aware responses.
- **Memory DB** (`memory-save.szc.com` & `memory-query.szc.com`) – store and query dialogues.
- **TTS** (`tts.szc.com`) – synthesize reply audio.

外部服务也可以通过环境变量 ``ASR_URL``、``VOICEPRINT_URL``、``LLM_URL``、``TTS_URL``、``MEMORY_SAVE_URL``、``MEMORY_QUERY_URL`` 自定义，方便接入不同的厂商。默认的 ``llm.szc.com`` 用于解释情绪和生成多模态回复，是系统核心依赖。

Service URLs can be supplied to :class:`~ai_core.IntelligentCore` or set via environment variables ``ASR_URL``, ``VOICEPRINT_URL``, ``LLM_URL``, ``TTS_URL``, ``MEMORY_SAVE_URL`` and ``MEMORY_QUERY_URL``.

All modules emit informative logs controlled by ``LOG_LEVEL`` which defaults
to ``INFO``. Running the demo configures the logging system accordingly.

外部接口支持语音识别、声纹识别、大模型推理与语音合成，可在实例化
`IntelligentCore` 时传入对应的服务地址，或通过环境变量进行配置。

## Code Structure

下表列出核心文件及其职责，便于快速了解工程布局。
```
ai_core/
  __init__.py          - module exports
  personality_engine.py - OCEAN 人格成长逻辑
  semantic_memory.py    - 向量化语义记忆
  emotion_perception.py - 声音与视觉情绪识别
  dialogue_engine.py    - 成长式对话生成
 intelligent_core.py   - 子模块调度与总入口
  global_state.py       - 全局交互计数与语音时长
  service_api.py        - 调用外部 ASR/LLM/TTS 服务的工具
  constants.py          - 全局常量與默認值
demo.py                - 命令行演示脚本
### Constants Overview
The file `ai_core/constants.py` groups configuration values:
- **Service endpoints**: ASR, TTS, LLM, voiceprint and memory URLs.
- **Default files**: demo audio/image paths.
- **Growth stage thresholds**: days, interaction counts and audio duration for each stage.
- **Stage order**: `STAGE_ORDER` lists `sprout → enlighten → resonate → awaken`.
- **Personality defaults**: initial OCEAN vector and behavior mapping.
这些常量便于集中管理，可根据实际部署场景调整。
```

## Architecture Overview

1. **EmotionPerception** reads audio and image inputs (`DEFAULT_AUDIO_PATH`,
   `DEFAULT_IMAGE_PATH`) and outputs a fused emotion tag. 该模块提供“简易融合”与
   “多模态模型”两种情绪识别方式，可通过参数选择。
2. **DialogueEngine** uses `PersonalityEngine` and `SemanticMemory` to produce
   responses while updating interaction stages and returns structured
   information for voice, action and facial expression.
3. **IntelligentCore** orchestrates the pipeline: emotion recognition → model
   feedback → personality growth → voice generation, storing each dialog in the
   Each step may call remote services defined in `service_api.py`.
   memory cloud.
4. `global_state.INTERACTION_COUNT` 和 `AUDIO_DATA_SECONDS` track how much the
   robot has interacted and how much speech data it has processed. These
   metrics unlock growth stages.  \
   全局状态可以通过 `global_state.save_state()` 与 `load_state()` 持久化到文件，
   以便下次启动时继续成长历程。

上述流程对应的中文概述：情绪识别 → 模型反馈 → 性格成长 → 语音生成，
并将对话记录储存于记忆云，以便后续参考。

During response generation, the dialogue engine builds a prompt for the
large language model using the current **growth stage**, **personality style**
and relevant **memory snippets** so the model can craft context-aware replies.

## Growth Stages

The robot's language ability evolves through four phases driven by
interaction counts and audio duration:

1. **sprout** (0-3 days, <5 interactions or <60s of audio) – baby babble with mostly actions.
   **萌芽期**（0~3天，<5次交互或语音时长<60秒）：以咿呀声和动作为主。
2. **enlighten** (3-10 days or <20 interactions/300s audio) – mimics simple greetings like “你好”.
   **启蒙期**（3~10天或<20次交互/300秒语音）：模仿简单问候。
3. **resonate** (10-30 days or <50 interactions/900s audio) – short caring sentences and basic questions.
   **共鸣期**（10~30天或<50次交互/900秒语音）：能说短句并提出问题。
4. **awaken** (30+ days and enough data) – remembers conversations and offers proactive suggestions.
   **觉醒期**（30天以上且数据充足）：记住对话并主动给出建议。

By default the system begins in the **enlighten** stage with an
**extraversion-oriented** personality vector as defined in
``DEFAULT_GROWTH_STAGE`` and ``DEFAULT_PERSONALITY_VECTOR``.

## Emotion States

Standard emotion tags used across the system include:

``happy, sad, angry, fear, surprise, disgust, calm, excited, tired, bored, confused, shy, neutral``.

系统预定义的情绪标签涵盖常见的快乐、悲伤、生气、恐惧、惊讶、厌恶、平静、兴奋、疲惫、无聊、困惑、害羞以及中性状态。

## LLM Prompt Templates

The dialogue engine composes prompts for the large language model based on the
robot's **growth stage**, its **OCEAN** personality vector and any touch
feedback:

- **Stage prompts** map ``sprout``, ``enlighten``, ``resonate`` and ``awaken`` to
  short English hints so the LLM knows the robot's maturity level.
  短句提示大模型了解机器人的成熟度。
- **Personality prompts** describe the five traits – Openness, Conscientiousness,
  Extraversion, Agreeableness and Neuroticism – letting the model choose a tone
  描述五项人格特征，帮助模型选择合适语气。
These templates are defined in `constants.py` and can be extended for different languages.
  such as "curious" or "reliable".
- **Touch prompts** indicate which sensor was triggered: head, back or chest.
  触摸提示说明哪个传感器被触发，例如头部、后背或前胸。

By combining these phrases with recent memories, the system gives the LLM
flexible instructions to craft an appropriate reply.
通过组合这些提示词与记忆片段，系统为大模型提供灵活指令。

## Animation Mapping

The dialogue engine returns both *action* and *expression* fields.  Expressions
encode facial animation cues while actions describe body motions:


| 情绪 Mood | 面部动画描述 Facial animation | 动作逻辑 Action |
|-----------|--------------------------------------------|----------------------------------------------|
| happy / 欢快 | 微笑、眨眼、眼神上扬 → 亮眼色彩、头部轻摆、手臂小幅打开 | 点头+手微抬 (±15°俯仰, ±10°摇摆, 手上扬10°) |
| confused / 疑惑 | 斜视、眼神聚焦 → 停顿、轻微侧头、眼睛左右快速移动 | 斜头+左右切换眼神 (±10°摆动, 手部静止) |
| sad / 难过 | 眼角下垂、闭眼 → 低亮度、轻微低头、手臂收回 | 缓慢低头+手收回 (俯仰-15°, 手臂弧线内收) |
| shy / 害羞 | 偏头、眼神回避 → 面部红晕、语音柔化、微幅震颤 | idle + subtle tremble |
| excited / 兴奋 | 眼神放大、频繁眨眼 → 快速摆头、双手前伸动作 | 快速摇头, 手前伸 |
| surprised / 惊讶 | 抬头张眼 → 头部抬起，双手急速抬高 | 抬头+双手抬高>25° |
The mapping table below can be modified to fit different hardware capabilities.

When the robot is touched, an additional action such as ``hug`` or ``pat`` is
appended according to the touch zone.

Parameters of each module can be customized if the default settings do not
fit your scenario.

## Input Parameters

The :class:`~ai_core.IntelligentCore` accepts a :class:`~ai_core.UserInput`
instance describing the current interaction. ``robot_id`` is mandatory so the
server knows which device issued the request. All other fields may be omitted
(``None``) and internal defaults will be used:

* ``audio_path`` – path to the user's voice recording (may be ``None``)
* ``user_id`` – optional speaker ID recognized from voiceprint service
* ``image_path`` – optional face image
* ``text`` – recognized or typed text
* ``video_path`` – optional video file analysed like an image
* ``touched`` – whether a touch sensor was activated
* ``touch_zone`` – integer ID of the touched area for more granular feedback
When values are missing, IntelligentCore will call the ASR and memory services defined in `constants.py`.
* ``robot_id`` – ID of the robot sending the request **(required)**

All parameters except ``robot_id`` are optional. When they are ``None`` the
system falls back to internal demo files.

## 简要说明

陪伴机器人智能大脑提供一系列用于构建 AI 陪伴机器人的 Python 模块，代码内含中英双语注释，方便理解和二次开发。
系统使用哈希向量检索语义记忆，情绪识别则结合语音强度、文本情感、面部表情及已有的人格与记忆信息进行多模态分析。系统依据累计交互次数与语音时长解锁“萌芽→启蒙→共鸣→觉醒”四个阶段，触摸交互时会给出声音、动作和表情反馈，持续更新“性格树”与“记忆云”。

在整体流程上，用户的语音、触摸或图像首先进入 ``IntelligentCore``，随后依次经历情绪识别、语义记忆检索、人格成长以及成长式对话生成，最终输出语音合成链接、动作指令及表情标签，实现“感知 → 思考 → 行动”的闭环。

### Code Execution Flow
1. Start the Python service or demo.
   启动 Python 服务或示例程序。
2. ``IntelligentCore`` collects audio, image and touch data.
   IntelligentCore 收集音频、图像和触摸数据。
3. ``EmotionPerception`` calls ASR, voiceprint and LLM services to determine user ID and mood.
   EmotionPerception 调用 ASR、声纹及 LLM 服务判定用户和情绪。
4. ``SemanticMemory`` sends records to the memory service and retrieves related history.
   SemanticMemory 将记录发送至记忆服务并检索关联历史。
5. ``PersonalityEngine`` updates the OCEAN vector which, along with the growth stage, shapes LLM prompts.
   PersonalityEngine 更新 OCEAN 向量，并结合成长阶段生成 LLM 提示。
6. ``DialogueEngine`` queries the LLM and TTS services to produce text and audio.
   DialogueEngine 调用 LLM 与 TTS 服务生成文本及语音。
7. The result includes action and facial animation tags.
   最终结果包含动作和面部动画标签。
成长阶段直接左右最终输出，使对话风格随互动次数与语音数据量逐步进化。
## Usage
Run `python demo.py --robot robotA` and start typing messages. Optional
arguments let you specify audio, image or video files to test multimodal input.
Type `quit` to exit.

使用方法：运行 `python demo.py --robot robotA` 开始交互，可通过
`--audio`、`--image`、`--video` 指定自定义文件。输入 `quit` 结束。
当交互包含触摸时，可输入触摸区域编号以获得对应动作反馈。

## HTTP Service

You can also run a lightweight HTTP server as a unified entry point:

The web service loads `IntelligentCore` and forwards each request so all remote modules are triggered in sequence.
该 HTTP 服务加载 IntelligentCore，将请求依次传入情绪识别、记忆服务和对话生成模块。
```bash
python service.py
```

Send a `POST` request to `http://localhost:8000/interact` with a JSON body
containing the fields described above.  The reply JSON has the following
structure and all fields are non-empty:

```json
{
  "text": "你好，很高兴见到你！",
  "audio": "audio_001.wav",
  "action": ["wave_hand", "smile"],
  "expression": "happy"
}
```

## Testing

Unit tests are provided for each core module. Execute them with:

```bash
python -m unittest discover -s tests
```

运行以上命令即可验证各模块和整体系统的基本功能。
