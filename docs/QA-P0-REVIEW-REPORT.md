# QA 评审报告 - P0 核心功能

**评审人**: 胡小测 (QA)  
**评审日期**: 2026-03-13 13:45  
**评审类型**: 并行评审 - Phase 1 P0 功能  
**评审状态**: ⚠️ 有条件通过

---

## 评审概况

| 项目 | 状态 |
|------|------|
| **代码审查** | ✅ 完成 |
| **功能测试** | ⚠️ 部分完成 (环境限制) |
| **问题记录** | ✅ 完成 |
| **评审结论** | ⚠️ 有条件通过 (需解决环境依赖) |

---

## P0 功能评审结果

### P0-1 日历视图 ✅ 通过

**验收标准**: 月视图正常显示，任务列表可见

**代码审查**:
- ✅ `src/ui/calendar_view.py` 实现完整
- ✅ 使用 QTableWidget 渲染 6x7 日历网格
- ✅ 支持月份切换 (◄/►按钮)
- ✅ 显示当月任务数量标记
- ✅ 标记今天、选中日期、周末
- ✅ 显示前后月日期 (灰色)

**实现细节**:
```python
# 日历表格渲染
self.calendar_table = QTableWidget()
self.calendar_table.setRowCount(6)
self.calendar_table.setColumnCount(7)
# 任务数量显示
item.setText(f"{day}\n({len(tasks)})")
```

**结论**: 代码逻辑完整，功能实现正确。

---

### P0-2 双击创建 ✅ 通过

**验收标准**: 双击弹出创建对话框，3 步内完成

**代码审查**:
- ✅ `calendar_view.py` 实现双击信号: `date_double_clicked`
- ✅ `main_window.py` 连接信号: `_add_task_on_date()`
- ✅ `task_dialog.py` 实现创建对话框
- ✅ 3 步流程：填写标题 → 选择日期 → 保存

**实现细节**:
```python
# 双击创建任务
def _on_cell_double_clicked(self, row: int, col: int):
    if item and item.text().isdigit():
        self.date_double_clicked.emit(current_date)

# 主窗口响应
self.calendar_view.date_double_clicked.connect(self._add_task_on_date)
```

**结论**: 交互流程清晰，实现正确。

---

### P0-3 拖拽修改 ✅ 通过

**验收标准**: 拖拽后任务日期立即更新

**代码审查**:
- ✅ `task_list.py` 实现拖拽启动 (`mouseMoveEvent`)
- ✅ 使用 QDrag 和 QMimeData 传递 task_id
- ✅ `calendar_view.py` 实现拖拽接受 (`dragEnterEvent`, `dropEvent`)
- ✅ `main_window.py` 实现回调 `_on_task_dropped()`
- ✅ 更新任务日期并刷新列表

**实现细节**:
```python
# 拖拽启动
mime_data.setData('task/id', str(self.task.id).encode())
drag.setMimeData(mime_data)

# 拖拽接受
if event.mimeData().hasFormat('task/id'):
    task_id = int(event.mimeData().data('task/id').data())
    self.on_task_dropped(task_id, new_date)
```

**结论**: 拖拽逻辑完整，但需要注意:
- ⚠️ 拖拽视觉反馈可以优化 (当前仅显示默认光标)
- ⚠️ 缺少拖拽取消功能 (按 ESC 取消)

---

### P0-4 任务 CRUD ✅ 通过

**验收标准**: 创建/查看/编辑/删除正常

**代码审查**:
- ✅ **Create**: `task_service.create_task()`
- ✅ **Read**: `task_service.get_task()`, `get_tasks_by_date()`
- ✅ **Update**: `task_service.update_task()`
- ✅ **Delete**: `task_service.delete_task()`
- ✅ UI 层: `task_dialog.py` 支持新建/编辑模式
- ✅ 右键菜单支持删除

**实现细节**:
```python
# 创建任务
def create_task(self, title: str, due_date: date, ...) -> Task:
    task = Task(title=title, due_date=due_date, ...)
    self.session.add(task)
    self.session.commit()

# 删除任务 (右键菜单)
delete_action.triggered.connect(lambda: self._delete_task(widget.task.id))
```

**结论**: CRUD 功能完整实现。

---

### P0-5 优先级管理 ✅ 通过

**验收标准**: P0/P1/P2 颜色区分正确

**代码审查**:
- ✅ `task.py` 模型: `priority` 字段 (1=低，2=中，3=高)
- ✅ `task_list.py` 实现颜色编码:
  - P0 高：红色背景 `#FEE2E2`, 边框 `#EF4444`
  - P1 中：黄色背景 `#FEF3C7`, 边框 `#F59E0B`
  - P2 低：绿色背景 `#D1FAE5`, 边框 `#10B981`
- ✅ 优先级标签显示 (P0 高/P1 中/P2 低)
- ✅ 高优先级任务标题加粗

**实现细节**:
```python
self.priority_colors = {
    3: {'bg': '#FEE2E2', 'border': '#EF4444', 'text': '#EF4444'},  # P0 高
    2: {'bg': '#FEF3C7', 'border': '#F59E0B', 'text': '#F59E0B'},  # P1 中
    1: {'bg': '#D1FAE5', 'border': '#10B981', 'text': '#10B981'},  # P2 低
}
```

**结论**: 优先级颜色区分清晰，符合验收标准。

---

### P0-6 完成状态 ✅ 通过

**验收标准**: 复选框标记，删除线显示

**代码审查**:
- ✅ `task.py` 模型: `status` 字段 (0=待办，1=进行中，2=已完成)
- ✅ `task.py` 实现 `mark_complete()` 方法
- ✅ `task_list.py` 实现复选框组件
- ✅ 已完成任务显示删除线 + 灰色
- ✅ 复选框状态与任务状态同步

**实现细节**:
```python
# 已完成样式
if task.status == 2:
    title_label.setStyleSheet("color: #999; text-decoration: line-through;")

# 复选框连接
self.checkbox.setChecked(task.status == 2)
widget.checkbox.toggled.connect(
    lambda checked, t=task: self.task_completed.emit(t.id, checked)
)
```

**结论**: 完成状态功能完整。

---

### P0-7 数据持久化 ✅ 通过

**验收标准**: 关闭重开数据不丢失

**代码审查**:
- ✅ 使用 SQLite 数据库 (`data/todo_calendar.db`)
- ✅ SQLAlchemy ORM 模型定义
- ✅ 数据库初始化: `db_manager.init_database()`
- ✅ 会话管理: `get_session()` 上下文管理器
- ✅ 自动创建默认分类

**实现细节**:
```python
DATABASE_URL = f"sqlite:///{os.path.join(DATABASE_DIR, 'todo_calendar.db')}"
engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(bind=engine)
```

**结论**: 数据持久化方案正确。

**⚠️ 测试限制**: 由于环境 Python 版本 (3.6.8) 与 PyQt6 要求 (3.8+) 不兼容，无法运行完整测试。建议升级 Python 环境后验证。

---

### P0-8 开箱即用 ⚠️ 部分通过

**验收标准**: PyInstaller 打包配置就绪

**代码审查**:
- ✅ `todo_calendar.spec` 配置文件存在
- ✅ 包含必要的 hiddenimports (PyQt6, sqlalchemy)
- ✅ 包含 assets 目录
- ✅ 配置 windowed 模式 (console=False)

**实现细节**:
```python
a = Analysis(
    ['main.py'],
    hiddenimports=[
        'PyQt6', 'sqlalchemy', 'sqlalchemy.dialects.sqlite',
    ],
    datas=[('assets', 'assets')],
)
```

**⚠️ 问题**:
1. 未测试实际打包过程 (环境限制)
2. 建议添加打包脚本: `scripts/build.sh` / `scripts/build.bat`
3. 建议在 README 中添加打包说明

**结论**: 配置文件就绪，但缺少打包脚本和文档。

---

## 发现问题清单

### 严重问题 (P0)

| ID | 问题描述 | 影响 | 建议 |
|----|----------|------|------|
| BUG-001 | Python 环境版本不兼容 | 无法运行/测试 | 升级系统 Python 至 3.10+ 或使用 conda/pyenv |

### 一般问题 (P1)

| ID | 问题描述 | 影响 | 建议 |
|----|----------|------|------|
| BUG-002 | 拖拽视觉反馈不足 | 用户体验差 | 添加拖拽预览高亮目标日期格子 |
| BUG-003 | 缺少拖拽取消功能 | 误操作无法撤销 | 支持 ESC 键取消拖拽 |
| BUG-004 | 缺少打包脚本 | 用户打包困难 | 添加 scripts/build.sh 和 build.bat |
| BUG-005 | 编辑任务缺少双击响应 | 交互不一致 | `task_list.py` 中实现双击编辑 |

### 优化建议 (P2)

| ID | 建议 | 优先级 |
|----|------|--------|
| OPT-001 | 添加任务计数缓存，避免频繁查询数据库 | P2 |
| OPT-002 | 添加键盘快捷键 (Ctrl+N 新建，Ctrl+S 保存) | P2 |
| OPT-003 | 添加任务搜索功能 | P2 |
| OPT-004 | 添加数据导出功能 (CSV/JSON) | P2 |

---

## 测试覆盖率

| 模块 | 文件 | 审查状态 | 测试状态 |
|------|------|----------|----------|
| **UI 层** | main_window.py | ✅ 完成 | ⚠️ 未运行 |
| | calendar_view.py | ✅ 完成 | ⚠️ 未运行 |
| | task_list.py | ✅ 完成 | ⚠️ 未运行 |
| | task_dialog.py | ✅ 完成 | ⚠️ 未运行 |
| **服务层** | task_service.py | ✅ 完成 | ✅ 代码审查通过 |
| **数据层** | db_manager.py | ✅ 完成 | ✅ 代码审查通过 |
| **模型层** | task.py | ✅ 完成 | ✅ 代码审查通过 |

---

## 评审结论

### ✅ 通过项 (7/8)
- P0-1 日历视图 ✅
- P0-2 双击创建 ✅
- P0-3 拖拽修改 ✅
- P0-4 任务 CRUD ✅
- P0-5 优先级管理 ✅
- P0-6 完成状态 ✅
- P0-7 数据持久化 ✅

### ⚠️ 有条件通过项 (1/8)
- P0-8 开箱即用 ⚠️ (缺少打包脚本和文档)

### 总体结论: **⚠️ 有条件通过**

**条件**:
1. 升级 Python 环境至 3.10+ 后验证功能
2. 补充打包脚本和文档
3. 修复 P1 问题 (拖拽视觉反馈、取消功能)

---

## 后续行动

### 立即执行 (P0)
- [ ] **FE+BE**: 升级 Python 环境并运行完整测试
- [ ] **PM**: 确认打包流程文档需求

### 本周内 (P1)
- [ ] **FE**: 优化拖拽视觉反馈
- [ ] **FE**: 添加拖拽取消功能
- [ ] **FE**: 添加双击任务编辑功能
- [ ] **FE**: 创建打包脚本

### 下次迭代 (P2)
- [ ] **FE**: 添加键盘快捷键
- [ ] **FE**: 实现任务搜索
- [ ] **FE**: 实现数据导出

---

## 发送给

- **PM**: 胡小产 - 进度协调
- **FE+BE**: 胡小前 - 功能修复
- **OCA**: 胡小豆 - 审计备案

---

**评审耗时**: 25 分钟  
**评审方式**: 代码审查 + 静态分析  
**测试环境限制**: Python 3.6.8 (需升级至 3.10+)
