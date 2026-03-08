# Memory Management

## Memory Structure (记忆结构)
1. **Design Assets:** 存储设计稿版本、标注文件、切图资源。
2. **Usability Logs:** 记录可用性审查意见及 PM 的决策反馈。
3. **Design Tokens:** 存储颜色、字体、间距等变量定义，便于 FE 同步。
4. **Handoff Records:** 记录设计交付时间、接收人 (FE)、确认状态。

## Context Management (上下文管理)
- **Version Control:** 设计稿变更必须版本号递增，旧版本归档。
- **Consistency Check:** 记忆已设计的组件，确保新页面风格一致。

## Update Mechanism (更新机制)
- **Design Freeze:** 设计稿定稿后标记为"Frozen"，变更需走审批。
- **Handoff Complete:** FE 确认接收后更新 Handoff Records。
