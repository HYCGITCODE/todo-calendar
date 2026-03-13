"""
提醒数据模型
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from src.models.base import Base


class Reminder(Base):
    """提醒模型 - 用于任务到期提醒"""
    __tablename__ = 'reminders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False, comment='关联任务 ID')
    
    # 提醒时间设置
    remind_at = Column(DateTime, nullable=False, comment='提醒时间')
    remind_before_minutes = Column(Integer, default=0, comment='提前提醒分钟数')
    
    # 状态
    is_active = Column(Boolean, default=True, comment='是否激活')
    triggered_at = Column(DateTime, comment='实际触发时间')
    
    # 审计字段
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关系
    task = relationship("Task", back_populates="reminders")
    
    def __repr__(self):
        return f"<Reminder(id={self.id}, task_id={self.task_id}, remind_at={self.remind_at})>"
    
    def is_triggered(self) -> bool:
        """检查提醒是否已触发"""
        return self.triggered_at is not None
    
    def is_due(self) -> bool:
        """检查提醒是否到期"""
        if not self.is_active:
            return False
        return datetime.now() >= self.remind_at
    
    def mark_triggered(self):
        """标记提醒已触发"""
        self.triggered_at = datetime.now()
        self.is_active = False
    
    @classmethod
    def create_for_task(cls, task_id: int, remind_at: datetime, 
                       remind_before_minutes: int = 0) -> 'Reminder':
        """
        为任务创建提醒
        
        Args:
            task_id: 任务 ID
            remind_at: 提醒时间
            remind_before_minutes: 提前提醒分钟数
            
        Returns:
            Reminder 实例
        """
        return cls(
            task_id=task_id,
            remind_at=remind_at,
            remind_before_minutes=remind_before_minutes
        )
