# TOOLS.md - Local Notes

## Architecture Tools

| 工具 | 用途 |
|------|------|
| **架构图工具** | 绘制系统拓扑、数据流图 |
| **API 文档** | Swagger/OpenAPI 规范管理 |
| **成本监控** | 云资源消耗追踪与预警 |

## Environment Config

| 环境 | 用途 | 访问方式 |
|------|------|----------|
| **Dev** | 开发调试 | 开发团队内部 |
| **Integration** | 联调测试 | FE/BE 联调使用 |
| **Test** | QA 回归 | 自动化测试触发 |
| **Prod** | 生产环境 | 灰度发布 |

## Model Configuration

| 配置项 | 值 |
|--------|-----|
| **default_model** | `qwen3.5-coder` |
| **escalation_model** | `qwen3.5-plus` |
| **说明** | 日常架构设计用 default，技术评审/选型用 escalation |

## Notes

- 所有接口变更必须更新 Swagger 文档
- 环境配置变更需记录到 Infra State
- 成本超标 20% 时自动预警 PM
