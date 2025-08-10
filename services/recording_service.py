"""Recording service for handling audio and video recording."""

import asyncio
import uuid
import time
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import json


class RecordingService:
    """Service for handling audio and video recording."""
    
    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(exist_ok=True)
        self.active_recordings: Dict[str, Dict] = {}
    
    async def start_recording(
        self, 
        recording_type: str, 
        robot_id: str, 
        session_id: str = ""
    ) -> str:
        """Start recording audio, video, or both."""
        recording_id = f"recording_{uuid.uuid4().hex}"
        
        # 验证录制类型
        if recording_type not in ["audio", "video", "both"]:
            recording_type = "audio"  # 默认为音频录制
        
        # 创建录制任务
        recording_task = {
            "id": recording_id,
            "type": recording_type,
            "robot_id": robot_id,
            "session_id": session_id,
            "start_time": time.time(),
            "status": "recording",
            "files": [],
            "error": None
        }
        
        self.active_recordings[recording_id] = recording_task
        
        try:
            # 根据录制类型启动相应的录制任务
            if recording_type in ["audio", "both"]:
                await self._start_audio_recording(recording_id)
            
            if recording_type in ["video", "both"]:
                await self._start_video_recording(recording_id)
            
            print(f"🎙️ 开始录制 {recording_type}, ID: {recording_id}, 机器人: {robot_id}")
            return recording_id
            
        except Exception as e:
            recording_task["error"] = str(e)
            recording_task["status"] = "error"
            print(f"❌ 开始录制失败: {e}")
            raise
    
    async def stop_recording(self, recording_id: str) -> Dict:
        """Stop recording and return file paths."""
        if recording_id not in self.active_recordings:
            raise ValueError(f"录制 {recording_id} 未找到")
        
        recording = self.active_recordings[recording_id]
        
        try:
            # 停止录制任务
            await self._stop_recording_tasks(recording_id)
            
            recording["status"] = "stopped"
            recording["end_time"] = time.time()
            recording["duration"] = recording["end_time"] - recording["start_time"]
            
            # 生成文件路径
            result = {
                "success": True,
                "recording_id": recording_id,
                "duration": recording["duration"],
                "files": recording["files"],
                "robot_id": recording["robot_id"],
                "session_id": recording["session_id"]
            }
            
            # 从活动录制中移除
            del self.active_recordings[recording_id]
            
            print(f"⏹️ 停止录制 {recording_id}, 时长: {recording['duration']:.2f}秒")
            return result
            
        except Exception as e:
            recording["error"] = str(e)
            recording["status"] = "error"
            print(f"❌ 停止录制失败: {e}")
            raise
    
    def get_recording_status(self, recording_id: str) -> Dict:
        """Get the status of a recording."""
        if recording_id not in self.active_recordings:
            return {"status": "not_found"}
        
        recording = self.active_recordings[recording_id]
        current_time = time.time()
        
        return {
            "id": recording_id,
            "type": recording["type"],
            "status": recording["status"],
            "robot_id": recording["robot_id"],
            "session_id": recording["session_id"],
            "start_time": recording["start_time"],
            "duration": current_time - recording["start_time"] if recording["status"] == "recording" else recording.get("duration", 0),
            "files": recording.get("files", []),
            "error": recording.get("error")
        }
    
    def list_active_recordings(self) -> list:
        """List all active recordings."""
        current_time = time.time()
        return [
            {
                "id": recording["id"],
                "type": recording["type"],
                "robot_id": recording["robot_id"],
                "session_id": recording["session_id"],
                "start_time": recording["start_time"],
                "duration": current_time - recording["start_time"],
                "status": recording["status"],
                "error": recording.get("error")
            }
            for recording in self.active_recordings.values()
        ]
    
    async def _start_audio_recording(self, recording_id: str):
        """Start audio recording using browser APIs."""
        recording = self.active_recordings[recording_id]
        
        try:
            # 模拟录制过程
            await asyncio.sleep(0.1)  # 模拟启动时间
            
            # 生成音频文件路径
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_filename = f"audio_{recording_id}_{timestamp}.webm"
            audio_path = str(self.upload_dir / audio_filename)
            
            recording["files"].append({
                "type": "audio",
                "path": audio_path,
                "filename": audio_filename,
                "size": 0,  # 实际大小将在录制完成后更新
                "duration": 0
            })
            
            print(f"🎵 音频录制已启动: {audio_path}")
            
        except Exception as e:
            recording["error"] = f"音频录制失败: {str(e)}"
            raise
    
    async def _start_video_recording(self, recording_id: str):
        """Start video recording using browser APIs."""
        recording = self.active_recordings[recording_id]
        
        try:
            # 模拟录制过程
            await asyncio.sleep(0.1)  # 模拟启动时间
            
            # 生成视频文件路径
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_filename = f"video_{recording_id}_{timestamp}.webm"
            video_path = str(self.upload_dir / video_filename)
            
            recording["files"].append({
                "type": "video",
                "path": video_path,
                "filename": video_filename,
                "size": 0,  # 实际大小将在录制完成后更新
                "duration": 0,
                "resolution": "1280x720"  # 默认分辨率
            })
            
            print(f"🎬 视频录制已启动: {video_path}")
            
        except Exception as e:
            recording["error"] = f"视频录制失败: {str(e)}"
            raise
    
    async def _stop_recording_tasks(self, recording_id: str):
        """Stop all recording tasks for a recording."""
        recording = self.active_recordings[recording_id]
        
        try:
            # 模拟停止录制过程
            await asyncio.sleep(0.1)  # 模拟停止时间
            
            # 更新文件信息
            for file_info in recording["files"]:
                # 模拟文件大小和时长
                file_info["size"] = 1024 * 1024  # 1MB
                file_info["duration"] = recording.get("duration", 0)
            
            print(f"⏹️ 录制任务已停止: {recording_id}")
            
        except Exception as e:
            recording["error"] = f"停止录制任务失败: {str(e)}"
            raise
    
    def get_recording_script(self) -> str:
        """Get JavaScript code for browser-based recording."""
        return """
        // 录制功能JavaScript代码
        class RecordingManager {
            constructor() {
                this.mediaRecorder = null;
                this.recordedChunks = [];
                this.isRecording = false;
                this.recordingType = 'audio';
                this.stream = null;
            }
            
            async startRecording(type = 'audio') {
                try {
                    this.recordingType = type;
                    const constraints = {
                        audio: type === 'audio' || type === 'both',
                        video: type === 'video' || type === 'both'
                    };
                    
                    this.stream = await navigator.mediaDevices.getUserMedia(constraints);
                    this.mediaRecorder = new MediaRecorder(this.stream);
                    
                    this.mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            this.recordedChunks.push(event.data);
                        }
                    };
                    
                    this.mediaRecorder.onstop = () => {
                        const blob = new Blob(this.recordedChunks, {
                            type: this.recordingType === 'audio' ? 'audio/webm' : 'video/webm'
                        });
                        
                        // 创建下载链接
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `recording_${Date.now()}.webm`;
                        a.click();
                        
                        URL.revokeObjectURL(url);
                    };
                    
                    this.mediaRecorder.start();
                    this.isRecording = true;
                    
                    console.log(`开始录制 ${type}`);
                    return true;
                } catch (error) {
                    console.error('录制失败:', error);
                    return false;
                }
            }
            
            stopRecording() {
                if (this.mediaRecorder && this.isRecording) {
                    this.mediaRecorder.stop();
                    this.isRecording = false;
                    
                    // 停止所有轨道
                    if (this.stream) {
                        this.stream.getTracks().forEach(track => track.stop());
                    }
                    
                    console.log('录制已停止');
                }
            }
            
            isRecording() {
                return this.isRecording;
            }
            
            getRecordingTime() {
                if (!this.isRecording) return 0;
                return Date.now() - this.startTime;
            }
        }
        
        // 创建全局录制管理器
        window.recordingManager = new RecordingManager();
        """
    
    def validate_recording_type(self, recording_type: str) -> bool:
        """Validate recording type."""
        return recording_type in ["audio", "video", "both"]
    
    def get_recording_stats(self) -> Dict:
        """Get recording statistics."""
        current_time = time.time()
        total_recordings = len(self.active_recordings)
        total_duration = sum(
            current_time - recording["start_time"] 
            for recording in self.active_recordings.values()
        )
        
        return {
            "total_recordings": total_recordings,
            "total_duration": total_duration,
            "audio_recordings": len([r for r in self.active_recordings.values() if r["type"] in ["audio", "both"]]),
            "video_recordings": len([r for r in self.active_recordings.values() if r["type"] in ["video", "both"]]),
            "error_count": len([r for r in self.active_recordings.values() if r.get("error")])
        } 