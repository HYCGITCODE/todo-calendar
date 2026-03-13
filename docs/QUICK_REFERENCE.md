# P0+P1 开发准备 - 快速参考

**创建时间**: 2026-03-13 13:45  
**状态**: ✅ 准备完成

---

## 📦 新增模块速查

### 服务层 (导入即用)

```python
from src.services import (
    SearchService,      # 搜索服务
    FilterService,      # 过滤服务
    ReminderService,    # 提醒服务
    StatsService,       # 统计服务
)

# 使用示例
search_service = SearchService(session)
results = search_service.search_by_keyword("任务")

filter_service = FilterService(session)
pending_tasks = filter_service.filter_by_status(0)

reminder_service = ReminderService(session)
overdue = reminder_service.get_overdue()

stats_service = StatsService(session)
stats = stats_service.get_basic_stats()
```

### UI 组件 (导入即用)

```python
from src.ui import (
    SearchBar,      # 搜索栏
    StatsPanel,     # 统计面板
    WeekView,       # 周视图
    DayView,        # 日视图
)

# 使用示例
search_bar = SearchBar()
search_bar.search_triggered.connect(self._on_search)

stats_panel = StatsPanel()
stats_panel.update_stats(stats_data)

week_view = WeekView(task_service)
week_view.date_selected.connect(self._on_date_selected)
```

### 模型层

```python
from src.models import (
    Task,             # 任务模型
    Category,         # 分类模型
    RecurringTask,    # 重复任务模型
    RecurrenceType,   # 重复类型枚举
)

# 重复任务示例
recurring = RecurringTask(
    title="每日站会",
    recurrence_type=RecurrenceType.DAILY,
    start_date=date.today()
)
next_date = recurring.get_next_occurrence()
```

---

## 🔧 关键 API

### SearchService

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `search_by_keyword` | keyword: str | List[Task] | 关键词搜索 |
| `search_by_category` | category_id: int | List[Task] | 分类搜索 |
| `search_by_priority` | priority: int | List[Task] | 优先级搜索 |
| `advanced_search` | 多条件 | List[Task] | 高级搜索 |

### FilterService

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `filter_by_category` | category_id, tasks | List[Task] | 分类过滤 |
| `filter_by_priority` | priority, tasks | List[Task] | 优先级过滤 |
| `filter_by_status` | status, tasks | List[Task] | 状态过滤 |
| `filter_overdue` | tasks | List[Task] | 逾期过滤 |
| `filter_today` | tasks | List[Task] | 今日过滤 |
| `apply_multiple_filters` | 多条件 | List[Task] | 多条件过滤 |

### ReminderService

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `get_due_today` | - | List[Task] | 今天到期 |
| `get_due_tomorrow` | - | List[Task] | 明天到期 |
| `get_overdue` | - | List[Task] | 逾期任务 |
| `get_reminder_summary` | - | dict | 提醒摘要 |
| `generate_daily_reminder_message` | - | str | 每日提醒消息 |

### StatsService

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `get_basic_stats` | - | dict | 基础统计 |
| `get_stats_by_priority` | - | dict | 优先级统计 |
| `get_stats_by_category` | - | List[dict] | 分类统计 |
| `get_weekly_stats` | - | dict | 周统计 |
| `get_monthly_stats` | - | dict | 月统计 |
| `get_productivity_score` | - | int | 生产力得分 |
| `get_full_report` | - | dict | 完整报告 |

---

## 🎨 UI 组件信号

### SearchBar

```python
search_triggered = pyqtSignal(str)      # 搜索关键词
filter_changed = pyqtSignal(dict)       # 过滤条件变化
clear_search = pyqtSignal()             # 清除搜索
```

### StatsPanel

```python
# 无信号，纯展示组件
# 调用 update_stats(stats_data) 更新数据
```

### WeekView

```python
date_selected = pyqtSignal(QDate)       # 日期选择
week_changed = pyqtSignal(int, int)     # 年份，周数
```

### DayView

```python
date_selected = pyqtSignal(QDate)       # 日期选择
task_requested = pyqtSignal(int)        # 请求编辑任务 ID
```

---

## 📝 集成步骤

### 1. 添加搜索栏到 MainWindow

```python
# 在 _init_ui 中添加
from src.ui.search_bar import SearchBar

self.search_bar = SearchBar()
self.search_bar.search_triggered.connect(self._on_search_triggered)
self.search_bar.filter_changed.connect(self._on_filter_changed)
main_layout.insertWidget(0, self.search_bar)  # 添加到顶部
```

### 2. 添加统计面板到 MainWindow

```python
# 在 _init_ui 中添加
from src.ui.stats_panel import StatsPanel

self.stats_panel = StatsPanel()
# 添加到侧边栏或底部
```

### 3. 添加视图切换

```python
# 在 MainWindow 中添加视图切换按钮
from src.ui.week_view import WeekView
from src.ui.day_view import DayView

self.week_view = WeekView(self.task_service)
self.day_view = DayView(self.task_service)

# 使用 QStackedWidget 切换视图
self.view_stack = QStackedWidget()
self.view_stack.addWidget(self.calendar_view)
self.view_stack.addWidget(self.week_view)
self.view_stack.addWidget(self.day_view)
```

---

## ✅ 检查清单

### 开发前检查
- [x] 所有模块语法正确
- [x] 所有导入路径正确
- [x] 单元测试已编写
- [x] 文档已更新

### 集成检查
- [ ] SearchBar 集成
- [ ] StatsPanel 集成
- [ ] WeekView 集成
- [ ] DayView 集成
- [ ] 视图切换功能
- [ ] 搜索功能连接
- [ ] 过滤功能连接
- [ ] 统计更新机制

### 测试检查
- [ ] 运行 test_p1_services.py
- [ ] 手动测试搜索功能
- [ ] 手动测试过滤功能
- [ ] 手动测试统计面板
- [ ] 手动测试周/日视图

### 打包检查
- [ ] 运行 PyInstaller
- [ ] 测试可执行文件
- [ ] 验证所有功能正常

---

## 🐛 常见问题

### Q: 导入失败怎么办？
A: 检查 `__init__.py` 是否正确导出模块

### Q: UI 组件不显示？
A: 确保调用了 `show()` 或添加到布局中

### Q: 信号不触发？
A: 检查信号连接是否正确，对象是否被垃圾回收

### Q: 数据库表不存在？
A: 运行 `init_database()` 创建所有表

---

## 📞 支持

**FE 胡小前**: UI 组件相关问题  
**BE 胡小后**: 服务层和模型层相关问题

---

**准备完成，随时开始开发！** 🚀
