"""Asynchronous HTTP service for the companion robot brain.

基于 FastAPI 的异步 HTTP 服务入口，可统一处理外部请求。
支持文件上传、麦克风、摄像头等功能。
"""

from __future__ import annotations

import json
import uuid
from typing import Any, Dict
from pathlib import Path

# 直接导入FastAPI相关模块
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import Response, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 使用正确的导入路径，避免循环导入问题
from ai_core.intelligent_core import IntelligentCore, UserInput

# 初始化核心组件
core = IntelligentCore()
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# 创建FastAPI应用
app = FastAPI(title="Companion Robot Brain API", version="1.0.0")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


def handle_request(payload: Dict[str, Any]):
    """Process a JSON payload and return AI response dict."""
    try:
        robot_id = payload.get("robot_id", "")
        text = payload.get("text")
        audio = payload.get("audio_path")
        image = payload.get("image_path")
        video = payload.get("video_path")
        zone = payload.get("touch_zone")
        
        user = UserInput(
            audio_path=audio,
            image_path=image,
            video_path=video,
            text=text,
            robot_id=robot_id,
            touch_zone=zone,
        )
        
        reply = core.process(user)
        return reply.as_dict()
    except Exception as e:
        print(f"处理请求时出错: {e}")
        raise


@app.post("/interact")
async def interact(payload: Dict[str, Any]):
    """Async HTTP endpoint bridging to :func:`handle_request`."""
    try:
        return handle_request(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/")
async def root_page():
    """Redirect to the verification page."""
    return RedirectResponse("/verify")


@app.get("/verify")
async def verify_page():
    """Serve the interactive HTML verification page."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Companion Robot Brain API</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; font-weight: bold; color: #333; }
            input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }
            button { background-color: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; margin: 5px; }
            button:hover { background-color: #0056b3; }
            button:disabled { background-color: #6c757d; cursor: not-allowed; }
            .result { margin-top: 20px; padding: 20px; background-color: #f8f9fa; border-radius: 4px; border-left: 4px solid #007bff; }
            .video-container { margin: 15px 0; text-align: center; }
            #videoElement, #audioElement { width: 100%; max-width: 400px; border-radius: 4px; }
            .file-upload { border: 2px dashed #ddd; padding: 20px; text-align: center; margin: 10px 0; border-radius: 4px; background-color: #fafafa; }
            .recording-controls { display: flex; gap: 10px; justify-content: center; margin: 10px 0; }
            .status { padding: 10px; margin: 10px 0; border-radius: 4px; font-weight: bold; }
            .status.recording { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .status.stopped { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            .preview { margin: 10px 0; }
            .preview audio, .preview video { max-width: 300px; }
            
            /* 新增样式：进度条和关闭按钮 */
            .progress-container { display: none; margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6; }
            .progress-bar { width: 100%; height: 20px; background-color: #e9ecef; border-radius: 10px; overflow: hidden; }
            .progress-fill { height: 100%; background: linear-gradient(90deg, #007bff, #0056b3); width: 0%; transition: width 0.3s ease; }
            .progress-text { margin-top: 8px; text-align: center; font-weight: bold; color: #495057; }
            .close-btn { background-color: #dc3545; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; margin-left: 10px; font-size: 12px; }
            .close-btn:hover { background-color: #c82333; }
            .status-indicator { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
            .status-active { background-color: #28a745; }
            .status-inactive { background-color: #6c757d; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Companion Robot Brain API</h1>
            
            <form id="interactForm">
                <div class="form-group">
                    <label for="robot_id">Robot ID:</label>
                    <input type="text" id="robot_id" name="robot_id" value="robotA" required>
                </div>
                
                <div class="form-group">
                    <label for="text">Text Input:</label>
                    <textarea id="text" name="text" rows="3" placeholder="Enter your message to the robot..."></textarea>
                </div>
                
                <div class="form-group">
                    <label>🎤 Audio Input <span class="status-indicator status-inactive" id="audio-status"></span>
                        <button type="button" class="close-btn" id="close-audio" style="display:none">关闭麦克风</button>
                    </label>
                    <div class="file-upload">
                        <p><strong>Option 1:</strong> Upload audio file</p>
                        <input type="file" id="audio_file" accept="audio/*">
                        <p><strong>Option 2:</strong> Record audio using microphone</p>
                        <div class="recording-controls">
                            <button type="button" id="startAudioBtn" onclick="startAudioRecording()">🎤 Start Recording</button>
                            <button type="button" id="stopAudioBtn" onclick="stopAudioRecording()" disabled>⏹️ Stop Recording</button>
                        </div>
                        <div id="audioStatus" class="status" style="display:none;"></div>
                        <div id="audioPreview" class="preview" style="display:none;"></div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>📷 Image/Video Input <span class="status-indicator status-inactive" id="video-status"></span>
                        <button type="button" class="close-btn" id="close-video" style="display:none">关闭摄像头</button>
                    </label>
                    <div class="file-upload">
                        <p><strong>Option 1:</strong> Upload files</p>
                        <input type="file" id="image_file" accept="image/*" placeholder="Upload image">
                        <input type="file" id="video_file" accept="video/*" placeholder="Upload video">
                        <p><strong>Option 2:</strong> Use camera</p>
                        <div class="recording-controls">
                            <button type="button" id="startVideoBtn" onclick="startCamera()">📹 Start Camera</button>
                            <button type="button" id="capturePhotoBtn" onclick="capturePhoto()" disabled>📸 Capture Photo</button>
                            <button type="button" id="startVideoRecBtn" onclick="startVideoRecording()" disabled>🎬 Start Video Recording</button>
                            <button type="button" id="stopVideoRecBtn" onclick="stopVideoRecording()" disabled>⏹️ Stop Video Recording</button>
                        </div>
                        <div id="videoStatus" class="status" style="display:none;"></div>
                        <div class="video-container">
                            <video id="videoElement" autoplay muted></video>
                            <canvas id="canvasElement" style="display:none;"></canvas>
                        </div>
                        <div id="videoPreview" class="preview" style="display:none;"></div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="touch_zone">👆 Touch Zone:</label>
                    <select id="touch_zone" name="touch_zone">
                        <option value="">None</option>
                        <option value="0">Head (0)</option>
                        <option value="1">Back (1)</option>
                        <option value="2">Chest (2)</option>
                    </select>
                </div>
                
                <!-- 进度条容器 -->
                <div class="progress-container" id="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progress-fill"></div>
                    </div>
                    <div class="progress-text" id="progress-text">正在处理请求...</div>
                </div>
                
                <button type="submit" style="width: 100%; font-size: 16px; padding: 15px;">🚀 Send Request to Robot</button>
            </form>
            
            <div class="result" id="result">Waiting for response...</div>
        </div>
        
        <script>
        // 全局变量
        let audioStream = null;
        let videoStream = null;
        let audioRecorder = null;
        let videoRecorder = null;
        let audioChunks = [];
        let videoChunks = [];
        
        // 进度条相关元素
        const progressContainer = document.getElementById('progress-container');
        const progressFill = document.getElementById('progress-fill');
        const progressText = document.getElementById('progress-text');
        
        // 状态指示器
        const audioStatus = document.getElementById('audio-status');
        const videoStatus = document.getElementById('video-status');
        
        // 关闭按钮
        const closeAudioBtn = document.getElementById('close-audio');
        const closeVideoBtn = document.getElementById('close-video');
        
        // 显示进度条
        function showProgress() {
            progressContainer.style.display = 'block';
            progressFill.style.width = '0%';
            progressText.textContent = '正在处理请求...';
            
            // 模拟进度更新
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += Math.random() * 15;
                if (progress > 90) progress = 90;
                progressFill.style.width = progress + '%';
            }, 200);
            
            return progressInterval;
        }
        
        // 隐藏进度条
        function hideProgress() {
            progressContainer.style.display = 'none';
        }
        
        // 更新状态指示器
        function updateStatus(element, isActive) {
            element.className = isActive ? 'status-indicator status-active' : 'status-indicator status-inactive';
        }
        
        // 关闭音频流
        function closeAudioStream() {
            if (audioStream) {
                audioStream.getTracks().forEach(track => track.stop());
                audioStream = null;
                updateStatus(audioStatus, false);
                closeAudioBtn.style.display = 'none';
                document.getElementById('audioElement').src = '';
            }
        }
        
        // 关闭视频流
        function closeVideoStream() {
            if (videoStream) {
                videoStream.getTracks().forEach(track => track.stop());
                videoStream = null;
                updateStatus(videoStatus, false);
                closeVideoBtn.style.display = 'none';
                document.getElementById('videoElement').srcObject = null;
            }
        }
        
        // 绑定关闭按钮事件
        closeAudioBtn.onclick = closeAudioStream;
        closeVideoBtn.onclick = closeVideoStream;
        
        // 音频录制功能
        async function startAudioRecording() {
            try {
                // 先停止之前的流
                if (audioStream) {
                    audioStream.getTracks().forEach(track => track.stop());
                }
                
                audioStream = await navigator.mediaDevices.getUserMedia({
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        autoGainControl: true,
                        sampleRate: 44100
                    }
                });
                
                updateStatus(audioStatus, true);
                closeAudioBtn.style.display = 'inline-block';
                
                audioRecorder = new MediaRecorder(audioStream, {
                    mimeType: 'audio/webm;codecs=opus'
                });
                audioChunks = [];
                
                audioRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };
                
                audioRecorder.onstop = async () => {
                    if (audioChunks.length > 0) {
                        const blob = new Blob(audioChunks, {type: 'audio/webm'});
                        const audioUrl = URL.createObjectURL(blob);
                        
                        // 创建音频元素用于预览
                        const audioElement = document.createElement('audio');
                        audioElement.controls = true;
                        audioElement.src = audioUrl;
                        
                        document.getElementById('audioPreview').innerHTML = '';
                        document.getElementById('audioPreview').appendChild(audioElement);
                        document.getElementById('audioPreview').style.display = 'block';
                        
                        // 自动上传音频文件
                        const formData = new FormData();
                        formData.append('file', blob, 'audio.webm');
                        
                        try {
                            const response = await fetch('/upload/audio', {
                                method: 'POST',
                                body: formData
                            });
                            const result = await response.json();
                            document.getElementById('audio_file').value = result.path;
                            console.log('Audio uploaded:', result.path);
                        } catch (error) {
                            console.error('Audio upload failed:', error);
                        }
                    }
                };
                
                audioRecorder.start(1000); // 每秒收集一次数据
                document.getElementById('startAudioBtn').disabled = true;
                document.getElementById('stopAudioBtn').disabled = false;
                document.getElementById('audioStatus').textContent = 'Recording...';
                document.getElementById('audioStatus').style.display = 'block';
                document.getElementById('audioStatus').className = 'status recording';
                
            } catch (error) {
                console.error('Audio recording error:', error);
                alert('无法访问麦克风: ' + error.message);
            }
        }
        
        function stopAudioRecording() {
            if (audioRecorder && audioRecorder.state !== 'inactive') {
                audioRecorder.stop();
                document.getElementById('startAudioBtn').disabled = false;
                document.getElementById('stopAudioBtn').disabled = true;
                document.getElementById('audioStatus').textContent = 'Recording stopped';
                document.getElementById('audioStatus').className = 'status stopped';
            }
        }
        
        // 视频录制功能
        async function startCamera() {
            try {
                // 先停止之前的流
                if (videoStream) {
                    videoStream.getTracks().forEach(track => track.stop());
                }
                
                videoStream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { ideal: 1280 },
                        height: { ideal: 720 },
                        frameRate: { ideal: 30 }
                    },
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true
                    }
                });
                
                updateStatus(videoStatus, true);
                closeVideoBtn.style.display = 'inline-block';
                
                const videoElement = document.getElementById('videoElement');
                videoElement.srcObject = videoStream;
                videoElement.play().catch(e => console.error('Video play error:', e));
                
                document.getElementById('startVideoBtn').disabled = true;
                document.getElementById('capturePhotoBtn').disabled = false;
                document.getElementById('startVideoRecBtn').disabled = false;
                document.getElementById('videoStatus').textContent = 'Camera active';
                document.getElementById('videoStatus').style.display = 'block';
                document.getElementById('videoStatus').className = 'status recording';
                
            } catch (error) {
                console.error('Camera error:', error);
                alert('无法访问摄像头: ' + error.message);
            }
        }
        
        function capturePhoto() {
            const canvas = document.getElementById('canvasElement');
            const video = document.getElementById('videoElement');
            
            if (!videoStream || video.videoWidth === 0) {
                alert('请先启动摄像头');
                return;
            }
            
            const context = canvas.getContext('2d');
            
            // 设置画布尺寸
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            // 绘制视频帧到画布
            context.drawImage(video, 0, 0);
            
            // 转换为blob并上传
            canvas.toBlob(async (blob) => {
                if (blob) {
                    const formData = new FormData();
                    formData.append('file', blob, 'photo.jpg');
                    
                    try {
                        const response = await fetch('/upload/image', {
                            method: 'POST',
                            body: formData
                        });
                        const result = await response.json();
                        document.getElementById('image_file').value = result.path;
                        
                        // 显示预览
                        const img = document.createElement('img');
                        img.src = result.path;
                        img.style.maxWidth = '300px';
                        img.style.borderRadius = '4px';
                        
                        document.getElementById('videoPreview').innerHTML = '';
                        document.getElementById('videoPreview').appendChild(img);
                        document.getElementById('videoPreview').style.display = 'block';
                        
                        console.log('Photo captured and uploaded:', result.path);
                    } catch (error) {
                        console.error('Photo upload failed:', error);
                        alert('照片上传失败: ' + error.message);
                    }
                }
            }, 'image/jpeg', 0.9);
        }
        
        function startVideoRecording() {
            if (!videoStream) {
                alert('请先启动摄像头');
                return;
            }
            
            // 检查支持的MIME类型
            const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9,opus') 
                ? 'video/webm;codecs=vp9,opus'
                : MediaRecorder.isTypeSupported('video/webm;codecs=vp8,opus')
                ? 'video/webm;codecs=vp8,opus'
                : 'video/webm';
            
            try {
                videoRecorder = new MediaRecorder(videoStream, { mimeType });
                videoChunks = [];
                
                videoRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        videoChunks.push(event.data);
                    }
                };
                
                videoRecorder.onstop = async () => {
                    if (videoChunks.length > 0) {
                        const blob = new Blob(videoChunks, {type: 'video/webm'});
                        const videoUrl = URL.createObjectURL(blob);
                        
                        // 创建视频元素用于预览
                        const videoElement = document.createElement('video');
                        videoElement.controls = true;
                        videoElement.src = videoUrl;
                        videoElement.style.maxWidth = '300px';
                        videoElement.style.borderRadius = '4px';
                        
                        document.getElementById('videoPreview').innerHTML = '';
                        document.getElementById('videoPreview').appendChild(videoElement);
                        document.getElementById('videoPreview').style.display = 'block';
                        
                        // 自动上传视频文件
                        const formData = new FormData();
                        formData.append('file', blob, 'video.webm');
                        
                        try {
                            const response = await fetch('/upload/video', {
                                method: 'POST',
                                body: formData
                            });
                            const result = await response.json();
                            document.getElementById('video_file').value = result.path;
                            console.log('Video uploaded:', result.path);
                        } catch (error) {
                            console.error('Video upload failed:', error);
                        }
                    }
                };
                
                videoRecorder.start(1000); // 每秒收集一次数据
                document.getElementById('startVideoRecBtn').disabled = true;
                document.getElementById('stopVideoRecBtn').disabled = false;
                document.getElementById('videoStatus').textContent = 'Recording video...';
                document.getElementById('videoStatus').className = 'status recording';
                
            } catch (error) {
                console.error('Video recording error:', error);
                alert('视频录制失败: ' + error.message);
            }
        }
        
        function stopVideoRecording() {
            if (videoRecorder && videoRecorder.state !== 'inactive') {
                videoRecorder.stop();
                document.getElementById('startVideoRecBtn').disabled = false;
                document.getElementById('stopVideoRecBtn').disabled = true;
                document.getElementById('videoStatus').textContent = 'Video recording stopped';
                document.getElementById('videoStatus').className = 'status stopped';
            }
        }
        
        // 页面卸载时清理资源
        window.addEventListener('beforeunload', () => {
            if (audioStream) {
                audioStream.getTracks().forEach(track => track.stop());
            }
            if (videoStream) {
                videoStream.getTracks().forEach(track => track.stop());
            }
        });
        
        // 检查浏览器支持
        function checkBrowserSupport() {
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                alert('您的浏览器不支持媒体设备访问，请使用现代浏览器如 Chrome、Firefox、Safari 等');
                return false;
            }
            return true;
        }
        
        // 页面加载时检查支持
        document.addEventListener('DOMContentLoaded', () => {
            checkBrowserSupport();
        });
        
        // 表单提交处理
        document.getElementById('interactForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // 检查是否有任何输入
            const text = document.getElementById('text').value.trim();
            const audioFile = document.getElementById('audio_file').files[0];
            const imageFile = document.getElementById('image_file').files[0];
            const videoFile = document.getElementById('video_file').files[0];
            
            if (!text && !audioFile && !imageFile && !videoFile) {
                alert('请至少提供文本、音频、图片或视频中的一种输入');
                return;
            }
            
            const formData = new FormData();
            formData.append('robot_id', document.getElementById('robot_id').value);
            formData.append('text', text);
            formData.append('touch_zone', document.getElementById('touch_zone').value);
            
            if (audioFile) {
                formData.append('audio_file', audioFile);
            }
            if (imageFile) {
                formData.append('image_file', imageFile);
            }
            if (videoFile) {
                formData.append('video_file', videoFile);
            }
            
            // 显示进度条
            const progressInterval = showProgress();
            
            try {
                const response = await fetch('/interact_with_files', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                // 完成进度条
                progressFill.style.width = '100%';
                progressText.textContent = '请求完成';
                
                const result = await response.json();
                document.getElementById('result').innerHTML = `
                    <h3>🤖 Robot Response:</h3>
                    <pre style="background-color: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto;">${JSON.stringify(result, null, 2)}</pre>
                `;
                
            } catch (error) {
                progressText.textContent = '请求失败: ' + error.message;
                document.getElementById('result').innerHTML = `
                    <h3>❌ Error:</h3>
                    <pre style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 4px;">${error.message}</pre>
                `;
            } finally {
                // 延迟隐藏进度条
                setTimeout(() => {
                    hideProgress();
                }, 1000);
                clearInterval(progressInterval);
            }
        });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "companion_robot_brain"}


@app.post("/upload/audio")
async def upload_audio(file: UploadFile = File(...)):
    """Receive an uploaded audio blob and save it."""
    try:
        # 验证文件类型
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Invalid audio file type")
        
        data = await file.read()
        if len(data) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # 生成文件名
        suffix = Path(file.filename).suffix if file.filename else '.webm'
        if suffix not in ['.wav', '.mp3', '.webm', '.ogg', '.m4a']:
            suffix = '.webm'
        
        name = UPLOAD_DIR / f"audio_{uuid.uuid4().hex}{suffix}"
        
        # 保存文件
        with open(name, "wb") as f:
            f.write(data)
        
        print(f"Audio file uploaded: {name} ({len(data)} bytes)")
        return {"path": str(name), "size": len(data), "type": file.content_type}
        
    except Exception as e:
        print(f"Audio upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload audio: {str(e)}")


@app.post("/upload/video")
async def upload_video(file: UploadFile = File(...)):
    """Receive an uploaded video blob and save it."""
    try:
        # 验证文件类型
        if not file.content_type or not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="Invalid video file type")
        
        data = await file.read()
        if len(data) == 0:
            raise HTTPException(status_code=400, detail="Empty video file")
        
        # 生成文件名
        suffix = Path(file.filename).suffix if file.filename else '.webm'
        if suffix not in ['.mp4', '.webm', '.avi', '.mov', '.mkv']:
            suffix = '.webm'
        
        name = UPLOAD_DIR / f"video_{uuid.uuid4().hex}{suffix}"
        
        # 保存文件
        with open(name, "wb") as f:
            f.write(data)
        
        print(f"Video file uploaded: {name} ({len(data)} bytes)")
        return {"path": str(name), "size": len(data), "type": file.content_type}
        
    except Exception as e:
        print(f"Video upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload video: {str(e)}")


@app.post("/upload/image")
async def upload_image(file: UploadFile = File(...)):
    """Receive an uploaded image and save it."""
    try:
        # 验证文件类型
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Invalid image file type")
        
        data = await file.read()
        if len(data) == 0:
            raise HTTPException(status_code=400, detail="Empty image file")
        
        # 生成文件名
        suffix = Path(file.filename).suffix if file.filename else '.png'
        if suffix not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            suffix = '.png'
        
        name = UPLOAD_DIR / f"image_{uuid.uuid4().hex}{suffix}"
        
        # 保存文件
        with open(name, "wb") as f:
            f.write(data)
        
        print(f"Image file uploaded: {name} ({len(data)} bytes)")
        return {"path": str(name), "size": len(data), "type": file.content_type}
        
    except Exception as e:
        print(f"Image upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")


@app.post("/interact_with_files")
async def interact_with_files(
    robot_id: str = Form(...),
    text: str = Form(""),
    audio_file: UploadFile = File(None),
    image_file: UploadFile = File(None),
    video_file: UploadFile = File(None),
    touch_zone: str = Form("")
):
    """Handle interaction with file uploads."""
    try:
        # 验证输入
        if not text.strip() and not audio_file and not image_file and not video_file:
            raise HTTPException(status_code=400, detail="At least one input (text, audio, image, or video) is required")
        
        # 保存上传的文件
        audio_path = None
        image_path = None
        video_path = None
        
        if audio_file:
            try:
                data = await audio_file.read()
                if len(data) == 0:
                    raise HTTPException(status_code=400, detail="Empty audio file")
                
                suffix = Path(audio_file.filename).suffix if audio_file.filename else '.webm'
                if suffix not in ['.wav', '.mp3', '.webm', '.ogg', '.m4a']:
                    suffix = '.webm'
                
                name = UPLOAD_DIR / f"audio_{uuid.uuid4().hex}{suffix}"
                with open(name, "wb") as f:
                    f.write(data)
                audio_path = str(name)
                print(f"Audio file saved: {audio_path} ({len(data)} bytes)")
            except Exception as e:
                print(f"Error saving audio file: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to save audio file: {str(e)}")
        
        if image_file:
            try:
                data = await image_file.read()
                if len(data) == 0:
                    raise HTTPException(status_code=400, detail="Empty image file")
                
                suffix = Path(image_file.filename).suffix if image_file.filename else '.png'
                if suffix not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                    suffix = '.png'
                
                name = UPLOAD_DIR / f"image_{uuid.uuid4().hex}{suffix}"
                with open(name, "wb") as f:
                    f.write(data)
                image_path = str(name)
                print(f"Image file saved: {image_path} ({len(data)} bytes)")
            except Exception as e:
                print(f"Error saving image file: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to save image file: {str(e)}")
        
        if video_file:
            try:
                data = await video_file.read()
                if len(data) == 0:
                    raise HTTPException(status_code=400, detail="Empty video file")
                
                suffix = Path(video_file.filename).suffix if video_file.filename else '.webm'
                if suffix not in ['.mp4', '.webm', '.avi', '.mov', '.mkv']:
                    suffix = '.webm'
                
                name = UPLOAD_DIR / f"video_{uuid.uuid4().hex}{suffix}"
                with open(name, "wb") as f:
                    f.write(data)
                video_path = str(name)
                print(f"Video file saved: {video_path} ({len(data)} bytes)")
            except Exception as e:
                print(f"Error saving video file: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to save video file: {str(e)}")
        
        # 创建用户输入
        user = UserInput(
            robot_id=robot_id,
            text=text.strip() if text.strip() else None,
            audio_path=audio_path,
            image_path=image_path,
            video_path=video_path,
            touch_zone=int(touch_zone) if touch_zone and touch_zone.isdigit() else None,
        )
        
        print(f"Processing request for robot {robot_id}")
        print(f"Text: {text}")
        print(f"Audio: {audio_path}")
        print(f"Image: {image_path}")
        print(f"Video: {video_path}")
        print(f"Touch zone: {touch_zone}")
        
        # 处理请求
        reply = core.process(user)
        result = reply.as_dict()
        
        print(f"Robot response: {result}")
        return result
        
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Error processing request: {exc}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(exc)}")


@app.post("/interact_stream")
async def interact_stream(
    robot_id: str = Form(...),
    text: str = Form(""),
    audio_file: UploadFile = File(None),
    image_file: UploadFile = File(None),
    video_file: UploadFile = File(None),
    touch_zone: str = Form("")
):
    """Handle interaction with file uploads and return streaming response."""
    from fastapi.responses import StreamingResponse
    import json
    
    async def generate_stream():
        try:
            # 验证输入
            if not text.strip() and not audio_file and not image_file and not video_file:
                yield f"data: {json.dumps({'error': 'At least one input (text, audio, image, or video) is required'})}\n\n"
                return
            
            # 保存上传的文件
            audio_path = None
            image_path = None
            video_path = None
            
            if audio_file:
                try:
                    data = await audio_file.read()
                    if len(data) == 0:
                        yield f"data: {json.dumps({'error': 'Empty audio file'})}\n\n"
                        return
                    
                    suffix = Path(audio_file.filename).suffix if audio_file.filename else '.webm'
                    if suffix not in ['.wav', '.mp3', '.webm', '.ogg', '.m4a']:
                        suffix = '.webm'
                    
                    name = UPLOAD_DIR / f"audio_{uuid.uuid4().hex}{suffix}"
                    with open(name, "wb") as f:
                        f.write(data)
                    audio_path = str(name)
                    print(f"Audio file saved: {audio_path} ({len(data)} bytes)")
                except Exception as e:
                    yield f"data: {json.dumps({'error': f'Failed to save audio file: {str(e)}'})}\n\n"
                    return
            
            if image_file:
                try:
                    data = await image_file.read()
                    if len(data) == 0:
                        yield f"data: {json.dumps({'error': 'Empty image file'})}\n\n"
                        return
                    
                    suffix = Path(image_file.filename).suffix if image_file.filename else '.png'
                    if suffix not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                        suffix = '.png'
                    
                    name = UPLOAD_DIR / f"image_{uuid.uuid4().hex}{suffix}"
                    with open(name, "wb") as f:
                        f.write(data)
                    image_path = str(name)
                    print(f"Image file saved: {image_path} ({len(data)} bytes)")
                except Exception as e:
                    yield f"data: {json.dumps({'error': f'Failed to save image file: {str(e)}'})}\n\n"
                    return
            
            if video_file:
                try:
                    data = await video_file.read()
                    if len(data) == 0:
                        yield f"data: {json.dumps({'error': 'Empty video file'})}\n\n"
                        return
                    
                    suffix = Path(video_file.filename).suffix if video_file.filename else '.webm'
                    if suffix not in ['.mp4', '.webm', '.avi', '.mov', '.mkv']:
                        suffix = '.webm'
                    
                    name = UPLOAD_DIR / f"video_{uuid.uuid4().hex}{suffix}"
                    with open(name, "wb") as f:
                        f.write(data)
                    video_path = str(name)
                    print(f"Video file saved: {video_path} ({len(data)} bytes)")
                except Exception as e:
                    yield f"data: {json.dumps({'error': f'Failed to save video file: {str(e)}'})}\n\n"
                    return
            
            # 创建用户输入
            user = UserInput(
                robot_id=robot_id,
                text=text.strip() if text.strip() else None,
                audio_path=audio_path,
                image_path=image_path,
                video_path=video_path,
                touch_zone=int(touch_zone) if touch_zone and touch_zone.isdigit() else None,
            )
            
            print(f"Processing streaming request for robot {robot_id}")
            print(f"Text: {text}")
            print(f"Audio: {audio_path}")
            print(f"Image: {image_path}")
            print(f"Video: {video_path}")
            print(f"Touch zone: {touch_zone}")
            
            # 处理请求并流式返回
            reply = core.process(user)
            result = reply.as_dict()
            
            # 发送完整结果
            yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
            
        except Exception as exc:
            print(f"Error processing streaming request: {exc}")
            yield f"data: {json.dumps({'error': f'Internal server error: {str(exc)}'})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )


def run_server(host: str = "127.0.0.1", port: int = 8000):
    """Start the FastAPI server using Uvicorn."""
    print(f"启动服务在 http://{host}:{port}")
    print("按 Ctrl+C 停止服务")
    print("访问 http://127.0.0.1:8000/verify 查看完整界面")
    try:
        uvicorn.run(app, host=host, port=port, log_level="info")
    except Exception as e:
        print(f"启动服务时出错: {e}")
        raise


if __name__ == "__main__":
    run_server()