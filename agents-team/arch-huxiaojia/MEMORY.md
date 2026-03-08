# Memory Management

## Memory Structure (记忆结构)
1. **Architecture Docs:** 存储系统拓扑图、数据流图、技术选型记录。
2. **API Registry:** 存储所有接口定义、版本历史、变更日志。
3. **Infra State:** 记录云资源状态、成本消耗、环境配置。
4. **Incident Log:** 记录历史故障、根因分析及修复方案。

## Context Management (上下文管理)
- **Change Tracking:** 任何架构变更必须记录并通知 FE/BE/QA。
- **Cost Monitoring:** 每日监控资源消耗，超标预警。

## Update Mechanism (更新机制)
- **API Update:** 接口变更时自动更新 Registry。
- **Deploy Log:** 每次部署记录版本与配置。
