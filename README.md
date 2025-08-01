# CRB
Companion Robot Brain
# 陪伴机器人智能大脑

The **Companion Robot Intelligent Brain** provides a set of Python modules for
building an AI companion with memory, personality growth, and emotional intelligence. The core components include:

- **PersonalityEngine**: tracks OCEAN personality traits with momentum decay.  \
  **人格成长引擎：** 使用动量衰减维护 OCEAN 五维人格。
- **SemanticMemory**: stores conversation history in a SQLite database with vector-based retrieval.
  sentence-transformer embeddings are used when available, falling back to
  hashed vectors. Records persist in SQLite so memories survive restarts.  \
  **语义记忆系统：** 采用 SQLite 数据库存储对话记录，基于向量检索，优先使用
  sentence-transformer 生成语义向量，如库缺失则退化为哈希向量。
- **EmotionPerception**: recognizes emotions from voice and face inputs.
  It integrates optional speech emotion models and face-expression classifiers with fallbacks to heuristics or an LLM-based approach.
  **情绪感知模块：** 可结合语音情绪识别库和人脸表情分类器；若模型不可用，
  则退化为简单规则或调用大模型.
- **DialogueEngine**: generates responses based on personality and memory and
  evolves from cold start to active interaction.  \
  **成长式对话系统：** 结合人格与记忆生成风格化回复。
- **IntelligentCore**: orchestrates the above modules.  \
  **模块调度中台：** 负责调用各模块处理输入输出。
- **PromptFusionEngine**: intelligently combines various factors (growth stage, personality traits, emotions, touch, memory) into optimized prompts.  \
  **提示词融合引擎：** 智能融合成长阶段、人格特质、情绪、触摸、记忆等因素，生成优化提示词。

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
与语义，再通过提示词融合引擎智能组合成长阶段、人格特质、记忆上下文等因素，通过大模型生成符合成长阶段和人格的回复，最终输出文本、语音、动作和表情。

## External Services

系统默认使用以下外部服务地址，可根据实际部署修改。
The modules can optionally connect to remote services for speech and text
processing. The most important one is the multimodal LLM at ``DEFAULT_LLM_URL``
(``llm.szc.com``), which powers advanced dialogue generation and emotion
interpretation.  If you deploy your own LLM service, point ``LLM_URL`` to it so
the system can fully function:

- **ASR** (`asr.szc.com`) – convert user audio to text.  语音识别服务
- **Voiceprint** (`voiceprint.szc.com`) – identify the speaker.  声纹识别服务
- **LLM** (`llm.szc.com`) – generate richer replies.  此地址在 ``DEFAULT_LLM_URL`` 中设定，用于故事讲述和情绪理解等高级功能
- **Memory DB** (`memory-save.szc.com` & `memory-query.szc.com`) – store and query dialogues with vector-based semantic search. If these services are unreachable, records will be saved to `memory.db` locally and queries will read from that file.  对话记录存取服务，支持基于向量的语义搜索
- **TTS** (`tts.szc.com`) – synthesize reply audio.  语音合成服务

外部服务也可以通过环境变量 ``ASR_URL``、``VOICEPRINT_URL``、``LLM_URL``、``TTS_URL``、``MEMORY_SAVE_URL``、``MEMORY_QUERY_URL`` 自定义，方便接入不同的厂商。其中 ``llm.szc.com`` 是系统生成回复和理解情绪的核心依赖。

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
  service_api.py        - 调用外部 ASR/LLM/TTS 服务的工具，可直接导入使用，无需单独启动
  constants.py          - 全局常量与默认值
  prompt_fusion.py      - 提示词融合算法
demo.py                - 命令行演示脚本
### Constants Overview
The file `ai_core/constants.py` groups configuration values:
- **Service endpoints**: ASR, TTS, LLM, voiceprint and memory URLs.
 - **Default files**: demo audio/image paths. They are resolved relative to
   the repository root so they work from any current directory.
- **Growth stage thresholds**: days, interaction counts and audio duration for each stage.
- **Stage order**: `STAGE_ORDER` lists `sprout → enlighten → resonate → awaken`.
- **Personality defaults**: initial OCEAN vector and behavior mapping.
- **SQLite DB path**: location of the persistent store `MEMORY_DB_PATH`.
- **Prompt fusion weights**: memory, personality, and emotion factor weights for optimized prompt generation.
这些常量便于集中管理，可根据实际部署场景调整。
```

## Architecture Overview

1. **EmotionPerception** reads audio and image inputs (`DEFAULT_AUDIO_PATH`,
   `DEFAULT_IMAGE_PATH`) and outputs a fused emotion tag.
   该模块提供“简易融合”与“多模态模型”两种情绪识别方式，可通过参数选择。
2. **DialogueEngine** uses `PersonalityEngine` and `SemanticMemory` to produce
   responses while updating interaction stages and returns structured
   information for voice, action and facial expression.
   该引擎会根据成长阶段和记忆内容生成对应语气与动作。
3. **IntelligentCore** orchestrates the pipeline: emotion recognition → model
   feedback → personality growth → voice generation, storing each dialog in the
   memory cloud. Each step may call remote services defined in
   `service_api.py`.
   **IntelligentCore 是此系统的中心组件，负责统一管理输入数据、依次
   调度情绪识别、记忆查询和对话生成等模块，确保从感知到回应的流程
   连贯执行，最终输出语音、动作与表情反馈。**
4. **PromptFusionEngine** intelligently combines growth stage, personality traits, emotions, touch interactions, and memory context into optimized prompts for the LLM.
   **提示词融合引擎智能融合成长阶段、人格特质、情绪、触摸交互和记忆上下文，为LLM生成优化提示词。**
5. `global_state.INTERACTION_COUNT` 和 `AUDIO_DATA_SECONDS` track how much the
   robot has interacted and how much speech data it has processed. These
   metrics unlock growth stages.  \
   全局状态可以通过 `global_state.save_state()` 与 `load_state()` 持久化到文件，
   以便下次启动时继续成长历程。

上述流程对应的中文概述：情绪识别 → 模型反馈 → 性格成长 → 语音生成，
并将对话记录储存于记忆云，以便后续参考。

During response generation, the dialogue engine uses **PromptFusionEngine** to build optimized prompts for the
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
   **觉醒期**（30天以上且数据充足）：记住对话并主动给出建议，能够基于历史记忆进行个性化对话。

The current stage and metrics persist automatically to ``state.json`` so
progress continues after restarting the program. Call
``global_state.get_growth_metrics()`` to visualize counts in your own UI.

By default the system begins in the **enlighten** stage with an
**extraversion-oriented** personality vector as defined in
``DEFAULT_GROWTH_STAGE`` and ``DEFAULT_PERSONALITY_VECTOR``.

## Emotion States

Standard emotion tags used across the system include:

``happy, sad, angry, fear, surprise, disgust, calm, excited, tired, bored, confused, shy, neutral``.

系统预定义的情绪标签涵盖常见的快乐、悲伤、生气、恐惧、惊讶、厌恶、平静、兴奋、疲惫、无聊、困惑、害羞以及中性状态。

## LLM Prompt Templates

The dialogue engine uses **PromptFusionEngine** to compose optimized prompts for the large language model based on the
robot's **growth stage**, its **OCEAN** personality vector, touch feedback, and memory context:

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
- **Memory prompts** provide context from previous conversations, helping the LLM generate more personalized and context-aware responses.
  记忆提示提供历史对话上下文，帮助LLM生成更个性化和情境感知的回复。

The **PromptFusionEngine** intelligently combines these factors using weighted fusion algorithms:
- **Growth stage factor**: weight=1.5, priority=5 (highest)
- **Personality traits factor**: weight=1.2, priority=4
- **User emotion factor**: weight=1.0, priority=3
- **Memory summary factor**: weight=0.6, priority=1
- **User input factor**: weight=2.0, priority=6 (required)

**提示词融合引擎**使用加权融合算法智能组合这些因素：
- **成长阶段因子**：权重=1.5，优先级=5（最高）
- **人格特质因子**：权重=1.2，优先级=4
- **用户情绪因子**：权重=1.0，优先级=3
- **记忆摘要因子**：权重=0.6，优先级=1
- **用户输入因子**：权重=2.0，优先级=6（必需）

By intelligently combining these factors with recent memories, the **PromptFusionEngine** gives the LLM
flexible instructions to craft an appropriate reply.
通过智能融合这些因素与记忆片段，提示词融合引擎为大模型提供灵活指令。

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
(``None``) and internal defaults will be used.
下表展示所有参数，除了 ``robot_id`` 之外均为可选项，可留空使用默认值：

| Parameter    | Type   | Description                                   | Example |
|--------------|--------|-----------------------------------------------|---------|
| ``audio_path`` | str or ``None`` | path to the user's voice recording | ``"user.wav"`` |
| ``image_path`` | str or ``None`` | face image path | ``"face.png"`` |
| ``video_path`` | str or ``None`` | optional video clip analysed as image | ``"video.mp4"`` |
| ``text`` | str or ``None`` | recognized or typed text | ``"你好"`` |
| ``touch_zone`` | int or ``None`` | touch area identifier | ``0`` |
| ``robot_id`` | str **required** | ID of the robot sending the request | ``"robotA"`` |

When values are missing, ``IntelligentCore`` calls the ASR and memory services
defined in ``constants.py``. All parameters except ``robot_id`` are optional and
default to demo data when ``None``.
以上字段涵盖一次互动可能提供的所有信息，音频、图片或视频可任选其一，
文本为空时系统会尝试通过 ASR 识别。

## 简要说明

陪伴机器人智能大脑提供一系列用于构建 AI 陪伴机器人的 Python 模块，代码内含中英双语注释，方便理解和二次开发。
系统使用向量化语义记忆检索，情绪识别则结合语音强度、文本情感、面部表情及已有的人格与记忆信息进行多模态分析。系统依据累计交互次数与语音时长解锁"萌芽→启蒙→共鸣→觉醒"四个阶段，触摸交互时会给出声音、动作和表情反馈，持续更新"性格树"与"记忆云"。

在整体流程上，用户的语音、触摸或图像首先进入 ``IntelligentCore``，随后依次经历情绪识别、语义记忆检索、人格成长、提示词融合以及成长式对话生成，最终输出语音合成链接、动作指令及表情标签，实现"感知 → 思考 → 行动"的闭环。系统通过智能记忆摘要和提示词融合算法，确保每次对话都能基于历史记忆进行个性化回复。

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
6. ``PromptFusionEngine`` intelligently combines growth stage, personality traits, emotions, touch interactions, and memory context into optimized prompts.
   PromptFusionEngine 智能融合成长阶段、人格特质、情绪、触摸交互和记忆上下文，生成优化提示词。
7. ``DialogueEngine`` queries the LLM and TTS services to produce text and audio.
   DialogueEngine 调用 LLM 与 TTS 服务生成文本及语音。
8. The result includes action and facial animation tags.
   最终结果包含动作和面部动画标签。
9. The conversation is stored in memory for future reference.
   对话记录存储到记忆中供未来参考。

成长阶段和记忆系统共同影响最终输出，使对话风格随互动次数与语音数据量逐步进化，同时保持个性化记忆。
## Usage
Run `python demo.py --robot_id robotA` and start typing messages. Optional
arguments let you specify text, audio, image or video files as well as a touch
zone to test multimodal input.
Example:

```bash
python demo.py --robot_id robotA --text "你好" --audio my.wav \
  --image face.png --video clip.mp4 --touch_zone 0
```

Type `quit` to exit.

使用方法：运行 `python demo.py --robot_id robotA` 开始交互，可通过
`--text`、`--audio`、`--image`、`--video`、`--touch_zone` 指定自定义文件或
触摸编号。输入 `quit` 结束。
当交互包含触摸时，可输入触摸区域编号以获得对应动作反馈。

## HTTP Service

You can also run an asynchronous HTTP service based on **FastAPI**:

The service relies on asynchronous wrappers in ``service_api.py`` so
external calls will not block processing. ``service_api.py`` itself does not
start a server; its helpers are imported by this HTTP layer. If ``FastAPI`` is
missing the synchronous :func:`handle_request` can still be used in your own
server.

The web application loads `IntelligentCore` and forwards requests so all modules run in sequence.  该 HTTP 服务基于 FastAPI 实现，依次调用情绪识别、记忆查询与对话生成模块。
```bash
# start with python
python service.py

# or start with uvicorn for auto reload
uvicorn service:app --reload
```

Open `http://localhost:8000/verify` in a browser to try the simple HTML verification page. It lets you submit text, media paths and touch zones and shows the JSON reply.
在浏览器访问 `http://localhost:8000/verify` 可查看基本的 HTML 验证界面，可输入文本、音频、图片、视频和触摸编号。

Alternatively you can start a richer demo using **Streamlit**:

```bash
streamlit run verify_app.py
```

该界面提供表单化的交互，可直接调用智能大脑模块并在网页中显示返回结果。

Send a `POST` request to `http://localhost:8000/interact` with a JSON body
containing the fields described above. Example request:

```json
{
  "robot_id": "robotA",
  "text": "你好",
  "audio_path": "user.wav",
  "image_path": "face.png",
  "video_path": "clip.mp4",
  "touch_zone": 0
}
```

该接口返回与命令行演示相同的结构化结果，可直接集成到前端或
其他服务。请求和返回内容均采用 UTF-8 编码，方便中文环境调试。

### Output Format

`IntelligentCore.process()` returns a `DialogueResponse` dataclass. When
converted with `as_dict()` the HTTP service responds with four non-empty fields.
该结构保证文本、音频、动作和表情四项内容均不为空，便于机器人执行相应反馈：

| Field | Type | Description |
|-------|------|-------------|
| ``text`` | ``str`` | Text reply from the LLM |
| ``audio`` | ``str`` | URL or path of the synthesized speech |
| ``action`` | ``list[str]`` | One or more robot action codes |
| ``expression`` | ``str`` | Facial expression tag |

Example response:

```json
{
  "text": "你好，很高兴见到你！",
  "audio": "audio_001.wav",
  "action": ["wave_hand", "smile"],
  "expression": "happy"
}
```

## Memory Data Service

A lightweight memory service is provided for local testing. 通过 `memory_service.py`
可以启动一个简易的存取服务。其后端可选择 `file`(默认) 或 `db`，由
环境变量 `MEMORY_SERVICE_BACKEND` 控制。

```bash
uvicorn memory_service:app --reload
```

- **POST /save** – store a memory record
- **POST /query** – search records with a text prompt

记录会写入 `memory_backup.json` 或 `memory.db`，供
``call_memory_save`` 与 ``call_memory_query`` 函数调用。

## Testing

Unit tests are provided for each core module. Execute them with:

```bash
python -m unittest discover -s tests
```

运行以上命令即可验证各模块和整体系统的基本功能。

