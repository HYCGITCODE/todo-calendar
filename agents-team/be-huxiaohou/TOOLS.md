# TOOLS.md - Local Notes

## Development Tools

| 工具 | 用途 |
|------|------|
| **API 文档** | Swagger/OpenAPI 接口规范管理 |
| **数据库工具** | Schema 管理、迁移脚本、数据查询 |
| **单元测试** | 业务逻辑测试覆盖 |

## Environment Config

| 环境 | 用途 | 访问地址 |
|------|------|----------|
| **Local** | 本地开发 | localhost:8080 |
| **Dev** | 开发联调 | dev-api.example.com |
| **Test** | QA 测试 | test-api.example.com |
| **Prod** | 生产环境 | api.example.com |

## Model Configuration

| 配置项 | 值 |
|--------|-----|
| **default_model** | `glm-5` |
| **说明** | 代码生成专用，适合业务逻辑与 API 开发 |

## Notes

- 所有接口必须有单元测试覆盖
- 敏感数据必须加密存储
- 接口变更必须同步更新 Swagger 文档
- 提测前必须完成联调自测 Checklist
