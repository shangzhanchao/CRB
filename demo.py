"""Command line demo for the Companion Robot Intelligent Brain.

命令行演示脚本，展示如何向智能大脑发送一次交互请求。

Usage examples::

    python demo.py --robot_id robotA --text "你好"
    python demo.py --robot_id robotA --audio voice.wav --image face.png --touch_zone 1
"""

import argparse
import json
import logging

from ai_core import IntelligentCore, UserInput
from ai_core.constants import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)


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
    args = parser.parse_args()

    core = IntelligentCore(llm_url=args.llm)

    user = UserInput(
        audio_path=args.audio,
        image_path=args.image,
        video_path=args.video,
        text=args.text,
        robot_id=args.robot_id,
        touch_zone=args.touch_zone,
    )

    reply = core.process(user)
    print(json.dumps(reply.as_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
