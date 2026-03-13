# Todo Calendar - 详细开发计划

## 📅 项目时间线

**项目启动**: 2026-03-13 00:02  
**当前状态**: PLANNING 阶段（08:26-08:56）  
**目标交付**: 2026-03-13 13:26（总计 13 小时 24 分钟）

---

## 🎯 阶段概览

| 阶段 | 时长 | 时间段 | 完成标准 |
|------|------|--------|----------|
| **PLANNING** | 30min | 08:26-08:56 | ✅ PRD 定稿 + GitHub 仓库就绪 |
| **DESIGNING** | 45min | 08:56-09:41 | TDD.md + UI 原型 + 数据库设计 |
| **DEVING** | 2.5h | 09:41-12:11 | P0 功能全部可演示 |
| **TESTING** | 45min | 12:11-12:56 | 测试报告 + Bug 修复 |
| **PACKAGING** | 30min | 12:56-13:26 | start.bat + exe 打包完成 |

---

## 🏗️ DESIGNING 阶段任务（08:56-09:41）

### 交付物清单
- [ ] TDD.md（技术设计文档）
- [ ] 数据库 schema 设计
- [ ] UI 原型草图
- [ ] 模块接口定义

### 数据库设计（SQLite）

```sql
-- 任务表
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,              -- 任务标题
    description TEXT,                  -- 任务描述
    priority INTEGER DEFAULT 1,        -- 0=P0(高), 1=P1(中), 2=P2(低)
    due_date DATE NOT NULL,            -- 计划日期
    completed BOOLEAN DEFAULT 0,       -- 完成状态
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 重复规则表（P1 功能预留）
CREATE TABLE recurrence_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    frequency TEXT,                    -- 'daily', 'weekly', 'monthly'
    interval INTEGER DEFAULT 1,
    end_date DATE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- 索引优化
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

### 模块架构

```
todo-calendar/
├── main.py                  # 程序入口（初始化 + 启动主窗口）
├── gui/
│   ├── __init__.py
│   ├── main_window.py       # 主窗口（包含菜单栏、工具栏）
│   ├── calendar_view.py     # 日历视图核心组件
│   ├── task_dialog.py       # 任务创建/编辑对话框
│   └── widgets.py           # 自定义控件（优先级标签、完成复选框）
├── models/
│   ├── __init__.py
│   └── task.py              # Task 数据类（CRUD 操作）
├── storage/
│   ├── __init__.py
│   └── database.py          # 数据库连接 + SQL 操作
└── utils/
    ├── __init__.py
    └── helpers.py           # 工具函数（日期格式化等）
```

### 核心类设计

```python
# Task 数据模型
@dataclass
class Task:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    priority: int = 1  # 0=P0, 1=P1, 2=P2
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    
    # 方法
    def toggle_complete(self) -> None: ...
    def to_dict(self) -> dict: ...
    @classmethod
    def from_dict(cls, data: dict) -> 'Task': ...

# 数据库操作类
class Database:
    def __init__(self, db_path: str = "tasks.db"): ...
    def create_task(self, task: Task) -> int: ...  # 返回 task_id
    def get_tasks_by_date(self, date: date) -> List[Task]: ...
    def update_task_date(self, task_id: int, new_date: date) -> None: ...
    def delete_task(self, task_id: int) -> None: ...

# 日历视图组件
class CalendarView(tk.Canvas):
    def __init__(self, parent, db: Database): ...
    def render_month(self, year: int, month: int) -> None: ...
    def _draw_day_cell(self, day: int, tasks: List[Task]) -> None: ...
    def _enable_drag_drop(self) -> None: ...
```

---

## 💻 DEVING 阶段详细任务（09:41-12:11）

### 时间盒 1: 数据库层（09:41-10:11, 30min）
**负责人**: BE  
**任务**:
- [ ] 创建 `storage/database.py` - Database 类
- [ ] 创建 `models/task.py` - Task 数据类
- [ ] 实现数据库初始化（建表 + 索引）
- [ ] 实现 CRUD 基础方法
- [ ] 编写简单测试（创建/读取任务）

**验收标准**:
```python
db = Database("test.db")
task = Task(title="测试任务", priority=0, due_date=date.today())
task_id = db.create_task(task)
tasks = db.get_tasks_by_date(date.today())
assert len(tasks) == 1
```

### 时间盒 2: 日历 UI（10:11-10:41, 30min）
**负责人**: FE  
**任务**:
- [ ] 创建 `gui/main_window.py` - 主窗口框架
- [ ] 创建 `gui/calendar_view.py` - 日历视图
- [ ] 实现月视图渲染（7 列 x 5-6 行）
- [ ] 显示星期标题（一/二/三/四/五/六/日）
- [ ] 标注周末（灰色背景）

**验收标准**:
- 窗口大小 800x600
- 能正确显示当前月份的日历格子
- 周末格子有视觉区分

### 时间盒 3: 任务创建（10:41-11:11, 30min）
**负责人**: FE  
**任务**:
- [ ] 创建 `gui/task_dialog.py` - 任务对话框
- [ ] 实现双击日历格子弹出对话框
- [ ] 对话框包含：标题输入框、优先级下拉框、描述文本框
- [ ] 点击保存后写入数据库
- [ ] 刷新日历视图显示新任务

**验收标准**:
- 双击任意日期格子弹出对话框
- 输入标题后保存，日历上显示任务标签
- 数据持久化（重启后仍存在）

### 时间盒 4: 拖拽功能（11:11-11:41, 30min）
**负责人**: FE+BE  
**任务**:
- [ ] 实现任务标签的拖拽开始事件
- [ ] 实现拖拽过程中的视觉反馈（半透明跟随）
- [ ] 实现拖拽释放到目标日期格子
- [ ] 调用数据库更新任务日期
- [ ] 刷新 UI 显示

**验收标准**:
- 拖拽任务到另一个日期，任务立即移动
- 数据库同步更新
- 拖拽过程流畅（无明显卡顿）

### 时间盒 5: 优先级 + 联调（11:41-12:11, 30min）
**负责人**: FE+BE  
**任务**:
- [ ] 实现优先级颜色（P0 红色、P1 黄色、P2 绿色）
- [ ] 实现完成状态复选框（点击打钩）
- [ ] 实现任务编辑（右键菜单或双击已存在任务）
- [ ] 实现任务删除功能
- [ ] 全功能联调测试

**验收标准**:
- 所有 P0 功能可流畅演示
- 无崩溃、无数据丢失
- 代码提交到 GitHub

---

## 🧪 TESTING 阶段任务（12:11-12:56）

### 测试用例清单

| ID | 测试项 | 测试步骤 | 预期结果 |
|----|--------|----------|----------|
| T01 | 创建任务 | 双击日期→输入标题→保存 | 任务显示在日历上 |
| T02 | 拖拽修改 | 拖拽任务到另一日期 | 任务移动到目标日期 |
| T03 | 优先级显示 | 创建 P0/P1/P2 任务各一个 | 颜色正确区分 |
| T04 | 完成状态 | 点击任务复选框 | 显示删除线，状态保存 |
| T05 | 数据持久化 | 创建任务→关闭程序→重新打开 | 任务仍存在 |
| T06 | 删除任务 | 右键任务→删除 | 任务从日历消失 |
| T07 | 跨月显示 | 切换到下个月 | 日历正确显示 |
| T08 | 边界测试 | 创建 100+ 任务 | 程序不卡顿，UI 正常 |

### 自测报告模板
```markdown
## 测试结果

- **总测试用例**: 8
- **通过**: X
- **失败**: Y
- **阻塞**: Z

### Bug 清单
| 严重程度 | 描述 | 复现步骤 |
|----------|------|----------|
| Critical | ... | ... |
| Major | ... | ... |
| Minor | ... | ... |
```

---

## 📦 PACKAGING 阶段任务（12:56-13:26）

### 打包流程

1. **安装依赖**
```bash
pip install pyinstaller
```

2. **创建打包脚本** `build.py`
```python
import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--windowed',
    '--name=TodoCalendar',
    '--icon=assets/icons/app.ico',
    '--add-data=assets;assets',
])
```

3. **创建启动脚本** `start.bat`
```batch
@echo off
start "" "TodoCalendar.exe"
exit
```

4. **执行打包**
```bash
python build.py
```

5. **测试打包结果**
- 在未安装 Python 的机器上测试
- 验证双击 start.bat 能启动
- 验证核心功能正常

### 交付物检查清单
- [ ] `dist/TodoCalendar.exe`
- [ ] `start.bat`
- [ ] `README.md`（包含使用说明）
- [ ] 测试视频/GIF（可选）

---

## 🚨 应急预案

### 如果时间不足（优先级调整）

**方案 A**（剩余 2 小时）:
- 砍掉拖拽功能，改用右键菜单修改日期
- 只做月视图，周/日视图延期
- 保证 P0-1 到 P0-8 核心功能

**方案 B**（剩余 1 小时）:
- 只做任务创建 + 日历显示
- 拖拽和优先级简化处理
- 先交付可用版本，后续迭代

### 技术备选方案

| 问题 | 原方案 | 备选方案 |
|------|--------|----------|
| Tkinter 拖拽复杂 | Canvas 拖拽 | 改用按钮 + 日期选择器 |
| PyInstaller 打包失败 | 单文件 exe | 多文件目录 + 快捷方式 |
| SQLite 并发问题 | 文件锁 | 简化为单线程访问 |

---

## 📊 进度追踪

更新时间：2026-03-13 08:56

| 阶段 | 计划开始 | 实际开始 | 计划完成 | 状态 |
|------|----------|----------|----------|------|
| PLANNING | 08:26 | 08:26 | 08:56 | ✅ 完成 |
| DESIGNING | 08:56 | - | 09:41 | 🔄 待开始 |
| DEVING | 09:41 | - | 12:11 | ⏳ 待开始 |
| TESTING | 12:11 | - | 12:56 | ⏳ 待开始 |
| PACKAGING | 12:56 | - | 13:26 | ⏳ 待开始 |

---

**文档创建时间**: 2026-03-13 08:56  
**最后更新**: 2026-03-13 08:56  
**下一步**: 移交给 Arch 胡小架进行技术设计评审
