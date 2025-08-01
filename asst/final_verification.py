#!/usr/bin/env python3
"""
最终验证脚本：检查进度条和摄像头/麦克风关闭功能是否完整实现
"""

import requests
import time

def verify_features():
    """验证所有新功能是否完整实现"""
    print("🔍 最终验证CRB新功能...")
    print("=" * 50)
    
    try:
        # 测试服务连接
        response = requests.get("http://localhost:8000/verify", timeout=10)
        print(f"✅ 服务连接成功，状态码: {response.status_code}")
        
        html_content = response.text
        
        # 验证进度条功能
        print("\n📊 验证进度条功能:")
        if "progress-container" in html_content:
            print("  ✅ 进度条容器已添加")
        else:
            print("  ❌ 进度条容器未找到")
            
        if "progress-bar" in html_content:
            print("  ✅ 进度条样式已添加")
        else:
            print("  ❌ 进度条样式未找到")
            
        if "showProgress" in html_content:
            print("  ✅ 显示进度条函数已添加")
        else:
            print("  ❌ 显示进度条函数未找到")
            
        if "hideProgress" in html_content:
            print("  ✅ 隐藏进度条函数已添加")
        else:
            print("  ❌ 隐藏进度条函数未找到")
        
        # 验证关闭功能
        print("\n🎛️ 验证关闭功能:")
        if "close-audio" in html_content:
            print("  ✅ 音频关闭按钮已添加")
        else:
            print("  ❌ 音频关闭按钮未找到")
            
        if "close-video" in html_content:
            print("  ✅ 视频关闭按钮已添加")
        else:
            print("  ❌ 视频关闭按钮未找到")
            
        if "closeAudioStream" in html_content:
            print("  ✅ 音频流关闭函数已添加")
        else:
            print("  ❌ 音频流关闭函数未找到")
            
        if "closeVideoStream" in html_content:
            print("  ✅ 视频流关闭函数已添加")
        else:
            print("  ❌ 视频流关闭函数未找到")
        
        # 验证状态指示器
        print("\n🔴 验证状态指示器:")
        if "status-indicator" in html_content:
            print("  ✅ 状态指示器样式已添加")
        else:
            print("  ❌ 状态指示器样式未找到")
            
        if "status-active" in html_content:
            print("  ✅ 活跃状态样式已添加")
        else:
            print("  ❌ 活跃状态样式未找到")
            
        if "status-inactive" in html_content:
            print("  ✅ 非活跃状态样式已添加")
        else:
            print("  ❌ 非活跃状态样式未找到")
            
        if "updateStatus" in html_content:
            print("  ✅ 状态更新函数已添加")
        else:
            print("  ❌ 状态更新函数未找到")
        
        # 验证样式完整性
        print("\n🎨 验证样式完整性:")
        if "close-btn" in html_content:
            print("  ✅ 关闭按钮样式已添加")
        else:
            print("  ❌ 关闭按钮样式未找到")
            
        if "progress-fill" in html_content:
            print("  ✅ 进度条填充样式已添加")
        else:
            print("  ❌ 进度条填充样式未找到")
            
        if "progress-text" in html_content:
            print("  ✅ 进度条文本样式已添加")
        else:
            print("  ❌ 进度条文本样式未找到")
        
        # 验证JavaScript功能
        print("\n⚙️ 验证JavaScript功能:")
        if "audioStream" in html_content:
            print("  ✅ 音频流变量已定义")
        else:
            print("  ❌ 音频流变量未定义")
            
        if "videoStream" in html_content:
            print("  ✅ 视频流变量已定义")
        else:
            print("  ❌ 视频流变量未定义")
            
        if "getUserMedia" in html_content:
            print("  ✅ 媒体设备访问功能已添加")
        else:
            print("  ❌ 媒体设备访问功能未找到")
        
        print("\n" + "=" * 50)
        print("🎉 验证完成！")
        print("\n💡 使用说明:")
        print("1. 打开浏览器访问: http://localhost:8000/verify")
        print("2. 测试进度条: 填写信息后点击发送按钮")
        print("3. 测试关闭功能: 启动摄像头/麦克风后点击红色关闭按钮")
        print("4. 观察状态指示器: 绿色表示活跃，灰色表示非活跃")
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务，请确保服务正在运行")
        print("💡 请运行: python service.py")
    except Exception as e:
        print(f"❌ 验证过程中出现错误: {e}")

if __name__ == "__main__":
    verify_features() 