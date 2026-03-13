"""
数据库测试
"""

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.task import Task
from src.models.category import Category, Base
from src.database.db_manager import init_database, get_session


class TestDatabaseInit:
    """数据库初始化测试"""
    
    def test_create_tables(self):
        """测试创建表"""
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        
        # 验证表存在
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        assert 'tasks' in tables
        assert 'categories' in tables
    
    def test_default_categories(self):
        """测试默认分类创建"""
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # 手动初始化默认分类
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
        
        # 验证分类数量
        count = session.query(Category).count()
        assert count == 4
        
        # 验证分类名称
        names = [cat.name for cat in session.query(Category).all()]
        assert '工作' in names
        assert '个人' in names
        
        session.close()


class TestTaskModel:
    """任务模型测试"""
    
    def test_task_repr(self):
        """测试任务字符串表示"""
        task = Task(
            id=1,
            title="Test Task",
            due_date=None
        )
        assert "Task(id=1" in repr(task)
    
    def test_mark_complete(self):
        """测试标记完成方法"""
        from datetime import datetime
        task = Task(
            title="Test",
            due_date=None,
            status=0
        )
        
        task.mark_complete()
        
        assert task.status == 2
        assert task.completed_at is not None


class TestCategoryModel:
    """分类模型测试"""
    
    def test_category_repr(self):
        """测试分类字符串表示"""
        category = Category(id=1, name="Test")
        assert "Category(id=1" in repr(category)
    
    def test_get_defaults(self):
        """测试获取默认分类"""
        defaults = Category.get_defaults()
        
        assert len(defaults) == 4
        assert all('name' in cat for cat in defaults)
        assert all('color' in cat for cat in defaults)
        assert all('icon' in cat for cat in defaults)
