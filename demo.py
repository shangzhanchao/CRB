"""Simple demo script for the Companion Robot Intelligent Brain.

陪伴机器人智能大脑演示脚本。
"""

from ai_core import IntelligentCore, UserInput


def main() -> None:
    """Run a console demo."""
    core = IntelligentCore()
    audio_path = "user1.wav"  # 占位语音文件，可替换为真实录音，文件名含身份
    image_path = "face.png"   # 占位图像文件，可替换为真实照片
    print("Type 'quit' to exit. 输入 'quit' 退出。")
    while True:
        text = input("User: ")
        if text.lower() == "quit":
            break
        touch = input("Touch robot? (y/n): ").lower() == "y"
        user = UserInput(
            audio_path=audio_path,
            image_path=image_path,
            text=text,
            touched=touch,
        )
        reply = core.process(user)
        print("AI:", reply.text)
        print("Voice style:", reply.voice, "Action:", reply.action, "Expression:", reply.expression)


if __name__ == "__main__":
    main()
