# Memory Management

## Memory Structure (记忆结构)
1. **Component Lib:** 存储组件库文档、版本及使用示例。
2. **UI State:** 记录页面状态逻辑、交互细节说明。
3. **Integration Log:** 记录接口联调问题及解决方案。
4. **Bug Fix Record:** 记录已修复的 UI Bug 及回归结果。

## Context Management (上下文管理)
- **Version Control:** 代码提交关联任务 ID。
- **Regression Check:** 修复 Bug 时记录可能影响的关联页面。

## Update Mechanism (更新机制)
- **Component Update:** 新增组件时更新文档。
- **Fix Confirm:** 修复 Bug 后更新状态为"待回归"。
