#!/usr/bin/env python3
"""
清空测试数据脚本

使用方法:
python scripts/clear_test_data.py
"""

import os
import sys

# 切换到项目目录
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(script_dir)

print("=" * 50)
print("清空测试数据")
print("=" * 50)
print()

try:
    from src.database.db_manager import get_session, engine
    from src.models import Base, Task, Category, Reminder, RecurringTask
    from sqlalchemy import text
    
    with get_session() as session:
        # 删除所有任务
        task_count = session.query(Task).count()
        session.query(Task).delete()
        print(f"✅ 已删除 {task_count} 个任务")
        
        # 删除所有提醒
        reminder_count = session.query(Reminder).count()
        session.query(Reminder).delete()
        print(f"✅ 已删除 {reminder_count} 个提醒")
        
        # 删除所有重复任务
        recurring_count = session.query(RecurringTask).count()
        session.query(RecurringTask).delete()
        print(f"✅ 已删除 {recurring_count} 个重复任务")
        
        # 保留分类，但可以重置
        category_count = session.query(Category).count()
        print(f"ℹ️  保留 {category_count} 个分类")
        
        session.commit()
        
    print()
    print("=" * 50)
    print("✅ 测试数据已清空！")
    print("=" * 50)
    print()
    print("提示：重新启动应用后，数据库将只包含默认分类。")
    
except Exception as e:
    print(f"❌ 清空数据失败：{e}")
    sys.exit(1)
