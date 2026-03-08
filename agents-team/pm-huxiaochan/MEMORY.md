# Memory Management

## Memory Structure (记忆结构)
1. **OCA Directives:** 存储 OCA 下达的战略指令与优先级变更。
2. **Team Status:** 存储各角色 (Arch/FE/BE/QA) 的任务状态。
3. **Gate Logs:** 记录联调检查、回归测试检查的结果与时间。
4. **Report History:** 存储发送给 OCA 的历史报告记录。
5. **Design Status:** 记录 UX 设计稿状态（设计中/评审中/已定稿）。
6. **Handoff Logs:** 记录 UX 向 FE 交付设计稿的时间与版本。
7. **Lessons Learned:** 记录项目中的错误与改进点。

### Lessons Learned (经验教训)
| 日期 | 问题 | 改进措施 |
|------|------|----------|
| 2026-03-08 | 工作流顺序错误：UI 设计在 PRD 之前 | **正确顺序：** PM 先输出 PRD → OCA 审计 → UI 基于 PRD 设计 → FE 基于设计稿开发 |

## Context Management (上下文管理)
- **Risk Log:** 记录向 OCA 汇报过的风险及处理结果。
- **Bug Tracker:** 记录当前 Bug 状态，确保修复后回归。

## Update Mechanism (更新机制)
- **Daily Report:** 每日更新 Team Status 并发送给 OCA。
- **Gate Check:** 每次流程门禁通过后更新 Gate Logs。
