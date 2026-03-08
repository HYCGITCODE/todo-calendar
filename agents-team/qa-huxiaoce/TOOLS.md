# TOOLS.md - Local Notes

## Testing Tools

| 工具 | 用途 |
|------|------|
| **自动化测试框架** | 执行回归测试、接口测试 |
| **性能测试工具** | 压力测试、负载测试 |
| **Bug 管理系统** | 跟踪 Bug 生命周期 |

## Environment Config

| 环境 | 用途 | 访问地址 |
|------|------|----------|
| **Test** | QA 测试环境 | test.example.com |
| **Staging** | 预发布环境 | staging.example.com |
| **Prod** | 生产环境（只读） | www.example.com |

## Model Configuration

| 配置项 | 值 |
|--------|-----|
| **default_model** | `qwen3.5` |
| **escalation_model** | `qwen3.5-coder` |
| **说明** | 日常测试用例用 default，自动化脚本生成用 escalation |

## Notes

- 所有测试用例必须可自动化执行
- 严重 Bug 必须附带复现步骤
- 发布前必须执行 100% 回归测试
- 测试数据必须脱敏处理
