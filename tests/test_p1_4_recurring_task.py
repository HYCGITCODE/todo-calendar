#!/usr/bin/env python3
"""
P1-4: 重复任务测试

测试重复任务的创建、管理和实例化功能
"""

import unittest
from datetime import date, timedelta
from sqlalchemy.orm import Session

from src.database.db_manager import init_database, get_session
from src.models.category import Category
from src.models.recurring_task import RecurringTask, RecurrenceType


class TestP1RecurringTask(unittest.TestCase):
    """P1-4: 重复任务测试"""
    
    def setUp(self):
        """每个测试前准备"""
        init_database()
        self.session = get_session().__enter__()
        self._create_test_data()
    
    def tearDown(self):
        """每个测试后清理"""
        self.session.close()
    
    def _create_test_data(self):
        """创建测试数据"""
        self.session.query(RecurringTask).delete()
        self.session.query(Category).delete()
        self.session.commit()
        
        # 创建分类
        cat1 = Category(name="Work", icon="💼", color="#3498db")
        cat2 = Category(name="Personal", icon="🏠", color="#27ae60")
        self.session.add_all([cat1, cat2])
        self.session.commit()
        
        self.work_category = cat1
        self.personal_category = cat2
    
    def test_create_daily_recurring_task(self):
        """P1-4-01: 测试创建每日重复任务"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="每日站会",
            description="团队每日例会",
            recurrence_type=RecurrenceType.DAILY,
            recurrence_interval=1,
            priority=2,
            category_id=self.work_category.id,
            start_date=today,
            is_active=True
        )
        
        self.session.add(recurring_task)
        self.session.commit()
        self.session.refresh(recurring_task)
        
        # 验证任务创建成功
        self.assertIsNotNone(recurring_task.id)
        self.assertEqual(recurring_task.title, "每日站会")
        self.assertEqual(recurring_task.recurrence_type, RecurrenceType.DAILY)
        self.assertEqual(recurring_task.recurrence_interval, 1)
        
        # 验证下次执行时间计算正确
        expected_next = recurring_task.get_next_occurrence(today)
        self.assertEqual(expected_next, today + timedelta(days=1))
        
        print("✅ 创建每日重复任务：PASS")
    
    def test_create_weekly_recurring_task(self):
        """P1-4-02: 测试创建每周重复任务"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="周报",
            description="每周工作总结",
            recurrence_type=RecurrenceType.WEEKLY,
            recurrence_interval=1,
            priority=2,
            category_id=self.work_category.id,
            start_date=today,
            is_active=True
        )
        
        self.session.add(recurring_task)
        self.session.commit()
        self.session.refresh(recurring_task)
        
        # 验证任务创建成功
        self.assertIsNotNone(recurring_task.id)
        self.assertEqual(recurring_task.title, "周报")
        self.assertEqual(recurring_task.recurrence_type, RecurrenceType.WEEKLY)
        
        # 验证下次执行时间计算正确 (使用 get_next_occurrence 方法)
        expected_next = recurring_task.get_next_occurrence(today)
        self.assertEqual(expected_next, today + timedelta(days=7))
        
        print("✅ 创建每周重复任务：PASS")
    
    def test_create_monthly_recurring_task(self):
        """P1-4-03: 测试创建每月重复任务"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="月度总结",
            description="每月工作总结",
            recurrence_type=RecurrenceType.MONTHLY,
            recurrence_interval=1,
            priority=1,
            category_id=self.work_category.id,
            start_date=today,
            is_active=True
        )
        
        self.session.add(recurring_task)
        self.session.commit()
        self.session.refresh(recurring_task)
        
        # 验证任务创建成功
        self.assertIsNotNone(recurring_task.id)
        self.assertEqual(recurring_task.title, "月度总结")
        self.assertEqual(recurring_task.recurrence_type, RecurrenceType.MONTHLY)
        
        # 验证下次执行时间计算正确
        expected_next = recurring_task.get_next_occurrence(today)
        self.assertIsNotNone(expected_next)
        self.assertGreater(expected_next, today)
        
        print("✅ 创建每月重复任务：PASS")
    
    def test_recurring_task标识(self):
        """P1-4-04: 测试重复任务标识"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="重复任务示例",
            recurrence_type=RecurrenceType.WEEKLY,
            recurrence_interval=1,
            priority=2,
            category_id=self.work_category.id,
            start_date=today,
            is_active=True
        )
        
        self.session.add(recurring_task)
        self.session.commit()
        
        # 验证重复规则可访问
        self.assertIsNotNone(recurring_task.recurrence_type)
        self.assertIsNotNone(recurring_task.recurrence_interval)
        
        # 验证 repr 包含重复信息
        repr_str = repr(recurring_task)
        self.assertIn("RecurringTask", repr_str)
        self.assertIn(str(recurring_task.id), repr_str)
        
        print("✅ 重复任务标识：PASS")
    
    def test_edit_recurring_task(self):
        """P1-4-05: 测试编辑重复任务"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="原始任务",
            recurrence_type=RecurrenceType.WEEKLY,
            recurrence_interval=1,
            priority=2,
            category_id=self.work_category.id,
            start_date=today,
            is_active=True
        )
        
        self.session.add(recurring_task)
        self.session.commit()
        
        # 编辑任务
        recurring_task.title = "修改后的任务"
        recurring_task.recurrence_interval = 2  # 改为每 2 周
        self.session.commit()
        self.session.refresh(recurring_task)
        
        # 验证修改成功
        self.assertEqual(recurring_task.title, "修改后的任务")
        self.assertEqual(recurring_task.recurrence_interval, 2)
        
        # 验证下次执行时间计算正确
        expected_next = recurring_task.get_next_occurrence(today)
        self.assertEqual(expected_next, today + timedelta(days=14))
        
        print("✅ 编辑重复任务：PASS")
    
    def test_delete_recurring_task(self):
        """P1-4-06: 测试删除重复任务"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="待删除任务",
            recurrence_type=RecurrenceType.DAILY,
            recurrence_interval=1,
            priority=2,
            category_id=self.work_category.id,
            start_date=today,
            is_active=True
        )
        
        self.session.add(recurring_task)
        self.session.commit()
        task_id = recurring_task.id
        
        # 删除任务
        self.session.delete(recurring_task)
        self.session.commit()
        
        # 验证删除成功
        deleted_task = self.session.query(RecurringTask).filter(
            RecurringTask.id == task_id
        ).first()
        self.assertIsNone(deleted_task)
        
        print("✅ 删除重复任务：PASS")
    
    def test_custom_interval_recurring_task(self):
        """P1-4-07: 测试自定义间隔重复任务"""
        today = date.today()
        
        # 创建每 2 周重复的任务
        recurring_task = RecurringTask(
            title="双周会议",
            recurrence_type=RecurrenceType.WEEKLY,
            recurrence_interval=2,
            priority=2,
            category_id=self.work_category.id,
            start_date=today,
            is_active=True
        )
        
        self.session.add(recurring_task)
        self.session.commit()
        self.session.refresh(recurring_task)
        
        # 验证下次执行时间计算正确
        expected_next = recurring_task.get_next_occurrence(today)
        self.assertEqual(expected_next, today + timedelta(days=14))
        
        print("✅ 自定义间隔重复任务：PASS")
    
    def test_get_next_occurrence_daily(self):
        """测试每日重复的下一次发生日期"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="每日任务",
            recurrence_type=RecurrenceType.DAILY,
            recurrence_interval=1,
            start_date=today
        )
        
        # 测试间隔 1 天
        next_date = recurring_task.get_next_occurrence(today)
        self.assertEqual(next_date, today + timedelta(days=1))
        
        # 测试间隔 3 天
        recurring_task.recurrence_interval = 3
        next_date = recurring_task.get_next_occurrence(today)
        self.assertEqual(next_date, today + timedelta(days=3))
        
        print("✅ 每日重复计算：PASS")
    
    def test_get_next_occurrence_weekly(self):
        """测试每周重复的下一次发生日期"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="每周任务",
            recurrence_type=RecurrenceType.WEEKLY,
            recurrence_interval=1,
            start_date=today
        )
        
        # 测试间隔 1 周
        next_date = recurring_task.get_next_occurrence(today)
        self.assertEqual(next_date, today + timedelta(weeks=1))
        
        # 测试间隔 2 周
        recurring_task.recurrence_interval = 2
        next_date = recurring_task.get_next_occurrence(today)
        self.assertEqual(next_date, today + timedelta(weeks=2))
        
        print("✅ 每周重复计算：PASS")
    
    def test_get_next_occurrence_monthly(self):
        """测试每月重复的下一次发生日期"""
        # 测试 1 月 31 日的情况
        jan_31 = date(2026, 1, 31)
        
        recurring_task = RecurringTask(
            title="每月任务",
            recurrence_type=RecurrenceType.MONTHLY,
            recurrence_interval=1,
            start_date=jan_31
        )
        
        # 1 月 31 日的下个月应该是 2 月 28 日 (或 29 日)
        next_date = recurring_task.get_next_occurrence(jan_31)
        self.assertEqual(next_date.month, 2)
        self.assertIn(next_date.day, [28, 29])
        
        print("✅ 每月重复计算：PASS")
    
    def test_get_next_occurrence_yearly(self):
        """测试每年重复的下一次发生日期"""
        today = date.today()
        
        recurring_task = RecurringTask(
            title="每年任务",
            recurrence_type=RecurrenceType.YEARLY,
            recurrence_interval=1,
            start_date=today
        )
        
        # 测试间隔 1 年
        next_date = recurring_task.get_next_occurrence(today)
        self.assertEqual(next_date.year, today.year + 1)
        self.assertEqual(next_date.month, today.month)
        self.assertEqual(next_date.day, today.day)
        
        print("✅ 每年重复计算：PASS")
    
    def test_recurring_task_defaults(self):
        """测试重复任务默认模板"""
        defaults = RecurringTask.get_defaults()
        
        # 验证有默认模板
        self.assertGreater(len(defaults), 0)
        
        # 验证包含每日、每周、每月模板
        types = [t['recurrence_type'] for t in defaults]
        self.assertIn(RecurrenceType.DAILY, types)
        self.assertIn(RecurrenceType.WEEKLY, types)
        self.assertIn(RecurrenceType.MONTHLY, types)
        
        print("✅ 重复任务默认模板：PASS")
    
    def test_recurring_task_active_status(self):
        """测试重复任务激活状态"""
        today = date.today()
        
        # 创建激活的重复任务
        active_task = RecurringTask(
            title="激活任务",
            recurrence_type=RecurrenceType.DAILY,
            start_date=today,
            is_active=True
        )
        
        # 创建停用的重复任务
        inactive_task = RecurringTask(
            title="停用任务",
            recurrence_type=RecurrenceType.DAILY,
            start_date=today,
            is_active=False
        )
        
        self.session.add_all([active_task, inactive_task])
        self.session.commit()
        
        # 验证状态
        self.assertTrue(active_task.is_active)
        self.assertFalse(inactive_task.is_active)
        
        print("✅ 重复任务激活状态：PASS")


if __name__ == '__main__':
    unittest.main(verbosity=2)
