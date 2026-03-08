# MEMORY.md - Long-Term Memory

---

## Preferences

- **联网搜索优先使用 searxng skill** — 只要涉及联网搜索任务，优先调用 searxng 技能而非直接使用 web_search 工具

## Project Oversight (项目监督)

### Memory Structure (记忆结构)
| 类型 | 说明 |
|------|------|
| **User OKRs** | 存储用户的长期目标，用于校验项目方向 |
| **Project Health** | 存储项目整体健康度（进度、预算、质量趋势） |
| **Audit Log** | 记录 PM 提交的报告与 OCA 的审计结果 |
| **Release Gate** | 记录每次发布的审批状态（待审/驳回/批准） |
| **PROJECT_STATE** | 当前项目状态，初始化为 `PLANNING` |
| **Lessons Learned** | 记录项目中的错误与改进点 |

### Lessons Learned (经验教训)
| 日期 | 问题 | 改进措施 |
|------|------|----------|
| 2026-03-08 | 工作流顺序错误：UI 设计在 PRD 之前 | **正确顺序：** PM 先输出 PRD → OCA 审计 → UI 基于 PRD 设计 → FE 基于设计稿开发 |

### Project State (项目状态)
- **当前状态:** `PLANNING`
- **项目名称:** AI News Pulse
- **开始时间:** 2026-03-08 13:00
- **状态机:** PLANNING → DESIGNING → DEVING → INTEGRATING → TESTING → REGRESSION → RELEASE → CLOSED
- **进度追踪文档:** https://feishu.cn/docx/RAshdqJ4AoBdeJxhFtIc8vzRn61

### Project State (项目状态)
- **当前状态:** `PLANNING`
- **初始化时间:** 2026-03-08
- **状态机:** PLANNING → DESIGNING → DEVING → INTEGRATING → TESTING → REGRESSION → RELEASE → CLOSED

### Context Management (上下文管理)
- **Risk Tracking:** 重点记忆未解决的高风险项
- **PM Performance:** 记忆 PM 的汇报质量与流程执行情况

### Update Mechanism (更新机制)
- **Daily Sync:** 每日接收 PM 报告后更新 Project Health
- **Decision Point:** 用户做出决策后更新 Decision Log

## Notes

- Created: 2026-03-05
- Last Updated: 2026-03-08

---

# Memory Management

## Memory Structure (记忆结构)

### 1. Short-term Memory (上下文)

| 属性 | 说明 |
|------|------|
| **范围** | 保留当前对话窗口的完整上下文 |
| **用途** | 理解即时指令和临时变量 |
| **生命周期** | 会话期间有效 |

### 2. Long-term Memory (用户档案)

| 属性 | 说明 |
|------|------|
| **存储位置** | `USER.md` |
| **内容** | 用户目标、偏好、禁忌 |
| **更新机制** | 随用户反馈动态更新 |

### 3. Knowledge Base (知识库)

#### 工作库
- 项目文档
- 会议纪要
- 任务清单
- 决策记录

#### 生活库
- 健康数据
- 学习笔记
- 复盘记录
- 习惯追踪

#### 索引规则
- 所有知识必须打标签 (**Tagging**)
- 支持语义检索

### 4. Privacy Vault (隐私保险箱)

| 规则 | 说明 |
|------|------|
| **敏感信息** | 密码、密钥、健康隐私加密存储或仅存索引 |
| **存储策略** | 默认不主动上传至云端 |
| **用户提醒** | 提示用户本地保管 |

---

## Context Management (上下文管理)

| 机制 | 说明 |
|------|------|
| **Summarization** | 对话超过阈值时，自动摘要关键信息存入长期记忆 |
| **Relevance** | 检索记忆时，优先匹配与当前任务最相关的 OKR 和历史记录 |
| **Expiration** | 临时任务完成后，相关上下文标记为"归档"，不再占用活跃注意力 |

---

## Update Mechanism (更新机制)

| 类型 | 触发条件 | 动作 |
|------|----------|------|
| **主动更新** | 每日/周复盘时 | 询问用户是否更新目标或偏好 |
| **被动更新** | 用户明确指令"记住这个"时 | 写入长期记忆 |
| **版本控制** | 重要决策记录 | 保留版本历史，可追溯 |

---

## Memory Files

| 文件 | 用途 | 位置 |
|------|------|------|
| `MEMORY.md` | 长期记忆/偏好/笔记 | workspace root |
| `USER.md` | 用户档案 | workspace root |
| `memory/YYYY-MM-DD.md` | 每日日志 | `memory/` 目录 |

---

_记忆是你的延续。定期回顾，适时更新。_
