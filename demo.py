"""Console demonstration of the Companion Robot Intelligent Brain.

控制台演示腳本，展示陪伴机器人智能大脑的基本流程。
"""

import argparse
import logging

from ai_core import IntelligentCore, UserInput
from ai_core.constants import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL)


def main() -> None:
    """Interact with the brain via the command line.

    命令行交互演示。
    """
    parser = argparse.ArgumentParser(description="Demo for the robot brain")
    parser.add_argument("--robot", default="robotA", help="robot id")
    parser.add_argument("--audio", help="audio path")
    parser.add_argument("--image", help="image path")
    parser.add_argument("--video", help="video path")
    parser.add_argument("--llm", help="LLM service URL")
    args = parser.parse_args()

    core = IntelligentCore(llm_url=args.llm)

    print("Type text and press Enter. 输入 'quit' 结束。")
    while True:
        text = input("User: ")
        if text.lower() == "quit":
            break
        touch = input("Touch? (y/n): ").lower() == "y"
        zone = None
        if touch:
            try:
                zone = int(input("Touch zone 0=head 1=back 2=chest: "))
            except ValueError:
                zone = None
        user = UserInput(
            audio_path=args.audio,
            image_path=args.image,
            video_path=args.video,
            text=text,
            robot_id=args.robot,
            touched=touch,
            touch_zone=zone,
        )
        reply = core.process(user)
        print("AI:", reply.text)
        print(f"voice={reply.voice} action={reply.action} expression={reply.expression} audio={reply.audio}")


if __name__ == "__main__":
    main()
