#!/usr/bin/env python3
"""
Todo Calendar - 主入口文件

一个简洁高效的个人任务管理工具
基于 PyQt6 + SQLite
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.config.logging_config import setup_logging
from src.database.db_manager import init_database, check_database_connection
from src.ui.main_window import MainWindow

# 获取日志记录器
logger = logging.getLogger(__name__)


def main():
    """应用入口函数"""
    try:
        # 初始化日志系统
        setup_logging(level='INFO', log_to_file=True)
        logger.info("=" * 50)
        logger.info("Todo Calendar 应用启动")
        logger.info("=" * 50)
        
        # 检查数据库连接
        if not check_database_connection():
            logger.error("数据库连接检查失败")
            return 1
        logger.info("数据库连接检查通过")
        
        # 初始化数据库
        init_database()
        logger.info("数据库初始化完成")
        
    except Exception as e:
        logger.critical(f"应用初始化失败：{e}", exc_info=True)
        return 1
    
    try:
        # 创建应用实例
        app = QApplication(sys.argv)
        
        # 设置应用信息
        app.setApplicationName("Todo Calendar")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("HuXiaodou")
        
        # 设置全局样式
        app.setStyle("Fusion")
        
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        logger.info("主窗口已显示")
        
        # 运行事件循环
        exit_code = app.exec()
        logger.info(f"应用退出，退出码：{exit_code}")
        return exit_code
        
    except Exception as e:
        logger.critical(f"应用运行错误：{e}", exc_info=True)
        return 1
    finally:
        logger.info("应用关闭")


if __name__ == "__main__":
    main()
