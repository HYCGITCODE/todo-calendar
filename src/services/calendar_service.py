"""
日历服务层 - 日历视图逻辑
"""

from datetime import date, timedelta
from calendar import monthrange
from typing import List, Tuple


class CalendarService:
    """日历服务类"""
    
    @staticmethod
    def get_month_days(year: int, month: int) -> List[date]:
        """获取月份中的所有日期"""
        days_in_month = monthrange(year, month)[1]
        return [date(year, month, day) for day in range(1, days_in_month + 1)]
    
    @staticmethod
    def get_calendar_grid(year: int, month: int) -> List[List[Tuple[date, bool]]]:
        """
        获取日历网格数据 (6 行 x7 列)
        返回：[(日期，是否当月)] 的二维数组
        """
        # 获取当月第一天是周几 (0=周一，6=周日)
        first_day = date(year, month, 1)
        start_weekday = first_day.weekday()
        
        # 获取当月天数
        days_in_month = monthrange(year, month)[1]
        
        # 计算需要显示的前一个月天数
        days_from_prev = start_weekday
        
        # 构建网格 (6 行 x7 列 = 42 个单元格)
        grid = []
        current_row = []
        
        # 添加前一个月的日期
        prev_month = 12 if month == 1 else month - 1
        prev_year = year - 1 if month == 1 else year
        prev_month_days = monthrange(prev_year, prev_month)[1]
        
        for day in range(prev_month_days - days_from_prev + 1, prev_month_days + 1):
            current_row.append((date(prev_year, prev_month, day), False))
        
        # 添加当月日期
        for day in range(1, days_in_month + 1):
            current_row.append((date(year, month, day), True))
            
            if len(current_row) == 7:
                grid.append(current_row)
                current_row = []
        
        # 添加后一个月的日期 (填满 42 格)
        next_month = 1 if month == 12 else month + 1
        next_year = year + 1 if month == 12 else year
        remaining_cells = 42 - len(grid) * 7 - len(current_row)
        
        for day in range(1, remaining_cells + 1):
            current_row.append((date(next_year, next_month, day), False))
        
        if current_row:
            grid.append(current_row)
        
        return grid
    
    @staticmethod
    def get_week_dates(target_date: date) -> List[date]:
        """获取指定日期所在周的日期列表"""
        # 找到周一
        monday = target_date - timedelta(days=target_date.weekday())
        return [monday + timedelta(days=i) for i in range(7)]
    
    @staticmethod
    def is_today(check_date: date) -> bool:
        """检查是否是今天"""
        return check_date == date.today()
    
    @staticmethod
    def is_weekend(check_date: date) -> bool:
        """检查是否是周末"""
        return check_date.weekday() >= 5
    
    @staticmethod
    def get_month_name(month: int) -> str:
        """获取月份名称"""
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        return months[month - 1]
    
    @staticmethod
    def get_month_name_zh(month: int) -> str:
        """获取月份中文名称"""
        return f"{month}月"
    
    @staticmethod
    def navigate_month(year: int, month: int, direction: int) -> Tuple[int, int]:
        """
        导航到上/下个月
        direction: -1=上月，1=下月
        返回：(year, month)
        """
        new_month = month + direction
        new_year = year
        
        if new_month < 1:
            new_month = 12
            new_year -= 1
        elif new_month > 12:
            new_month = 1
            new_year += 1
        
        return new_year, new_month
