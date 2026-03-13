"""
重复任务数据模型
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, date
from enum import IntEnum

from src.models.base import Base


class RecurrenceType(IntEnum):
    """重复类型枚举"""
    DAILY = 1      # 每天
    WEEKLY = 2     # 每周
    MONTHLY = 3    # 每月
    YEARLY = 4     # 每年
    CUSTOM = 5     # 自定义 (每周特定几天)


class RecurringTask(Base):
    """重复任务模型"""
    __tablename__ = 'recurring_tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment='任务标题')
    description = Column(String(1000), comment='任务描述')
    
    # 重复规则
    recurrence_type = Column(Integer, default=1, comment='重复类型：1=每天，2=每周，3=每月，4=每年，5=自定义')
    recurrence_interval = Column(Integer, default=1, comment='重复间隔 (如：每 2 周)')
    recurrence_days = Column(String(20), comment='自定义重复日 (如：1,3,5 表示周一三五)')
    
    # 任务属性
    priority = Column(Integer, default=1, comment='优先级：1=低，2=中，3=高')
    category_id = Column(Integer, ForeignKey('categories.id'), comment='分类 ID')
    
    # 时间设置
    start_date = Column(Date, nullable=False, comment='开始日期')
    end_date = Column(Date, comment='结束日期 (可选)')
    
    # 实例化任务
    last_generated_date = Column(Date, comment='最后生成实例的日期')
    next_due_date = Column(Date, comment='下次到期日期')
    
    # 状态
    is_active = Column(Boolean, default=True, comment='是否激活')
    created_at = Column(String, default=datetime.now, comment='创建时间')
    updated_at = Column(String, default=datetime.now, comment='更新时间')
    
    def __repr__(self):
        return f"<RecurringTask(id={self.id}, title='{self.title}', type={self.recurrence_type})>"
    
    def get_next_occurrence(self, from_date: date = None) -> date:
        """计算下次发生日期"""
        from datetime import timedelta
        import calendar
        
        if from_date is None:
            from_date = date.today()
        
        if self.recurrence_type == RecurrenceType.DAILY:
            return from_date + timedelta(days=self.recurrence_interval)
        elif self.recurrence_type == RecurrenceType.WEEKLY:
            return from_date + timedelta(weeks=self.recurrence_interval)
        elif self.recurrence_type == RecurrenceType.MONTHLY:
            months = self.recurrence_interval
            month = from_date.month - 1 + months
            year = from_date.year + month // 12
            month = month % 12 + 1
            day = min(from_date.day, calendar.monthrange(year, month)[1])
            return date(year, month, day)
        elif self.recurrence_type == RecurrenceType.YEARLY:
            years = self.recurrence_interval
            try:
                return from_date.replace(year=from_date.year + years)
            except ValueError:
                return from_date.replace(year=from_date.year + years, day=28)
        elif self.recurrence_type == RecurrenceType.CUSTOM:
            if self.recurrence_days:
                days = [int(d) for d in self.recurrence_days.split(',')]
                current_weekday = from_date.weekday()
                for day_offset in range(1, 8):
                    target_weekday = (current_weekday + day_offset) % 7
                    if target_weekday in days:
                        return from_date + timedelta(days=day_offset)
            return from_date + timedelta(weeks=1)
        return from_date + timedelta(days=1)
    
    @classmethod
    def get_defaults(cls):
        """返回一些默认重复任务模板"""
        return [
            {'title': '每日站会', 'recurrence_type': RecurrenceType.DAILY, 'recurrence_interval': 1, 'priority': 2, 'start_date': date.today()},
            {'title': '周报', 'recurrence_type': RecurrenceType.WEEKLY, 'recurrence_interval': 1, 'priority': 2, 'start_date': date.today()},
            {'title': '月度总结', 'recurrence_type': RecurrenceType.MONTHLY, 'recurrence_interval': 1, 'priority': 1, 'start_date': date.today()}
        ]
