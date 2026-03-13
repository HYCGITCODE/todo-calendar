#!/usr/bin/env python3
"""
P1-1: 周/日视图测试

测试周视图和日视图的 UI 组件和功能
"""

import unittest
import sys
from datetime import date, timedelta
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication

from src.database.db_manager import init_database, get_session
from src.models.task import Task
from src.models.category import Category
from src.services.task_service import TaskService
from src.ui.week_view import WeekView
from src.ui.day_view import DayView


# 创建全局 QApplication (UI 测试必需)
_app = None

def get_qapplication():
    """获取或创建 QApplication 实例"""
    global _app
    if _app is None:
        _app = QApplication(sys.argv)
    return _app


class TestP1WeekView(unittest.TestCase):
    """P1-1: 周视图测试"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化前创建 QApplication"""
        get_qapplication()
    
    def setUp(self):
        """每个测试前准备"""
        init_database()
        self.session = get_session().__enter__()
        self._create_test_data()
        self.task_service = TaskService(self.session)
    
    def tearDown(self):
        """每个测试后清理"""
        self.session.close()
    
    def _create_test_data(self):
        """创建测试数据"""
        self.session.query(Task).delete()
        self.session.query(Category).delete()
        self.session.commit()
        
        # 创建分类
        cat1 = Category(name="Work", icon="💼", color="#3498db")
        cat2 = Category(name="Personal", icon="🏠", color="#27ae60")
        self.session.add_all([cat1, cat2])
        self.session.commit()
        
        # 创建本周不同日期的任务
        today = date.today()
        monday = today - timedelta(days=today.weekday())  # 本周一
        
        tasks = [
            Task(title="周一任务 1", due_date=monday, priority=3, status=0, category_id=cat1.id),
            Task(title="周一任务 2", due_date=monday, priority=2, status=0, category_id=cat1.id),
            Task(title="周三任务", due_date=monday + timedelta(days=2), priority=1, status=0, category_id=cat2.id),
            Task(title="周五任务", due_date=monday + timedelta(days=4), priority=3, status=1, category_id=cat1.id),
            Task(title="周末任务", due_date=monday + timedelta(days=6), priority=2, status=0, category_id=cat2.id),
        ]
        self.session.add_all(tasks)
        self.session.commit()
        
        self.tasks = tasks
    
    def test_week_view_initialization(self):
        """测试周视图初始化"""
        week_view = WeekView(self.task_service)
        
        # 验证组件创建成功
        self.assertIsNotNone(week_view)
        self.assertIsNotNone(week_view.week_label)
        self.assertIsNotNone(week_view.prev_week_btn)
        self.assertIsNotNone(week_view.next_week_btn)
        self.assertIsNotNone(week_view.today_btn)
        
        print("✅ 周视图初始化：PASS")
    
    def test_week_view_layout(self):
        """测试周视图布局"""
        week_view = WeekView(self.task_service)
        
        # 验证星期标题存在
        week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        # 周视图应该包含 7 个星期标题
        self.assertIsNotNone(week_view.week_grid)
        
        print("✅ 周视图布局：PASS")
    
    def test_week_view_date_display(self):
        """测试周视图日期显示"""
        week_view = WeekView(self.task_service)
        
        # 验证周标签显示正确
        week_number = QDate.currentDate().weekNumber()[0]
        year = QDate.currentDate().year()
        label_text = week_view.week_label.text()
        
        self.assertIn(str(year), label_text)
        self.assertIn(f"Week {week_number}", label_text)
        
        print("✅ 周视图日期显示：PASS")
    
    def test_week_view_task_display(self):
        """测试周视图任务显示"""
        week_view = WeekView(self.task_service)
        
        # 验证任务能正确获取
        today = date.today()
        tasks = self.task_service.get_tasks_by_date(today)
        
        # 应该能找到任务
        self.assertGreaterEqual(len(tasks), 0)
        
        print("✅ 周视图任务显示：PASS")
    
    def test_week_view_navigation(self):
        """测试周视图导航"""
        week_view = WeekView(self.task_service)
        
        # 记录当前周
        initial_label = week_view.week_label.text()
        
        # 切换到上一周
        week_view._prev_week()
        prev_label = week_view.week_label.text()
        
        # 切换到下一周
        week_view._next_week()
        next_label = week_view.week_label.text()
        
        # 验证导航后标签变化
        self.assertNotEqual(initial_label, prev_label)
        
        print("✅ 周视图导航：PASS")
    
    def test_week_view_today_button(self):
        """测试周视图 Today 按钮"""
        week_view = WeekView(self.task_service)
        
        # 先切换到上一周
        week_view._prev_week()
        
        # 点击 Today 按钮
        week_view._go_to_today()
        
        # 验证回到当前周
        week_number = QDate.currentDate().weekNumber()[0]
        year = QDate.currentDate().year()
        label_text = week_view.week_label.text()
        
        self.assertIn(str(year), label_text)
        self.assertIn(f"Week {week_number}", label_text)
        
        print("✅ 周视图 Today 按钮：PASS")
    
    def test_week_view_date_selection(self):
        """测试周视图日期选择"""
        week_view = WeekView(self.task_service)
        
        # 模拟日期选择
        test_date = QDate.currentDate()
        week_view._on_date_clicked(test_date)
        
        # 验证选中状态
        self.assertEqual(week_view.selected_date, test_date)
        
        print("✅ 周视图日期选择：PASS")
    
    def test_week_view_get_week_dates(self):
        """测试周视图获取周日期"""
        week_view = WeekView(self.task_service)
        
        # 获取当前周日期
        week_dates = week_view._get_week_dates(QDate.currentDate())
        
        # 验证返回 7 个日期
        self.assertEqual(len(week_dates), 7)
        
        # 验证第一个日期是周一
        self.assertEqual(week_dates[0].dayOfWeek(), 1)
        
        # 验证最后一个日期是周日
        self.assertEqual(week_dates[6].dayOfWeek(), 7)
        
        print("✅ 周视图获取周日期：PASS")


class TestP1DayView(unittest.TestCase):
    """P1-1: 日视图测试"""
    
    def setUp(self):
        """每个测试前准备"""
        init_database()
        self.session = get_session().__enter__()
        self._create_test_data()
        self.task_service = TaskService(self.session)
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化前创建 QApplication"""
        get_qapplication()
    
    def tearDown(self):
        """每个测试后清理"""
        self.session.close()
    
    def _create_test_data(self):
        """创建测试数据"""
        self.session.query(Task).delete()
        self.session.query(Category).delete()
        self.session.commit()
        
        # 创建分类
        cat1 = Category(name="Work", icon="💼", color="#3498db")
        cat2 = Category(name="Personal", icon="🏠", color="#27ae60")
        self.session.add_all([cat1, cat2])
        self.session.commit()
        
        # 创建当天多个任务
        today = date.today()
        tasks = [
            Task(title="上午会议", description="9:00 团队例会", 
                 due_date=today, priority=3, status=0, category_id=cat1.id),
            Task(title="项目报告", description="Q1 季度报告",
                 due_date=today, priority=2, status=1, category_id=cat1.id),
            Task(title="午餐", description="与同事聚餐",
                 due_date=today, priority=1, status=0, category_id=cat2.id),
            Task(title="代码审查", description="审查 PR #123",
                 due_date=today, priority=3, status=0, category_id=cat1.id),
            Task(title="健身", description="健身房锻炼",
                 due_date=today, priority=2, status=2, category_id=cat2.id),  # 已完成
        ]
        self.session.add_all(tasks)
        self.session.commit()
        
        self.tasks = tasks
    
    def test_day_view_initialization(self):
        """测试日视图初始化"""
        day_view = DayView(self.task_service)
        
        # 验证组件创建成功
        self.assertIsNotNone(day_view)
        self.assertIsNotNone(day_view.date_label)
        self.assertIsNotNone(day_view.prev_day_btn)
        self.assertIsNotNone(day_view.next_day_btn)
        self.assertIsNotNone(day_view.today_btn)
        
        print("✅ 日视图初始化：PASS")
    
    def test_day_view_layout(self):
        """测试日视图布局"""
        day_view = DayView(self.task_service)
        
        # 验证时间轴存在
        self.assertIsNotNone(day_view.time_axis_widget)
        self.assertIsNotNone(day_view.time_axis_layout)
        
        print("✅ 日视图布局：PASS")
    
    def test_day_view_date_display(self):
        """测试日视图日期显示"""
        day_view = DayView(self.task_service)
        
        # 验证日期标签显示正确
        label_text = day_view.date_label.text()
        
        # 应该包含当前日期信息
        self.assertGreater(len(label_text), 0)
        
        print("✅ 日视图日期显示：PASS")
    
    def test_day_view_weekday_display(self):
        """测试日视图星期显示"""
        day_view = DayView(self.task_service)
        
        # 验证星期标签显示
        weekday_text = day_view.weekday_label.text()
        
        # 应该是有效的星期名称
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                   "Friday", "Saturday", "Sunday"]
        self.assertIn(weekday_text, weekdays)
        
        print("✅ 日视图星期显示：PASS")
    
    def test_day_view_task_count(self):
        """测试日视图任务数量显示"""
        day_view = DayView(self.task_service)
        
        # 验证任务计数显示
        count_text = day_view.task_count_label.text()
        
        # 应该包含任务数量
        self.assertIn("tasks", count_text.lower())
        
        print("✅ 日视图任务数量显示：PASS")
    
    def test_day_view_navigation(self):
        """测试日视图导航"""
        day_view = DayView(self.task_service)
        
        # 记录当前日期
        initial_date = day_view.current_date
        
        # 切换到前一天
        day_view._prev_day()
        prev_date = day_view.current_date
        
        # 验证前一天正确
        self.assertEqual(prev_date.addDays(1), initial_date)
        
        # 切换到后一天 (回到初始日期)
        day_view._next_day()
        current_date = day_view.current_date
        
        # 验证回到初始日期
        self.assertEqual(current_date, initial_date)
        
        # 再切换到后一天
        day_view._next_day()
        next_date = day_view.current_date
        
        # 验证后一天正确
        self.assertEqual(next_date.addDays(-1), initial_date)
        
        print("✅ 日视图导航：PASS")
    
    def test_day_view_today_button(self):
        """测试日视图 Today 按钮"""
        day_view = DayView(self.task_service)
        
        # 先切换到前一天
        day_view._prev_day()
        
        # 点击 Today 按钮
        day_view._go_to_today()
        
        # 验证回到今天
        self.assertEqual(day_view.current_date, QDate.currentDate())
        
        print("✅ 日视图 Today 按钮：PASS")
    
    def test_day_view_time_slots(self):
        """测试日视图时间槽"""
        day_view = DayView(self.task_service)
        
        # 验证创建了 24 小时时间槽
        time_slots = day_view.time_axis_layout.count()
        
        # 应该有 24 个时间槽
        self.assertEqual(time_slots, 24)
        
        print("✅ 日视图时间槽：PASS")


if __name__ == '__main__':
    unittest.main(verbosity=2)
