"""
搜索服务 - 任务搜索功能
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.models.task import Task


class SearchService:
    """任务搜索服务"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def search_by_keyword(self, keyword: str) -> List[Task]:
        """
        按关键词搜索任务
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的任务列表
        """
        if not keyword:
            return []
        
        return self.session.query(Task).filter(
            or_(
                Task.title.contains(keyword),
                Task.description.contains(keyword)
            )
        ).order_by(Task.due_date.desc()).all()
    
    def search_by_category(self, category_id: int) -> List[Task]:
        """
        按分类搜索任务
        
        Args:
            category_id: 分类 ID
            
        Returns:
            该分类下的任务列表
        """
        return self.session.query(Task).filter(
            Task.category_id == category_id
        ).order_by(Task.due_date).all()
    
    def search_by_priority(self, priority: int) -> List[Task]:
        """
        按优先级搜索任务
        
        Args:
            priority: 优先级 (1=低，2=中，3=高)
            
        Returns:
            该优先级的任务列表
        """
        return self.session.query(Task).filter(
            Task.priority == priority
        ).order_by(Task.due_date).all()
    
    def search_by_status(self, status: int) -> List[Task]:
        """
        按状态搜索任务
        
        Args:
            status: 状态 (0=待办，1=进行中，2=已完成)
            
        Returns:
            该状态的任务列表
        """
        return self.session.query(Task).filter(
            Task.status == status
        ).order_by(Task.due_date).all()
    
    def advanced_search(
        self,
        keyword: str = None,
        category_id: int = None,
        priority: int = None,
        status: int = None,
        start_date=None,
        end_date=None
    ) -> List[Task]:
        """
        高级搜索 - 支持多条件组合
        
        Args:
            keyword: 关键词
            category_id: 分类 ID
            priority: 优先级
            status: 状态
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            匹配的任务列表
        """
        query = self.session.query(Task)
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                or_(
                    Task.title.contains(keyword),
                    Task.description.contains(keyword)
                )
            )
        
        # 分类过滤
        if category_id:
            query = query.filter(Task.category_id == category_id)
        
        # 优先级过滤
        if priority:
            query = query.filter(Task.priority == priority)
        
        # 状态过滤
        if status is not None:
            query = query.filter(Task.status == status)
        
        # 日期范围过滤
        if start_date:
            query = query.filter(Task.due_date >= start_date)
        if end_date:
            query = query.filter(Task.due_date <= end_date)
        
        return query.order_by(Task.due_date, Task.priority.desc()).all()
