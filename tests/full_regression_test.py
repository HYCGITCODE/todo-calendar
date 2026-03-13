#!/usr/bin/env python3
"""
Todo Calendar - 完整功能回归测试

测试所有 P0+P1 功能
"""

import sys
import os

# 切换到项目目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("=" * 60)
print("Todo Calendar - 完整功能回归测试")
print("=" * 60)
print()

# 测试 1: 模块导入
print("[1/10] 测试模块导入...")
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import QDate
    from src.database.db_manager import init_database, get_session, check_database_connection
    from src.models import Task, Category, Reminder, RecurringTask
    from src.services.task_service import TaskService
    from src.services.search_service import SearchService
    from src.services.filter_service import FilterService
    from src.services.reminder_service import ReminderService
    from src.services.stats_service import StatsService
    from src.ui.main_window import MainWindow
    from src.ui.calendar_view import CalendarView
    from src.ui.week_view import WeekView
    from src.ui.day_view import DayView
    from src.ui.task_dialog import TaskDialog
    from src.ui.search_bar import SearchBar
    print("✅ 所有模块导入成功")
except Exception as e:
    print(f"❌ 模块导入失败：{e}")
    sys.exit(1)

# 测试 2: 数据库连接
print("\n[2/10] 测试数据库连接...")
try:
    if check_database_connection():
        print("✅ 数据库连接正常")
    else:
        print("❌ 数据库连接失败")
        sys.exit(1)
except Exception as e:
    print(f"❌ 数据库连接测试失败：{e}")
    sys.exit(1)

# 测试 3: 数据库初始化
print("\n[3/10] 测试数据库初始化...")
try:
    init_database()
    print("✅ 数据库初始化成功")
except Exception as e:
    print(f"❌ 数据库初始化失败：{e}")
    sys.exit(1)

# 测试 4: TaskService CRUD
print("\n[4/10] 测试任务 CRUD 操作...")
try:
    with get_session() as session:
        task_service = TaskService(session)
        
        # 创建任务
        task = task_service.create_task(
            title="测试任务",
            description="回归测试",
            due_date=QDate.currentDate().toPyDate(),
            priority=2,
            category_id=1
        )
        print(f"  ✅ 创建任务：ID={task.id}")
        
        # 查询任务
        retrieved_task = task_service.get_task(task.id)
        assert retrieved_task.title == "测试任务"
        print(f"  ✅ 查询任务：{retrieved_task.title}")
        
        # 更新任务
        task_service.update_task(task.id, title="更新后的任务")
        updated_task = task_service.get_task(task.id)
        assert updated_task.title == "更新后的任务"
        print(f"  ✅ 更新任务：{updated_task.title}")
        
        # 标记完成
        task_service.mark_task_completed(task.id, True)
        completed_task = task_service.get_task(task.id)
        assert completed_task.status == 2
        print(f"  ✅ 标记完成：status={completed_task.status}")
        
        # 删除任务
        task_service.delete_task(task.id)
        deleted_task = task_service.get_task(task.id)
        assert deleted_task is None
        print(f"  ✅ 删除任务：ID={task.id}")
        
except Exception as e:
    print(f"❌ 任务 CRUD 测试失败：{e}")
    sys.exit(1)

# 测试 5: 搜索服务
print("\n[5/10] 测试搜索服务...")
try:
    with get_session() as session:
        search_service = SearchService(session)
        
        # 创建测试数据
        task = search_service._create_test_task("搜索测试任务")
        
        # 搜索
        results = search_service.search("搜索")
        assert len(results) > 0
        print(f"  ✅ 搜索功能：找到 {len(results)} 个结果")
        
        # 清理
        search_service._delete_test_task(task.id)
        
except Exception as e:
    print(f"❌ 搜索服务测试失败：{e}")
    sys.exit(1)

# 测试 6: 过滤服务
print("\n[6/10] 测试过滤服务...")
try:
    with get_session() as session:
        filter_service = FilterService(session)
        
        # 测试优先级过滤
        tasks = filter_service.filter_by_priority(2)
        print(f"  ✅ 优先级过滤：P1 任务 {len(tasks)} 个")
        
        # 测试状态过滤
        tasks = filter_service.filter_by_status(0)
        print(f"  ✅ 状态过滤：未完成 {len(tasks)} 个")
        
except Exception as e:
    print(f"❌ 过滤服务测试失败：{e}")
    sys.exit(1)

# 测试 7: 提醒服务
print("\n[7/10] 测试提醒服务...")
try:
    with get_session() as session:
        reminder_service = ReminderService(session)
        
        # 获取今日提醒
        reminders = reminder_service.get_todays_reminders()
        print(f"  ✅ 今日提醒：{len(reminders)} 个")
        
except Exception as e:
    print(f"❌ 提醒服务测试失败：{e}")
    sys.exit(1)

# 测试 8: 统计服务
print("\n[8/10] 测试统计服务...")
try:
    with get_session() as session:
        stats_service = StatsService(session)
        
        # 获取本周统计
        stats = stats_service.get_week_stats()
        print(f"  ✅ 本周统计：完成 {stats.get('completed', 0)} 个")
        
        # 获取月度统计
        stats = stats_service.get_month_stats()
        print(f"  ✅ 本月统计：完成 {stats.get('completed', 0)} 个")
        
except Exception as e:
    print(f"❌ 统计服务测试失败：{e}")
    sys.exit(1)

# 测试 9: UI 组件创建
print("\n[9/10] 测试 UI 组件创建...")
try:
    app = QApplication(sys.argv)
    
    # 测试主窗口
    main_window = MainWindow()
    print("  ✅ 主窗口创建成功")
    
    # 测试日历视图
    with get_session() as session:
        task_service = TaskService(session)
        calendar_view = CalendarView(task_service)
        print("  ✅ 日历视图创建成功")
        
        # 测试周视图
        week_view = WeekView(task_service)
        print("  ✅ 周视图创建成功")
        
        # 测试日视图
        day_view = DayView(task_service)
        print("  ✅ 日视图创建成功")
        
        # 测试搜索栏
        search_bar = SearchBar()
        print("  ✅ 搜索栏创建成功")
        
        # 测试任务对话框
        task_dialog = TaskDialog(task_service)
        print("  ✅ 任务对话框创建成功")
    
except Exception as e:
    print(f"❌ UI 组件测试失败：{e}")
    sys.exit(1)

# 测试 10: 删除任务专项测试
print("\n[10/10] 测试删除任务功能...")
try:
    with get_session() as session:
        task_service = TaskService(session)
        
        # 创建任务
        task = task_service.create_task(
            title="删除测试任务",
            due_date=QDate.currentDate().toPyDate()
        )
        task_id = task.id
        print(f"  ✅ 创建测试任务：ID={task_id}")
        
        # 删除任务
        result = task_service.delete_task(task_id)
        assert result is True
        print(f"  ✅ 删除任务成功：ID={task_id}")
        
        # 验证已删除
        deleted_task = task_service.get_task(task_id)
        assert deleted_task is None
        print(f"  ✅ 验证删除：任务已不存在")
        
except Exception as e:
    print(f"❌ 删除任务测试失败：{e}")
    sys.exit(1)

# 总结
print()
print("=" * 60)
print("✅ 所有测试通过！")
print("=" * 60)
print()
print("测试覆盖:")
print("  - 模块导入 ✅")
print("  - 数据库连接 ✅")
print("  - 数据库初始化 ✅")
print("  - 任务 CRUD ✅")
print("  - 搜索服务 ✅")
print("  - 过滤服务 ✅")
print("  - 提醒服务 ✅")
print("  - 统计服务 ✅")
print("  - UI 组件 ✅")
print("  - 删除任务 ✅")
print()
print("可以安全运行应用！")
