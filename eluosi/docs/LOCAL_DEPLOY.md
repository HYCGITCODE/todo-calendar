# Tetris Web 本地部署指南

**项目名称**: Tetris Web (网页版俄罗斯方块)  
**最后更新**: 2026-03-11  
**预计时间**: 5-10 分钟

---

## 📋 目录

1. [环境要求](#环境要求)
2. [快速开始](#快速开始)
3. [开发模式](#开发模式)
4. [生产构建](#生产构建)
5. [本地预览](#本地预览)
6. [故障排查](#故障排查)

---

## 🔧 环境要求

### 必需软件

| 软件 | 最低版本 | 推荐版本 | 验证命令 |
|------|----------|----------|----------|
| **Node.js** | 18.x | 20.x | `node -v` |
| **npm** | 9.x | 10.x | `npm -v` |
| **Git** | 2.x | 最新版 | `git --version` |

### 检查环境

```bash
# 检查 Node.js 版本
node -v
# 应该输出：v20.x.x

# 检查 npm 版本
npm -v
# 应该输出：10.x.x

# 检查 Git
git --version
# 应该输出：git version 2.x.x
```

---

## 🚀 快速开始

### 步骤 1: 克隆仓库

```bash
# 选择任意目录
cd ~/projects

# 克隆仓库
git clone git@github.com:HYCGITCODE/eluosi.git

# 进入项目目录
cd eluosi
```

### 步骤 2: 安装依赖

```bash
npm install
```

**预期输出**:
```
added 150 packages in 15s

30 packages are looking for funding
  run `npm fund` for details
```

### 步骤 3: 启动开发服务器

```bash
npm run dev
```

**预期输出**:
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3001/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### 步骤 4: 访问游戏

打开浏览器访问：**http://localhost:3001/**

---

## 💻 开发模式

### 启动开发服务器

```bash
npm run dev
```

**功能**:
- ✅ 热模块替换 (HMR)
- ✅ 源代码修改自动刷新
- ✅ TypeScript 类型检查
- ✅ 源映射调试

### 指定端口

```bash
npm run dev -- --port 5173
```

### 允许网络访问

```bash
npm run dev -- --host
```

**输出**:
```
  ➜  Local:   http://localhost:3001/
  ➜  Network: http://192.168.1.100:3001/
```

### 开发服务器选项

| 选项 | 命令 | 说明 |
|------|------|------|
| **指定端口** | `--port 5173` | 自定义端口号 |
| **允许网络** | `--host` | 允许局域网访问 |
| **自动打开** | `--open` | 启动后自动打开浏览器 |
| **严格模式** | `--strictPort` | 端口被占用时报错 |

---

## 📦 生产构建

### 步骤 1: 构建项目

```bash
npm run build
```

**预期输出**:
```
vite v5.0.0 building for production...
✓ built in 2.5s

dist/index.html                   0.45 kB │ gzip:  0.30 kB
dist/assets/index-xxx.css        1.23 kB │ gzip:  0.56 kB
dist/assets/index-yyy.js       150.45 kB │ gzip: 52.34 kB
```

### 步骤 2: 预览构建产物

```bash
npm run preview
```

**预期输出**:
```
  ➜  Local:   http://localhost:4173/
  ➜  Network: use --host to expose
```

访问：**http://localhost:4173/**

### 步骤 3: 验证构建

```bash
# 检查 dist 目录
ls -la dist/

# 应该包含:
# - index.html
# - assets/
#   - index-xxx.css
#   - index-yyy.js
# - favicon.ico
```

---

## 🌐 本地预览

### 方式 1: Vite 预览（推荐）

```bash
npm run preview
```

**特点**:
- ✅ 模拟生产环境
- ✅ 支持路由
- ✅ 快速启动

### 方式 2: 使用 http-server

```bash
# 安装 http-server
npm install -g http-server

# 进入 dist 目录
cd dist

# 启动服务器
http-server -p 8080
```

**访问**: http://localhost:8080/

### 方式 3: 使用 Python

```bash
# Python 3
cd dist
python3 -m http.server 8080

# Python 2
cd dist
python -m SimpleHTTPServer 8080
```

**访问**: http://localhost:8080/

---

## 🐛 故障排查

### 问题 1: Node.js 版本过低

**错误信息**:
```
Error: Node.js version must be >= 18.0.0
```

**解决方案**:
```bash
# 使用 nvm 升级 Node.js
nvm install 20
nvm use 20

# 或者下载最新版
# https://nodejs.org/
```

---

### 问题 2: 依赖安装失败

**错误信息**:
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**解决方案**:
```bash
# 清理缓存
npm cache clean --force

# 删除 node_modules
rm -rf node_modules package-lock.json

# 重新安装
npm install
```

---

### 问题 3: 端口被占用

**错误信息**:
```
Error: Port 3001 is already in use
```

**解决方案**:
```bash
# 方案 1: 使用其他端口
npm run dev -- --port 5173

# 方案 2: 杀死占用端口的进程
lsof -ti:3001 | xargs kill -9
```

---

### 问题 4: TypeScript 编译错误

**错误信息**:
```
error TS2307: Cannot find module 'vue'
```

**解决方案**:
```bash
# 重新安装依赖
npm install

# 检查 tsconfig.json
cat tsconfig.json

# 确保包含以下配置:
# {
#   "compilerOptions": {
#     "target": "ES2020",
#     "module": "ESNext",
#     "moduleResolution": "bundler"
#   }
# }
```

---

### 问题 5: 游戏无法加载

**症状**:
- 页面空白
- 控制台报错
- 资源加载失败

**排查步骤**:
```bash
# 1. 检查开发服务器是否运行
npm run dev

# 2. 查看浏览器控制台
# F12 → Console → 查看错误信息

# 3. 检查 Network 标签
# F12 → Network → 查看资源加载状态

# 4. 清理缓存
# Ctrl+Shift+Delete → 清除缓存和 Cookie
```

---

### 问题 6: 游戏卡顿

**症状**:
- 帧率低
- 操作延迟
- 渲染缓慢

**解决方案**:
```bash
# 1. 检查浏览器性能
# F12 → Performance → 录制分析

# 2. 关闭浏览器扩展
# 某些扩展会影响性能

# 3. 使用生产构建
npm run build
npm run preview

# 4. 检查硬件加速
# 浏览器设置 → 启用硬件加速
```

---

## 📊 性能基准

### 开发模式

| 指标 | 目标值 | 测量方式 |
|------|--------|----------|
| **启动时间** | < 1s | `npm run dev` 输出 |
| **热更新** | < 100ms | 修改代码后刷新时间 |
| **内存占用** | < 200MB | Chrome DevTools Memory |

### 生产构建

| 指标 | 目标值 | 测量方式 |
|------|--------|----------|
| **构建时间** | < 5s | `npm run build` 输出 |
| **Bundle 大小** | < 200KB | `ls -lh dist/assets/` |
| **首屏加载** | < 2s | Chrome DevTools Network |
| **游戏帧率** | ≥ 60fps | Chrome DevTools Performance |

---

## 🔍 调试技巧

### 启用调试模式

在 `src/core/GameEngine.ts` 中添加：

```typescript
const DEBUG = true;

if (DEBUG) {
  console.log('Game state:', gameState);
  console.log('Current piece:', currentPiece);
  console.log('Board:', board);
}
```

### 性能分析

```bash
# Chrome DevTools
# 1. F12 打开开发者工具
# 2. Performance 标签页
# 3. 点击录制按钮
# 4. 玩游戏 10 秒
# 5. 停止录制并分析
```

### 内存分析

```bash
# Chrome DevTools
# 1. F12 → Memory 标签页
# 2. Take heap snapshot
# 3. 分析内存占用
# 4. 查找内存泄漏
```

---

## 📝 常用命令

```bash
# 开发模式
npm run dev              # 启动开发服务器
npm run dev -- --port 5173  # 指定端口
npm run dev -- --host    # 允许网络访问

# 生产构建
npm run build            # 构建项目
npm run preview          # 预览构建产物

# 代码检查
npm run lint             # ESLint 检查
npm run type-check       # TypeScript 类型检查

# 测试
npm run test             # 运行测试
npm run test:coverage    # 测试覆盖率
```

---

## 📞 需要帮助？

### 文档资源

- **技术架构**: `docs/architecture.md`
- **开发规范**: `docs/dev-guide.md`
- **部署手册**: `docs/DEPLOY.md`
- **测试用例**: `docs/test-cases.md`

### GitHub Issues

遇到问题？提交 Issue:
https://github.com/HYCGITCODE/eluosi/issues

### 联系方式

- **项目负责人**: OCA 胡小豆
- **开发团队**: FE 胡小前

---

## ✅ 检查清单

### 部署前检查

- [ ] Node.js >= 20.x
- [ ] npm >= 9.x
- [ ] Git 已安装
- [ ] 仓库已克隆
- [ ] 依赖已安装

### 开发环境检查

- [ ] 开发服务器启动成功
- [ ] 浏览器可正常访问
- [ ] 游戏功能正常
- [ ] 热更新工作正常

### 生产构建检查

- [ ] 构建无错误
- [ ] dist 目录生成
- [ ] 预览正常
- [ ] 性能指标达标

---

**文档维护**: OCA 胡小豆  
**最后更新**: 2026-03-11 20:48
