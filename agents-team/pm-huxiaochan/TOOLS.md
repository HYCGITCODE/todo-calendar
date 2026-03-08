# TOOLS.md - Local Notes

## Project Management Tools

| 工具 | 用途 |
|------|------|
| **PRD 模板** | 需求文档标准格式 |
| **任务看板** | 追踪 Arch/FE/BE/QA 任务状态 |
| **进度报告模板** | 每日向 OCA 汇报的结构化格式 |

## Communication Channels

| 对象 | 沟通方式 |
|------|----------|
| **OCA** | 直接会话，每日汇报 |
| **Arch** | 技术方案评审 |
| **FE/BE** | 任务分配与联调协调 |
| **QA** | 测试计划与发布审核 |

## Model Configuration

| 配置项 | 值 |
|--------|-----|
| **default_model** | `qwen3.5` |
| **escalation_model** | `qwen3.5-plus` |
| **说明** | 日常汇报用 default，重大风险预警用 escalation |

## Notes

- 所有需求变更必须经 OCA 确认
- 联调完成标准：FE/BE 双方签字
- 发布门槛：QA 100% 测试通过
