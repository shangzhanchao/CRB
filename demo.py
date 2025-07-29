"""Simple demo script for the AI companion robot.

AI陪伴机器人演示脚本。
"""

from ai_core import IntelligentCore, UserInput


def main() -> None:
    """Run a console demo."""
    core = IntelligentCore()
    audio_path = "voice.wav"  # 占位语音文件，可替换为真实录音
    image_path = "face.png"   # 占位图像文件，可替换为真实照片
    print("Type 'quit' to exit. 输入 'quit' 退出。")
    while True:
        text = input("User: ")
        if text.lower() == "quit":
            break
        user = UserInput(audio_path=audio_path, image_path=image_path, text=text)
        reply = core.process(user)
        print("AI:", reply)


if __name__ == "__main__":
    main()
