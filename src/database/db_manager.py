"""
数据库管理模块

提供数据库连接、会话管理和异常处理
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from contextlib import contextmanager
from typing import Optional

# 先导入 Base，再导入模型
from src.models import Base, Task, Category, RecurringTask, Reminder

# 日志配置
logger = logging.getLogger(__name__)

# 数据库配置
DATABASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
DATABASE_URL = f"sqlite:///{os.path.join(DATABASE_DIR, 'todo_calendar.db')}"

# 创建数据库目录
try:
    os.makedirs(DATABASE_DIR, exist_ok=True)
    logger.debug(f"数据库目录已创建：{DATABASE_DIR}")
except OSError as e:
    logger.error(f"创建数据库目录失败：{e}")
    raise

# 创建引擎
try:
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
    logger.info(f"数据库引擎已创建：{DATABASE_URL}")
except Exception as e:
    logger.error(f"创建数据库引擎失败：{e}")
    raise

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database() -> bool:
    """
    初始化数据库，创建所有表
    
    Returns:
        是否成功初始化
        
    Raises:
        SQLAlchemyError: 数据库操作失败
    """
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表结构已创建")
        
        # 初始化默认分类
        _init_default_categories()
        
        logger.info(f"✓ 数据库初始化完成：{DATABASE_URL}")
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"数据库初始化失败 - SQLAlchemy 错误：{e}")
        raise
    except Exception as e:
        logger.error(f"数据库初始化失败 - 未知错误：{e}")
        raise


def _init_default_categories() -> None:
    """
    初始化默认分类
    
    Raises:
        SQLAlchemyError: 数据库操作失败
    """
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
            logger.info(f"✓ 已创建 {len(defaults)} 个默认分类")
        else:
            logger.debug(f"已存在 {existing_count} 个分类，跳过初始化")
            
    except IntegrityError as e:
        session.rollback()
        logger.error(f"初始化分类失败 - 完整性错误：{e}")
        raise
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"初始化分类失败 - SQLAlchemy 错误：{e}")
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"初始化分类失败 - 未知错误：{e}")
        raise
    finally:
        session.close()


@contextmanager
def get_session() -> Session:
    """
    获取数据库会话的上下文管理器
    
    自动处理会话的创建、提交/回滚和关闭
    
    Yields:
        Session: 数据库会话对象
        
    Raises:
        SQLAlchemyError: 数据库操作失败时回滚并抛出异常
    """
    session = SessionLocal()
    try:
        yield session
        # 如果没有异常，自动提交
        # 注意：调用者可以选择手动 commit，这里不自动提交以避免重复提交
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"数据库操作失败 - SQLAlchemy 错误：{e}")
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"数据库操作失败 - 未知错误：{e}")
        raise
    finally:
        session.close()


def get_engine():
    """获取数据库引擎"""
    return engine


def check_database_connection() -> bool:
    """
    检查数据库连接是否正常
    
    Returns:
        连接是否正常
    """
    try:
        # 尝试连接数据库
        with engine.connect() as conn:
            # 使用 select(1) 而不是 text()，更符合 SQLAlchemy 2.0 规范
            from sqlalchemy import select
            conn.execute(select(1))
        logger.debug("数据库连接检查通过")
        return True
    except Exception as e:
        logger.error(f"数据库连接检查失败：{e}")
        return False
