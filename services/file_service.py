"""File service for handling file uploads and management."""

import uuid
from pathlib import Path
from typing import Dict, Optional
from fastapi import UploadFile, HTTPException
from ai_core.intelligent_core import UserInput


class FileService:
    """Service for handling file operations."""
    
    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir
        self.upload_dir.mkdir(exist_ok=True)
    
    async def upload_file(self, file: UploadFile, file_type: str) -> Dict:
        """Upload a single file."""
        try:
            if not file.filename:
                raise HTTPException(status_code=400, detail="No filename provided")
            
            # 生成唯一文件名
            file_extension = Path(file.filename).suffix
            unique_filename = f"{file_type}_{uuid.uuid4().hex}{file_extension}"
            file_path = self.upload_dir / unique_filename
            
            # 保存文件
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            return {
                "success": True,
                "filename": unique_filename,
                "path": str(file_path),
                "size": len(content),
                "type": file_type
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    async def handle_file_uploads(
        self,
        audio_file: Optional[UploadFile] = None,
        image_file: Optional[UploadFile] = None,
        video_file: Optional[UploadFile] = None
    ) -> Dict[str, Optional[str]]:
        """Handle multiple file uploads and return file paths."""
        file_paths = {
            'audio': None,
            'image': None,
            'video': None
        }
        
        # 处理音频文件
        if audio_file:
            result = await self.upload_file(audio_file, "audio")
            file_paths['audio'] = result['path']
        
        # 处理图像文件
        if image_file:
            result = await self.upload_file(image_file, "image")
            file_paths['image'] = result['path']
        
        # 处理视频文件
        if video_file:
            result = await self.upload_file(video_file, "video")
            file_paths['video'] = result['path']
        
        return file_paths
    
    async def handle_multiple_files(self, files: list[UploadFile]) -> Dict[str, Optional[str]]:
        """Handle multiple files from a list and return file paths."""
        file_paths = {
            'audio': None,
            'image': None,
            'video': None
        }
        
        for file in files:
            if file.content_type:
                if file.content_type.startswith('audio/'):
                    result = await self.upload_file(file, "audio")
                    file_paths['audio'] = result['path']
                elif file.content_type.startswith('image/'):
                    result = await self.upload_file(file, "image")
                    file_paths['image'] = result['path']
                elif file.content_type.startswith('video/'):
                    result = await self.upload_file(file, "video")
                    file_paths['video'] = result['path']
        
        return file_paths
    
    def get_file_info(self, file_path: str) -> Dict:
        """Get information about a file."""
        path = Path(file_path)
        if not path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return {
            "filename": path.name,
            "size": path.stat().st_size,
            "created": path.stat().st_ctime,
            "modified": path.stat().st_mtime
        }
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False
    
    def list_files(self, file_type: Optional[str] = None) -> list:
        """List files in upload directory."""
        files = []
        for file_path in self.upload_dir.iterdir():
            if file_path.is_file():
                if file_type is None or file_path.name.startswith(file_type):
                    files.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "created": file_path.stat().st_ctime
                    })
        return files 