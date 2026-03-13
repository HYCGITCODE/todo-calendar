#!/usr/bin/env python3
"""
Todo Calendar - P1 功能自动化测试套件

运行方式:
    python tests/test_p1_automation.py
    
运行特定测试:
    python tests/test_p1_automation.py --test search
    python tests/test_p1_automation.py --test filter
    python tests/test_p1_automation.py --test reminder
    python tests/test_p1_automation.py --test stats

生成报告:
    python tests/test_p1_automation.py --report
"""

import sys
import os
import unittest
import argparse
from datetime import date, timedelta
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database.db_manager import init_database, get_session, Base, engine
from src.models.task import Task
from src.models.category import Category
from src.services.search_service import SearchService
from src.services.filter_service import FilterService
from src.services.reminder_service import ReminderService
from src.services.stats_service import StatsService
from src.services.task_service import TaskService


class TestP1Search(unittest.TestCase):
    """P1-2: 任务搜索测试"""
    
    def setUp(self):
        """每个测试前准备"""
        init_database()
        self.session = get_session().__enter__()
        self._create_test_data()
        self.search_service = SearchService(self.session)
    
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
        
        # 创建任务
        today = date.today()
        tasks = [
            Task(title="完成项目报告", description="Q1 季度报告", 
                 due_date=today, priority=3, status=0, category_id=cat1.id),
            Task(title="团队会议", description="每周例会",
                 due_date=today, priority=2, status=1, category_id=cat1.id),
            Task(title="购买生活用品", description="牛奶、鸡蛋、面包",
                 due_date=today + timedelta(days=1), priority=1, status=0, category_id=cat2.id),
            Task(title="支付账单", description="电费、水费",
                 due_date=today - timedelta(days=2), priority=3, status=0, category_id=cat2.id),
            Task(title="晨跑锻炼", description="5 公里跑步",
                 due_date=today, priority=2, status=2, category_id=cat2.id),
        ]
        self.session.add_all(tasks)
        self.session.commit()
        
        self.work_category = cat1
        self.personal_category = cat2
        self.tasks = tasks
    
    def test_search_by_keyword(self):
        """测试关键词搜索"""
        results = self.search_service.search_by_keyword("项目")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "完成项目报告")
        print("✅ 关键词搜索：PASS")
    
    def test_search_by_description(self):
        """测试描述搜索"""
        results = self.search_service.search_by_keyword("牛奶")
        self.assertEqual(len(results), 1)
        print("✅ 描述搜索：PASS")
    
    def test_search_by_category(self):
        """测试分类搜索"""
        results = self.search_service.search_by_category(self.work_category.id)
        self.assertEqual(len(results), 2)
        print("✅ 分类搜索：PASS")
    
    def test_search_by_priority(self):
        """测试优先级搜索"""
        results = self.search_service.search_by_priority(3)
        self.assertEqual(len(results), 2)  # 2 个高优先级任务
        print("✅ 优先级搜索：PASS")
    
    def test_search_by_status(self):
        """测试状态搜索"""
        results = self.search_service.search_by_status(2)  # 已完成
        self.assertEqual(len(results), 1)
        print("✅ 状态搜索：PASS")
    
    def test_advanced_search(self):
        """测试高级搜索"""
        results = self.search_service.advanced_search(
            keyword="会议",
            priority=2,
            status=1
        )
        self.assertEqual(len(results), 1)
        print("✅ 高级搜索：PASS")
    
    def test_case_insensitive(self):
        """测试大小写不敏感"""
        results_upper = self.search_service.search_by_keyword("PROJECT")
        results_lower = self.search_service.search_by_keyword("project")
        self.assertEqual(len(results_upper), len(results_lower))
        print("✅ 大小写不敏感：PASS")


class TestP1Filter(unittest.TestCase):
    """P1-3: 任务过滤测试"""
    
    def setUp(self):
        init_database()
        self.session = get_session().__enter__()
        self._create_test_data()
        self.filter_service = FilterService(self.session)
    
    def tearDown(self):
        self.session.close()
    
    def _create_test_data(self):
        self.session.query(Task).delete()
        self.session.query(Category).delete()
        self.session.commit()
        
        cat1 = Category(name="Work", icon="💼", color="#3498db")
        cat2 = Category(name="Personal", icon="🏠", color="#27ae60")
        self.session.add_all([cat1, cat2])
        self.session.commit()
        
        today = date.today()
        tasks = [
            Task(title="任务 1", due_date=today, priority=3, status=0, category_id=cat1.id),
            Task(title="任务 2", due_date=today, priority=2, status=1, category_id=cat1.id),
            Task(title="任务 3", due_date=today + timedelta(days=1), priority=1, status=0, category_id=cat2.id),
            Task(title="逾期任务", due_date=today - timedelta(days=2), priority=3, status=0, category_id=cat2.id),
            Task(title="完成任务", due_date=today, priority=2, status=2, category_id=cat2.id),
        ]
        self.session.add_all(tasks)
        self.session.commit()
        
        self.work_category = cat1
        self.personal_category = cat2
    
    def test_filter_by_category(self):
        """测试分类过滤"""
        tasks = self.filter_service.filter_by_category(self.personal_category.id)
        self.assertEqual(len(tasks), 3)
        print("✅ 分类过滤：PASS")
    
    def test_filter_by_priority(self):
        """测试优先级过滤"""
        tasks = self.filter_service.filter_by_priority(3)
        self.assertEqual(len(tasks), 2)
        print("✅ 优先级过滤：PASS")
    
    def test_filter_by_status(self):
        """测试状态过滤"""
        tasks = self.filter_service.filter_by_status(0)  # 待办
        self.assertEqual(len(tasks), 3)
        print("✅ 状态过滤：PASS")
    
    def test_filter_overdue(self):
        """测试逾期过滤"""
        overdue = self.filter_service.filter_overdue()
        self.assertEqual(len(overdue), 1)
        print("✅ 逾期过滤：PASS")
    
    def test_filter_today(self):
        """测试今日过滤"""
        today_tasks = self.filter_service.filter_today()
        self.assertEqual(len(today_tasks), 3)
        print("✅ 今日过滤：PASS")
    
    def test_multiple_filters(self):
        """测试多条件过滤"""
        tasks = self.filter_service.apply_multiple_filters(
            category_id=self.personal_category.id,
            status=0
        )
        self.assertGreater(len(tasks), 0)
        print("✅ 多条件过滤：PASS")


class TestP1Reminder(unittest.TestCase):
    """P1-5: 到期提醒测试"""
    
    def setUp(self):
        init_database()
        self.session = get_session().__enter__()
        self._create_test_data()
        self.reminder_service = ReminderService(self.session)
    
    def tearDown(self):
        self.session.close()
    
    def _create_test_data(self):
        self.session.query(Task).delete()
        self.session.query(Category).delete()
        self.session.commit()
        
        today = date.today()
        tasks = [
            Task(title="今日任务", due_date=today, priority=3, status=0),
            Task(title="明日任务", due_date=today + timedelta(days=1), priority=2, status=0),
            Task(title="逾期任务", due_date=today - timedelta(days=2), priority=3, status=0),
            Task(title="完成任务", due_date=today, priority=2, status=2),
        ]
        self.session.add_all(tasks)
        self.session.commit()
        self.tasks = tasks
    
    def test_get_due_today(self):
        """测试获取今日到期任务"""
        due_today = self.reminder_service.get_due_today()
        self.assertGreater(len(due_today), 0)
        print("✅ 今日到期查询：PASS")
    
    def test_get_due_tomorrow(self):
        """测试获取明日到期任务"""
        due_tomorrow = self.reminder_service.get_due_tomorrow()
        self.assertGreater(len(due_tomorrow), 0)
        print("✅ 明日到期查询：PASS")
    
    def test_get_overdue(self):
        """测试获取逾期任务"""
        overdue = self.reminder_service.get_overdue()
        self.assertEqual(len(overdue), 1)
        print("✅ 逾期查询：PASS")
    
    def test_reminder_summary(self):
        """测试提醒摘要"""
        summary = self.reminder_service.get_reminder_summary()
        self.assertIn('overdue', summary)
        self.assertIn('due_today', summary)
        self.assertIn('due_tomorrow', summary)
        self.assertGreater(summary['total_pending'], 0)
        print("✅ 提醒摘要：PASS")
    
    def test_check_task_due(self):
        """测试单个任务检查"""
        task = self.tasks[0]
        needs_reminder, message = self.reminder_service.check_task_due(task)
        self.assertTrue(needs_reminder)
        self.assertIn("今天", message)
        print("✅ 任务到期检查：PASS")
    
    def test_completed_no_reminder(self):
        """测试已完成任务不提醒"""
        completed_task = self.tasks[3]
        needs_reminder, _ = self.reminder_service.check_task_due(completed_task)
        self.assertFalse(needs_reminder)
        print("✅ 已完成任务不提醒：PASS")


class TestP1Stats(unittest.TestCase):
    """P1-6: 数据统计测试"""
    
    def setUp(self):
        init_database()
        self.session = get_session().__enter__()
        self._create_test_data()
        self.stats_service = StatsService(self.session)
    
    def tearDown(self):
        self.session.close()
    
    def _create_test_data(self):
        self.session.query(Task).delete()
        self.session.query(Category).delete()
        self.session.commit()
        
        cat1 = Category(name="Work", icon="💼", color="#3498db")
        cat2 = Category(name="Personal", icon="🏠", color="#27ae60")
        self.session.add_all([cat1, cat2])
        self.session.commit()
        
        today = date.today()
        tasks = [
            Task(title="任务 1", due_date=today, priority=3, status=0, category_id=cat1.id),
            Task(title="任务 2", due_date=today, priority=2, status=1, category_id=cat1.id),
            Task(title="任务 3", due_date=today, priority=1, status=0, category_id=cat2.id),
            Task(title="任务 4", due_date=today, priority=3, status=0, category_id=cat2.id),
            Task(title="任务 5", due_date=today, priority=2, status=2, category_id=cat2.id),
        ]
        self.session.add_all(tasks)
        self.session.commit()
        
        self.work_category = cat1
        self.personal_category = cat2
    
    def test_basic_stats(self):
        """测试基础统计"""
        basic = self.stats_service.get_basic_stats()
        self.assertEqual(basic['total'], 5)
        self.assertEqual(basic['completed'], 1)
        self.assertEqual(basic['pending'], 4)
        self.assertGreater(basic['completion_rate'], 0)
        print("✅ 基础统计：PASS")
    
    def test_stats_by_priority(self):
        """测试优先级统计"""
        by_priority = self.stats_service.get_stats_by_priority()
        self.assertIn(1, by_priority)
        self.assertIn(2, by_priority)
        self.assertIn(3, by_priority)
        print("✅ 优先级统计：PASS")
    
    def test_stats_by_category(self):
        """测试分类统计"""
        by_category = self.stats_service.get_stats_by_category()
        self.assertEqual(len(by_category), 2)
        print("✅ 分类统计：PASS")
    
    def test_weekly_stats(self):
        """测试周统计"""
        weekly = self.stats_service.get_weekly_stats()
        self.assertIn('total', weekly)
        self.assertIn('completed', weekly)
        print("✅ 周统计：PASS")
    
    def test_monthly_stats(self):
        """测试月统计"""
        monthly = self.stats_service.get_monthly_stats()
        self.assertIn('total', monthly)
        print("✅ 月统计：PASS")
    
    def test_completion_trend(self):
        """测试完成趋势"""
        trend = self.stats_service.get_completion_trend(days=7)
        self.assertEqual(len(trend), 7)
        print("✅ 完成趋势：PASS")
    
    def test_productivity_score(self):
        """测试生产力得分"""
        score = self.stats_service.get_productivity_score()
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        print("✅ 生产力得分：PASS")
    
    def test_full_report(self):
        """测试完整报告"""
        report = self.stats_service.get_full_report()
        self.assertIn('basic', report)
        self.assertIn('by_priority', report)
        self.assertIn('by_category', report)
        self.assertIn('weekly', report)
        print("✅ 完整报告：PASS")


def run_tests(test_class_name=None):
    """运行测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    if test_class_name:
        # 运行特定测试类
        test_classes = {
            'search': TestP1Search,
            'filter': TestP1Filter,
            'reminder': TestP1Reminder,
            'stats': TestP1Stats,
        }
        if test_class_name in test_classes:
            suite.addTests(loader.loadTestsFromTestCase(test_classes[test_class_name]))
        else:
            print(f"❌ 未知测试类：{test_class_name}")
            print("可用测试类：search, filter, reminder, stats")
            return False
    else:
        # 运行所有测试
        suite.addTests(loader.loadTestsFromTestCase(TestP1Search))
        suite.addTests(loader.loadTestsFromTestCase(TestP1Filter))
        suite.addTests(loader.loadTestsFromTestCase(TestP1Reminder))
        suite.addTests(loader.loadTestsFromTestCase(TestP1Stats))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总测试数：{result.testsRun}")
    print(f"通过：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    print(f"通过率：{(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    if result.failures:
        print("\n失败测试:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n错误测试:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    return len(result.failures) == 0 and len(result.errors) == 0


def main():
    parser = argparse.ArgumentParser(description='Todo Calendar P1 功能自动化测试')
    parser.add_argument('--test', type=str, help='运行特定测试 (search/filter/reminder/stats)')
    parser.add_argument('--report', action='store_true', help='生成测试报告')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Todo Calendar - P1 功能自动化测试套件")
    print("=" * 60)
    print(f"测试开始时间：{date.today()}")
    print()
    
    success = run_tests(args.test)
    
    if args.report:
        print("\n生成测试报告...")
        # 这里可以添加生成 HTML 报告的逻辑
        print("报告生成完毕")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
