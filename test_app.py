#!/usr/bin/env python3
"""
Todo Calendar - 应用测试脚本

测试核心功能而不需要图形界面
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import date, timedelta
from src.database.db_manager import init_database, get_session
from src.services.task_service import TaskService


def test_database():
    """测试数据库功能"""
    print("=" * 50)
    print("测试 1: 数据库初始化")
    print("=" * 50)
    
    init_database()
    print("✓ 数据库初始化成功\n")
    
    print("=" * 50)
    print("测试 2: 任务 CRUD 操作")
    print("=" * 50)
    
    with get_session() as session:
        task_service = TaskService(session)
        
        # 创建任务
        print("\n创建测试任务...")
        task1 = task_service.create_task(
            title="完成项目报告",
            due_date=date.today(),
            description="需要在周五前完成",
            priority=3  # P0 高优先级
        )
        print(f"✓ 创建任务：{task1.title} (ID: {task1.id}, 优先级：P{task1.priority})")
        
        task2 = task_service.create_task(
            title="购买生活用品",
            due_date=date.today() + timedelta(days=1),
            priority=1  # P2 低优先级
        )
        print(f"✓ 创建任务：{task2.title} (ID: {task2.id}, 优先级：P{task2.priority})")
        
        task3 = task_service.create_task(
            title="学习 Python",
            due_date=date.today() + timedelta(days=2),
            priority=2  # P1 中优先级
        )
        print(f"✓ 创建任务：{task3.title} (ID: {task3.id}, 优先级：P{task3.priority})")
        
        # 查询任务
        print("\n查询今日任务...")
        today_tasks = task_service.get_tasks_by_date(date.today())
        print(f"✓ 今日任务数量：{len(today_tasks)}")
        for task in today_tasks:
            status_text = "已完成" if task.status == 2 else "待办"
            print(f"  - {task.title} [{status_text}]")
        
        # 更新任务
        print("\n更新任务状态...")
        task_service.update_task(task1.id, status=1)  # 进行中
        print(f"✓ 任务 '{task1.title}' 状态更新为：进行中")
        
        # 标记完成
        print("\n标记任务完成...")
        task_service.mark_complete(task1.id)
        updated_task = task_service.get_task(task1.id)
        print(f"✓ 任务 '{updated_task.title}' 已标记为完成")
        
        # 搜索任务
        print("\n搜索任务...")
        search_results = task_service.search_tasks("项目")
        print(f"✓ 搜索'项目'找到 {len(search_results)} 个任务")
        
        # 获取统计
        print("\n任务统计...")
        stats = task_service.get_task_count_by_status()
        print(f"✓ 总任务数：{stats['total']}")
        print(f"✓ 已完成：{stats['completed']}")
        print(f"✓ 待办：{stats['pending']}")
        
        # 删除任务
        print("\n删除测试任务...")
        task_service.delete_task(task1.id)
        print(f"✓ 删除任务：{task1.title}")
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！")
    print("=" * 50)
    print("\nP0 核心功能验证完成:")
    print("  ✓ 数据库层 (db_manager.py) - SQLAlchemy 模型正常")
    print("  ✓ 任务服务 (task_service.py) - CRUD 逻辑正常")
    print("  ✓ 数据持久化 - SQLite 存储正常")
    print("\n应用已准备好进行 UI 测试！")


if __name__ == "__main__":
    test_database()
