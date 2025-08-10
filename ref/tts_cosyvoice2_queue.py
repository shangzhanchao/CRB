from gradio_client import Client, handle_file
import os
import time
import shutil
import uuid
import threading
import queue
import re
import wave
import pyaudio
import numpy as np
import traceback
import sys

# 定义模块的公共接口
__all__ = ['TTSGenerator', 'check_dependencies', 'main']
import shutil
import uuid
import threading
import queue
import re
import wave
import pyaudio
import numpy as np
import traceback
import sys


class TTSGenerator:
    def __init__(self, api_url, audio_file, target_dir):
        self.client = Client(api_url)
        self.audio_file = audio_file
        self.target_dir = target_dir
        os.makedirs(target_dir, exist_ok=True)

        # 验证音频文件存在
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"❌ 音频文件不存在: {audio_file}")

        print(f"✅ API客户端已创建 | 参考音频: {os.path.basename(audio_file)}")

        # 基础参数配置
        self.base_params = {
            # "mode_checkbox_group": "3s极速复刻",
            # "sft_dropdown": "Tailor_Korean",  # API要求必填字段
            # "prompt_text": "全球视角，本地声音。您的专属新闻播报，精选内容，带给您最具影响力的报道。",
            # "prompt_wav_upload": handle_file(audio_file),  # 使用传入的音频文件
            # "prompt_wav_record": None,
            # "instruct_text": "",  # 极速复刻模式下无需指令文本
            # "seed": 0,
            # "stream": False,  # 必须为小写字符串
            # "speed": 1,  # 语速调节

            "mode_checkbox_group": "预训练音色",
            "sft_dropdown": "Tailor_Korean",
            "prompt_text": "",
            "prompt_wav_upload": None,
            "prompt_wav_record": None,
            "instruct_text": "",
            "seed": 0,
            "stream": False,
            "speed": 1,
        }

        # 创建线程通信队列
        self.text_queue = queue.Queue()
        self.audio_queue = queue.Queue(maxsize=3)  # 减小队列大小避免积压

        # 初始化PyAudio
        try:
            self.p = pyaudio.PyAudio()
            self.stream = None  # 全局音频流
            self.audio_params = None  # 存储音频参数
        except Exception as e:
            print(f"❌ PyAudio初始化失败: {e}")
            print("请确保已安装PyAudio: pip install pyaudio")
            raise

        # 状态跟踪
        self.generation_complete = False
        self.playback_complete = False
        self.stop_playback = threading.Event()

        # 调试计数器
        self.generated_count = 0
        self.played_count = 0

    def split_text(self, long_text):
        """分割长文本为句子，确保自然停顿点"""
        # 改进分割逻辑，考虑中文标点
        sentences = re.split(r'(?<=[。！？；…])', long_text)
        return [s.strip() for s in sentences if s.strip()]

    def load_audio_data(self, file_path):
        """加载音频数据到内存，并确保参数一致性"""
        try:
            with wave.open(file_path, 'rb') as wf:
                params = {
                    'nchannels': wf.getnchannels(),
                    'sampwidth': wf.getsampwidth(),
                    'framerate': wf.getframerate(),
                    'nframes': wf.getnframes(),
                    'comptype': wf.getcomptype(),
                    'compname': wf.getcompname()
                }
                audio_data = wf.readframes(wf.getnframes())

            return params, audio_data
        except Exception as e:
            print(f"🔥 音频加载失败: {file_path} - {str(e)}")
            return None, None

    def generate_worker(self):
        """音频生成工作线程，添加节流控制"""
        print("🚀 音频生成线程启动")
        while not self.stop_playback.is_set():
            # 获取待处理文本
            try:
                sentence = self.text_queue.get(timeout=1)
                if sentence is None:  # 终止信号
                    break
            except queue.Empty:
                if self.generation_complete:
                    break
                continue

            # 检查队列积压情况
            if self.audio_queue.qsize() >= 2:
                time.sleep(0.5)  # 队列积压时暂停生成

            print(f"🔊 生成中: 「{sentence}」")
            try:
                # 复制基础参数并设置当前文本
                params = self.base_params.copy()
                params["tts_text"] = sentence

                # 生成音频
                start_time = time.time()
                result = self.client.predict(**params, api_name="/generate_audio")

                if not result or not isinstance(result, str):
                    print(f"❌ 生成失败: {sentence}")
                    continue

                # 创建目标文件路径
                target_file = os.path.join(self.target_dir, f"audio_{uuid.uuid4().hex}.wav")
                shutil.copyfile(result, target_file)

                # 加载音频数据到内存
                audio_params, audio_data = self.load_audio_data(target_file)

                if audio_data:
                    # 首次生成时初始化音频参数
                    if self.audio_params is None:
                        self.audio_params = audio_params
                        print(f"🎚️ 音频参数初始化: {audio_params}")

                    # 检查参数一致性
                    if (audio_params['framerate'] != self.audio_params['framerate'] or
                            audio_params['nchannels'] != self.audio_params['nchannels'] or
                            audio_params['sampwidth'] != self.audio_params['sampwidth']):
                        print(f"⚠️ 音频参数不一致! 期望: {self.audio_params}, 实际: {audio_params}")

                    # 放入音频队列等待播放
                    self.audio_queue.put((sentence, audio_data))
                    self.generated_count += 1

                    # 计算生成耗时
                    elapsed = time.time() - start_time
                    print(f"✅ 生成完成 | 耗时: {elapsed:.2f}s | 句子: 「{sentence}」")
                else:
                    print(f"❌ 音频加载失败: {sentence}")

                # 清理临时文件
                if os.path.exists(result):
                    os.unlink(result)
                if os.path.exists(target_file):
                    os.unlink(target_file)

            except Exception as e:
                print(f"🔥 生成异常: {str(e)}")
                traceback.print_exc()

        print("🛑 音频生成线程退出")

    def init_audio_stream(self, audio_params):
        """初始化全局音频流"""
        if self.stream is None and audio_params:
            try:
                self.stream = self.p.open(
                    format=self.p.get_format_from_width(audio_params['sampwidth']),
                    channels=audio_params['nchannels'],
                    rate=audio_params['framerate'],
                    output=True
                )
                print(
                    f"🔈 初始化全局音频流 | 采样率: {audio_params['framerate']} Hz | 通道: {audio_params['nchannels']}")
                return True
            except Exception as e:
                print(f"❌ 音频流初始化失败: {str(e)}")
                return False
        return False

    def play_worker(self):
        """音频播放工作线程，使用全局音频流"""
        print("🎧 音频播放线程启动")

        while not self.stop_playback.is_set():
            # 获取待播放音频
            try:
                audio_item = self.audio_queue.get(timeout=2)
                if audio_item is None:  # 终止信号
                    break

                sentence, audio_data = audio_item
                print(f"▶️ 准备播放: 「{sentence}」 | 数据量: {len(audio_data)}字节")

                # 如果是第一个音频，初始化音频流
                if self.stream is None:
                    # 使用第一个音频的参数初始化
                    if self.audio_params is None:
                        print("⚠️ 音频参数未初始化，无法播放")
                        continue

                    if not self.init_audio_stream(self.audio_params):
                        print("❌ 音频流初始化失败，跳过播放")
                        continue

                # 播放音频
                start_time = time.time()

                # 分块播放音频
                chunk_size = 1024
                total_bytes = len(audio_data)
                bytes_played = 0

                while bytes_played < total_bytes and not self.stop_playback.is_set():
                    chunk = audio_data[bytes_played:bytes_played + chunk_size]
                    try:
                        if self.stream and self.stream.is_active():
                            self.stream.write(chunk)
                        bytes_played += len(chunk)

                        # 添加进度显示
                        progress = bytes_played / total_bytes * 100
                        if int(progress) % 25 == 0:  # 每25%显示一次进度
                            print(f"  ▏ 播放进度: {progress:.1f}%", end='\r')
                    except Exception as e:
                        print(f"❌ 播放错误: {e}")
                        break

                # 添加句间自然停顿 (100ms)
                if not self.stop_playback.is_set() and self.stream and self.stream.is_active():
                    try:
                        # 创建静音帧 (16位PCM格式)
                        silence_duration = 0.1  # 秒
                        silence_samples = int(self.audio_params['framerate'] * silence_duration)
                        silence_data = b'\x00' * silence_samples * self.audio_params['nchannels'] * self.audio_params[
                            'sampwidth']
                        self.stream.write(silence_data)
                    except Exception as e:
                        print(f"❌ 静音添加失败: {e}")

                elapsed = time.time() - start_time
                print(f"\n✅ 播放完成 | 耗时: {elapsed:.2f}s | 句子: 「{sentence}」")
                self.played_count += 1

                # 标记任务完成
                self.audio_queue.task_done()

            except queue.Empty:
                if self.playback_complete:
                    break
                continue
            except Exception as e:
                print(f"🔥 播放异常: {str(e)}")
                traceback.print_exc()

        # 关闭音频流
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            print("🔇 音频流已关闭")

        print("🛑 音频播放线程退出")

    def process_text(self, long_text):
        """处理长文本，添加流程控制"""
        # 分割文本
        sentences = self.split_text(long_text)
        print(f"📝 分割为 {len(sentences)} 个句子:")
        for i, s in enumerate(sentences, 1):
            print(f"{i}. {s}")

        # 启动工作线程
        gen_thread = threading.Thread(target=self.generate_worker, daemon=True)
        play_thread = threading.Thread(target=self.play_worker, daemon=True)
        gen_thread.start()
        play_thread.start()

        # 填充文本队列（触发生成）
        for sentence in sentences:
            self.text_queue.put(sentence)
        self.generation_complete = True

        # 等待处理完成
        self.text_queue.join()  # 等待所有文本处理完成
        self.audio_queue.join()  # 等待所有音频播放完成
        self.playback_complete = True

        # 发送终止信号
        self.text_queue.put(None)
        self.audio_queue.put(None)

        # 设置停止标志
        self.stop_playback.set()

        # 等待线程结束
        gen_thread.join(timeout=5)
        play_thread.join(timeout=5)

        print(f"\n🎉 所有句子处理完成! 生成: {self.generated_count} | 播放: {self.played_count}")

    def __del__(self):
        """清理资源"""
        self.stop_playback.set()  # 确保停止事件已设置

        # 关闭音频流
        if hasattr(self, 'stream') and self.stream:
            self.stream.stop_stream()
            self.stream.close()

        # 终止PyAudio
        if hasattr(self, 'p') and self.p:
            self.p.terminate()

        print("♻️ 资源已清理")


def check_dependencies():
    """检查必要的依赖是否已安装"""
    missing_deps = []
    
    try:
        import gradio_client
    except ImportError:
        missing_deps.append("gradio_client")
    
    try:
        import pyaudio
    except ImportError:
        missing_deps.append("pyaudio")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    if missing_deps:
        print("❌ 缺少必要的依赖包:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n请运行以下命令安装:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    
    return True


def main():
    # 检查依赖
    if not check_dependencies():
        return

    # 配置参数 - 使用相对路径和可配置的API地址
    API_URL = os.getenv("TTS_API_URL", "http://172.16.80.22:50000/")
    
    # 根据操作系统设置默认路径
    if sys.platform.startswith('win'):
        # Windows路径
        AUDIO_FILE = os.getenv("TTS_AUDIO_FILE", "C:\\temp\\long.wav")
        TARGET_DIR = os.getenv("TTS_TARGET_DIR", "C:\\temp\\tts_output")
    else:
        # Unix/Linux/macOS路径
        AUDIO_FILE = os.getenv("TTS_AUDIO_FILE", "/tmp/long.wav")
        TARGET_DIR = os.getenv("TTS_TARGET_DIR", "/tmp/tts_output")

    # 要处理的文本
    LONG_TEXT = ("夏天是炎热的,火辣辣的太阳高高地挂在空中,把热心情地洒向大地。我们不必穿着厚厚的衣服,显得笨手笨脚;也不必为大风沙烦恼。如果下起雨来,就在小雨中奔跑,洗一个痛快的凉水澡。夏天是多彩的。盛开的鲜花,碧绿的草地,墙上爬满了绿色的植物,街上飘动着漂亮的衣裙。如果有朋友来,从冰箱里拿出黑子红瓤的西瓜招待他们,那感觉真好!夏天是有趣的。白天,可以在浓浓的树荫下,听知了悠长的鸣叫,看点点光影在地上闪耀。晚上,可以到田边听青蛙的赛歌会,看萤火虫提着灯笼在草丛中游行。夏天是悠闲的。我们扛着鱼竿去多久鱼,提着水桶去捉虾,背着救生圈去游泳。还可以自制冰淇淋,学做美味的凉拦佳肴。或者白天躺在竹椅上读书,夜晚望着星空畅想。夏天是迷人的,是我们最喜爱的季节,一切都在夏天里走向成熟。")

    print(f"🔧 配置信息:")
    print(f"   API地址: {API_URL}")
    print(f"   音频文件: {AUDIO_FILE}")
    print(f"   输出目录: {TARGET_DIR}")
    print(f"   操作系统: {sys.platform}")

    try:
        # 创建TTS处理器
        tts = TTSGenerator(API_URL, AUDIO_FILE, TARGET_DIR)

        # 处理文本
        start_time = time.time()
        tts.process_text(LONG_TEXT)
        total_time = time.time() - start_time
        print(f"⏱️ 总耗时: {total_time:.2f}秒")

    except FileNotFoundError as e:
        print(f"❌ 文件错误: {e}")
        print("请确保音频文件存在，或设置正确的TTS_AUDIO_FILE环境变量")
    except ConnectionError as e:
        print(f"❌ 连接错误: {e}")
        print("请检查API服务器是否运行，或设置正确的TTS_API_URL环境变量")
    except Exception as e:
        print(f"🔥 主程序异常: {str(e)}")
        traceback.print_exc()
    finally:
        # 确保资源被释放
        if 'tts' in locals():
            del tts
        print("🏁 程序执行结束")


if __name__ == "__main__":
    main()