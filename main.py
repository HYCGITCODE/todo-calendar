#!/usr/bin/env python3
"""
Todo Calendar - 主入口文件

一个简洁高效的个人任务管理工具
基于 PyQt6 + SQLite
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.database.db_manager import init_database
from src.ui.main_window import MainWindow


def main():
    """应用入口函数"""
    # 初始化数据库
    init_database()
    
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
    
    # 运行事件循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
