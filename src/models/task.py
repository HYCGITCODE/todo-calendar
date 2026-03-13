"""
任务数据模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from src.models.base import Base


class Task(Base):
    """任务模型"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment='任务标题')
    description = Column(String(1000), comment='任务描述')
    due_date = Column(Date, nullable=False, comment='截止日期')
    priority = Column(Integer, default=1, comment='优先级：1=低，2=中，3=高')
    status = Column(Integer, default=0, comment='状态：0=待办，1=进行中，2=已完成')
    category_id = Column(Integer, ForeignKey('categories.id'), comment='分类 ID')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    completed_at = Column(DateTime, comment='完成时间')
    
    category = relationship("Category", back_populates="tasks")
    reminders = relationship("Reminder", back_populates="task", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status})>"
    
    def mark_complete(self):
        """标记任务为完成"""
        self.status = 2
        self.completed_at = datetime.now()
    
    def is_overdue(self):
        """检查任务是否逾期"""
        from datetime import date
        return self.status != 2 and self.due_date < date.today()
