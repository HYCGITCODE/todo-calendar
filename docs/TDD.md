# Todo Calendar - 技术设计文档 (TDD.md)

**版本**: v1.0  
**创建时间**: 2026-03-13  
**作者**: Arch Agent  
**状态**: DESIGNING

---

## 1. 技术栈选型

### 1.1 前端框架选择

| 选项 | Tkinter | PyQt5/PyQt6 |
|------|---------|-------------|
| **学习曲线** | 低 | 中 |
| **UI 美观度** | 一般 | 优秀 |
| **跨平台** | ✅ | ✅ |
| **社区支持** | 官方标准库 | 活跃社区 |
| **打包大小** | ~30MB | ~50MB |
| **开发效率** | 高 | 中 |

### 🎯 最终选择：**PyQt6**

**理由**:
1. **UI 美观度优先**: Todo Calendar 作为个人效率工具，良好的视觉体验能提升使用意愿
2. **现代化组件**: PyQt6 支持 QML、灵活样式表，可实现日历视图的优雅展示
3. **长期维护**: 活跃的社区和持续更新，比 Tkinter 更适合复杂 UI 需求
4. **打包成熟**: PyInstaller 对 PyQt6 支持完善

### 1.2 完整技术栈

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| **前端** | Python | 3.9+ | 主开发语言 |
| **UI 框架** | PyQt6 | 6.4+ | 图形界面 |
| **数据存储** | SQLite | 3.35+ | 本地数据库 |
| **ORM** | SQLAlchemy | 2.0+ | 数据库操作 |
| **打包工具** | PyInstaller | 6.0+ | 可执行文件生成 |
| **日期处理** | python-dateutil | 2.8+ | 日历逻辑 |

---

## 2. 系统架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────┐
│              Presentation Layer             │
│  ┌─────────────┐  ┌─────────────────────┐  │
│  │ MainWindow  │  │   Dialog Components │  │
│  │  (QMainWindow)│  │  (TaskDialog, etc) │  │
│  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│              Business Logic Layer           │
│  ┌─────────────┐  ┌─────────────────────┐  │
│  │ TaskManager │  │   CalendarManager   │  │
│  │  (CRUD)     │  │   (View Logic)      │  │
│  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────┐
│              Data Access Layer              │
│  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Database   │  │      Models         │  │
│  │  (SQLite)   │  │   (SQLAlchemy)      │  │
│  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 2.2 核心模块划分

| 模块 | 文件 | 职责 |
|------|------|------|
| **UI 层** | `ui/main_window.py` | 主窗口、菜单栏、状态栏 |
| **UI 层** | `ui/calendar_view.py` | 日历网格视图组件 |
| **UI 层** | `ui/task_dialog.py` | 任务创建/编辑对话框 |
| **UI 层** | `ui/task_list.py` | 任务列表视图 |
| **业务层** | `services/task_service.py` | 任务 CRUD 逻辑 |
| **业务层** | `services/calendar_service.py` | 日历视图逻辑 |
| **数据层** | `models/task.py` | 任务数据模型 |
| **数据层** | `database/db_manager.py` | 数据库连接管理 |
| **入口** | `main.py` | 应用启动入口 |

---

## 3. 数据模型设计

### 3.1 SQLite 表结构

#### 表 1: tasks (任务表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 任务 ID |
| title | TEXT | NOT NULL | 任务标题 |
| description | TEXT | | 任务描述 |
| due_date | DATE | NOT NULL | 截止日期 |
| priority | INTEGER | DEFAULT 1 | 优先级 (1=低，2=中，3=高) |
| status | INTEGER | DEFAULT 0 | 状态 (0=待办，1=进行中，2=已完成) |
| category | TEXT | | 分类标签 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 更新时间 |
| completed_at | DATETIME | | 完成时间 |

#### 表 2: categories (分类表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 分类 ID |
| name | TEXT | NOT NULL UNIQUE | 分类名称 |
| color | TEXT | DEFAULT '#CCCCCC' | 分类颜色 (十六进制) |
| icon | TEXT | | 分类图标 (emoji 或路径) |
| sort_order | INTEGER | DEFAULT 0 | 排序顺序 |

### 3.2 SQLAlchemy 模型定义

```python
# models/task.py
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    due_date = Column(Date, nullable=False)
    priority = Column(Integer, default=1)  # 1=Low, 2=Medium, 3=High
    status = Column(Integer, default=0)  # 0=Todo, 1=In Progress, 2=Done
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    completed_at = Column(DateTime)
    
    category = relationship("Category", back_populates="tasks")

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    color = Column(String(7), default='#CCCCCC')
    icon = Column(String(20))
    sort_order = Column(Integer, default=0)
    
    tasks = relationship("Task", back_populates="category")
```

---

## 4. UI 界面原型设计

### 4.1 主界面布局

```
┌─────────────────────────────────────────────────────────────┐
│  Todo Calendar                                    [—][□][×] │
├─────────────────────────────────────────────────────────────┤
│  [File] [Edit] [View] [Help]                                │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────────────────────────┐  │
│  │              │  │  ◄  March 2026  ►                   │  │
│  │  Categories  │  │  ┌───┬───┬───┬───┬───┬───┬───┐     │  │
│  │  ──────────  │  │  │Mon│Tue│Wed│Thu│Fri│Sat│Sun│     │  │
│  │  ☑ All       │  │  ├───┼───┼───┼───┼───┼───┼───┤     │  │
│  │  🏠 Work     │  │  │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │     │  │
│  │  🏠 Personal │  │  ├───┼───┼───┼───┼───┼───┼───┤     │  │
│  │  🛒 Shopping │  │  │ 8 │ 9 │10 │11 │12 │13 │14 │     │  │
│  │  📚 Learning │  │  ├───┼───┼───┼───┼───┼───┼───┤     │  │
│  │              │  │  │15 │16 │17 │18 │19 │20 │21 │     │  │
│  │  [+ Add Cat] │  │  └───┴───┴───┴───┴───┴───┴───┘     │  │
│  └──────────────┘  └─────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Today's Tasks (March 13)                          [+ Add]  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ ☐ [High]   Submit project proposal          🏠 Work   │  │
│  │ ☐ [Medium] Buy groceries                     🛒 Shop  │  │
│  │ ✓ [Low]    Read chapter 3                     📚 Learn│  │
│  └───────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Tasks: 15 | Completed: 8 | Pending: 7                      │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 核心界面组件

| 组件 | PyQt6 类 | 说明 |
|------|----------|------|
| 主窗口 | QMainWindow | 应用主框架 |
| 日历网格 | QTableWidget | 月视图日历展示 |
| 任务列表 | QListWidget | 当日任务列表 |
| 分类树 | QTreeWidget | 左侧分类导航 |
| 任务对话框 | QDialog | 任务创建/编辑弹窗 |
| 优先级选择 | QComboBox | 高/中/低优先级 |
| 日期选择 | QDateEdit | 截止日期选择器 |

### 4.3 交互流程

#### 创建任务流程
```
用户点击 [+ Add] 
    ↓
弹出 TaskDialog (模态对话框)
    ↓
填写：标题、描述、日期、优先级、分类
    ↓
点击 [Save]
    ↓
TaskService.create_task()
    ↓
数据库插入 + UI 刷新
    ↓
关闭对话框
```

#### 完成任务流程
```
用户点击任务复选框
    ↓
TaskService.update_status(task_id, COMPLETED)
    ↓
数据库更新 completed_at
    ↓
UI 标记为完成 (删除线 + 灰色)
    ↓
状态栏计数更新
```

---

## 5. 项目目录结构

```
todo-calendar/
├── main.py                    # 应用入口
├── requirements.txt           # Python 依赖
├── setup.py                   # 打包配置
├── README.md                  # 项目说明
│
├── src/
│   ├── __init__.py
│   ├── ui/                    # UI 组件
│   │   ├── __init__.py
│   │   ├── main_window.py     # 主窗口
│   │   ├── calendar_view.py   # 日历视图
│   │   ├── task_list.py       # 任务列表
│   │   ├── task_dialog.py     # 任务对话框
│   │   └── category_panel.py  # 分类面板
│   │
│   ├── services/              # 业务逻辑
│   │   ├── __init__.py
│   │   ├── task_service.py    # 任务服务
│   │   └── calendar_service.py# 日历服务
│   │
│   ├── models/                # 数据模型
│   │   ├── __init__.py
│   │   ├── task.py            # 任务模型
│   │   └── category.py        # 分类模型
│   │
│   └── database/              # 数据库层
│       ├── __init__.py
│       ├── db_manager.py      # 数据库管理
│       └── init_db.py         # 初始化脚本
│
├── assets/                    # 资源文件
│   ├── icons/                 # 图标
│   └── styles/                # QSS 样式表
│
├── tests/                     # 测试
│   ├── __init__.py
│   ├── test_task_service.py
│   └── test_database.py
│
└── docs/                      # 文档
    ├── PRD.md
    ├── TDD.md
    └── USER_GUIDE.md
```

---

## 6. 关键实现细节

### 6.1 数据库初始化

```python
# database/init_db.py
from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "sqlite:///todo_calendar.db"

def init_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine
```

### 6.2 日历视图渲染

```python
# ui/calendar_view.py
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QDate

class CalendarView(QTableWidget):
    def render_month(self, year: int, month: int):
        # 计算当月天数
        days_in_month = QDate(year, month, 1).daysInMonth()
        # 设置网格
        self.setRowCount(6)
        self.setColumnCount(7)
        # 填充日期
        for day in range(1, days_in_month + 1):
            item = QTableWidgetItem(str(day))
            # 查询当天任务数，添加角标
            task_count = self.get_task_count(year, month, day)
            if task_count > 0:
                item.setText(f"{day}\n({task_count})")
```

### 6.3 PyInstaller 打包配置

```python
# setup.py / spec file
from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],
    hiddenimports=collect_submodules('PyQt6'),
    ...
)
```

---

## 7. 开发里程碑

| 阶段 | 任务 | 预计工时 | 交付物 |
|------|------|----------|--------|
| **Phase 1** | 项目骨架 + 数据库 | 2h | 可运行空壳 |
| **Phase 2** | 主窗口 + 日历视图 | 3h | 日历可切换月份 |
| **Phase 3** | 任务 CRUD | 3h | 任务可增删改查 |
| **Phase 4** | 分类系统 | 1h | 分类管理功能 |
| **Phase 5** | 样式优化 + 打包 | 2h | 可执行文件 |
| **总计** | | **11h** | 完整应用 |

---

## 8. 风险与应对

| 风险 | 概率 | 影响 | 应对方案 |
|------|------|------|----------|
| PyQt6 学习曲线 | 中 | 中 | 参考官方示例，优先实现核心功能 |
| 日历渲染性能 | 低 | 低 | 使用 QTableWidget 虚拟化，仅渲染可见区域 |
| PyInstaller 打包失败 | 中 | 高 | 提前测试打包流程，准备备用方案 (cx_Freeze) |
| 数据库迁移问题 | 低 | 中 | 使用 Alembic 管理数据库版本 |

---

## 9. 验收标准

- [ ] 应用可独立运行 (无需 Python 环境)
- [ ] 任务 CRUD 操作流畅无卡顿
- [ ] 日历视图正确显示月份/日期
- [ ] 数据持久化可靠 (重启不丢失)
- [ ] 打包后文件大小 < 100MB
- [ ] 启动时间 < 3 秒

---

**设计评审**: ⏳ 待评审  
**评审人**: PM, QA  
**批准进入开发**: ⏳ 等待批准
