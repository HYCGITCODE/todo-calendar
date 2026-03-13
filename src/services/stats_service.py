"""
统计服务 - 任务数据统计功能
"""

from datetime import datetime, date, timedelta
from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.task import Task
from src.models.category import Category


class StatsService:
    """任务统计服务"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_basic_stats(self) -> dict:
        """
        获取基础统计数据
        
        Returns:
            包含基础统计的字典
        """
        total = self.session.query(Task).count()
        completed = self.session.query(Task).filter(Task.status == 2).count()
        pending = total - completed
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': round(completion_rate, 1)
        }
    
    def get_stats_by_priority(self) -> dict:
        """
        按优先级统计
        
        Returns:
            各优先级的任务数量
        """
        stats = {}
        for priority in [1, 2, 3]:
            count = self.session.query(Task).filter(Task.priority == priority).count()
            completed = self.session.query(Task).filter(
                Task.priority == priority,
                Task.status == 2
            ).count()
            stats[priority] = {
                'total': count,
                'completed': completed,
                'pending': count - completed
            }
        return stats
    
    def get_stats_by_category(self) -> List[dict]:
        """
        按分类统计
        
        Returns:
            各分类的统计数据列表
        """
        categories = self.session.query(Category).all()
        stats = []
        
        for cat in categories:
            total = self.session.query(Task).filter(Task.category_id == cat.id).count()
            completed = self.session.query(Task).filter(
                Task.category_id == cat.id,
                Task.status == 2
            ).count()
            
            stats.append({
                'category_id': cat.id,
                'category_name': cat.name,
                'category_icon': cat.icon,
                'category_color': cat.color,
                'total': total,
                'completed': completed,
                'pending': total - completed
            })
        
        # 按任务数量排序
        stats.sort(key=lambda x: x['total'], reverse=True)
        return stats
    
    def get_stats_by_date_range(self, start_date: date, end_date: date) -> dict:
        """
        按日期范围统计
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            日期范围内的统计数据
        """
        total = self.session.query(Task).filter(
            Task.due_date >= start_date,
            Task.due_date <= end_date
        ).count()
        
        completed = self.session.query(Task).filter(
            Task.due_date >= start_date,
            Task.due_date <= end_date,
            Task.status == 2
        ).count()
        
        return {
            'total': total,
            'completed': completed,
            'pending': total - completed,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
        }
    
    def get_daily_stats(self, target_date: date) -> dict:
        """
        获取单日统计
        
        Args:
            target_date: 目标日期
            
        Returns:
            单日统计数据
        """
        return self.get_stats_by_date_range(target_date, target_date)
    
    def get_weekly_stats(self, target_date: date = None) -> dict:
        """
        获取周统计
        
        Args:
            target_date: 目标日期 (默认今天)
            
        Returns:
            周统计数据
        """
        if target_date is None:
            target_date = date.today()
        
        # 本周一
        start_of_week = target_date - timedelta(days=target_date.weekday())
        # 本周日
        end_of_week = start_of_week + timedelta(days=6)
        
        return self.get_stats_by_date_range(start_of_week, end_of_week)
    
    def get_monthly_stats(self, target_date: date = None) -> dict:
        """
        获取月统计
        
        Args:
            target_date: 目标日期 (默认今天)
            
        Returns:
            月统计数据
        """
        if target_date is None:
            target_date = date.today()
        
        start_of_month = target_date.replace(day=1)
        
        # 计算月末
        if target_date.month == 12:
            end_of_month = target_date.replace(year=target_date.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = target_date.replace(month=target_date.month + 1, day=1) - timedelta(days=1)
        
        return self.get_stats_by_date_range(start_of_month, end_of_month)
    
    def get_completion_trend(self, days: int = 7) -> List[dict]:
        """
        获取完成趋势
        
        Args:
            days: 统计天数
            
        Returns:
            每日完成数量的列表
        """
        today = date.today()
        trend = []
        
        for i in range(days - 1, -1, -1):
            day = today - timedelta(days=i)
            completed = self.session.query(Task).filter(
                func.date(Task.completed_at) == day,
                Task.status == 2
            ).count()
            
            total = self.session.query(Task).filter(
                Task.due_date == day
            ).count()
            
            trend.append({
                'date': day,
                'completed': completed,
                'total': total,
                'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
            })
        
        return trend
    
    def get_productivity_score(self) -> int:
        """
        计算生产力得分
        
        算法:
        - 基础分：完成的任务数 * 10
        - 高优先级奖励：完成的高优先级任务 * 5
        - 逾期惩罚：逾期任务 * -3
        - 完成率奖励：完成率 * 20
        
        Returns:
            生产力得分 (0-100)
        """
        stats = self.get_basic_stats()
        priority_stats = self.get_stats_by_priority()
        overdue_count = self.session.query(Task).filter(
            Task.due_date < date.today(),
            Task.status != 2
        ).count()
        
        # 基础分
        score = stats['completed'] * 10
        
        # 高优先级奖励
        high_priority_completed = priority_stats.get(3, {}).get('completed', 0)
        score += high_priority_completed * 5
        
        # 逾期惩罚
        score -= overdue_count * 3
        
        # 完成率奖励
        score += stats['completion_rate'] * 0.2
        
        # 限制在 0-100 范围
        return max(0, min(100, int(score)))
    
    def get_full_report(self) -> dict:
        """
        获取完整统计报告
        
        Returns:
            包含所有统计数据的报告
        """
        return {
            'basic': self.get_basic_stats(),
            'by_priority': self.get_stats_by_priority(),
            'by_category': self.get_stats_by_category(),
            'weekly': self.get_weekly_stats(),
            'monthly': self.get_monthly_stats(),
            'trend': self.get_completion_trend(),
            'productivity_score': self.get_productivity_score(),
            'generated_at': datetime.now()
        }
