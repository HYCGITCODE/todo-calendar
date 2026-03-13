"""
数据库管理模块
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

# 先导入 Base，再导入模型
from src.models import Base, Task, Category, RecurringTask


# 数据库配置
DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DATABASE_URL = f"sqlite:///{os.path.join(DATABASE_DIR, 'todo_calendar.db')}"

# 创建数据库目录
os.makedirs(DATABASE_DIR, exist_ok=True)

# 创建引擎
engine = create_engine(DATABASE_URL, echo=False)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)
    
    # 初始化默认分类
    _init_default_categories()
    
    print(f"✓ 数据库初始化完成：{DATABASE_URL}")


def _init_default_categories():
    """初始化默认分类"""
    session = SessionLocal()
    try:
        # 检查是否已有分类
        existing_count = session.query(Category).count()
        if existing_count == 0:
            # 添加默认分类
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
            print(f"✓ 已创建 {len(defaults)} 个默认分类")
    except Exception as e:
        session.rollback()
        print(f"✗ 初始化分类失败：{e}")
    finally:
        session.close()


@contextmanager
def get_session() -> Session:
    """获取数据库会话的上下文管理器"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_engine():
    """获取数据库引擎"""
    return engine
