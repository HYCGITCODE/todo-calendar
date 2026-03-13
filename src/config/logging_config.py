"""
日志配置模块

提供统一的日志系统，支持：
- 控制台输出
- 文件输出（按日期滚动）
- 日志级别配置
- 格式化输出
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional


# 日志配置
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5  # 保留 5 个备份文件


def setup_logging(level: str = LOG_LEVEL, log_to_file: bool = True) -> None:
    """
    配置日志系统
    
    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: 是否输出到文件
    """
    # 创建日志目录
    if log_to_file:
        os.makedirs(LOG_DIR, exist_ok=True)
    
    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # 清除现有的处理器（避免重复）
    if root_logger.handlers:
        root_logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 文件处理器（按大小滚动）
    if log_to_file:
        log_file = os.path.join(LOG_DIR, f'todo_calendar_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # 记录日志系统启动
    logging.info(f"日志系统已启动 - 级别：{level}, 日志目录：{LOG_DIR if log_to_file else '仅控制台'}")


def get_logger(name: str) -> logging.Logger:
    """
    获取命名日志记录器
    
    Args:
        name: 日志记录器名称（通常使用模块名 __name__）
        
    Returns:
        配置好的日志记录器
    """
    return logging.getLogger(name)


# 便捷函数
def log_debug(logger: logging.Logger, message: str, **kwargs) -> None:
    """记录调试日志"""
    if kwargs:
        logger.debug(f"{message} - {kwargs}")
    else:
        logger.debug(message)


def log_info(logger: logging.Logger, message: str, **kwargs) -> None:
    """记录信息日志"""
    if kwargs:
        logger.info(f"{message} - {kwargs}")
    else:
        logger.info(message)


def log_warning(logger: logging.Logger, message: str, **kwargs) -> None:
    """记录警告日志"""
    if kwargs:
        logger.warning(f"{message} - {kwargs}")
    else:
        logger.warning(message)


def log_error(logger: logging.Logger, message: str, exc_info: bool = False, **kwargs) -> None:
    """
    记录错误日志
    
    Args:
        message: 错误消息
        exc_info: 是否记录异常堆栈
        kwargs: 额外信息
    """
    if kwargs:
        logger.error(f"{message} - {kwargs}", exc_info=exc_info)
    else:
        logger.error(message, exc_info=exc_info)


def log_critical(logger: logging.Logger, message: str, exc_info: bool = False, **kwargs) -> None:
    """
    记录严重错误日志
    
    Args:
        message: 错误消息
        exc_info: 是否记录异常堆栈
        kwargs: 额外信息
    """
    if kwargs:
        logger.critical(f"{message} - {kwargs}", exc_info=exc_info)
    else:
        logger.critical(message, exc_info=exc_info)
