"""
Phase 2 P1 功能测试
测试所有 P1 增强功能
"""

import unittest
from datetime import date, timedelta
from sqlalchemy.orm import Session

from src.database.db_manager import get_session, init_database, Base, engine
from src.models.task import Task
from src.models.category import Category
from src.services.search_service import SearchService
from src.services.filter_service import FilterService
from src.services.reminder_service import ReminderService
from src.services.stats_service import StatsService


class TestP1Features(unittest.TestCase):
    """P1 功能测试类"""
    
    @classmethod
    def setUpClass(cls):
        """测试前初始化"""
        init_database()
        cls.session = get_session().__enter__()
        
        # 清理旧数据
        cls.session.query(Task).delete()
        cls.session.query(Category).delete()
        cls.session.commit()
        
        # 创建测试数据
        cls._create_test_data()
    
    @classmethod
    def tearDownClass(cls):
        """测试后清理"""
        cls.session.close()
    
    @classmethod
    def _create_test_data(cls):
        """创建测试数据"""
        # 创建分类
        cat1 = Category(name="Work", icon="💼", color="#3498db")
        cat2 = Category(name="Personal", icon="🏠", color="#27ae60")
        cls.session.add_all([cat1, cat2])
        cls.session.commit()
        
        # 创建任务
        today = date.today()
        tasks = [
            Task(title="Complete project report", description="Q1 report", 
                 due_date=today, priority=3, status=0, category_id=cat1.id),
            Task(title="Team meeting", description="Weekly sync",
                 due_date=today, priority=2, status=1, category_id=cat1.id),
            Task(title="Buy groceries", description="Milk, eggs, bread",
                 due_date=today + timedelta(days=1), priority=1, status=0, category_id=cat2.id),
            Task(title="Pay bills", description="Electricity, water",
                 due_date=today - timedelta(days=2), priority=3, status=0, category_id=cat2.id),
            Task(title="Exercise", description="Morning run",
                 due_date=today, priority=2, status=2, category_id=cat2.id),  # Completed
        ]
        cls.session.add_all(tasks)
        cls.session.commit()
        
        # 保存引用
        cls.work_category = cat1
        cls.personal_category = cat2
        cls.tasks = tasks
    
    def test_p1_2_search_service(self):
        """P1-2: 测试搜索服务"""
        search_service = SearchService(self.session)
        
        # 测试关键词搜索
        results = search_service.search_by_keyword("project")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Complete project report")
        
        # 测试描述搜索
        results = search_service.search_by_keyword("groceries")
        self.assertEqual(len(results), 1)
        
        # 测试分类搜索
        results = search_service.search_by_category(self.work_category.id)
        self.assertEqual(len(results), 2)
        
        # 测试优先级搜索
        results = search_service.search_by_priority(3)
        self.assertEqual(len(results), 2)  # 2 high priority tasks
        
        # 测试状态搜索
        results = search_service.search_by_status(2)  # Completed
        self.assertEqual(len(results), 1)
        
        # 测试高级搜索
        results = search_service.advanced_search(
            keyword="meeting",
            priority=2,
            status=1
        )
        self.assertEqual(len(results), 1)
        
        print("✅ P1-2 Search Service: PASS")
    
    def test_p1_3_filter_service(self):
        """P1-3: 测试过滤服务"""
        filter_service = FilterService(self.session)
        
        # 测试分类过滤
        tasks = filter_service.filter_by_category(self.personal_category.id)
        self.assertEqual(len(tasks), 3)
        
        # 测试优先级过滤
        tasks = filter_service.filter_by_priority(3)
        self.assertEqual(len(tasks), 2)
        
        # 测试状态过滤
        tasks = filter_service.filter_by_status(0)  # Pending
        self.assertEqual(len(tasks), 3)
        
        # 测试日期范围过滤
        start = date.today()
        end = start + timedelta(days=7)
        tasks = filter_service.filter_by_date_range(start, end)
        self.assertGreater(len(tasks), 0)
        
        # 测试逾期过滤
        overdue = filter_service.filter_overdue()
        self.assertEqual(len(overdue), 1)  # "Pay bills" is overdue
        
        # 测试今日过滤
        today_tasks = filter_service.filter_today()
        self.assertEqual(len(today_tasks), 3)
        
        # 测试多条件过滤
        tasks = filter_service.apply_multiple_filters(
            category_id=self.personal_category.id,
            status=0
        )
        self.assertGreater(len(tasks), 0)
        
        print("✅ P1-3 Filter Service: PASS")
    
    def test_p1_5_reminder_service(self):
        """P1-5: 测试提醒服务"""
        reminder_service = ReminderService(self.session)
        
        # 测试今日到期
        due_today = reminder_service.get_due_today()
        self.assertGreater(len(due_today), 0)
        
        # 测试明日到期
        due_tomorrow = reminder_service.get_due_tomorrow()
        self.assertGreater(len(due_tomorrow), 0)
        
        # 测试逾期
        overdue = reminder_service.get_overdue()
        self.assertEqual(len(overdue), 1)
        
        # 测试提醒摘要
        summary = reminder_service.get_reminder_summary()
        self.assertIn('overdue', summary)
        self.assertIn('due_today', summary)
        self.assertIn('due_tomorrow', summary)
        self.assertGreater(summary['total_pending'], 0)
        
        # 测试单个任务检查
        task = self.tasks[0]  # "Complete project report"
        needs_reminder, message = reminder_service.check_task_due(task)
        self.assertTrue(needs_reminder)
        self.assertIn("今天到期", message)
        
        # 测试每日提醒消息生成
        reminder_msg = reminder_service.generate_daily_reminder_message()
        self.assertIn("逾期任务", reminder_msg)
        self.assertIn("今天到期", reminder_msg)
        
        print("✅ P1-5 Reminder Service: PASS")
    
    def test_p1_6_stats_service(self):
        """P1-6: 测试统计服务"""
        stats_service = StatsService(self.session)
        
        # 测试基础统计
        basic = stats_service.get_basic_stats()
        self.assertEqual(basic['total'], 5)
        self.assertEqual(basic['completed'], 1)
        self.assertEqual(basic['pending'], 4)
        self.assertGreater(basic['completion_rate'], 0)
        
        # 测试优先级统计
        by_priority = stats_service.get_stats_by_priority()
        self.assertIn(1, by_priority)
        self.assertIn(2, by_priority)
        self.assertIn(3, by_priority)
        
        # 测试分类统计
        by_category = stats_service.get_stats_by_category()
        self.assertEqual(len(by_category), 2)
        
        # 测试周统计
        weekly = stats_service.get_weekly_stats()
        self.assertIn('total', weekly)
        self.assertIn('completed', weekly)
        
        # 测试月统计
        monthly = stats_service.get_monthly_stats()
        self.assertIn('total', monthly)
        
        # 测试完成趋势
        trend = stats_service.get_completion_trend(days=7)
        self.assertEqual(len(trend), 7)
        
        # 测试生产力得分
        score = stats_service.get_productivity_score()
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        
        # 测试完整报告
        report = stats_service.get_full_report()
        self.assertIn('basic', report)
        self.assertIn('by_priority', report)
        self.assertIn('by_category', report)
        self.assertIn('weekly', report)
        self.assertIn('monthly', report)
        self.assertIn('trend', report)
        self.assertIn('productivity_score', report)
        
        print("✅ P1-6 Stats Service: PASS")


if __name__ == '__main__':
    unittest.main(verbosity=2)
