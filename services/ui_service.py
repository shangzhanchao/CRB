"""UI service for handling HTML content and UI-related logic."""

from typing import Dict, Any, Optional
from pathlib import Path


class UIService:
    """Service for handling UI-related functionality."""
    
    def __init__(self):
        self.base_template = self._get_base_template()
        self.recording_script = self._get_recording_script()
    
    def _get_base_template(self) -> str:
        """Get the base HTML template."""
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>智能陪伴机器人</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Microsoft YaHei', Arial, sans-serif; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: #333;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    text-align: center;
                    margin-bottom: 30px;
                    color: white;
                }
                .header h1 {
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .main-content {
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    margin-bottom: 20px;
                }
                .input-section {
                    margin-bottom: 30px;
                }
                .input-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                    color: #555;
                }
                input[type="text"], textarea {
                    width: 100%;
                    padding: 12px;
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    font-size: 16px;
                    transition: border-color 0.3s;
                }
                input[type="text"]:focus, textarea:focus {
                    outline: none;
                    border-color: #667eea;
                }
                textarea {
                    min-height: 120px;
                    resize: vertical;
                }
                .btn {
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: all 0.3s;
                    font-weight: bold;
                }
                .btn:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                }
                .btn-primary {
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    color: white;
                }
                .btn-primary:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }
                .btn-success {
                    background: #28a745;
                    color: white;
                }
                .btn-success:hover {
                    background: #218838;
                }
                .btn-danger {
                    background: #dc3545;
                    color: white;
                }
                .btn-danger:hover {
                    background: #c82333;
                }
                .btn-info {
                    background: #17a2b8;
                    color: white;
                }
                .btn-info:hover {
                    background: #138496;
                }
                .main-action {
                    background: linear-gradient(45deg, #28a745, #20c997);
                    color: white;
                    font-size: 18px;
                    padding: 15px 30px;
                    margin: 20px 0;
                    border-radius: 12px;
                    box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
                    transition: all 0.3s ease;
                    font-weight: bold;
                }
                .main-action:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
                }
                .main-action:disabled {
                    opacity: 0.7;
                    transform: none;
                }
                .recording-section {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                }
                .recording-controls {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 15px;
                    flex-wrap: wrap;
                }
                .recording-status {
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 10px;
                    display: none;
                }
                .status-recording {
                    background: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                }
                .status-stopped {
                    background: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }
                .progress-container {
                    margin: 15px 0;
                    display: none;
                }
                .progress-bar {
                    width: 100%;
                    height: 20px;
                    background: #e9ecef;
                    border-radius: 10px;
                    overflow: hidden;
                    margin-bottom: 10px;
                }
                .progress-fill {
                    height: 100%;
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    width: 0%;
                    transition: width 0.3s ease;
                    border-radius: 10px;
                }
                .recording-time {
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 10px;
                }
                .response-section {
                    margin-top: 30px;
                }
                .response-content {
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 20px;
                    margin-top: 15px;
                    white-space: pre-wrap;
                    line-height: 1.6;
                    border-left: 4px solid #667eea;
                }
                .ai-response {
                    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                    border-radius: 12px;
                    padding: 20px;
                    margin-top: 15px;
                    border-left: 4px solid #2196f3;
                    box-shadow: 0 2px 10px rgba(33, 150, 243, 0.1);
                }
                .ai-response-header {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-bottom: 15px;
                }
                .ai-avatar {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background: linear-gradient(45deg, #667eea, #764ba2);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 20px;
                }
                .ai-info {
                    flex: 1;
                }
                .ai-name {
                    font-weight: bold;
                    color: #1976d2;
                    font-size: 16px;
                }
                .ai-status {
                    color: #666;
                    font-size: 12px;
                }
                .ai-content {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }
                .ai-text {
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid rgba(33, 150, 243, 0.2);
                    line-height: 1.6;
                }
                .ai-emotion {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    background: white;
                    padding: 10px 15px;
                    border-radius: 8px;
                    border: 1px solid rgba(33, 150, 243, 0.2);
                }
                .emotion-icon {
                    font-size: 24px;
                }
                .emotion-text {
                    color: #1976d2;
                    font-weight: bold;
                }
                .ai-action {
                    background: white;
                    padding: 10px 15px;
                    border-radius: 8px;
                    border: 1px solid rgba(33, 150, 243, 0.2);
                    color: #666;
                    font-style: italic;
                }
                .ai-audio {
                    background: white;
                    padding: 10px 15px;
                    border-radius: 8px;
                    border: 1px solid rgba(33, 150, 243, 0.2);
                }
                .ai-audio audio {
                    width: 100%;
                    border-radius: 4px;
                }
                .ai-expression {
                    background: white;
                    padding: 10px 15px;
                    border-radius: 8px;
                    border: 1px solid rgba(33, 150, 243, 0.2);
                    color: #666;
                }
                .ai-intimacy {
                    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                    padding: 10px 15px;
                    border-radius: 8px;
                    border: 1px solid rgba(255, 154, 158, 0.3);
                    color: #d63384;
                    font-weight: bold;
                }
                .ai-touch-response {
                    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                    padding: 10px 15px;
                    border-radius: 8px;
                    border: 1px solid rgba(168, 237, 234, 0.3);
                    color: #0d6efd;
                    font-weight: bold;
                }
                .ai-stats {
                    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                    padding: 10px 15px;
                    border-radius: 8px;
                    border: 1px solid rgba(255, 236, 210, 0.3);
                    color: #fd7e14;
                    font-size: 12px;
                }

                .touch-zones {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    margin-bottom: 20px;
                }
                .touch-zone {
                    padding: 15px;
                    border: 2px solid #ddd;
                    border-radius: 12px;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                }
                .touch-zone:hover {
                    border-color: #667eea;
                    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                    transform: translateY(-2px);
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
                }
                .touch-zone.selected {
                    border-color: #667eea;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
                }
                .touch-zone.selected strong {
                    color: white;
                }
                .touch-zone.selected small {
                    color: rgba(255, 255, 255, 0.8);
                }
                .touch-zone strong {
                    display: block;
                    font-size: 16px;
                    margin-bottom: 5px;
                    color: #333;
                }
                .touch-zone small {
                    color: #666;
                    font-size: 12px;
                }
                .recording-preview {
                    margin-top: 15px;
                    display: none;
                }
                .recording-preview video,
                .recording-preview audio {
                    width: 100%;
                    border-radius: 8px;
                    margin-top: 10px;
                }
                .loading {
                    display: none;
                    text-align: center;
                    padding: 20px;
                }
                .spinner {
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #667eea;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 10px;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                .error {
                    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    border-radius: 8px;
                    padding: 12px;
                    margin-bottom: 15px;
                    border-left: 4px solid #dc3545;
                }
                .success {
                    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                    color: #155724;
                    border: 1px solid #c3e6cb;
                    border-radius: 8px;
                    padding: 12px;
                    margin-bottom: 15px;
                    border-left: 4px solid #28a745;
                }
                .info {
                    background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
                    color: #0c5460;
                    border: 1px solid #bee5eb;
                    border-radius: 8px;
                    padding: 12px;
                    margin-bottom: 15px;
                    border-left: 4px solid #17a2b8;
                }
                .chat-history {
                    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                    border-radius: 12px;
                    padding: 20px;
                    margin-top: 20px;
                    border-left: 4px solid #ffc107;
                }
                .chat-history h3 {
                    margin: 0 0 15px 0;
                    color: #f57c00;
                    font-size: 18px;
                }
                .chat-list {
                    max-height: 300px;
                    overflow-y: auto;
                    border: 1px solid rgba(255, 193, 7, 0.2);
                    border-radius: 8px;
                    background: white;
                }
                .chat-item {
                    padding: 12px 15px;
                    border-bottom: 1px solid #eee;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                .chat-item:hover {
                    background: #f8f9fa;
                }
                .chat-item:last-child {
                    border-bottom: none;
                }
                .chat-time {
                    font-size: 12px;
                    color: #666;
                    margin-bottom: 5px;
                }
                .chat-input {
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 5px;
                }
                .chat-reply {
                    font-size: 14px;
                    color: #666;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }
                .no-chat-history {
                    text-align: center;
                    padding: 20px;
                    color: #666;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 智能陪伴机器人</h1>
                    <p>您的智能AI助手，支持多模态交互</p>
                </div>
                
                <div class="main-content">
                    <div class="input-section">
                        <div class="input-group">
                            <label for="robotId">🤖 机器人ID:</label>
                            <input type="text" id="robotId" value="robotA" placeholder="请输入机器人ID">
                        </div>
                        
                        <div class="input-group">
                            <label for="userInput">💬 用户输入:</label>
                            <textarea id="userInput" placeholder="请输入您的问题或指令..."></textarea>
                        </div>
                        
                        <div class="input-group">
                            <label>🖐️ 抚摸区域:</label>
                            <div class="touch-zones">
                                <div class="touch-zone" data-zone="0" onclick="selectTouchZone(0)">
                                    <strong>头部</strong><br>
                                    <small>温柔抚摸</small>
                                </div>
                                <div class="touch-zone" data-zone="1" onclick="selectTouchZone(1)">
                                    <strong>背后</strong><br>
                                    <small>舒适按摩</small>
                                </div>
                                <div class="touch-zone" data-zone="2" onclick="selectTouchZone(2)">
                                    <strong>胸口</strong><br>
                                    <small>亲密接触</small>
                                </div>
                            </div>
                        </div>
                        
                        <!-- 主要操作按钮 -->
                        <div style="text-align: center; margin: 30px 0;">
                            <button class="btn main-action" id="sendMessageBtn" onclick="sendMessage()" type="button">
                                💬 发送消息
                            </button>
                        </div>
                    </div>
                    
                    <div class="recording-section">
                        <h3>🎥 录制功能</h3>
                        

                        
                        <div class="recording-controls">
                            <button class="btn btn-success" onclick="startRecording('audio')">
                                🎤 开始录音
                            </button>
                            <button class="btn btn-success" onclick="startRecording('video')">
                                📹 开始录像
                            </button>
                            <button class="btn btn-danger" onclick="stopRecording()">
                                ⏹️ 停止录制
                            </button>
                            <button class="btn btn-info" onclick="getActiveRecordings()">
                                📋 查看录制
                            </button>
                        </div>
                        <div class="recording-status" id="recordingStatus"></div>
                        <div class="progress-container" id="progressContainer">
                            <div class="recording-time" id="recordingTime">00:00</div>
                            <div class="progress-bar">
                                <div class="progress-fill" id="progressFill"></div>
                            </div>
                        </div>
                        <div class="recording-preview" id="recordingPreview"></div>
                    </div>
                    
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        <p>处理中，请稍候...</p>
                    </div>
                    
                    <div class="response-section">
                        <h3>🤖 AI回复</h3>
                        <div class="ai-response" id="aiResponse" style="display: none;">
                            <div class="ai-response-header">
                                <div class="ai-avatar">🤖</div>
                                <div class="ai-info">
                                    <div class="ai-name">智能陪伴机器人</div>
                                    <div class="ai-status">正在思考...</div>
                                </div>
                            </div>
                            <div class="ai-content" id="aiContent">
                                <!-- AI回复内容将在这里动态生成 -->
                            </div>
                        </div>
                        <div class="response-content" id="responseContent">
                            等待您的输入...
                        </div>
                    </div>
                    
                    <div class="chat-history">
                        <h3>📋 对话记录</h3>
                        <div class="chat-list" id="chatList">
                            <div class="no-chat-history">暂无对话记录</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                // 全局变量
                let currentSessionId = '';
                let currentRecordingId = '';
                let recordingStartTime = 0;
                let recordingInterval = null;
                let mediaRecorder = null;
                let recordedChunks = [];
                let selectedTouchZone = 0; // 默认选择头部
                let isProcessing = false; // 防止重复提交
                let chatHistory = []; // 对话历史记录
                
                // 页面加载时初始化
                document.addEventListener('DOMContentLoaded', function() {
                    console.log('页面加载完成，开始初始化...');
                    initializeApp();
                });
                
                // 提前定义：选择抚摸区域（函数声明，支持提升）
                function selectTouchZone(zone) {
                    try {
                        if (zone < 0 || zone > 2) {
                            zone = 0; // 默认头部
                        }
                        
                        selectedTouchZone = zone;
                        console.log('选择抚摸区域:', zone);
                        
                        // 移除所有选中状态
                        document.querySelectorAll('.touch-zone').forEach(el => {
                            el.classList.remove('selected');
                        });
                        
                        // 添加选中状态到当前选择
                        const selectedElement = document.querySelector(`[data-zone="${zone}"]`);
                        if (selectedElement) {
                            selectedElement.classList.add('selected');
                        }
                        
                        showInfo(`已选择抚摸区域: ${getTouchZoneName(zone)}`);
                    } catch (error) {
                        console.error('选择抚摸区域失败:', error);
                        showError('选择抚摸区域失败: ' + error.message);
                    }
                }

                // 初始化应用
                function initializeApp() {
                    try {
                        selectTouchZone(0); // 默认选择头部
                        
                        // 添加键盘事件监听
                        document.getElementById('userInput').addEventListener('keypress', function(e) {
                            if (e.key === 'Enter' && e.ctrlKey) {
                                e.preventDefault();
                                sendMessage();
                            }
                        });
                        

                        
                        // 加载持久化的对话历史
                        loadChatHistory();
                        
                        console.log('应用初始化完成');
                        showInfo('页面加载完成，所有功能已就绪');
                    } catch (error) {
                        console.error('初始化失败:', error);
                        showError('页面初始化失败: ' + error.message);
                    }
                }
                
                // 导出到全局，供内联onclick调用
                window.selectTouchZone = selectTouchZone;
                
                // 获取抚摸区域名称
                function getTouchZoneName(zone) {
                    const zones = ['头部', '背后', '胸口'];
                    return zones[zone] || '未知区域';
                }
                
                // 发送消息（挂到window避免作用域问题，便于按钮直接调用）
                window.sendMessage = async function() {
                    if (isProcessing) {
                        showError('正在处理中，请稍候...');
                        return;
                    }
                    
                    const robotId = document.getElementById('robotId').value;
                    const userInput = document.getElementById('userInput').value;
                    
                    if (!userInput.trim()) {
                        showError('请输入消息');
                        return;
                    }
                    
                    isProcessing = true;
                    const sendButton = document.getElementById('sendMessageBtn');
                    sendButton.disabled = true;
                    sendButton.textContent = '发送中...';
                    
                    showLoading(true);
                    
                    try {
                        console.log('开始发送消息...');
                        
                        const formData = new FormData();
                        formData.append('robot_id', robotId);
                        formData.append('user_input', userInput);
                        formData.append('session_id', currentSessionId);
                        formData.append('touch_zone', selectedTouchZone);
                        

                        
                        const response = await fetch('/interact_with_files', {
                            method: 'POST',
                            body: formData
                        });
                        
                        console.log('服务器响应状态:', response.status);
                        
                        if (!response.ok) {
                            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                        }
                        
                        const result = await response.json();
                        console.log('服务器响应:', result);
                        
                        if (result.status === 'success') {
                            // 显示丰富的AI回复
                            displayAIResponse(result);
                            
                            // 添加到对话历史
                            addToChatHistory(userInput, result);
                            
                            if (result.data && result.data.session) {
                                currentSessionId = result.data.session.session_id;
                            }
                            showSuccess('消息发送成功');
                        } else {
                            showError(result.error || '发送失败');
                        }
                    } catch (error) {
                        console.error('发送消息失败:', error);
                        showError('网络错误: ' + error.message);
                    } finally {
                        isProcessing = false;
                        sendButton.disabled = false;
                        sendButton.textContent = '💬 发送消息';
                        showLoading(false);
                        
                        // 清空输入框
                        document.getElementById('userInput').value = '';
                    }
                }
                
                // 显示丰富的AI回复
                function displayAIResponse(result) {
                    const aiResponse = document.getElementById('aiResponse');
                    const aiContent = document.getElementById('aiContent');
                    try {
                        // 清空之前的内容
                        aiContent.innerHTML = '';
                        
                        if (!result || !result.data) {
                            const textDiv = document.createElement('div');
                            textDiv.className = 'ai-text';
                            textDiv.textContent = '暂无数据';
                            aiContent.appendChild(textDiv);
                            aiResponse.style.display = 'block';
                            return;
                        }
                        const data = result.data;
                        
                        // 文本回复（兼容当content为JSON字符串时，仅展示其中的text字段）
                        if (data.reply) {
                            const textDiv = document.createElement('div');
                            textDiv.className = 'ai-text';

                            // 尝试从字符串中提取JSON（支持```json代码块和嵌入式JSON），避免使用正则以规避低版本内核对正则的兼容性问题
                            let replyContent = data.reply.content || '';
                            let parsedJson = null;
                            try {
                                if (typeof replyContent === 'string') {
                                    let raw = replyContent.trim();
                                    // 去除代码块围栏 ```json ... ```（非正则实现）
                                    if (raw.startsWith('```')) {
                                        const firstNewline = raw.indexOf('\n');
                                        if (firstNewline !== -1) {
                                            raw = raw.slice(firstNewline + 1);
                                        } else {
                                            // 单行 ```json 无换行的情况，去掉前缀
                                            raw = raw.slice(3);
                                        }
                                        if (raw.endsWith('```')) raw = raw.slice(0, -3);
                                        raw = raw.trim();
                                    }
                                    if (raw.startsWith('{') && raw.endsWith('}')) {
                                        parsedJson = JSON.parse(raw);
                                    } else {
                                        const first = raw.indexOf('{');
                                        const last = raw.lastIndexOf('}');
                                        if (first !== -1 && last !== -1 && last > first) {
                                            const candidate = raw.slice(first, last + 1);
                                            parsedJson = JSON.parse(candidate);
                                        }
                                    }
                                }
                            } catch (e) {
                                parsedJson = null;
                            }

                            if (parsedJson && parsedJson.text) {
                                replyContent = parsedJson.text;
                            }
                            textDiv.textContent = replyContent;
                            aiContent.appendChild(textDiv);

                            // 当服务端未解析emotion/action/expression时，前端补充解析
                            if (parsedJson) {
                                // emotion
                                if (!data.emotion && parsedJson.emotion) {
                                    const emotionDiv = document.createElement('div');
                                    emotionDiv.className = 'ai-emotion';
                                    const emotionIcon = document.createElement('span');
                                    emotionIcon.className = 'emotion-icon';
                                    emotionIcon.textContent = getEmotionIcon(parsedJson.emotion);
                                    const emotionText = document.createElement('span');
                                    emotionText.className = 'emotion-text';
                                    emotionText.textContent = parsedJson.emotion;
                                    emotionDiv.appendChild(emotionIcon);
                                    emotionDiv.appendChild(emotionText);
                                    aiContent.appendChild(emotionDiv);
                                }
                                // action(s)
                                if (!data.action && (parsedJson.action || parsedJson.actions)) {
                                    const actions = Array.isArray(parsedJson.action || parsedJson.actions)
                                        ? (parsedJson.action || parsedJson.actions)
                                        : [parsedJson.action || parsedJson.actions];
                                    if (actions.length) {
                                        const actionDiv = document.createElement('div');
                                        actionDiv.className = 'ai-action';
                                        actionDiv.innerHTML = '<strong>🤸 机器人动作:</strong><br>';
                                        actions.forEach(act => {
                                            const actionItem = document.createElement('div');
                                            actionItem.style.marginTop = '5px';
                                            actionItem.style.padding = '5px';
                                            actionItem.style.backgroundColor = 'rgba(33, 150, 243, 0.1)';
                                            actionItem.style.borderRadius = '4px';
                                            actionItem.textContent = String(act);
                                            actionDiv.appendChild(actionItem);
                                        });
                                        aiContent.appendChild(actionDiv);
                                    }
                                }
                                // expression(s)
                                if (!data.expression && (parsedJson.expression || parsedJson.expressions)) {
                                    const expr = parsedJson.expression || parsedJson.expressions;
                                    const exprStr = Array.isArray(expr) ? expr.join('|') : String(expr);
                                    const expressionDiv = document.createElement('div');
                                    expressionDiv.className = 'ai-expression';
                                    expressionDiv.innerHTML = `
                                        <strong>😊 机器人表情:</strong> ${exprStr}
                                    `;
                                    aiContent.appendChild(expressionDiv);
                                }
                            }
                        }
                        
                        // 情感信息
                        if (data.emotion) {
                            const emotionDiv = document.createElement('div');
                            emotionDiv.className = 'ai-emotion';
                            
                            const emotionIcon = document.createElement('span');
                            emotionIcon.className = 'emotion-icon';
                            emotionIcon.textContent = getEmotionIcon(data.emotion.value);
                            
                            const emotionText = document.createElement('span');
                            emotionText.className = 'emotion-text';
                            emotionText.textContent = data.emotion.description;
                            
                            emotionDiv.appendChild(emotionIcon);
                            emotionDiv.appendChild(emotionText);
                            aiContent.appendChild(emotionDiv);
                        }
                        
                        // 动作信息
                        if (data.action && Array.isArray(data.action)) {
                            const actionDiv = document.createElement('div');
                            actionDiv.className = 'ai-action';
                            actionDiv.innerHTML = '<strong>🤸 机器人动作:</strong><br>';
                            
                            data.action.forEach(action => {
                                const actionItem = document.createElement('div');
                                actionItem.style.marginTop = '5px';
                                actionItem.style.padding = '5px';
                                actionItem.style.backgroundColor = 'rgba(33, 150, 243, 0.1)';
                                actionItem.style.borderRadius = '4px';
                                actionItem.textContent = action;
                                actionDiv.appendChild(actionItem);
                            });
                            
                            aiContent.appendChild(actionDiv);
                        }
                        
                        // 表情信息
                        if (data.expression) {
                            const expressionDiv = document.createElement('div');
                            expressionDiv.className = 'ai-expression';
                            expressionDiv.innerHTML = `<strong>😊 机器人表情:</strong> ${data.expression}`;
                            aiContent.appendChild(expressionDiv);
                        }
                        
                        // 音频信息
                        if (data.audio && data.audio !== 'n/a') {
                            const audioDiv = document.createElement('div');
                            audioDiv.className = 'ai-audio';
                            audioDiv.innerHTML = '<strong>🎵 语音回复:</strong><br>';
                            
                            const audioElement = document.createElement('audio');
                            audioElement.controls = true;
                            audioElement.src = data.audio;
                            audioDiv.appendChild(audioElement);
                            aiContent.appendChild(audioDiv);
                        }
                        
                        // 亲密度信息
                        if (data.interaction_details && data.interaction_details.touch_zone) {
                            const intimacyDiv = document.createElement('div');
                            intimacyDiv.className = 'ai-intimacy';
                            intimacyDiv.innerHTML = `<strong>💕 亲密度信息:</strong> 抚摸${data.interaction_details.touch_zone.name}，增进感情`;
                            aiContent.appendChild(intimacyDiv);
                        }
                        
                        // 抚摸响应信息
                        if (data.interaction_details && data.interaction_details.touch_zone) {
                            const touchDiv = document.createElement('div');
                            touchDiv.className = 'ai-touch-response';
                            touchDiv.innerHTML = `<strong>🖐️ 抚摸反馈:</strong> 感受到${data.interaction_details.touch_zone.name}的温柔抚摸`;
                            aiContent.appendChild(touchDiv);
                        }
                        
                        // 统计信息
                        if (data.memory_count !== undefined) {
                            const statsDiv = document.createElement('div');
                            statsDiv.className = 'ai-stats';
                            statsDiv.innerHTML = `<strong>📊 系统统计:</strong> 记忆数量: ${data.memory_count}, 会话ID: ${data.session_id || 'N/A'}`;
                            aiContent.appendChild(statsDiv);
                        }
                        
                        // 动作信息（如果不在interaction_details中）
                        if (data.action && !data.interaction_details) {
                            const actionDiv = document.createElement('div');
                            actionDiv.className = 'ai-action';
                            actionDiv.textContent = `🤖 动作: ${data.action}`;
                            aiContent.appendChild(actionDiv);
                        }
                        
                        // 显示AI回复区域
                        aiResponse.style.display = 'block';
                        
                        // 更新AI状态
                        const aiStatus = document.querySelector('.ai-status');
                        aiStatus.textContent = '回复完成';
                    } catch (err) {
                        console.error('displayAIResponse错误:', err);
                        const textDiv = document.createElement('div');
                        textDiv.className = 'ai-text';
                        textDiv.textContent = '渲染回复时出错: ' + (err && err.message ? err.message : String(err));
                        aiContent.appendChild(textDiv);
                        aiResponse.style.display = 'block';
                    }
                }
                
                // 获取情感图标
                function getEmotionIcon(emotion) {
                    const icons = {
                        'happy': '😊',
                        'sad': '😢',
                        'angry': '😠',
                        'excited': '🤩',
                        'calm': '😌',
                        'anxious': '😰',
                        'neutral': '😐'
                    };
                    return icons[emotion] || '😐';
                }
                
                // 添加到对话历史
                function addToChatHistory(userInput, result) {
                    const chatItem = {
                        time: new Date().toLocaleString('zh-CN'),
                        input: userInput,
                        reply: result.data?.reply?.content || '无回复',
                        timestamp: Date.now()
                    };
                    
                    chatHistory.unshift(chatItem); // 添加到开头
                    
                    // 限制历史记录数量
                    if (chatHistory.length > 50) {
                        chatHistory = chatHistory.slice(0, 50);
                    }
                    
                    // 保存到本地存储
                    saveChatHistory();
                    
                    updateChatHistoryDisplay();
                }
                
                // 保存对话历史到本地存储
                function saveChatHistory() {
                    try {
                        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
                        console.log('对话历史已保存到本地存储');
                    } catch (error) {
                        console.error('保存对话历史失败:', error);
                    }
                }
                
                // 从本地存储加载对话历史
                function loadChatHistory() {
                    try {
                        const savedHistory = localStorage.getItem('chatHistory');
                        if (savedHistory) {
                            chatHistory = JSON.parse(savedHistory);
                            console.log('从本地存储加载对话历史:', chatHistory.length, '条记录');
                            updateChatHistoryDisplay();
                        }
                    } catch (error) {
                        console.error('加载对话历史失败:', error);
                        chatHistory = [];
                    }
                }
                
                // 更新对话历史显示
                function updateChatHistoryDisplay() {
                    const chatList = document.getElementById('chatList');
                    
                    if (chatHistory.length === 0) {
                        chatList.innerHTML = '<div class="no-chat-history">暂无对话记录</div>';
                        return;
                    }
                    
                    chatList.innerHTML = '';
                    
                    chatHistory.forEach((chat, index) => {
                        const chatItem = document.createElement('div');
                        chatItem.className = 'chat-item';
                        chatItem.onclick = () => showChatDetail(chat);
                        
                        chatItem.innerHTML = `
                            <div class="chat-time">${chat.time}</div>
                            <div class="chat-input">${chat.input}</div>
                            <div class="chat-reply">${chat.reply}</div>
                        `;
                        
                        chatList.appendChild(chatItem);
                    });
                }
                
                // 显示对话详情
                function showChatDetail(chat) {
                    const detail = `时间: ${chat.time}\n用户输入: ${chat.input}\nAI回复: ${chat.reply}`;
                    showInfo(detail);
                }
                
                // 开始录制
                async function startRecording(type) {
                    try {
                        const robotId = document.getElementById('robotId').value;
                        
                        console.log(`开始${type === 'audio' ? '录音' : '录像'}...`);
                        
                        // 先启动浏览器录制
                        const success = await startBrowserRecording(type);
                        if (!success) {
                            showError('无法启动录制，请检查浏览器权限');
                            return;
                        }
                        
                        // 通知服务器开始录制
                        const response = await fetch('/start_recording', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                recording_type: type,
                                robot_id: robotId,
                                session_id: currentSessionId
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            currentRecordingId = result.recording_id;
                            recordingStartTime = Date.now();
                            
                            const statusDiv = document.getElementById('recordingStatus');
                            statusDiv.textContent = `${type === 'audio' ? '录音' : '录像'}进行中...`;
                            statusDiv.className = 'recording-status status-recording';
                            statusDiv.style.display = 'block';
                            
                            // 显示进度条
                            document.getElementById('progressContainer').style.display = 'block';
                            
                            // 开始计时
                            startRecordingTimer();
                            
                            showSuccess(`${type === 'audio' ? '录音' : '录像'}已开始`);
                        } else {
                            showError(result.error || '开始录制失败');
                        }
                    } catch (error) {
                        console.error('开始录制失败:', error);
                        showError('网络错误: ' + error.message);
                    }
                }
                
                // 启动浏览器录制
                async function startBrowserRecording(type) {
                    try {
                        const constraints = type === 'audio' 
                            ? { audio: true }
                            : { audio: true, video: true };
                        
                        const stream = await navigator.mediaDevices.getUserMedia(constraints);
                        mediaRecorder = new MediaRecorder(stream);
                        recordedChunks = [];
                        
                        mediaRecorder.ondataavailable = (event) => {
                            if (event.data.size > 0) {
                                recordedChunks.push(event.data);
                            }
                        };
                        
                        mediaRecorder.onstop = () => {
                            const blob = new Blob(recordedChunks, {
                                type: type === 'audio' ? 'audio/wav' : 'video/webm'
                            });
                            
                            // 显示预览
                            showRecordingPreview(blob, type);
                            
                            // 上传文件
                            uploadRecording(blob, type);
                        };
                        
                        mediaRecorder.start();
                        return true;
                    } catch (error) {
                        console.error('录制失败:', error);
                        return false;
                    }
                }
                
                // 停止录制
                async function stopRecording() {
                    if (!currentRecordingId) {
                        showError('没有正在进行的录制');
                        return;
                    }
                    
                    try {
                        console.log('停止录制...');
                        
                        // 停止浏览器录制
                        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                            mediaRecorder.stop();
                            mediaRecorder.stream.getTracks().forEach(track => track.stop());
                        }
                        
                        // 通知服务器停止录制
                        const response = await fetch('/stop_recording', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                recording_id: currentRecordingId
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.status === 'success') {
                            const statusDiv = document.getElementById('recordingStatus');
                            statusDiv.textContent = '录制已停止';
                            statusDiv.className = 'recording-status status-stopped';
                            
                            stopRecordingTimer();
                            currentRecordingId = '';
                            
                            showSuccess('录制已停止');
                        } else {
                            showError(result.error || '停止录制失败');
                        }
                    } catch (error) {
                        console.error('停止录制失败:', error);
                        showError('网络错误: ' + error.message);
                    }
                }
                
                // 显示录制预览
                function showRecordingPreview(blob, type) {
                    const previewDiv = document.getElementById('recordingPreview');
                    previewDiv.style.display = 'block';
                    
                    if (type === 'audio') {
                        previewDiv.innerHTML = '<h4>🎵 录音预览:</h4><audio controls></audio>';
                        const audio = previewDiv.querySelector('audio');
                        audio.src = URL.createObjectURL(blob);
                    } else {
                        previewDiv.innerHTML = '<h4>🎬 视频预览:</h4><video controls></video>';
                        const video = previewDiv.querySelector('video');
                        video.src = URL.createObjectURL(blob);
                    }
                }
                
                // 上传录制文件
                async function uploadRecording(blob, type) {
                    const formData = new FormData();
                    formData.append('file', blob, `recording_${Date.now()}.${type === 'audio' ? 'wav' : 'webm'}`);
                    
                    try {
                        const response = await fetch(`/upload/${type}`, {
                            method: 'POST',
                            body: formData
                        });
                        
                        const result = await response.json();
                        if (result.success) {
                            showSuccess('录制文件已保存');
                        } else {
                            showError('保存录制文件失败');
                        }
                    } catch (error) {
                        console.error('上传录制文件失败:', error);
                        showError('上传录制文件失败: ' + error.message);
                    }
                }
                
                // 获取活跃录制
                async function getActiveRecordings() {
                    try {
                        const response = await fetch('/active_recordings');
                        const result = await response.json();
                        
                        if (result.success) {
                            const recordings = result.recordings;
                            if (recordings.length > 0) {
                                let message = '当前活跃录制:\\n';
                                recordings.forEach(rec => {
                                    message += `- ${rec.type} 录制 (${rec.robot_id}): ${rec.duration.toFixed(1)}秒\\n`;
                                });
                                showInfo(message);
                            } else {
                                showInfo('当前没有活跃的录制');
                            }
                        } else {
                            showError('获取录制信息失败');
                        }
                    } catch (error) {
                        console.error('获取活跃录制失败:', error);
                        showError('网络错误: ' + error.message);
                    }
                }

                // 导出录制相关到全局，保证内联按钮可调用
                window.startRecording = startRecording;
                window.stopRecording = stopRecording;
                window.getActiveRecordings = getActiveRecordings;
                
                // 开始录制计时器
                function startRecordingTimer() {
                    recordingInterval = setInterval(() => {
                        const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
                        const minutes = Math.floor(elapsed / 60);
                        const seconds = elapsed % 60;
                        document.getElementById('recordingTime').textContent = 
                            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
                        
                        // 更新进度条
                        const progress = Math.min((elapsed / 300) * 100, 100); // 5分钟最大
                        document.getElementById('progressFill').style.width = progress + '%';
                    }, 1000);
                }
                
                // 停止录制计时器
                function stopRecordingTimer() {
                    if (recordingInterval) {
                        clearInterval(recordingInterval);
                        recordingInterval = null;
                    }
                    document.getElementById('recordingTime').textContent = '00:00';
                    document.getElementById('progressFill').style.width = '0%';
                    document.getElementById('progressContainer').style.display = 'none';
                }
                

                
                // 显示加载状态
                function showLoading(show) {
                    document.getElementById('loading').style.display = show ? 'block' : 'none';
                }
                
                // 显示错误信息
                function showError(message) {
                    console.error('错误:', message);
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error';
                    errorDiv.textContent = message;
                    
                    const mainContent = document.querySelector('.main-content');
                    mainContent.insertBefore(errorDiv, mainContent.firstChild);
                    
                    setTimeout(() => {
                        errorDiv.remove();
                    }, 5000);
                }
                
                // 显示成功信息
                function showSuccess(message) {
                    console.log('成功:', message);
                    const successDiv = document.createElement('div');
                    successDiv.className = 'success';
                    successDiv.textContent = message;
                    
                    const mainContent = document.querySelector('.main-content');
                    mainContent.insertBefore(successDiv, mainContent.firstChild);
                    
                    setTimeout(() => {
                        successDiv.remove();
                    }, 3000);
                }
                
                // 显示信息
                function showInfo(message) {
                    console.log('信息:', message);
                    const infoDiv = document.createElement('div');
                    infoDiv.className = 'info';
                    infoDiv.textContent = message;
                    
                    const mainContent = document.querySelector('.main-content');
                    mainContent.insertBefore(infoDiv, mainContent.firstChild);
                    
                    setTimeout(() => {
                        infoDiv.remove();
                    }, 5000);
                }
            </script>
            <script>
                // 全局错误捕获，便于快速定位前端无响应问题
                window.addEventListener('error', function (e) {
                    console.error('全局错误捕获:', e.message, e.filename, e.lineno, e.colno);
                    try {
                        const mainContent = document.querySelector('.main-content');
                        const err = document.createElement('div');
                        err.className = 'error';
                        err.textContent = '前端运行错误: ' + e.message;
                        mainContent.insertBefore(err, mainContent.firstChild);
                        setTimeout(() => err.remove(), 8000);
                    } catch (_) {}
                });
            </script>
        </body>
        </html>
        """
    
    def _get_recording_script(self) -> str:
        """Get the recording JavaScript code."""
        return """
        // 录制功能JavaScript代码
        class RecordingManager {
            constructor() {
                this.mediaRecorder = null;
                this.recordedChunks = [];
                this.isRecording = false;
                this.recordingType = null;
            }
            
            async startRecording(type) {
                try {
                    const constraints = type === 'audio' 
                        ? { audio: true }
                        : { audio: true, video: true };
                    
                    const stream = await navigator.mediaDevices.getUserMedia(constraints);
                    this.mediaRecorder = new MediaRecorder(stream);
                    this.recordingType = type;
                    
                    this.mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            this.recordedChunks.push(event.data);
                        }
                    };
                    
                    this.mediaRecorder.onstop = () => {
                        const blob = new Blob(this.recordedChunks, {
                            type: type === 'audio' ? 'audio/wav' : 'video/webm'
                        });
                        this.saveRecording(blob, type);
                    };
                    
                    this.mediaRecorder.start();
                    this.isRecording = true;
                    
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
                    this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
                }
            }
            
            async saveRecording(blob, type) {
                const formData = new FormData();
                formData.append('file', blob, `recording_${Date.now()}.${type === 'audio' ? 'wav' : 'webm'}`);
                formData.append('file_type', type);
                
                try {
                    const response = await fetch('/upload/' + type, {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    if (result.success) {
                        console.log('录制文件已保存:', result.file_path);
                    } else {
                        console.error('保存录制文件失败:', result.error);
                    }
                } catch (error) {
                    console.error('上传录制文件失败:', error);
                }
            }
        }
        
        // 创建全局录制管理器
        window.recordingManager = new RecordingManager();
        """
    
    def get_verify_page(self) -> str:
        """Get the verification page HTML."""
        return self.base_template
    
    def get_dashboard_page(self) -> str:
        """Get the dashboard page HTML."""
        return self.base_template
    
    def get_recording_script(self) -> str:
        """Get the recording JavaScript code."""
        return self.recording_script 

    # Minimal page for step-by-step isolation testing
    def get_min_verify_page(self) -> str:
        return """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <title>UI Smoke Test</title>
          <style>
            body{font-family:Arial,Helvetica,sans-serif;margin:0;background:#f6f7fb;color:#0f172a}
            .wrap{max-width:820px;margin:0 auto;padding:24px}
            .card{background:#fff;border-radius:12px;box-shadow:0 6px 20px rgba(2,6,23,.08);padding:18px;margin-bottom:16px}
            .btn{border:0;border-radius:10px;padding:10px 14px;background:#2563eb;color:#fff;font-weight:700;cursor:pointer}
            pre{white-space:pre-wrap;background:#0b1020;color:#e5e7eb;padding:12px;border-radius:8px}
          </style>
        </head>
        <body>
          <div class="wrap">
            <div class="card">
              <h2>✅ 页面最小化加载成功</h2>
              <p>默认信息：等待您的输入...</p>
            </div>
            <div class="card">
              <h3>健康检查</h3>
              <button class="btn" id="btnHealth">调用 /health</button>
              <pre id="out">尚未调用</pre>
            </div>
          </div>
          <script>
          (function(){
            var btn=document.getElementById('btnHealth');
            var out=document.getElementById('out');
            if(btn){
              btn.addEventListener('click', async function(){
                out.textContent='调用中...';
                try{
                  const r=await fetch('/health');
                  const t=await r.text();
                  out.textContent='状态: '+r.status+'\n\n'+t;
                }catch(e){
                  out.textContent='失败: '+(e&&e.message?e.message:String(e));
                }
              });
            }
          })();
          </script>
        </body>
        </html>
        """

    def get_plain_verify_page(self) -> str:
        return """
        <!doctype html>
        <html lang="zh-CN">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <title>Plain Verify</title>
        </head>
        <body>
          <h2>Plain Page</h2>
          <p>如果此页面无任何报错，说明错误来自脚本或扩展注入。</p>
          <p>下一步可逐步启用脚本验证具体环节。</p>
        </body>
        </html>
        """

    def get_ultra_min_verify_page(self) -> str:
        # 仅 ASCII 字符，无样式，最小脚本
        return """
        <!doctype html>
        <html>
        <head>
          <meta charset="utf-8">
          <title>Ultra Min Verify</title>
        </head>
        <body>
          <h3>Ultra Minimal Page</h3>
          <p>Default: waiting...</p>
          <button id="btn">Call /health</button>
          <pre id="out">idle</pre>
          <script>
          (function(){
            var b=document.getElementById('btn');
            var o=document.getElementById('out');
            if(!b||!o){ return; }
            b.addEventListener('click', function(){
              o.textContent='calling...';
              fetch('/health').then(function(r){
                return r.text().then(function(t){
                  o.textContent='status: '+r.status+'\n'+t;
                });
              }).catch(function(e){
                o.textContent='error: '+(e && e.message ? e.message : String(e));
              });
            });
          })();
          </script>
        </body>
        </html>
        """