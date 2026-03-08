# Memory Management

## Memory Structure (记忆结构)
1. **API Docs:** 存储接口定义、错误码字典、变更历史。
2. **DB Schema:** 存储数据库结构、迁移脚本。
3. **Logic Map:** 记录核心业务逻辑流程图。
4. **Bug Fix Record:** 记录已修复的后端 Bug 及回归结果。

## Context Management (上下文管理)
- **Data Consistency:** 记录数据一致性校验结果。
- **Regression Check:** 修复 Bug 时记录可能影响的关联接口。

## Update Mechanism (更新机制)
- **API Update:** 接口变更时同步通知 FE/QA。
- **Fix Confirm:** 修复 Bug 后更新状态为"待回归"。
