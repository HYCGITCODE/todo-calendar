# AI News Pulse - 部署指南

**项目**: AI 行业新闻聚合应用  
**版本**: 1.1.0  
**最后更新**: 2026-03-11

---

## 🚀 快速部署（Render - 推荐）

**优势**: 免费、自动 HTTPS、自动部署、10 分钟上线

### 部署步骤

1. **访问 Render**: https://render.com

2. **创建 Web Service**: 
   - 登录 Dashboard
   - 点击 **New** → **Web Service**

3. **连接仓库**: 
   - 选择 GitHub 仓库 `HYCGITCODE/ai-news-pulse`
   - 如未看到仓库，点击 **Configure account** 授权

4. **配置**:
   | 配置项 | 值 |
   |--------|-----|
   | **Region** | Oregon (免费) |
   | **Build Command** | `cd backend && npm install && cd ../frontend && npm install && npm run build` |
   | **Start Command** | `cd backend && npm start` |
   | **环境变量** | `NODE_ENV=production`, `PORT=3000` |
   | **Instance Type** | Free |

5. **部署**: 点击 **Create Web Service**

6. **验证**: 访问 `https://<你的域名>.onrender.com/health`
   - 预期返回：`{"status": "ok", "timestamp": "..."}`

[截图：Render 创建服务页面]

### 自动部署

- ✅ 默认开启
- Push 到 `master` 分支自动触发部署
- 部署过程约 5-10 分钟

### 查看日志

- Dashboard → 选择服务 → **Logs** 标签页
- 实时查看部署日志和运行日志

[截图：Render Logs 页面]

### 详细教程

完整部署手册（含截图、FAQ、故障排查）: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

---

## 📋 其他部署方案

---

## 系统要求

### 最低配置

| 组件 | 版本 | 说明 |
|------|------|------|
| **Node.js** | >= 18.0.0 | 必需 |
| **npm** | >= 9.0.0 | 随 Node.js 安装 |
| **内存** | >= 512MB | 运行时需求 |
| **磁盘** | >= 200MB | 依赖 + 缓存 |

### 推荐配置

| 组件 | 版本 | 说明 |
|------|------|------|
| **Node.js** | >= 20.0.0 | LTS 版本 |
| **内存** | >= 1GB | 更流畅运行 |
| **系统** | Linux/macOS/Windows | 全平台支持 |

---

## 方案 A: Railway 部署

**优势**: 自动部署、免费额度、HTTPS、自动扩缩容

### 部署步骤

1. 打开 https://railway.app
2. 点击 **New Project** → **Deploy from GitHub repo**
3. 选择 `ai-news-pulse` 仓库
4. Railway 自动识别 `railway.json` 配置
5. 点击 **Deploy**

### 环境变量配置

在 Railway 面板添加:
```
NODE_ENV=production
```

### 验证部署

部署完成后，Railway 会分配一个域名：
```
https://<你的项目>.railway.app
```

访问 `https://<你的项目>.railway.app/health` 验证。

---

## 方案 B: Docker 部署

### Dockerfile

在项目根目录创建 `Dockerfile`:

```dockerfile
# 后端
FROM node:20-alpine AS backend
WORKDIR /app
COPY backend/package*.json ./
RUN npm ci --only=production
COPY backend/ ./
EXPOSE 3000
CMD ["npm", "start"]

# 前端
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# 生产环境
FROM nginx:alpine
COPY --from=frontend /app/dist /usr/share/nginx/html
COPY --from=backend /app /app
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 构建并运行

```bash
# 构建镜像
docker build -t ai-news-pulse .

# 运行容器
docker run -p 80:80 ai-news-pulse
```

### 验证

访问 `http://localhost/health`

---

## 方案 C: VPS 手动部署

**适用**: 自有服务器、云服务器（阿里云、腾讯云、AWS 等）

### 1. 安装 Node.js

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# CentOS/RHEL
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs
```

### 2. 克隆并安装

```bash
git clone https://github.com/HYCGITCODE/ai-news-pulse.git
cd ai-news-pulse
cd backend && npm install
cd ../frontend && npm install
```

### 3. 配置 systemd 服务

**后端服务** (`/etc/systemd/system/ai-news-backend.service`):
```ini
[Unit]
Description=AI News Pulse Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/ai-news-pulse/backend
ExecStart=/usr/bin/node src/server.js
Restart=always
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

**前端服务** (`/etc/systemd/system/ai-news-frontend.service`):
```ini
[Unit]
Description=AI News Pulse Frontend
After=network.target ai-news-backend.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/ai-news-pulse/frontend
ExecStart=/usr/bin/npm run dev
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

### 4. 启动服务

```bash
# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ai-news-backend
sudo systemctl start ai-news-frontend

# 设置开机自启
sudo systemctl enable ai-news-backend
sudo systemctl enable ai-news-frontend

# 查看状态
sudo systemctl status ai-news-backend
sudo systemctl status ai-news-frontend
```

### 5. 配置 Nginx 反向代理（可选）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 后端 API
    location /api {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 本地开发部署

### 步骤 1: 克隆仓库

```bash
git clone https://github.com/HYCGITCODE/ai-news-pulse.git
cd ai-news-pulse
```

### 步骤 2: 安装后端依赖

```bash
cd backend
npm install
```

### 步骤 3: 安装前端依赖

```bash
cd ../frontend
npm install
```

### 步骤 4: 启动后端服务

```bash
cd backend
npm run dev
```

验证后端：访问 http://localhost:3000/health

### 步骤 5: 启动前端服务（新终端）

```bash
cd frontend
npm run dev
```

验证前端：访问 http://localhost:5173

---

## 环境变量配置

### 后端环境变量

| 变量名 | 默认值 | 说明 | 必需 |
|--------|--------|------|------|
| `PORT` | 3000 | 后端服务端口 | 否 |
| `NODE_ENV` | development | 运行环境 | 否 |

### 前端环境变量

| 变量名 | 默认值 | 说明 | 必需 |
|--------|--------|------|------|
| `VITE_API_URL` | /api | API 基础 URL | 否 |

---

## 常见问题 FAQ

### Q1: 端口被占用

**错误**: `EADDRINUSE: address already in use :::3000`

**解决**:
```bash
# 查找占用端口的进程
lsof -ti:3000

# 杀死进程
kill -9 <PID>

# 或修改端口
PORT=3001 npm start
```

---

### Q2: 依赖安装失败

**错误**: `npm ERR! code EACCES`

**解决**:
```bash
# 清理 npm 缓存
npm cache clean --force

# 修复权限（推荐）
sudo chown -R $(whoami) ~/.npm

# 重新安装
npm install
```

---

### Q3: 前端无法连接后端

**错误**: `Network Error` 或 `CORS Error`

**解决**:
1. 确认后端已启动：`curl http://localhost:3000/health`
2. 检查 CORS 配置（`backend/src/server.js`）
3. 确认前端 API URL 配置正确

---

### Q4: RSS 抓取失败

**错误**: 新闻列表为空

**解决**:
1. 检查网络连接
2. 验证 RSS 源是否可访问
3. 查看后端日志：`tail -f backend/logs/*.log`
4. 手动触发刷新：`curl -X POST http://localhost:3000/api/news/refresh`

---

### Q5: 构建失败

**错误**: `npm run build` 失败

**解决**:
```bash
# 清理 node_modules
rm -rf node_modules package-lock.json

# 重新安装
npm install

# 重新构建
npm run build
```

---

## 性能优化建议

### 1. 启用缓存

后端已实现 1 小时缓存，无需额外配置。

### 2. CDN 加速（生产环境）

将前端静态资源部署到 CDN:
- Cloudflare Pages
- Vercel
- Netlify

### 3. 数据库优化（如需扩展）

当前使用内存缓存，如需持久化:
```bash
# 安装 Redis
sudo apt-get install redis-server

# 修改 backend/src/services/cache.js
# 使用 Redis 替代 node-cache
```

---

## 监控与日志

### 查看日志

```bash
# 后端日志
tail -f backend/logs/*.log

# systemd 日志
journalctl -u ai-news-backend -f
journalctl -u ai-news-frontend -f
```

### 健康检查

```bash
# 后端健康状态
curl http://localhost:3000/health

# 前端页面
curl http://localhost:5173
```

---

## 安全建议

### 1. 防火墙配置

```bash
# 仅允许必要端口
sudo ufw allow 3000
sudo ufw allow 5173
sudo ufw enable
```

### 2. HTTPS 配置（生产环境）

使用 Let's Encrypt 免费证书:
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. 定期更新依赖

```bash
# 检查可更新的依赖
npm outdated

# 更新依赖
npm update
```

---

## 部署方案对比

| 方案 | 难度 | 成本 | 部署时间 | 推荐场景 |
|------|------|------|----------|----------|
| **Render** | ⭐ 简单 | 免费 | 10 分钟 | MVP、快速上线 |
| **Railway** | ⭐⭐ 中等 | $5 免费额度 | 15 分钟 | 需要更多资源 |
| **Docker** | ⭐⭐⭐ 较复杂 | 服务器成本 | 30 分钟 | 自定义环境 |
| **VPS** | ⭐⭐⭐⭐ 复杂 | 服务器成本 | 1 小时 | 完全控制 |

---

## 技术支持

- **GitHub Issues**: https://github.com/HYCGITCODE/ai-news-pulse/issues
- **详细教程**: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)
- **项目文档**: `/docs` 目录

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.1.0 | 2026-03-11 | 新增 Render 一键部署方案、render.yaml 配置文件 |
| 1.0.0 | 2026-03-09 | 初始发布 |

---

**祝部署顺利！** 🚀
