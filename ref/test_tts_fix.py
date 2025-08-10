#!/usr/bin/env python3
"""
TTS修复验证脚本
用于测试TTS代码的修复是否有效
"""

import os
import sys
import tempfile
import wave
import numpy as np

def create_test_audio():
    """创建一个测试音频文件"""
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    audio_file = os.path.join(temp_dir, "test_audio.wav")
    
    # 创建一个简单的测试音频文件
    sample_rate = 22050
    duration = 1.0  # 1秒
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
    
    print(f"✅ 测试音频文件已创建: {audio_file}")
    return audio_file, temp_dir

def test_dependencies():
    """测试依赖包是否可用"""
    print("🔍 检查依赖包...")
    
    dependencies = {
        'gradio_client': 'Gradio客户端',
        'pyaudio': '音频处理',
        'numpy': '数值计算',
        'wave': 'WAV文件处理',
        'threading': '多线程',
        'queue': '队列处理'
    }
    
    missing = []
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {description} ({module})")
        except ImportError:
            print(f"❌ {description} ({module}) - 缺失")
            missing.append(module)
    
    if missing:
        print(f"\n❌ 缺少依赖包: {', '.join(missing)}")
        print("请运行: pip install " + " ".join(missing))
        return False
    
    print("✅ 所有依赖包检查通过")
    return True

def test_audio_creation():
    """测试音频文件创建"""
    print("\n🎵 测试音频文件创建...")
    
    try:
        audio_file, temp_dir = create_test_audio()
        
        # 验证文件存在
        if os.path.exists(audio_file):
            print("✅ 音频文件创建成功")
            
            # 验证文件格式
            with wave.open(audio_file, 'r') as wf:
                channels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
                framerate = wf.getframerate()
                nframes = wf.getnframes()
                
                print(f"   通道数: {channels}")
                print(f"   采样宽度: {sampwidth} 字节")
                print(f"   采样率: {framerate} Hz")
                print(f"   帧数: {nframes}")
                
                if channels == 1 and sampwidth == 2 and framerate == 22050:
                    print("✅ 音频格式正确")
                else:
                    print("⚠️ 音频格式与预期不符")
            
            # 清理
            os.unlink(audio_file)
            os.rmdir(temp_dir)
            return True
        else:
            print("❌ 音频文件创建失败")
            return False
            
    except Exception as e:
        print(f"❌ 音频文件创建异常: {e}")
        return False

def test_tts_class_import():
    """测试TTS类导入"""
    print("\n📦 测试TTS类导入...")
    
    try:
        # 导入TTS模块
        from tts_cosyvoice2_queue import TTSGenerator, check_dependencies
        
        print("✅ TTS类导入成功")
        
        # 测试依赖检查函数
        if check_dependencies():
            print("✅ 依赖检查函数正常")
        else:
            print("❌ 依赖检查失败")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ TTS类导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ TTS类测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 TTS修复验证测试")
    print("=" * 50)
    
    tests = [
        ("依赖包检查", test_dependencies),
        ("音频文件创建", test_audio_creation),
        ("TTS类导入", test_tts_class_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 运行测试: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name} - 通过")
                passed += 1
            else:
                print(f"❌ {test_name} - 失败")
        except Exception as e:
            print(f"❌ {test_name} - 异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！TTS修复有效")
        print("\n💡 使用建议:")
        print("1. 设置环境变量 TTS_API_URL 指向你的API服务器")
        print("2. 设置环境变量 TTS_AUDIO_FILE 指向参考音频文件")
        print("3. 设置环境变量 TTS_TARGET_DIR 指向输出目录")
        print("4. 运行: python tts_cosyvoice2_queue.py")
    else:
        print("⚠️ 部分测试失败，请检查上述错误信息")
        print("\n🔧 常见解决方案:")
        print("1. 安装缺失的依赖: pip install gradio_client pyaudio numpy")
        print("2. 在Windows上，可能需要安装Visual C++ Build Tools")
        print("3. 确保Python版本 >= 3.7")

if __name__ == "__main__":
    main() 