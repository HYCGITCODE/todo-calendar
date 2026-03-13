# Todo Calendar - 安装与部署指南

> 📅 一个简洁高效的桌面待办任务管理工具，支持日历视图、拖拽操作、任务统计

---

## 📋 目录

1. [项目简介](#项目简介)
2. [系统要求](#系统要求)
3. [快速开始](#快速开始)
4. [开发环境部署](#开发环境部署)
5. [生产环境打包](#生产环境打包)
6. [使用说明](#使用说明)
7. [常见问题](#常见问题)
8. [技术栈](#技术栈)

---

## 项目简介

**Todo Calendar** 是一款开箱即用的桌面待办任务管理工具，通过直观的日历视图管理任务，支持：

- ✅ **月/周/日视图** - 多种时间粒度查看任务
- ✅ **双击创建** - 日历格子双击快速创建任务
- ✅ **拖拽修改** - 拖拽任务到其他日期
- ✅ **任务 CRUD** - 创建、查看、编辑、删除
- ✅ **优先级管理** - P0/P1/P2 三级优先级，颜色区分
- ✅ **任务搜索** - 全文搜索，实时结果
- ✅ **任务过滤** - 按优先级/状态过滤
- ✅ **重复任务** - 每周/每月自动重复
- ✅ **到期提醒** - 任务到期自动提醒
- ✅ **数据统计** - 完成数统计面板
- ✅ **数据持久化** - SQLite 本地存储
- ✅ **开箱即用** - PyInstaller 打包，双击启动

---

## 系统要求

### 最低配置
| 项目 | 要求 |
|------|------|
| **操作系统** | Windows 10/11 (64 位) |
| **Python 版本** | 3.8+ (推荐 3.10+) |
| **内存** | 512 MB |
| **磁盘空间** | 200 MB |

### 开发环境
| 项目 | 要求 |
|------|------|
| **Python** | 3.10+ |
| **Git** | 2.0+ |
| **IDE** | VS Code / PyCharm (可选) |

---

## 快速开始

### 方式一：下载可执行文件 (推荐)

1. **下载**
   - 从 [GitHub Releases](https://github.com/HYCGITCODE/todo-calendar/releases) 下载最新版本
   - 或联系开发者获取 `Todo Calendar.exe`

2. **解压**
   ```
   解压到任意目录，如：D:\Apps\Todo Calendar\
   ```

3. **启动**
   ```
   双击 start.bat 或 Todo Calendar.exe
   ```

**无需安装 Python 环境，开箱即用！** ✅

---

### 方式二：从源码运行

1. **克隆仓库**
   ```bash
   git clone https://github.com/HYCGITCODE/todo-calendar.git
   cd todo-calendar
   ```

2. **创建虚拟环境**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **启动应用**
   ```bash
   python main.py
   ```

---

## 开发环境部署

### 1. 环境准备

```bash
# 检查 Python 版本 (需要 3.8+)
python --version

# 检查 Git
git --version
```

### 2. 克隆项目

```bash
git clone https://github.com/HYCGITCODE/todo-calendar.git
cd todo-calendar
```

### 3. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 4. 验证安装

```bash
# 运行测试
python -m pytest tests/ -v

# 启动应用
python main.py
```

### 5. 项目结构

```
todo-calendar/
├── main.py                    # 应用入口
├── requirements.txt           # Python 依赖
├── todo_calendar.spec         # PyInstaller 配置
├── start.bat                  # 启动脚本
├── build.bat                  # 打包脚本
├── README.md                  # 项目说明
├── DEPLOY.md                  # 部署指南 (本文件)
├── src/
│   ├── ui/                    # UI 组件
│   │   ├── main_window.py     # 主窗口
│   │   ├── calendar_view.py   # 日历视图
│   │   ├── week_view.py       # 周视图
│   │   ├── day_view.py        # 日视图
│   │   ├── task_dialog.py     # 任务对话框
│   │   ├── task_list.py       # 任务列表
│   │   ├── search_bar.py      # 搜索栏
│   │   └── stats_panel.py     # 统计面板
│   ├── services/              # 业务逻辑
│   │   ├── task_service.py    # 任务服务
│   │   ├── search_service.py  # 搜索服务
│   │   ├── filter_service.py  # 过滤服务
│   │   ├── reminder_service.py# 提醒服务
│   │   └── stats_service.py   # 统计服务
│   ├── models/                # 数据模型
│   │   ├── task.py            # 任务模型
│   │   ├── category.py        # 分类模型
│   │   ├── reminder.py        # 提醒模型
│   │   └── recurring_task.py  # 重复任务模型
│   ├── database/              # 数据库层
│   │   └── db_manager.py      # 数据库管理
│   ├── config/                # 配置
│   │   └── logging_config.py  # 日志配置
│   └── data/                  # 数据
│       └── todo_calendar.db   # SQLite 数据库
├── assets/
│   └── styles/
│       └── default.qss        # 样式表
├── tests/                     # 测试
│   ├── test_database.py
│   ├── test_task_service.py
│   └── test_p1_automation.py
└── docs/                      # 文档
    ├── PRD.md
    ├── TDD.md
    └── DESIGN.md
```

---

## 生产环境打包

### Windows 打包步骤

1. **准备环境**
   ```bash
   # 确保 Python 3.8+ 已安装
   python --version

   # 安装依赖
   pip install -r requirements.txt
   ```

2. **执行打包**
   ```batch
   # 在项目根目录执行
   build.bat
   ```

   或手动执行：
   ```batch
   pyinstaller --clean todo_calendar.spec
   ```

3. **验证打包**
   ```
   打包完成后，在 dist/Todo Calendar/ 目录找到：
   - Todo Calendar.exe (可执行文件)
   - start.bat (启动脚本)
   ```

4. **测试运行**
   ```batch
   cd dist/Todo Calendar/
   start.bat
   ```

### 打包参数说明

`todo_calendar.spec` 配置包含：
- ✅ 所有 PyQt6 二进制文件
- ✅ SQLite 数据库支持
- ✅ SQLAlchemy 及方言
- ✅ python-dateutil 模块
- ✅ assets 资源文件
- ✅ QSS 样式表
- ✅ 排除不必要的模块（减小体积）

### 打包后文件结构

```
dist/Todo Calendar/
├── Todo Calendar.exe    # 主程序 (~50MB)
├── start.bat            # 启动脚本
├── todo_calendar.db     # 数据库 (首次运行生成)
└── logs/                # 日志目录 (首次运行生成)
```

---

## 使用说明

### 1. 启动应用

```bash
# 方式一：双击 start.bat
# 方式二：双击 Todo Calendar.exe
# 方式三：命令行启动
python main.py
```

### 2. 创建任务

**方法一：双击创建**
1. 在日历格子上双击
2. 输入任务标题
3. 选择优先级 (P0/P1/P2)
4. 点击"创建"

**方法二：快捷键**
- `Ctrl+N` - 新建任务

### 3. 编辑任务

**双击任务** - 在任务列表或日历视图中双击任务即可编辑

### 4. 拖拽修改日期

1. 鼠标左键按住任务
2. 拖拽到目标日期
3. 松开鼠标完成修改

**提示**: 按 `ESC` 可取消拖拽

### 5. 标记任务完成

点击任务前的复选框 ✓，任务显示删除线表示完成

### 6. 视图切换

| 按钮 | 功能 |
|------|------|
| 📅 **月** | 月视图 (默认) |
| 📆 **周** | 周视图 |
| 📄 **日** | 日视图 |

### 7. 任务搜索

1. 点击顶部搜索栏
2. 输入关键词
3. 实时显示搜索结果

### 8. 任务过滤

点击过滤按钮，选择：
- 全部任务
- P0 高优先级
- P1 中优先级
- P2 低优先级
- 已完成
- 未完成

### 9. 重复任务设置

创建/编辑任务时：
1. 勾选"重复"
2. 选择重复规则：
   - 每周重复
   - 每月重复
   - 自定义规则

### 10. 查看统计

右侧统计面板显示：
- 本周完成任务数
- 本月完成任务数
- 各优先级任务分布
- 任务完成率

---

## 常见问题

### Q1: 启动时提示 "找不到 PyQt6"

**解决方案**:
```bash
# 重新安装依赖
pip install -r requirements.txt

# 或手动安装 PyQt6
pip install PyQt6>=6.4.0
```

### Q2: 打包后文件体积过大

**原因**: PyQt6 包含完整 Qt 库

**优化方案**:
```bash
# 使用 UPX 压缩
build.bat --upx

# 或手动指定排除模块
pyinstaller --exclude-module matplotlib todo_calendar.spec
```

### Q3: 数据丢失怎么办

**数据位置**:
```
%APPDATA%/Todo Calendar/todo_calendar.db
# 或
src/data/todo_calendar.db
```

**备份建议**: 定期复制 `todo_calendar.db` 文件

### Q4: 如何重置所有数据

**方法一**: 删除数据库文件
```bash
# 关闭应用后删除
del src/data/todo_calendar.db
# 重启应用会自动创建新数据库
```

**方法二**: 使用应用内功能
- 设置 → 清除所有数据

### Q5: 支持 macOS/Linux 吗

**当前状态**: 仅支持 Windows

**开发中**: macOS/Linux 版本计划中

**临时方案**: 使用源码运行方式
```bash
# macOS/Linux
python3 main.py
```

### Q6: 如何修改主题颜色

**当前版本**: 支持默认主题

**自定义**: 编辑 `assets/styles/default.qss`

---

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| **编程语言** | Python | 3.8+ |
| **UI 框架** | PyQt6 | 6.4+ |
| **数据存储** | SQLite | 3.35+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **日期处理** | python-dateutil | 2.8+ |
| **打包工具** | PyInstaller | 6.0+ |
| **测试框架** | pytest | 7.4+ |

---

## 📞 支持与反馈

### 问题反馈
- GitHub Issues: https://github.com/HYCGITCODE/todo-calendar/issues
- 邮箱：support@todocalendar.com

### 功能建议
- GitHub Discussions: https://github.com/HYCGITCODE/todo-calendar/discussions

### 版本更新
- Releases: https://github.com/HYCGITCODE/todo-calendar/releases

---

## 📄 许可证

MIT License

---

## 🎉 快速上手指南

**5 分钟快速开始**:

1. **下载** - 从 GitHub 下载最新版本
2. **解压** - 解压到任意目录
3. **启动** - 双击 `start.bat`
4. **创建** - 双击日历格子创建第一个任务
5. **拖拽** - 尝试拖拽任务修改日期

**就这么简单！** 🚀

---

**最后更新**: 2026-03-13  
**版本**: v1.0.0
