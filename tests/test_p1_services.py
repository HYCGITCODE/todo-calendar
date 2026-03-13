"""
P1 功能测试 - 搜索、过滤、提醒、统计
"""

import pytest
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.task import Task, Base
from src.models.category import Category
from src.services.search_service import SearchService
from src.services.filter_service import FilterService
from src.services.reminder_service import ReminderService
from src.services.stats_service import StatsService


@pytest.fixture
def test_session():
    """创建测试数据库会话"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 创建默认分类
    defaults = Category.get_defaults()
    for i, cat in enumerate(defaults):
        category = Category(
            name=cat['name'],
            color=cat['color'],
            icon=cat['icon'],
            sort_order=i
        )
        session.add(category)
    session.commit()
    
    yield session
    session.close()


@pytest.fixture
def sample_tasks(test_session):
    """创建样本任务"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    tasks = [
        Task(title="High Priority Task", due_date=today, priority=3, status=0, category_id=1),
        Task(title="Medium Priority Task", due_date=today, priority=2, status=0, category_id=1),
        Task(title="Low Priority Task", due_date=today, priority=1, status=0, category_id=2),
        Task(title="Completed Task", due_date=today, priority=2, status=2, category_id=1),
        Task(title="Overdue Task", due_date=yesterday, priority=3, status=0, category_id=1),
        Task(title="Future Task", due_date=tomorrow, priority=1, status=0, category_id=3),
    ]
    
    for task in tasks:
        test_session.add(task)
    test_session.commit()
    
    return tasks


class TestSearchService:
    """搜索服务测试"""
    
    def test_search_by_keyword(self, test_session, sample_tasks):
        """测试关键词搜索"""
        service = SearchService(test_session)
        results = service.search_by_keyword("High")
        
        assert len(results) == 1
        assert results[0].title == "High Priority Task"
    
    def test_search_by_category(self, test_session, sample_tasks):
        """测试分类搜索"""
        service = SearchService(test_session)
        results = service.search_by_category(1)
        
        assert len(results) >= 3  # 分类 1 至少有 3 个任务
    
    def test_search_by_priority(self, test_session, sample_tasks):
        """测试优先级搜索"""
        service = SearchService(test_session)
        results = service.search_by_priority(3)
        
        assert len(results) == 2  # 高优先级有 2 个任务
    
    def test_advanced_search(self, test_session, sample_tasks):
        """测试高级搜索"""
        service = SearchService(test_session)
        results = service.advanced_search(
            keyword="Task",
            priority=3,
            status=0
        )
        
        assert len(results) >= 1


class TestFilterService:
    """过滤服务测试"""
    
    def test_filter_by_priority(self, test_session, sample_tasks):
        """测试优先级过滤"""
        service = FilterService(test_session)
        results = service.filter_by_priority(3)
        
        assert len(results) == 2
    
    def test_filter_by_status(self, test_session, sample_tasks):
        """测试状态过滤"""
        service = FilterService(test_session)
        results = service.filter_by_status(2)  # 已完成
        
        assert len(results) == 1
    
    def test_filter_overdue(self, test_session, sample_tasks):
        """测试逾期过滤"""
        service = FilterService(test_session)
        results = service.filter_overdue()
        
        assert len(results) == 1
        assert results[0].title == "Overdue Task"
    
    def test_filter_today(self, test_session, sample_tasks):
        """测试今日过滤"""
        service = FilterService(test_session)
        results = service.filter_today()
        
        assert len(results) == 4  # 今天有 4 个任务
    
    def test_apply_multiple_filters(self, test_session, sample_tasks):
        """测试多条件过滤"""
        service = FilterService(test_session)
        results = service.apply_multiple_filters(
            priority=3,
            status=0
        )
        
        assert len(results) == 2


class TestReminderService:
    """提醒服务测试"""
    
    def test_get_due_today(self, test_session, sample_tasks):
        """测试获取今日到期任务"""
        service = ReminderService(test_session)
        tasks = service.get_due_today()
        
        assert len(tasks) == 3  # 排除已完成的
    
    def test_get_overdue(self, test_session, sample_tasks):
        """测试获取逾期任务"""
        service = ReminderService(test_session)
        tasks = service.get_overdue()
        
        assert len(tasks) == 1
        assert tasks[0].title == "Overdue Task"
    
    def test_get_reminder_summary(self, test_session, sample_tasks):
        """测试提醒摘要"""
        service = ReminderService(test_session)
        summary = service.get_reminder_summary()
        
        assert summary['overdue'] == 1
        assert summary['due_today'] == 3
        assert summary['total_pending'] == 5
    
    def test_check_task_due(self, test_session, sample_tasks):
        """测试任务到期检查"""
        service = ReminderService(test_session)
        overdue_task = sample_tasks[4]  # 逾期任务
        
        needs_reminder, message = service.check_task_due(overdue_task)
        
        assert needs_reminder is True
        assert "逾期" in message
    
    def test_generate_daily_reminder_message(self, test_session, sample_tasks):
        """测试生成每日提醒消息"""
        service = ReminderService(test_session)
        message = service.generate_daily_reminder_message()
        
        assert isinstance(message, str)
        assert len(message) > 0


class TestStatsService:
    """统计服务测试"""
    
    def test_get_basic_stats(self, test_session, sample_tasks):
        """测试基础统计"""
        service = StatsService(test_session)
        stats = service.get_basic_stats()
        
        assert stats['total'] == 6
        assert stats['completed'] == 1
        assert stats['pending'] == 5
        assert stats['completion_rate'] > 0
    
    def test_get_stats_by_priority(self, test_session, sample_tasks):
        """测试按优先级统计"""
        service = StatsService(test_session)
        stats = service.get_stats_by_priority()
        
        assert 3 in stats  # 高优先级
        assert stats[3]['total'] == 2
    
    def test_get_stats_by_category(self, test_session, sample_tasks):
        """测试按分类统计"""
        service = StatsService(test_session)
        stats = service.get_stats_by_category()
        
        assert len(stats) == 4  # 4 个默认分类
    
    def test_get_productivity_score(self, test_session, sample_tasks):
        """测试生产力得分"""
        service = StatsService(test_session)
        score = service.get_productivity_score()
        
        assert 0 <= score <= 100
    
    def test_get_full_report(self, test_session, sample_tasks):
        """测试完整报告"""
        service = StatsService(test_session)
        report = service.get_full_report()
        
        assert 'basic' in report
        assert 'by_priority' in report
        assert 'by_category' in report
        assert 'productivity_score' in report
