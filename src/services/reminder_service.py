"""
提醒服务 - 任务到期提醒功能
"""

from datetime import datetime, date, timedelta
from typing import List, Tuple
from sqlalchemy.orm import Session

from src.models.task import Task


class ReminderService:
    """任务提醒服务"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_due_today(self) -> List[Task]:
        """
        获取今天到期的任务
        
        Returns:
            今天到期的任务列表
        """
        today = date.today()
        return self.session.query(Task).filter(
            Task.due_date == today,
            Task.status != 2  # 未完成
        ).order_by(Task.priority.desc()).all()
    
    def get_due_tomorrow(self) -> List[Task]:
        """
        获取明天到期的任务
        
        Returns:
            明天到期的任务列表
        """
        tomorrow = date.today() + timedelta(days=1)
        return self.session.query(Task).filter(
            Task.due_date == tomorrow,
            Task.status != 2
        ).order_by(Task.priority.desc()).all()
    
    def get_due_this_week(self) -> List[Task]:
        """
        获取本周到期的任务
        
        Returns:
            本周到期的任务列表
        """
        today = date.today()
        # 本周一
        start_of_week = today - timedelta(days=today.weekday())
        # 本周日
        end_of_week = start_of_week + timedelta(days=6)
        
        return self.session.query(Task).filter(
            Task.due_date >= start_of_week,
            Task.due_date <= end_of_week,
            Task.status != 2
        ).order_by(Task.due_date, Task.priority.desc()).all()
    
    def get_overdue(self) -> List[Task]:
        """
        获取逾期任务
        
        Returns:
            逾期任务列表
        """
        today = date.today()
        return self.session.query(Task).filter(
            Task.due_date < today,
            Task.status != 2
        ).order_by(Task.due_date).all()
    
    def get_upcoming(self, days: int = 7) -> List[Task]:
        """
        获取即将到来的任务
        
        Args:
            days: 未来多少天
            
        Returns:
            即将到来的任务列表
        """
        today = date.today()
        end_date = today + timedelta(days=days)
        
        return self.session.query(Task).filter(
            Task.due_date >= today,
            Task.due_date <= end_date,
            Task.status != 2
        ).order_by(Task.due_date, Task.priority.desc()).all()
    
    def get_reminder_summary(self) -> dict:
        """
        获取提醒摘要
        
        Returns:
            包含各类提醒数量的字典
        """
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        overdue_count = self.session.query(Task).filter(
            Task.due_date < today,
            Task.status != 2
        ).count()
        
        due_today_count = self.session.query(Task).filter(
            Task.due_date == today,
            Task.status != 2
        ).count()
        
        due_tomorrow_count = self.session.query(Task).filter(
            Task.due_date == tomorrow,
            Task.status != 2
        ).count()
        
        return {
            'overdue': overdue_count,
            'due_today': due_today_count,
            'due_tomorrow': due_tomorrow_count,
            'total_pending': self.session.query(Task).filter(
                Task.status != 2
            ).count()
        }
    
    def check_task_due(self, task: Task) -> Tuple[bool, str]:
        """
        检查单个任务的到期状态
        
        Args:
            task: 任务对象
            
        Returns:
            (是否需要提醒，提醒消息)
        """
        if task.status == 2:  # 已完成
            return False, ""
        
        today = date.today()
        days_until_due = (task.due_date - today).days
        
        if days_until_due < 0:
            return True, f"⚠️ 任务已逾期 {abs(days_until_due)} 天：{task.title}"
        elif days_until_due == 0:
            return True, f"⏰ 任务今天到期：{task.title}"
        elif days_until_due == 1:
            return True, f"📅 任务明天到期：{task.title}"
        elif days_until_due <= 3:
            return True, f"📌 任务 {days_until_due} 天后到期：{task.title}"
        
        return False, ""
    
    def get_all_reminders(self) -> List[Tuple[Task, str]]:
        """
        获取所有需要提醒的任务
        
        Returns:
            (任务，提醒消息) 的列表
        """
        pending_tasks = self.session.query(Task).filter(
            Task.status != 2
        ).all()
        
        reminders = []
        for task in pending_tasks:
            needs_reminder, message = self.check_task_due(task)
            if needs_reminder:
                reminders.append((task, message))
        
        # 按优先级排序 (逾期 > 今天 > 明天 > 未来)
        reminders.sort(key=lambda x: (
            x[0].due_date,
            -x[0].priority  # 高优先级优先
        ))
        
        return reminders
    
    def generate_daily_reminder_message(self) -> str:
        """
        生成每日提醒消息
        
        Returns:
            格式化的提醒消息
        """
        summary = self.get_reminder_summary()
        lines = []
        
        # 逾期任务
        if summary['overdue'] > 0:
            overdue_tasks = self.get_overdue()
            lines.append(f"⚠️ **逾期任务**: {summary['overdue']} 个")
            for task in overdue_tasks[:3]:  # 只显示前 3 个
                lines.append(f"   - {task.title}")
            if summary['overdue'] > 3:
                lines.append(f"   ... 还有 {summary['overdue'] - 3} 个")
            lines.append("")
        
        # 今天到期
        if summary['due_today'] > 0:
            due_today = self.get_due_today()
            lines.append(f"⏰ **今天到期**: {summary['due_today']} 个")
            for task in due_today:
                priority_icon = {1: "🔵", 2: "🟡", 3: "🔴"}
                lines.append(f"   {priority_icon.get(task.priority, '🔵')} {task.title}")
            lines.append("")
        
        # 明天到期
        if summary['due_tomorrow'] > 0:
            lines.append(f"📅 **明天到期**: {summary['due_tomorrow']} 个")
            lines.append("")
        
        # 总结
        lines.append(f"📊 **待办总计**: {summary['total_pending']} 个")
        
        return "\n".join(lines)
