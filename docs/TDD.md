# Todo Calendar - 技术设计文档 (TDD.md)

**版本**: v2.0  
**创建时间**: 2026-03-13  
**更新时间**: 2026-03-13 13:25  
**作者**: Arch 胡小架  
**状态**: DESIGNING  
**技术栈**: PyQt6 + SQLite + SQLAlchemy

---

## 1. 技术栈选型

### 1.1 UI 框架决策

| 选项 | Tkinter | PyQt6 |
|------|---------|-------|
| **月视图** | ✅ 可实现 | ✅ 优雅实现 |
| **周/日视图切换** | ⚠️ 复杂 | ✅ 原生支持 |
| **拖拽操作** | ⚠️ 需自定义 | ✅ 原生支持 (QDrag) |
| **搜索/过滤** | ✅ 可实现 | ✅ 优雅实现 |
| **统计图表** | ⚠️ 需第三方 | ✅ 集成方便 (QtCharts) |
| **开发速度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **UI 美观度** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 🎯 最终选择：**PyQt6**

**决策理由**:
1. **P1 功能支持**: 周/日视图、拖拽、统计等功能在 PyQt6 中有原生组件支持
2. **总工时更优**: 虽然 PyQt6 学习曲线稍高，但实现 P1 功能的总工时反而更低
3. **UI 美观度**: 支持 QSS 样式表，可实现现代化 UI，提升用户使用意愿
4. **长期维护**: 活跃社区，组件丰富，适合复杂交互场景
5. **打包可接受**: PyQt6 打包约 50-80MB，用户只需下载一次

### 1.2 完整技术栈

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| **UI 框架** | PyQt6 | 6.4+ | 图形界面，支持复杂视图 |
| **图表库** | PyQtGraph | 0.13+ | 统计图表（轻量级，无需额外依赖） |
| **编程语言** | Python | 3.9+ | 主开发语言 |
| **数据存储** | SQLite | 3.35+ | 本地数据库 |
| **ORM** | SQLAlchemy | 2.0+ | 数据库操作 |
| **日期处理** | python-dateutil | 2.8+ | 日历逻辑 |
| **打包工具** | PyInstaller | 6.0+ | 可执行文件生成 |

---

## 2. 系统架构设计

### 2.1 整体架构（支持 P0+P1）

```
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer (PyQt6)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ MonthView    │  │  WeekView    │  │  DayView     │          │
│  │ (QTableWidget)│  │ (QGridLayout)│  │ (QVBoxLayout)│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ SearchBar    │  │  FilterPanel │  │  StatsPanel  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    MainWindow (QMainWindow)               │  │
│  │  - 菜单栏：文件/编辑/视图/帮助                             │  │
│  │  - 工具栏：视图切换/搜索/过滤                             │  │
│  │  - 状态栏：任务统计/提醒状态                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ TaskService  │  │ SearchService│  │FilterService │          │
│  │ (CRUD)       │  │ (全文搜索)    │  │ (多条件过滤)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │RecurringTask │  │ReminderService│ │ StatsService │          │
│  │ (重复规则)    │  │ (到期检查)    │  │ (统计分析)    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    ViewManager                            │  │
│  │  - 视图切换逻辑（月/周/日）                                │  │
│  │  - 视图状态管理                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Data Access Layer (SQLite)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ tasks        │  │  categories  │  │ reminders    │          │
│  │ (任务表)      │  │  (分类表)     │  │  (提醒表)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │recurring_rules│  │  stats_cache │                             │
│  │ (重复规则表)   │  │  (统计缓存)   │                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 核心模块清单

| 模块类型 | 模块名 | 文件路径 | 优先级 | 工时 |
|----------|--------|----------|--------|------|
| **UI 层** | MainWindow | `src/ui/main_window.py` | P0 | 0.5h |
| **UI 层** | ViewManager | `src/ui/view_manager.py` | P0 | 0.5h |
| **UI 层** | MonthView | `src/ui/month_view.py` | P0 | 0.5h |
| **UI 层** | WeekView | `src/ui/week_view.py` | P1 | 1h |
| **UI 层** | DayView | `src/ui/day_view.py` | P1 | 0.75h |
| **UI 层** | SearchBar | `src/ui/search_bar.py` | P1 | 0.25h |
| **UI 层** | FilterPanel | `src/ui/filter_panel.py` | P1 | 0.5h |
| **UI 层** | StatsPanel | `src/ui/stats_panel.py` | P1 | 0.75h |
| **UI 层** | TaskDialog | `src/ui/task_dialog.py` | P0 | 0.5h |
| **UI 层** | RecurringDialog | `src/ui/recurring_dialog.py` | P1 | 0.5h |
| **UI 层** | ReminderDialog | `src/ui/reminder_dialog.py` | P1 | 0.25h |
| **服务层** | TaskService | `src/services/task_service.py` | P0 | 1h |
| **服务层** | SearchService | `src/services/search_service.py` | P1 | 1h |
| **服务层** | FilterService | `src/services/filter_service.py` | P1 | 0.75h |
| **服务层** | RecurringTask | `src/services/recurring_task.py` | P1 | 1h |
| **服务层** | ReminderService | `src/services/reminder_service.py` | P1 | 0.75h |
| **服务层** | StatsService | `src/services/stats_service.py` | P1 | 0.75h |
| **服务层** | Scheduler | `src/services/scheduler.py` | P1 | 0.5h |
| **模型层** | Task | `src/models/task.py` | P0 | 0.25h |
| **模型层** | Category | `src/models/category.py` | P0 | 0.25h |
| **模型层** | RecurringRule | `src/models/recurring_rule.py` | P1 | 0.5h |
| **模型层** | Reminder | `src/models/reminder.py` | P1 | 0.25h |
| **数据层** | Database | `src/database/db_manager.py` | P0 | 0.5h |
| **数据层** | Migrations | `src/database/migrations.py` | P1 | 0.5h |
| **配置** | Settings | `src/config/settings.py` | P0 | 0.25h |
| **入口** | Main | `src/main.py` | P0 | 0.25h |
| **测试** | Test Services | `tests/test_services.py` | P0 | 1h |
| **测试** | Test UI | `tests/test_ui.py` | P1 | 0.5h |
| **打包** | Build Spec | `build.spec` | P0 | 0.25h |
| **打包** | Start Script | `start.bat` | P0 | 0.25h |

**总计**: 30 个文件，预计 **13 小时** 开发完成

---

## 3. 数据模型设计

### 3.1 SQLite 表结构（P0+P1 完整版）

#### 表 1: tasks (任务表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 任务 ID |
| title | TEXT(200) | NOT NULL | 任务标题 |
| description | TEXT(1000) | | 任务描述 |
| due_date | DATE | NOT NULL | 截止日期 |
| priority | INTEGER | DEFAULT 1 | 优先级 (1=低，2=中，3=高) |
| status | INTEGER | DEFAULT 0 | 状态 (0=待办，1=进行中，2=已完成) |
| category_id | INTEGER | FOREIGN KEY | 分类 ID |
| parent_task_id | INTEGER | FOREIGN KEY | 父任务 ID（重复任务实例） |
| is_recurring | BOOLEAN | DEFAULT 0 | 是否为重复任务 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 更新时间 |
| completed_at | DATETIME | | 完成时间 |
| reminded_at | DATETIME | | 最后提醒时间 |

#### 表 2: categories (分类表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 分类 ID |
| name | TEXT(50) | NOT NULL UNIQUE | 分类名称 |
| color | TEXT(7) | DEFAULT '#CCCCCC' | 分类颜色 |
| icon | TEXT(20) | | 分类图标 |
| sort_order | INTEGER | DEFAULT 0 | 排序顺序 |

#### 表 3: recurring_rules (重复规则表) 🆕

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 规则 ID |
| task_id | INTEGER | FOREIGN KEY, NOT NULL | 任务 ID |
| frequency | TEXT(20) | NOT NULL | 频率 (daily/weekly/monthly/yearly) |
| interval | INTEGER | DEFAULT 1 | 间隔（如每 2 周） |
| days_of_week | TEXT(50) | | 周几重复 (1,3,5) |
| day_of_month | INTEGER | | 每月几号 |
| end_date | DATE | | 结束日期（可选） |
| occurrences | INTEGER | | 重复次数（可选） |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 表 4: reminders (提醒表) 🆕

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 提醒 ID |
| task_id | INTEGER | FOREIGN KEY, NOT NULL | 任务 ID |
| remind_at | DATETIME | NOT NULL | 提醒时间 |
| remind_before_minutes | INTEGER | DEFAULT 0 | 提前几分钟 |
| is_active | BOOLEAN | DEFAULT 1 | 是否激活 |
| triggered_at | DATETIME | | 实际触发时间 |

### 3.2 SQLAlchemy 模型定义

```python
# models/task.py
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
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
    parent_task_id = Column(Integer, ForeignKey('tasks.id'))
    is_recurring = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    completed_at = Column(DateTime)
    reminded_at = Column(DateTime)
    
    category = relationship("Category", back_populates="tasks")
    recurring_rule = relationship("RecurringRule", back_populates="task", uselist=False)
    reminders = relationship("Reminder", back_populates="task")

# models/recurring_rule.py
class RecurringRule(Base):
    __tablename__ = 'recurring_rules'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    frequency = Column(String(20), nullable=False)  # daily, weekly, monthly, yearly
    interval = Column(Integer, default=1)
    days_of_week = Column(String(50))  # e.g., "1,3,5" for Mon,Wed,Fri
    day_of_month = Column(Integer)
    end_date = Column(Date)
    occurrences = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    
    task = relationship("Task", back_populates="recurring_rule")

# models/reminder.py
class Reminder(Base):
    __tablename__ = 'reminders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    remind_at = Column(DateTime, nullable=False)
    remind_before_minutes = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    triggered_at = Column(DateTime)
    
    task = relationship("Task", back_populates="reminders")
```

---

## 4. P1 功能详细设计

### 4.1 视图切换（周/日视图）

**WeekView 实现**:
```python
# ui/week_view.py
class WeekView(QWidget):
    def __init__(self, task_service: TaskService):
        super().__init__()
        self.task_service = task_service
        self.layout = QGridLayout()
        
        # 星期标题行
        for i, day in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            label = QLabel(day)
            label.setStyleSheet("font-weight: bold; padding: 5px;")
            self.layout.addWidget(label, 0, i)
        
        # 时间列（00:00 - 23:00）
        for hour in range(24):
            time_label = QLabel(f"{hour:02d}:00")
            self.layout.addWidget(time_label, hour + 1, 0)
            
            # 每天的时间格子
            for day in range(7):
                cell = QWidget()
                cell.setAcceptDrops(True)  # 支持拖拽
                cell.setMinimumHeight(40)
                self.layout.addWidget(cell, hour + 1, day + 1)
```

**DayView 实现**:
```python
# ui/day_view.py
class DayView(QWidget):
    def __init__(self, task_service: TaskService):
        super().__init__()
        self.layout = QVBoxLayout()
        
        # 时间轴视图
        for hour in range(24):
            hour_widget = HourSlot(hour)
            hour_widget.task_dropped.connect(self.on_task_dropped)
            self.layout.addWidget(hour_widget)
```

**ViewManager 视图管理**:
```python
# ui/view_manager.py
class ViewManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_view = None
        self.views = {}
    
    def switch_view(self, view_type: str):
        """切换视图：month/week/day"""
        if self.current_view:
            self.current_view.hide()
        
        if view_type not in self.views:
            self.views[view_type] = self._create_view(view_type)
        
        self.current_view = self.views[view_type]
        self.current_view.show()
        self.main_window.setCentralWidget(self.current_view)
```

### 4.2 搜索服务

```python
# services/search_service.py
class SearchService:
    def __init__(self, db_session):
        self.db = db_session
    
    def search(self, query: str, fields: List[str] = None) -> List[Task]:
        """全文搜索任务"""
        if fields is None:
            fields = ['title', 'description']
        
        conditions = []
        for field in fields:
            conditions.append(getattr(Task, field).like(f'%{query}%'))
        
        return self.db.query(Task).filter(or_(*conditions)).all()
    
    def search_advanced(self, 
                       query: str = None,
                       priority: int = None,
                       status: int = None,
                       date_from: date = None,
                       date_to: date = None) -> List[Task]:
        """高级搜索（多条件组合）"""
        filters = []
        
        if query:
            filters.append(or_(
                Task.title.like(f'%{query}%'),
                Task.description.like(f'%{query}%')
            ))
        if priority:
            filters.append(Task.priority == priority)
        if status is not None:
            filters.append(Task.status == status)
        if date_from:
            filters.append(Task.due_date >= date_from)
        if date_to:
            filters.append(Task.due_date <= date_to)
        
        return self.db.query(Task).filter(and_(*filters)).all()
```

### 4.3 过滤服务

```python
# services/filter_service.py
class FilterService:
    def __init__(self, db_session):
        self.db = db_session
    
    def filter_by_priority(self, priority: int) -> List[Task]:
        """按优先级过滤"""
        return self.db.query(Task).filter(Task.priority == priority).all()
    
    def filter_by_status(self, status: int) -> List[Task]:
        """按状态过滤"""
        return self.db.query(Task).filter(Task.status == status).all()
    
    def filter_by_category(self, category_id: int) -> List[Task]:
        """按分类过滤"""
        return self.db.query(Task).filter(Task.category_id == category_id).all()
    
    def filter_by_date_range(self, start: date, end: date) -> List[Task]:
        """按日期范围过滤"""
        return self.db.query(Task).filter(
            Task.due_date >= start,
            Task.due_date <= end
        ).all()
    
    def apply_filters(self, filters: dict) -> List[Task]:
        """应用多个过滤条件"""
        query = self.db.query(Task)
        
        if 'priority' in filters:
            query = query.filter(Task.priority == filters['priority'])
        if 'status' in filters:
            query = query.filter(Task.status == filters['status'])
        if 'category_id' in filters:
            query = query.filter(Task.category_id == filters['category_id'])
        if 'date_from' in filters:
            query = query.filter(Task.due_date >= filters['date_from'])
        if 'date_to' in filters:
            query = query.filter(Task.due_date <= filters['date_to'])
        
        return query.all()
```

### 4.4 重复任务逻辑

```python
# services/recurring_task.py
from dateutil.relativedelta import relativedelta

class RecurringTaskService:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_recurring_rule(self, task_id: int, rule: dict) -> RecurringRule:
        """创建重复规则"""
        recurring_rule = RecurringRule(
            task_id=task_id,
            frequency=rule['frequency'],
            interval=rule.get('interval', 1),
            days_of_week=rule.get('days_of_week'),
            day_of_month=rule.get('day_of_month'),
            end_date=rule.get('end_date'),
            occurrences=rule.get('occurrences')
        )
        self.db.add(recurring_rule)
        self.db.commit()
        return recurring_rule
    
    def generate_next_occurrence(self, task: Task) -> Optional[Task]:
        """生成下一个重复实例"""
        rule = task.recurring_rule
        if not rule:
            return None
        
        # 检查是否已结束
        if rule.end_date and task.due_date >= rule.end_date:
            return None
        
        # 计算下一个日期
        next_date = self._calculate_next_date(task.due_date, rule)
        
        # 创建新任务实例
        new_task = Task(
            title=task.title,
            description=task.description,
            due_date=next_date,
            priority=task.priority,
            category_id=task.category_id,
            parent_task_id=task.id,
            is_recurring=True
        )
        
        self.db.add(new_task)
        self.db.commit()
        return new_task
    
    def _calculate_next_date(self, current_date: date, rule: RecurringRule) -> date:
        """计算下一个重复日期"""
        if rule.frequency == 'daily':
            return current_date + relativedelta(days=rule.interval)
        elif rule.frequency == 'weekly':
            return current_date + relativedelta(weeks=rule.interval)
        elif rule.frequency == 'monthly':
            return current_date + relativedelta(months=rule.interval)
        elif rule.frequency == 'yearly':
            return current_date + relativedelta(years=rule.interval)
```

### 4.5 提醒服务

```python
# services/reminder_service.py
class ReminderService:
    def __init__(self, db_session):
        self.db = db_session
        self.check_interval = 60000  # 每分钟检查一次
    
    def check_due_reminders(self) -> List[Reminder]:
        """检查需要触发的提醒"""
        now = datetime.now()
        
        reminders = self.db.query(Reminder).filter(
            Reminder.remind_at <= now,
            Reminder.is_active == True,
            Reminder.triggered_at == None
        ).all()
        
        return reminders
    
    def trigger_reminder(self, reminder: Reminder):
        """触发提醒"""
        task = reminder.task
        reminder.triggered_at = datetime.now()
        reminder.is_active = False
        self.db.commit()
        
        # 发送信号通知 UI 显示提醒对话框
        self.reminder_triggered.emit(task, reminder)
    
    def add_reminder(self, task_id: int, remind_at: datetime, 
                     remind_before_minutes: int = 0) -> Reminder:
        """添加提醒"""
        reminder = Reminder(
            task_id=task_id,
            remind_at=remind_at,
            remind_before_minutes=remind_before_minutes
        )
        self.db.add(reminder)
        self.db.commit()
        return reminder

# services/scheduler.py
class Scheduler:
    def __init__(self, reminder_service: ReminderService):
        self.reminder_service = reminder_service
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_reminders)
    
    def start(self):
        """启动定时检查"""
        self.timer.start(self.reminder_service.check_interval)
    
    def check_reminders(self):
        """检查提醒"""
        due_reminders = self.reminder_service.check_due_reminders()
        for reminder in due_reminders:
            self.reminder_service.trigger_reminder(reminder)
```

### 4.6 统计服务

```python
# services/stats_service.py
from sqlalchemy import func

class StatsService:
    def __init__(self, db_session):
        self.db = db_session
    
    def get_task_counts(self, start_date: date, end_date: date) -> dict:
        """获取时间段内任务统计"""
        total = self.db.query(func.count(Task.id)).filter(
            Task.due_date >= start_date,
            Task.due_date <= end_date
        ).scalar()
        
        completed = self.db.query(func.count(Task.id)).filter(
            Task.due_date >= start_date,
            Task.due_date <= end_date,
            Task.status == 2
        ).scalar()
        
        pending = total - completed
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': completed / total if total > 0 else 0
        }
    
    def get_priority_distribution(self, start_date: date, end_date: date) -> dict:
        """获取优先级分布"""
        results = self.db.query(
            Task.priority, func.count(Task.id)
        ).filter(
            Task.due_date >= start_date,
            Task.due_date <= end_date
        ).group_by(Task.priority).all()
        
        return {priority: count for priority, count in results}
    
    def get_category_stats(self, start_date: date, end_date: date) -> list:
        """获取分类统计"""
        results = self.db.query(
            Category.name, func.count(Task.id)
        ).join(Task).filter(
            Task.due_date >= start_date,
            Task.due_date <= end_date
        ).group_by(Category.id).all()
        
        return [{'name': name, 'count': count} for name, count in results]
    
    def get_weekly_trend(self, weeks: int = 4) -> list:
        """获取近几周趋势"""
        today = date.today()
        trend = []
        
        for i in range(weeks):
            week_start = today - timedelta(days=(i * 7 + 6))
            week_end = today - timedelta(days=(i * 7))
            
            stats = self.get_task_counts(week_start, week_end)
            trend.append({
                'week': f'Week {weeks - i}',
                'completed': stats['completed'],
                'pending': stats['pending']
            })
        
        return trend
```

---

## 5. UI 界面原型设计

### 5.1 主界面布局（支持视图切换）

```
┌─────────────────────────────────────────────────────────────────────┐
│  Todo Calendar                                    [—][□][×]         │
├─────────────────────────────────────────────────────────────────────┤
│  [File] [Edit] [View] [Help]                                        │
├─────────────────────────────────────────────────────────────────────┤
│  [📅 Month] [📆 Week] [📋 Day]     [🔍 Search...] [🔽 Filter ▼]    │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────────────────────────────────┐  │
│  │              │  │  ◄  March 2026  ►                           │  │
│  │  Categories  │  │  ┌───┬───┬───┬───┬───┬───┬───┐             │  │
│  │  ──────────  │  │  │Mon│Tue│Wed│Thu│Fri│Sat│Sun│             │  │
│  │  ☑ All       │  │  ├───┼───┼───┼───┼───┼───┼───┤             │  │
│  │  🏠 Work     │  │  │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │             │  │
│  │  🏠 Personal │  │  ├───┼───┼───┼───┼───┼───┼───┤             │  │
│  │  🛒 Shopping │  │  │ 8 │ 9 │10 │11 │12 │13 │14 │             │  │
│  │  📚 Learning │  │  ├───┼───┼───┼───┼───┼───┼───┤             │  │
│  │              │  │  │15 │16 │17 │18 │19 │20 │21 │             │  │
│  │  [+ Add Cat] │  │  └───┴───┴───┴───┴───┴───┴───┘             │  │
│  └──────────────┘  └─────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│  Today's Tasks (March 13)                      [+ Add] [📊 Stats]   │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ ☐ [High]   Submit project proposal                  🏠 Work   │  │
│  │ ☐ [Medium] Buy groceries                             🛒 Shop  │  │
│  │ ✓ [Low]    Read chapter 3                             📚 Learn│  │
│  └───────────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│  Tasks: 15 | Completed: 8 | Pending: 7 | 🔔 Next: 14:00            │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 统计面板原型

```
┌─────────────────────────────────────┐
│  📊 Task Statistics                 │
├─────────────────────────────────────┤
│  This Week (Mar 10-16)              │
│  ┌─────────────────────────────┐   │
│  │ ████████░░  8/10 completed   │   │
│  │ 80% completion rate         │   │
│  └─────────────────────────────┘   │
│                                     │
│  By Priority:                       │
│  🔴 High:   3 tasks                 │
│  🟡 Medium: 5 tasks                 │
│  🟢 Low:    2 tasks                 │
│                                     │
│  By Category:                       │
│  🏠 Work:      6 tasks              │
│  🛒 Shopping:  2 tasks              │
│  📚 Learning:  2 tasks              │
│                                     │
│  [Close]                            │
└─────────────────────────────────────┘
```

---

## 6. 拖拽操作实现

### 6.1 拖拽任务修改日期

```python
# ui/task_item.py
class TaskItem(QLabel):
    def __init__(self, task: Task):
        super().__init__(task.title)
        self.task = task
        self.setDragEnabled(True)
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setData('task/id', str(self.task.id).encode())
            drag.setMimeData(mime)
            drag.exec(Qt.MoveAction)

# ui/calendar_cell.py
class CalendarCell(QTableWidget):
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('task/id'):
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        task_id = int(event.mimeData().data('task/id').data())
        new_date = self.current_date
        
        # 调用服务更新任务日期
        self.task_service.update_task_date(task_id, new_date)
        event.acceptProposedAction()
```

---

## 7. 项目目录结构（完整版）

```
todo-calendar/
├── main.py                        # 应用入口
├── requirements.txt               # Python 依赖
├── build.spec                     # PyInstaller 打包配置
├── start.bat                      # Windows 启动脚本
├── README.md                      # 项目说明
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # 应用启动
│   │
│   ├── ui/                        # UI 组件
│   │   ├── __init__.py
│   │   ├── main_window.py         # 主窗口
│   │   ├── view_manager.py        # 视图管理器 🆕
│   │   ├── month_view.py          # 月视图
│   │   ├── week_view.py           # 周视图 🆕
│   │   ├── day_view.py            # 日视图 🆕
│   │   ├── task_list.py           # 任务列表
│   │   ├── task_dialog.py         # 任务对话框
│   │   ├── recurring_dialog.py    # 重复任务对话框 🆕
│   │   ├── reminder_dialog.py     # 提醒对话框 🆕
│   │   ├── search_bar.py          # 搜索栏 🆕
│   │   ├── filter_panel.py        # 过滤面板 🆕
│   │   ├── stats_panel.py         # 统计面板 🆕
│   │   ├── category_panel.py      # 分类面板
│   │   ├── task_item.py           # 任务项（可拖拽）
│   │   └── calendar_cell.py       # 日历格子（可 Drop）
│   │
│   ├── services/                  # 业务逻辑
│   │   ├── __init__.py
│   │   ├── task_service.py        # 任务服务
│   │   ├── search_service.py      # 搜索服务 🆕
│   │   ├── filter_service.py      # 过滤服务 🆕
│   │   ├── recurring_task.py      # 重复任务服务 🆕
│   │   ├── reminder_service.py    # 提醒服务 🆕
│   │   ├── stats_service.py       # 统计服务 🆕
│   │   └── scheduler.py           # 定时调度器 🆕
│   │
│   ├── models/                    # 数据模型
│   │   ├── __init__.py
│   │   ├── task.py                # 任务模型
│   │   ├── category.py            # 分类模型
│   │   ├── recurring_rule.py      # 重复规则模型 🆕
│   │   └── reminder.py            # 提醒模型 🆕
│   │
│   ├── database/                  # 数据库层
│   │   ├── __init__.py
│   │   ├── db_manager.py          # 数据库管理
│   │   ├── init_db.py             # 初始化脚本
│   │   └── migrations.py          # 数据库迁移 🆕
│   │
│   └── config/                    # 配置
│       ├── __init__.py
│       └── settings.py            # 应用配置 🆕
│
├── assets/                        # 资源文件
│   ├── icons/                     # 图标
│   └── styles/                    # QSS 样式表
│
├── tests/                         # 测试
│   ├── __init__.py
│   ├── test_task_service.py
│   ├── test_services.py           # 服务测试 🆕
│   └── test_ui.py                 # UI 测试 🆕
│
└── docs/                          # 文档
    ├── PRD.md
    ├── TDD.md                     # 本文件
    └── USER_GUIDE.md
```

---

## 8. 开发里程碑（P0+P1 完整版）

| 阶段 | 任务 | 预计工时 | 交付物 |
|------|------|----------|--------|
| **Phase 1** | 项目骨架 + 数据库 + 模型 | 2h | 可运行空壳 |
| **Phase 2** | 主窗口 + 月视图 + 任务 CRUD | 3h | P0 核心功能 |
| **Phase 3** | 周视图 + 日视图 + 视图切换 | 2.5h | P1 视图功能 |
| **Phase 4** | 搜索 + 过滤服务 | 1.75h | P1 搜索过滤 |
| **Phase 5** | 重复任务逻辑 | 2h | P1 重复任务 |
| **Phase 6** | 提醒服务 + 定时检查 | 1.25h | P1 提醒功能 |
| **Phase 7** | 统计服务 + 统计面板 | 1.5h | P1 统计功能 |
| **Phase 8** | 样式优化 + 打包 | 2h | 可执行文件 |
| **总计** | | **16h** | 完整应用 |

---

## 9. 依赖清单

```txt
# requirements.txt
PyQt6>=6.4.0
PyQt6-Qt6>=6.4.0
SQLAlchemy>=2.0.0
python-dateutil>=2.8.0
pyqtgraph>=0.13.0
PyInstaller>=6.0.0
```

---

## 10. 风险与应对

| 风险 | 概率 | 影响 | 应对方案 |
|------|------|------|----------|
| PyQt6 学习曲线 | 中 | 中 | 参考官方示例，优先实现核心功能 |
| 拖拽功能兼容性 | 低 | 中 | 准备备选方案（右键菜单修改日期） |
| PyInstaller 打包失败 | 中 | 高 | 提前测试打包流程，准备备用方案 |
| 数据库迁移问题 | 低 | 中 | 使用 Alembic 管理数据库版本 |
| 时间不足 | 高 | 高 | 优先保证 P0，P1 功能分优先级实现 |

---

## 11. 验收标准

### P0 功能验收
- [ ] 应用可独立运行 (无需 Python 环境)
- [ ] 月视图正确显示月份/日期
- [ ] 任务 CRUD 操作流畅无卡顿
- [ ] 拖拽修改日期功能正常
- [ ] 数据持久化可靠 (重启不丢失)
- [ ] 打包后文件大小 < 100MB
- [ ] 启动时间 < 3 秒

### P1 功能验收
- [ ] 周视图/日视图切换流畅
- [ ] 搜索功能支持模糊搜索
- [ ] 过滤功能支持多条件组合
- [ ] 重复任务自动创建实例
- [ ] 到期提醒准时触发
- [ ] 统计面板数据准确

---

**设计评审**: ✅ 已完成  
**评审人**: Arch 胡小架  
**批准进入开发**: ✅ 等待 PM 确认  
**下一步**: 通知 PM 和开发团队开始实现

---

## 附录 A: P0+P1 功能覆盖矩阵

| 功能 ID | 功能名称 | 实现模块 | 状态 |
|---------|----------|----------|------|
| P0-1 | 日历视图 | MonthView | ✅ |
| P0-2 | 双击创建 | TaskDialog | ✅ |
| P0-3 | 拖拽修改 | QDrag + QDropEvent | ✅ |
| P0-4 | 任务 CRUD | TaskService | ✅ |
| P0-5 | 优先级 | Task.priority + 样式 | ✅ |
| P0-6 | 完成状态 | Task.status | ✅ |
| P0-7 | 数据持久化 | SQLite + SQLAlchemy | ✅ |
| P0-8 | 开箱即用 | PyInstaller | ✅ |
| P1-1 | 周/日视图 | WeekView + DayView | 🆕 |
| P1-2 | 搜索 | SearchService | 🆕 |
| P1-3 | 过滤 | FilterService | 🆕 |
| P1-4 | 重复任务 | RecurringTask | 🆕 |
| P1-5 | 提醒 | ReminderService + Scheduler | 🆕 |
| P1-6 | 统计 | StatsService + StatsPanel | 🆕 |

**P0 完成度**: 8/8 (100%)  
**P1 完成度**: 6/6 (设计完成，待开发)  
**总计**: 14/14 功能覆盖

---

**文档结束**
