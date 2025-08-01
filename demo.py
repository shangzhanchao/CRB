"""Command line demo for the Companion Robot Intelligent Brain.

命令行演示脚本，展示如何向智能大脑发送一次交互请求。

Usage examples::

    python demo.py --robot_id robotA --text "你好"
    python demo.py --robot_id robotA --audio voice.wav --image face.png --touch_zone 1
"""

import argparse
import json
import logging
import sys

from ai_core import IntelligentCore, UserInput
from ai_core.constants import LOG_LEVEL

# 配置详细的日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('robot_demo.log', encoding='utf-8')
    ]
)


def main() -> None:
    """Run a single interaction using command line parameters.

    通过命令行参数执行一次交互。
    """
    parser = argparse.ArgumentParser(description="Demo for the robot brain")
    parser.add_argument("--robot_id", required=True, help="robot identifier")
    parser.add_argument("--text", help="user text input")
    parser.add_argument("--audio", help="path to audio file")
    parser.add_argument("--image", help="path to face image")
    parser.add_argument("--video", help="path to video clip")
    parser.add_argument(
        "--touch_zone",
        type=int,
        choices=[0, 1, 2],
        help="touch sensor zone: 0=head, 1=back, 2=chest",
    )
    parser.add_argument("--llm", help="LLM service URL")
    parser.add_argument("--show_status", action="store_true", help="显示robot状态信息")
    args = parser.parse_args()

    # 创建智能核心
    core = IntelligentCore(llm_url=args.llm)
    
    # 显示robot状态信息
    if args.show_status:
        print("🤖 Robot状态信息")
        print("=" * 50)
        print(f"🆔 Robot ID: {args.robot_id}")
        print(f"🌱 成长阶段: {core.dialogue.stage}")
        print(f"🎭 人格风格: {core.dialogue.personality.get_personality_style()}")
        print(f"📊 人格向量: {core.dialogue.personality.vector}")
        print(f"⭐ 主导特质: {core.dialogue.personality.get_dominant_traits()}")
        print(f"💾 记忆记录数: {len(core.dialogue.memory.records)}")
        # 导入global_state模块
        from ai_core import global_state
        print(f"📈 交互次数: {global_state.INTERACTION_COUNT}")
        print(f"🎵 音频时长: {global_state.AUDIO_DATA_SECONDS:.1f}秒")
        print("=" * 50)
        print()

    # 显示记忆信息
    if core.dialogue.memory.records:
        print("💾 最近记忆记录")
        print("-" * 30)
        recent_memories = core.dialogue.memory.records[-3:]  # 显示最近3条
        for i, memory in enumerate(recent_memories, 1):
            print(f"{i}. 用户: {memory['user_text']}")
            print(f"   AI: {memory['ai_response']}")
            print(f"   情绪: {memory['mood_tag']}")
            print(f"   时间: {memory['time']}")
            print()
    
    print("🔄 开始处理用户输入...")
    print()

    user = UserInput(
        audio_path=args.audio,
        image_path=args.image,
        video_path=args.video,
        text=args.text,
        robot_id=args.robot_id,
        touch_zone=args.touch_zone,
    )

    reply = core.process(user)
    
    print("✅ 处理完成！")
    print("📤 输出结果:")
    print(json.dumps(reply.as_dict(), ensure_ascii=False, indent=2))
    
    # 显示处理后的状态变化
    if args.show_status:
        print("\n🔄 处理后状态变化:")
        print("-" * 30)
        print(f"🌱 成长阶段: {core.dialogue.stage}")
        print(f"🎭 人格风格: {core.dialogue.personality.get_personality_style()}")
        print(f"📊 人格向量: {core.dialogue.personality.vector}")
        print(f"💾 记忆记录数: {len(core.dialogue.memory.records)}")
        print(f"📈 交互次数: {global_state.INTERACTION_COUNT}")


if __name__ == "__main__":
    main()