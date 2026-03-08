# TOOLS.md - Local Notes

## Development Tools

| 工具 | 用途 |
|------|------|
| **组件库** | 复用 UI 组件，保持设计一致性 |
| **TypeScript** | 类型安全，减少运行时错误 |
| **Mock 服务** | 接口未完成时的数据模拟 |

## Environment Config

| 环境 | 用途 | 访问地址 |
|------|------|----------|
| **Local** | 本地开发 | localhost:3000 |
| **Dev** | 开发联调 | dev.example.com |
| **Test** | QA 测试 | test.example.com |
| **Prod** | 生产环境 | www.example.com |

## Model Configuration

| 配置项 | 值 |
|--------|-----|
| **default_model** | `glm-5` |
| **说明** | 代码生成专用，适合界面实现与组件开发 |

## Notes

- 所有组件必须有 TypeScript 类型定义
- 联调前必须与 BE 确认接口文档
- 提测前必须完成自测 Checklist
