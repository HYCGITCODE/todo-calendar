# 🚨 打包环境要求与说明

## ⚠️ 重要提示

**当前服务器环境不满足打包要求！**

- 当前 Python 版本：3.6.8
- 最低要求 Python 版本：3.8+
- PyQt6 需要 Python 3.8+ 才能安装

## ✅ 解决方案

### 方案 A: 在 Windows 机器上打包（推荐）

这是**官方推荐**的方式，因为最终产物是 Windows .exe 文件。

**步骤**:

1. **准备 Windows 环境**
   - Windows 10/11
   - Python 3.8+ (推荐 3.10+)
   - 从 https://www.python.org/downloads/ 下载

2. **克隆项目**
   ```batch
   git clone <repo-url>
   cd todo-calendar
   ```

3. **安装依赖**
   ```batch
   pip install -r requirements.txt
   ```

4. **运行打包**
   ```batch
   build.bat
   ```

5. **测试**
   - 在 `dist/Todo Calendar/` 目录找到生成的文件
   - 运行 `start.bat` 测试
   - 复制到无 Python 环境的机器测试

### 方案 B: 在 Linux 安装新 Python

如果必须在当前服务器打包：

```bash
# 安装 Python 3.10 (需要 root 权限)
sudo yum install python3.10 python3.10-pip -y

# 创建新虚拟环境
python3.10 -m venv venv3.10
source venv3.10/bin/activate

# 安装依赖
pip install -r requirements.txt

# 打包
pyinstaller todo_calendar.spec
```

## 📦 已准备的打包文件

以下文件已准备好，可以直接使用：

| 文件 | 说明 | 状态 |
|------|------|------|
| `build.bat` | Windows 打包脚本 | ✅ 已创建 |
| `start.bat` | 启动脚本 | ✅ 已创建 |
| `todo_calendar.spec` | PyInstaller 配置 | ✅ 已更新 |
| `requirements.txt` | 生产依赖 | ✅ 已优化 |
| `BUILD_GUIDE.md` | 打包指南 | ✅ 已创建 |
| `test_build.py` | 打包测试脚本 | ✅ 已创建 |

## 📋 依赖清单

```txt
PyQt6>=6.4.0          # UI 框架
PyQt6-Qt6>=6.4.0      # Qt6 核心
SQLAlchemy>=2.0.0     # 数据库 ORM
python-dateutil>=2.8.2 # 日期工具
pyinstaller>=6.0.0    # 打包工具
```

## 🔧 打包配置说明

### todo_calendar.spec 包含内容

1. **数据文件**
   - `assets/` - 资源文件夹
   - `assets/styles/default.qss` - 样式表
   - `src/data/` - 数据目录（用于存储数据库）

2. **隐藏导入**
   - PyQt6 所有模块
   - SQLAlchemy 及 SQLite 方言
   - python-dateutil

3. **排除模块**（减小体积）
   - matplotlib
   - numpy
   - pandas
   - tkinter
   - unittest

4. **图标**
   - 如果 `assets/icon.ico` 存在则使用
   - 否则使用系统默认图标

## 🎯 打包输出

### 目录结构

```
dist/
└── Todo Calendar/
    ├── Todo Calendar.exe    # 主程序
    ├── start.bat            # 启动脚本
    ├── assets/
    │   └── styles/
    │       └── default.qss  # 样式表
    └── _internal/           # 运行时文件（onefile 模式无此目录）
```

### 文件大小预估

- **onefile 模式**: ~50-80 MB (单个 exe)
- **onedir 模式**: ~150-200 MB (目录)

## ✅ 测试清单

打包完成后，在**干净环境**测试：

- [ ] 无 Python 环境的机器可以运行
- [ ] 程序正常启动
- [ ] 界面显示正常
- [ ] 可以创建/编辑/删除任务
- [ ] 重启后数据保留
- [ ] 样式表加载正常
- [ ] 所有 P0 功能可用

## 🐛 常见问题

### 1. PyQt6 安装失败

**错误**: `No module named PyQt6`

**原因**: Python 版本过低或 qmake 未安装

**解决**:
```bash
# 升级 Python 到 3.8+
# 或安装 Qt 开发工具
sudo apt install qtbase5-dev  # Linux
```

### 2. 数据库路径错误

**错误**: 无法创建数据库文件

**解决**: 数据库会自动创建在用户数据目录，确保有写入权限

### 3. 样式表未加载

**错误**: 界面显示默认样式

**解决**: 检查 `assets/styles/default.qss` 是否正确打包到 dist 目录

### 4. 图标缺失

**警告**: `icon.ico not found`

**解决**: 
- 创建 `assets/icon.ico` 
- 或从 spec 文件移除 icon 参数

## 📞 需要帮助？

查看完整文档：
- [BUILD_GUIDE.md](BUILD_GUIDE.md) - 详细打包指南
- [README.md](README.md) - 项目说明
- [DEPLOY.md](DEPLOY.md) - 部署指南

---

**最后更新**: 2026-03-13  
**准备状态**: ✅ 所有打包文件已就绪，等待 Windows 环境执行
