# Render 部署手册 - AI News Pulse

本文档指导如何将 AI News Pulse 项目部署到 Render 平台。

---

## 1. 准备工作

### 1.1 Render 账号注册

1. 访问 [https://render.com](https://render.com)
2. 点击 **Get Started for Free** 按钮
3. 使用 GitHub 账号登录并授权（推荐）或使用邮箱注册

[截图：Render 首页注册按钮]

### 1.2 GitHub 账号授权

- 如使用 GitHub 登录，Render 会自动请求访问你的 GitHub 仓库权限
- 确保授权 Render 访问 `HYCGITCODE/ai-news-pulse` 仓库
- 如未自动授权，可在 Render Dashboard → Settings → Connected Accounts 中手动连接

[截图：GitHub 授权页面]

---

## 2. 创建 Web Service

### 2.1 登录 Render Dashboard

1. 登录 [https://dashboard.render.com](https://dashboard.render.com)
2. 点击右上角 **New** 按钮
3. 选择 **Web Service**

[截图：Render Dashboard 页面，New 按钮位置]

### 2.2 连接 GitHub 仓库

1. 在 **Connect a repository** 页面，选择 `HYCGITCODE/ai-news-pulse`
2. 如未看到该仓库，点击 **Configure account** 授权 Render 访问
3. 点击 **Connect** 按钮

[截图：选择 GitHub 仓库页面]

---

## 3. 配置服务

按以下参数填写 Web Service 配置：

| 配置项 | 值 |
|--------|-----|
| **Name** | `ai-news-pulse` |
| **Region** | Oregon (免费套餐) |
| **Branch** | `master` |
| **Root Directory** | 留空（不填） |
| **Runtime** | Node |
| **Build Command** | `cd backend && npm install && cd ../frontend && npm install && npm run build` |
| **Start Command** | `cd backend && npm start` |
| **Instance Type** | Free |

[截图：Web Service 配置页面，填写各项参数]

---

## 4. 环境变量配置

在 **Environment Variables** 部分，添加以下变量：

| Key | Value |
|-----|-------|
| `NODE_ENV` | `production` |
| `PORT` | `3000` |

**操作步骤：**
1. 点击 **Add Environment Variable** 按钮
2. 输入 Key 和 Value
3. 点击 **Add** 确认

[截图：环境变量配置页面]

---

## 5. 启动部署

### 5.1 创建服务

1. 确认所有配置无误
2. 点击 **Create Web Service** 按钮

[截图：确认创建按钮]

### 5.2 等待部署完成

- 部署过程约需 **5-10 分钟**
- 可在 **Logs** 标签页查看实时部署日志
- 部署成功后状态显示为 **Live**

[截图：部署进度页面，Logs 标签页]

### 5.3 获取公网域名

部署成功后，Render 会分配一个公网域名，格式为：
```
https://ai-news-pulse.onrender.com
```

可在 **Overview** 页面顶部找到该域名。

[截图：服务概览页面，显示公网域名]

---

## 6. 验证部署

### 6.1 访问主页

在浏览器中访问：
```
https://ai-news-pulse.onrender.com
```

确认页面正常加载。

### 6.2 健康检查

访问健康检查端点：
```
https://ai-news-pulse.onrender.com/health
```

预期返回 JSON 格式的健康状态，如：
```json
{"status": "ok", "timestamp": "2026-03-11T..."}
```

[截图：健康检查返回结果]

---

## 7. 自动部署

### 7.1 默认开启

- Render 默认开启 **Auto-Deploy** 功能
- 每次 push 到 `master` 分支会自动触发部署

### 7.2 关闭自动部署（可选）

如需关闭：
1. 进入服务页面 → **Settings** 标签页
2. 找到 **Auto-Deploy** 选项
3. 切换为 **Off**

[截图：Settings 页面，Auto-Deploy 开关]

---

## 8. 常见问题 FAQ

### 8.1 部署失败怎么办？

**排查步骤：**
1. 进入 **Logs** 标签页，查看错误日志
2. 常见错误：
   - `npm install` 失败 → 检查 `package.json` 依赖
   - `build` 失败 → 检查前端构建配置
   - `start` 失败 → 检查启动命令和端口配置
3. 修复代码后 push 到 master，自动重新部署

### 8.2 如何查看日志？

1. 进入服务页面
2. 点击 **Logs** 标签页
3. 可实时查看或下载历史日志

[截图：Logs 页面]

### 8.3 如何回滚？

1. 进入服务页面 → **Events** 标签页
2. 找到之前成功的部署记录
3. 点击该记录的 **...** 菜单
4. 选择 **Rollback to this version**

[截图：Events 页面，回滚操作]

### 8.4 免费额度限制

| 限制项 | 免费套餐额度 |
|--------|-------------|
| **每月使用时长** | 750 小时（约 31 天连续运行） |
| **内存** | 512 MB |
| **CPU** | 共享 CPU |
| **带宽** | 100 GB/月 |
| **部署次数** | 无限制 |

**注意：**
- 免费服务在 15 分钟无流量后会进入休眠
- 下次访问时需约 30 秒冷启动时间
- 如需生产环境稳定运行，建议升级到付费套餐（$7/月起）

---

## 附录：render.yaml 参考

本项目已包含 `render.yaml` 配置文件，也可通过 CLI 部署：

```yaml
services:
  - type: web
    name: ai-news-pulse
    env: node
    buildCommand: cd backend && npm install && cd ../frontend && npm install && npm run build
    startCommand: cd backend && npm start
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 3000
    plan: free
    region: oregon
    branch: master
    autoDeploy: true
```

---

**文档版本：** v1.0  
**最后更新：** 2026-03-11  
**维护者：** Arch 胡小架
