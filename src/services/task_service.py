"""
任务服务层 - 业务逻辑
"""

from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.models.task import Task
from src.models.category import Category


class TaskService:
    """任务服务类"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_task(self, title: str, due_date: date, 
                    description: str = "", priority: int = 1,
                    category_id: Optional[int] = None) -> Task:
        """创建新任务"""
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            category_id=category_id
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """获取单个任务"""
        return self.session.query(Task).filter(Task.id == task_id).first()
    
    def get_tasks_by_date(self, target_date: date) -> List[Task]:
        """获取指定日期的任务"""
        return self.session.query(Task).filter(
            Task.due_date == target_date
        ).order_by(Task.priority.desc(), Task.created_at).all()
    
    def get_tasks_by_date_range(self, start_date: date, end_date: date) -> List[Task]:
        """获取日期范围内的任务"""
        return self.session.query(Task).filter(
            and_(Task.due_date >= start_date, Task.due_date <= end_date)
        ).order_by(Task.due_date, Task.priority.desc()).all()
    
    def get_tasks_by_category(self, category_id: int) -> List[Task]:
        """获取指定分类的任务"""
        return self.session.query(Task).filter(
            Task.category_id == category_id
        ).order_by(Task.due_date).all()
    
    def get_pending_tasks(self) -> List[Task]:
        """获取所有待办任务"""
        return self.session.query(Task).filter(
            Task.status == 0
        ).order_by(Task.due_date, Task.priority.desc()).all()
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """更新任务"""
        task = self.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            self.session.commit()
            self.session.refresh(task)
        return task
    
    def mark_complete(self, task_id: int) -> Optional[Task]:
        """标记任务为完成"""
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            self.session.commit()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """删除任务"""
        task = self.get_task(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False
    
    def get_task_count_by_status(self) -> dict:
        """获取各状态任务数量"""
        total = self.session.query(Task).count()
        completed = self.session.query(Task).filter(Task.status == 2).count()
        pending = total - completed
        return {
            'total': total,
            'completed': completed,
            'pending': pending
        }
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """搜索任务"""
        return self.session.query(Task).filter(
            Task.title.contains(keyword) | Task.description.contains(keyword)
        ).order_by(Task.due_date).all()
