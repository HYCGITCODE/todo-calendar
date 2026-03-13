"""
任务服务测试
"""

import pytest
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.task import Task, Base
from src.services.task_service import TaskService


@pytest.fixture
def test_session():
    """创建测试数据库会话"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def task_service(test_session):
    """创建任务服务实例"""
    return TaskService(test_session)


class TestTaskService:
    """任务服务测试类"""
    
    def test_create_task(self, task_service):
        """测试创建任务"""
        task = task_service.create_task(
            title="Test Task",
            due_date=date.today(),
            description="Test Description",
            priority=2
        )
        
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.priority == 2
        assert task.status == 0  # 默认待办
    
    def test_get_task(self, task_service):
        """测试获取任务"""
        created = task_service.create_task(
            title="Get Task Test",
            due_date=date.today()
        )
        
        retrieved = task_service.get_task(created.id)
        assert retrieved is not None
        assert retrieved.title == "Get Task Test"
    
    def test_update_task(self, task_service):
        """测试更新任务"""
        task = task_service.create_task(
            title="Original Title",
            due_date=date.today()
        )
        
        updated = task_service.update_task(
            task.id,
            title="Updated Title",
            priority=3
        )
        
        assert updated.title == "Updated Title"
        assert updated.priority == 3
    
    def test_mark_complete(self, task_service):
        """测试标记任务完成"""
        task = task_service.create_task(
            title="Complete Test",
            due_date=date.today()
        )
        
        completed = task_service.mark_complete(task.id)
        
        assert completed.status == 2
        assert completed.completed_at is not None
    
    def test_delete_task(self, task_service):
        """测试删除任务"""
        task = task_service.create_task(
            title="Delete Test",
            due_date=date.today()
        )
        
        result = task_service.delete_task(task.id)
        assert result is True
        
        deleted = task_service.get_task(task.id)
        assert deleted is None
    
    def test_get_tasks_by_date(self, task_service):
        """测试按日期获取任务"""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        task_service.create_task(title="Today Task 1", due_date=today)
        task_service.create_task(title="Today Task 2", due_date=today)
        task_service.create_task(title="Tomorrow Task", due_date=tomorrow)
        
        today_tasks = task_service.get_tasks_by_date(today)
        assert len(today_tasks) == 2
    
    def test_search_tasks(self, task_service):
        """测试搜索任务"""
        task_service.create_task(
            title="Important Meeting",
            description="Discuss project roadmap",
            due_date=date.today()
        )
        
        results = task_service.search_tasks("Meeting")
        assert len(results) == 1
        assert results[0].title == "Important Meeting"
    
    def test_get_task_count_by_status(self, task_service):
        """测试获取任务统计"""
        task_service.create_task(title="Task 1", due_date=date.today())
        task_service.create_task(title="Task 2", due_date=date.today())
        task = task_service.create_task(title="Task 3", due_date=date.today())
        
        task_service.mark_complete(task.id)
        
        stats = task_service.get_task_count_by_status()
        assert stats['total'] == 3
        assert stats['completed'] == 1
        assert stats['pending'] == 2
