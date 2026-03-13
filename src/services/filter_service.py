"""
过滤服务 - 任务过滤功能
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from src.models.task import Task


class FilterService:
    """任务过滤服务"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def filter_by_category(
        self, 
        category_id: Optional[int],
        tasks: List[Task] = None
    ) -> List[Task]:
        """
        按分类过滤任务
        
        Args:
            category_id: 分类 ID (None 表示全部)
            tasks: 可选的任务列表 (不提供则查询全部)
            
        Returns:
            过滤后的任务列表
        """
        if tasks is None:
            if category_id is None:
                return self.session.query(Task).order_by(Task.due_date).all()
            else:
                return self.session.query(Task).filter(
                    Task.category_id == category_id
                ).order_by(Task.due_date).all()
        
        if category_id is None:
            return tasks
        
        return [t for t in tasks if t.category_id == category_id]
    
    def filter_by_priority(
        self,
        priority: Optional[int],
        tasks: List[Task] = None
    ) -> List[Task]:
        """
        按优先级过滤任务
        
        Args:
            priority: 优先级 (None 表示全部)
            tasks: 可选的任务列表
            
        Returns:
            过滤后的任务列表
        """
        if tasks is None:
            if priority is None:
                return self.session.query(Task).order_by(Task.due_date).all()
            else:
                return self.session.query(Task).filter(
                    Task.priority == priority
                ).order_by(Task.due_date).all()
        
        if priority is None:
            return tasks
        
        return [t for t in tasks if t.priority == priority]
    
    def filter_by_status(
        self,
        status: Optional[int],
        tasks: List[Task] = None
    ) -> List[Task]:
        """
        按状态过滤任务
        
        Args:
            status: 状态 (None 表示全部)
            tasks: 可选的任务列表
            
        Returns:
            过滤后的任务列表
        """
        if tasks is None:
            if status is None:
                return self.session.query(Task).order_by(Task.due_date).all()
            else:
                return self.session.query(Task).filter(
                    Task.status == status
                ).order_by(Task.due_date).all()
        
        if status is None:
            return tasks
        
        return [t for t in tasks if t.status == status]
    
    def filter_by_date_range(
        self,
        start_date: date,
        end_date: date,
        tasks: List[Task] = None
    ) -> List[Task]:
        """
        按日期范围过滤任务
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            tasks: 可选的任务列表
            
        Returns:
            过滤后的任务列表
        """
        if tasks is None:
            return self.session.query(Task).filter(
                Task.due_date >= start_date,
                Task.due_date <= end_date
            ).order_by(Task.due_date).all()
        
        return [t for t in tasks if start_date <= t.due_date <= end_date]
    
    def filter_overdue(self, tasks: List[Task] = None) -> List[Task]:
        """
        过滤逾期任务
        
        Args:
            tasks: 可选的任务列表
            
        Returns:
            逾期任务列表
        """
        today = date.today()
        
        if tasks is None:
            return self.session.query(Task).filter(
                Task.due_date < today,
                Task.status != 2  # 未完成
            ).order_by(Task.due_date).all()
        
        return [t for t in tasks if t.due_date < today and t.status != 2]
    
    def filter_today(self, tasks: List[Task] = None) -> List[Task]:
        """
        过滤今日任务
        
        Args:
            tasks: 可选的任务列表
            
        Returns:
            今日任务列表
        """
        today = date.today()
        
        if tasks is None:
            return self.session.query(Task).filter(
                Task.due_date == today
            ).order_by(Task.priority.desc(), Task.created_at).all()
        
        return [t for t in tasks if t.due_date == today]
    
    def filter_this_week(self, tasks: List[Task] = None) -> List[Task]:
        """
        过滤本周任务
        
        Args:
            tasks: 可选的任务列表
            
        Returns:
            本周任务列表
        """
        from datetime import timedelta
        
        today = date.today()
        # 本周一
        start_of_week = today - timedelta(days=today.weekday())
        # 本周日
        end_of_week = start_of_week + timedelta(days=6)
        
        return self.filter_by_date_range(start_of_week, end_of_week, tasks)
    
    def filter_this_month(self, tasks: List[Task] = None) -> List[Task]:
        """
        过滤本月任务
        
        Args:
            tasks: 可选的任务列表
            
        Returns:
            本月任务列表
        """
        today = date.today()
        start_of_month = today.replace(day=1)
        
        # 计算月末
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        return self.filter_by_date_range(start_of_month, end_of_month, tasks)
    
    def apply_multiple_filters(
        self,
        category_id: Optional[int] = None,
        priority: Optional[int] = None,
        status: Optional[int] = None,
        show_overdue_only: bool = False
    ) -> List[Task]:
        """
        应用多个过滤条件
        
        Args:
            category_id: 分类 ID
            priority: 优先级
            status: 状态
            show_overdue_only: 是否只显示逾期任务
            
        Returns:
            过滤后的任务列表
        """
        # 先获取基础任务列表
        if show_overdue_only:
            tasks = self.filter_overdue()
        else:
            tasks = None
        
        # 依次应用过滤
        tasks = self.filter_by_category(category_id, tasks)
        tasks = self.filter_by_priority(priority, tasks)
        tasks = self.filter_by_status(status, tasks)
        
        return tasks
