"""
任务服务层 - 业务逻辑

提供任务相关的业务逻辑操作，包含完整的异常处理和日志记录
"""

import logging
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.models.task import Task
from src.models.category import Category

# 日志记录器
logger = logging.getLogger(__name__)


class TaskService:
    """任务服务类"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_task(self, title: str, due_date: date, 
                    description: str = "", priority: int = 1,
                    category_id: Optional[int] = None) -> Task:
        """
        创建新任务
        
        Args:
            title: 任务标题
            due_date: 截止日期
            description: 任务描述
            priority: 优先级 (1=低，2=中，3=高)
            category_id: 分类 ID
            
        Returns:
            创建的任务对象
            
        Raises:
            IntegrityError: 数据完整性错误
            SQLAlchemyError: 数据库操作错误
            ValueError: 参数验证失败
        """
        try:
            # 参数验证
            if not title or not title.strip():
                raise ValueError("任务标题不能为空")
            
            task = Task(
                title=title.strip(),
                description=description,
                due_date=due_date,
                priority=priority,
                category_id=category_id
            )
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
            logger.info(f"创建任务成功：ID={task.id}, title='{title}'")
            return task
            
        except IntegrityError as e:
            self.session.rollback()
            logger.error(f"创建任务失败 - 完整性错误：{e}")
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"创建任务失败 - 数据库错误：{e}")
            raise
        except ValueError as e:
            logger.warning(f"创建任务失败 - 参数验证失败：{e}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"创建任务失败 - 未知错误：{e}")
            raise
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        获取单个任务
        
        Args:
            task_id: 任务 ID
            
        Returns:
            任务对象，不存在则返回 None
            
        Raises:
            SQLAlchemyError: 数据库操作错误
        """
        try:
            task = self.session.query(Task).filter(Task.id == task_id).first()
            if task:
                logger.debug(f"获取任务成功：ID={task_id}")
            else:
                logger.debug(f"任务不存在：ID={task_id}")
            return task
        except SQLAlchemyError as e:
            logger.error(f"获取任务失败 - 数据库错误：ID={task_id}, error={e}")
            raise
        except Exception as e:
            logger.error(f"获取任务失败 - 未知错误：ID={task_id}, error={e}")
            raise
    
    def get_tasks_by_date(self, target_date: date) -> List[Task]:
        """获取指定日期的任务"""
        try:
            tasks = self.session.query(Task).filter(
                Task.due_date == target_date
            ).order_by(Task.priority.desc(), Task.created_at).all()
            logger.debug(f"获取日期 {target_date} 的任务：{len(tasks)} 个")
            return tasks
        except SQLAlchemyError as e:
            logger.error(f"获取日期任务失败 - 数据库错误：{e}")
            raise
        except Exception as e:
            logger.error(f"获取日期任务失败 - 未知错误：{e}")
            raise
    
    def get_tasks_by_date_range(self, start_date: date, end_date: date) -> List[Task]:
        """获取日期范围内的任务"""
        try:
            tasks = self.session.query(Task).filter(
                and_(Task.due_date >= start_date, Task.due_date <= end_date)
            ).order_by(Task.due_date, Task.priority.desc()).all()
            logger.debug(f"获取日期范围 [{start_date}, {end_date}] 的任务：{len(tasks)} 个")
            return tasks
        except SQLAlchemyError as e:
            logger.error(f"获取日期范围任务失败 - 数据库错误：{e}")
            raise
        except Exception as e:
            logger.error(f"获取日期范围任务失败 - 未知错误：{e}")
            raise
    
    def get_tasks_by_category(self, category_id: int) -> List[Task]:
        """获取指定分类的任务"""
        try:
            tasks = self.session.query(Task).filter(
                Task.category_id == category_id
            ).order_by(Task.due_date).all()
            logger.debug(f"获取分类 {category_id} 的任务：{len(tasks)} 个")
            return tasks
        except SQLAlchemyError as e:
            logger.error(f"获取分类任务失败 - 数据库错误：{e}")
            raise
        except Exception as e:
            logger.error(f"获取分类任务失败 - 未知错误：{e}")
            raise
    
    def get_pending_tasks(self) -> List[Task]:
        """获取所有待办任务"""
        try:
            tasks = self.session.query(Task).filter(
                Task.status == 0
            ).order_by(Task.due_date, Task.priority.desc()).all()
            logger.debug(f"获取待办任务：{len(tasks)} 个")
            return tasks
        except SQLAlchemyError as e:
            logger.error(f"获取待办任务失败 - 数据库错误：{e}")
            raise
        except Exception as e:
            logger.error(f"获取待办任务失败 - 未知错误：{e}")
            raise
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """
        更新任务
        
        Args:
            task_id: 任务 ID
            **kwargs: 要更新的字段
            
        Returns:
            更新后的任务对象，不存在则返回 None
            
        Raises:
            SQLAlchemyError: 数据库操作错误
            ValueError: 参数验证失败
        """
        try:
            task = self.get_task(task_id)
            if task:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                self.session.commit()
                self.session.refresh(task)
                logger.info(f"更新任务成功：ID={task_id}")
            else:
                logger.warning(f"更新任务失败 - 任务不存在：ID={task_id}")
            return task
        except IntegrityError as e:
            self.session.rollback()
            logger.error(f"更新任务失败 - 完整性错误：ID={task_id}, error={e}")
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"更新任务失败 - 数据库错误：ID={task_id}, error={e}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"更新任务失败 - 未知错误：ID={task_id}, error={e}")
            raise
    
    def mark_complete(self, task_id: int) -> Optional[Task]:
        """
        标记任务为完成
        
        Args:
            task_id: 任务 ID
            
        Returns:
            更新后的任务对象，不存在则返回 None
            
        Raises:
            SQLAlchemyError: 数据库操作错误
        """
        try:
            task = self.get_task(task_id)
            if task:
                task.mark_complete()
                self.session.commit()
                logger.info(f"标记任务完成：ID={task_id}, title='{task.title}'")
            else:
                logger.warning(f"标记任务完成失败 - 任务不存在：ID={task_id}")
            return task
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"标记任务完成失败 - 数据库错误：ID={task_id}, error={e}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"标记任务完成失败 - 未知错误：ID={task_id}, error={e}")
            raise
    
    def delete_task(self, task_id: int) -> bool:
        """
        删除任务
        
        Args:
            task_id: 任务 ID
            
        Returns:
            是否删除成功
            
        Raises:
            SQLAlchemyError: 数据库操作错误
        """
        try:
            task = self.get_task(task_id)
            if task:
                task_title = task.title
                self.session.delete(task)
                self.session.commit()
                logger.info(f"删除任务成功：ID={task_id}, title='{task_title}'")
                return True
            else:
                logger.warning(f"删除任务失败 - 任务不存在：ID={task_id}")
                return False
        except IntegrityError as e:
            self.session.rollback()
            logger.error(f"删除任务失败 - 完整性错误：ID={task_id}, error={e}")
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"删除任务失败 - 数据库错误：ID={task_id}, error={e}")
            raise
        except Exception as e:
            self.session.rollback()
            logger.error(f"删除任务失败 - 未知错误：ID={task_id}, error={e}")
            raise
    
    def get_task_count_by_status(self) -> dict:
        """获取各状态任务数量"""
        try:
            total = self.session.query(Task).count()
            completed = self.session.query(Task).filter(Task.status == 2).count()
            pending = total - completed
            logger.debug(f"获取任务统计：总计={total}, 已完成={completed}, 待办={pending}")
            return {
                'total': total,
                'completed': completed,
                'pending': pending
            }
        except SQLAlchemyError as e:
            logger.error(f"获取任务统计失败 - 数据库错误：{e}")
            raise
        except Exception as e:
            logger.error(f"获取任务统计失败 - 未知错误：{e}")
            raise
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """
        搜索任务
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的任务列表
            
        Raises:
            SQLAlchemyError: 数据库操作错误
        """
        try:
            if not keyword or not keyword.strip():
                logger.warning("搜索关键词为空")
                return []
            
            tasks = self.session.query(Task).filter(
                Task.title.contains(keyword) | Task.description.contains(keyword)
            ).order_by(Task.due_date).all()
            logger.info(f"搜索任务 '{keyword}': 找到 {len(tasks)} 个")
            return tasks
        except SQLAlchemyError as e:
            logger.error(f"搜索任务失败 - 数据库错误：{e}")
            raise
        except Exception as e:
            logger.error(f"搜索任务失败 - 未知错误：{e}")
            raise
