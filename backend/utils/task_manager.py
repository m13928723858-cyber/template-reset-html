from typing import Dict, Any, Optional
from datetime import datetime

class TaskManager:
    """任务管理器：管理处理任务的状态"""
    
    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
    
    def create_task(self, task_id: str, file_path: str) -> Dict[str, Any]:
        """创建新任务"""
        task = {
            "task_id": task_id,
            "status": "uploaded",
            "file_path": file_path,
            "created_at": datetime.now().isoformat(),
            "progress": {
                "stage": "uploaded",
                "percentage": 0,
                "message": "文件已上传"
            }
        }
        self.tasks[task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务信息"""
        return self.tasks.get(task_id)
    
    def update_task(self, task_id: str, updates: Dict[str, Any]):
        """更新任务信息"""
        if task_id in self.tasks:
            self.tasks[task_id].update(updates)
            self.tasks[task_id]["updated_at"] = datetime.now().isoformat()
    
    def delete_task(self, task_id: str):
        """删除任务"""
        if task_id in self.tasks:
            del self.tasks[task_id]
    
    def list_tasks(self) -> Dict[str, Dict[str, Any]]:
        """列出所有任务"""
        return self.tasks
