#!/usr/bin/env python3
"""
测试打包后的应用程序

运行此脚本验证：
1. 所有模块可以正常导入
2. 数据库可以正常初始化
3. UI 组件可以正常加载
"""

import sys
import os

def test_imports():
    """测试所有必要模块的导入"""
    print("测试模块导入...")
    
    try:
        import PyQt6.QtWidgets
        print("✓ PyQt6.QtWidgets")
    except ImportError as e:
        print(f"✗ PyQt6.QtWidgets: {e}")
        return False
    
    try:
        import PyQt6.QtCore
        print("✓ PyQt6.QtCore")
    except ImportError as e:
        print(f"✗ PyQt6.QtCore: {e}")
        return False
    
    try:
        import PyQt6.QtGui
        print("✓ PyQt6.QtGui")
    except ImportError as e:
        print(f"✗ PyQt6.QtGui: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✓ SQLAlchemy")
    except ImportError as e:
        print(f"✗ SQLAlchemy: {e}")
        return False
    
    try:
        import dateutil
        print("✓ python-dateutil")
    except ImportError as e:
        print(f"✗ python-dateutil: {e}")
        return False
    
    return True


def test_database():
    """测试数据库初始化"""
    print("\n测试数据库初始化...")
    
    try:
        from src.database.db_manager import init_database, get_session
        init_database()
        print("✓ 数据库初始化成功")
        
        # 测试会话
        with get_session() as session:
            print("✓ 数据库会话正常")
        
        return True
    except Exception as e:
        print(f"✗ 数据库测试失败：{e}")
        return False


def test_ui():
    """测试 UI 组件"""
    print("\n测试 UI 组件...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow
        
        app = QApplication(sys.argv)
        window = MainWindow()
        print("✓ 主窗口创建成功")
        
        # 不显示窗口，仅测试创建
        # window.show()
        
        return True
    except Exception as e:
        print(f"✗ UI 测试失败：{e}")
        return False


def test_assets():
    """测试资源文件"""
    print("\n测试资源文件...")
    
    assets = [
        'assets/styles/default.qss',
    ]
    
    all_exist = True
    for asset in assets:
        if os.path.exists(asset):
            print(f"✓ {asset}")
        else:
            print(f"✗ {asset} (不存在)")
            all_exist = False
    
    return all_exist


def main():
    """运行所有测试"""
    print("=" * 50)
    print("Todo Calendar - 打包测试")
    print("=" * 50)
    
    results = []
    
    # 切换到项目目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    results.append(("模块导入", test_imports()))
    results.append(("资源文件", test_assets()))
    results.append(("数据库", test_database()))
    results.append(("UI 组件", test_ui()))
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计：{passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！可以开始打包。")
        return 0
    else:
        print("\n⚠️  部分测试失败，请修复后再打包。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
