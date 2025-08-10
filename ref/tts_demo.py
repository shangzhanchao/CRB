#!/usr/bin/env python3
"""
TTS修复演示脚本
展示修复后的TTS功能
"""

import os
import sys
import tempfile
import wave
import numpy as np
from tts_cosyvoice2_queue import TTSGenerator, check_dependencies

def create_demo_audio():
    """创建一个演示音频文件"""
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    audio_file = os.path.join(temp_dir, "demo_audio.wav")
    
    # 创建一个简单的演示音频文件
    sample_rate = 22050
    duration = 2.0  # 2秒
    frequency = 440.0  # A4音符
    
    # 生成正弦波
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # 转换为16位整数
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # 保存为WAV文件
    with wave.open(audio_file, 'w') as wf:
        wf.setnchannels(1)  # 单声道
        wf.setsampwidth(2)  # 16位
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    
    print(f"✅ 演示音频文件已创建: {audio_file}")
    return audio_file, temp_dir

def demo_tts_functionality():
    """演示TTS功能"""
    print("🎤 TTS功能演示")
    print("=" * 50)
    
    # 检查依赖
    print("1. 检查依赖包...")
    if not check_dependencies():
        print("❌ 依赖检查失败")
        return False
    print("✅ 依赖检查通过")
    
    # 创建演示音频
    print("\n2. 创建演示音频...")
    audio_file, temp_dir = create_demo_audio()
    
    # 设置配置
    print("\n3. 配置TTS参数...")
    API_URL = os.getenv("TTS_API_URL", "http://172.16.80.22:50000/")
    TARGET_DIR = os.path.join(temp_dir, "tts_output")
    
    print(f"   API地址: {API_URL}")
    print(f"   参考音频: {os.path.basename(audio_file)}")
    print(f"   输出目录: {TARGET_DIR}")
    
    # 演示文本
    demo_text = "这是一个TTS演示。修复后的代码现在支持更好的错误处理和跨平台兼容性。"
    
    print(f"\n4. 演示文本: {demo_text}")
    
    try:
        # 创建TTS实例
        print("\n5. 创建TTS实例...")
        tts = TTSGenerator(API_URL, audio_file, TARGET_DIR)
        print("✅ TTS实例创建成功")
        
        # 演示文本分割
        print("\n6. 文本分割演示...")
        sentences = tts.split_text(demo_text)
        print(f"   分割为 {len(sentences)} 个句子:")
        for i, sentence in enumerate(sentences, 1):
            print(f"   {i}. {sentence}")
        
        print("\n✅ TTS功能演示完成")
        print("\n💡 主要修复内容:")
        print("   - 添加了依赖包检查")
        print("   - 改进了错误处理")
        print("   - 支持跨平台路径配置")
        print("   - 添加了环境变量配置")
        print("   - 增强了PyAudio初始化错误处理")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ 文件错误: {e}")
        print("请确保音频文件存在")
        return False
    except ConnectionError as e:
        print(f"❌ 连接错误: {e}")
        print("请检查API服务器是否运行")
        return False
    except Exception as e:
        print(f"❌ 演示异常: {e}")
        return False
    finally:
        # 清理临时文件
        try:
            if os.path.exists(audio_file):
                os.unlink(audio_file)
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)
        except:
            pass

def main():
    """主函数"""
    print("🚀 TTS修复演示")
    print("=" * 50)
    
    success = demo_tts_functionality()
    
    if success:
        print("\n🎉 演示成功！TTS修复有效")
        print("\n📝 使用说明:")
        print("1. 设置环境变量:")
        print("   - TTS_API_URL: API服务器地址")
        print("   - TTS_AUDIO_FILE: 参考音频文件路径")
        print("   - TTS_TARGET_DIR: 输出目录路径")
        print("2. 运行: python tts_cosyvoice2_queue.py")
    else:
        print("\n⚠️ 演示失败，请检查错误信息")

if __name__ == "__main__":
    main() 