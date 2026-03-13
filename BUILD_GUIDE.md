# Todo Calendar - 打包指南

## 📦 打包准备

### 1. 环境要求

- Python 3.8+
- Windows 10/11 (用于生成 .exe)
- 所有依赖已安装

### 2. 安装依赖

```bash
cd todo-calendar
pip install -r requirements.txt
```

### 3. 图标文件

确保 `assets/icon.ico` 存在。如果不存在，PyInstaller 会使用默认图标。

可以从以下来源获取图标：
- 使用在线工具生成：https://www.icoconverter.com/
- 或使用 PyInstaller 默认图标

## 🚀 打包步骤

### Windows

```batch
build.bat
```

或手动执行：

```batch
pyinstaller todo_calendar.spec
```

### Linux/macOS

```bash
pyinstaller todo_calendar.spec
```

## 📁 输出文件

打包完成后，会在 `dist/` 目录生成：

```
dist/
└── Todo Calendar/
    ├── Todo Calendar.exe      # 主程序 (Windows)
    ├── Todo Calendar          # 主程序 (Linux/macOS)
    ├── assets/                # 资源文件
    │   └── styles/
    │       └── default.qss
    └── src/
        └── data/              # 数据目录
```

## ✅ 测试打包

### 1. 干净环境测试

```bash
# 创建测试目录
mkdir test-deploy
cd test-deploy

# 复制 dist 内容
cp -r ../dist/Todo\ Calendar/* .

# 运行程序
./start.bat  # Windows
# 或
./Todo\ Calendar  # Linux/macOS
```

### 2. 验证项目

- [ ] 程序能正常启动
- [ ] 界面显示正常
- [ ] 能创建任务
- [ ] 数据能保存（重启后数据还在）
- [ ] 样式表加载正常

## 🔧 常见问题

### 1. 缺少图标文件

**错误**: `icon.ico not found`

**解决**: 
- 创建占位图标或移除 icon 参数
- 使用 PyInstaller 默认图标

### 2. 数据库路径问题

**错误**: 程序运行时无法创建数据库

**解决**: 
数据库会自动创建在用户数据目录：
- Windows: `%APPDATA%/HuXiaodou/Todo Calendar/data/`
- Linux: `~/.local/share/HuXiaodou/Todo Calendar/data/`
- macOS: `~/Library/Application Support/HuXiaodou/Todo Calendar/data/`

### 3. 缺少 PyQt6 模块

**错误**: `ImportError: No module named PyQt6`

**解决**:
```bash
pip install PyQt6>=6.4.0
```

### 4. 打包体积过大

**优化**:
- 检查 spec 文件中的 excludes
- 使用 `--onefile` 模式
- 启用 UPX 压缩（已默认启用）

## 📝 构建配置

### todo_calendar.spec 关键配置

```python
# 包含的数据文件
datas = [
    ('assets', 'assets'),
    ('assets/styles/default.qss', 'assets/styles/default.qss'),
    ('src/data/', 'src/data'),
]

# 隐藏导入（PyInstaller 无法自动检测）
hiddenimports = [
    'PyQt6.QtCore',
    'sqlalchemy.dialects.sqlite',
    'dateutil.parser',
]
```

## 🎯 发布清单

发布前检查：

- [ ] build.bat 测试通过
- [ ] 程序在无 Python 环境运行正常
- [ ] 数据持久化正常
- [ ] 所有 P0 功能测试通过
- [ ] 版本号已更新
- [ ] README 已更新

## 📊 构建时间

- 首次构建：~2-3 分钟
- 增量构建：~30 秒

## 🔗 相关文档

- [README.md](README.md) - 项目说明
- [PRD.md](PRD.md) - 产品需求
- [DEPLOY.md](DEPLOY.md) - 部署指南
