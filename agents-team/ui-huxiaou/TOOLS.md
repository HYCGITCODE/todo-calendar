# TOOLS.md - Local Notes

## Design Tools

| 工具 | 用途 |
|------|------|
| **设计软件** | Figma/Sketch 高保真设计稿 |
| **标注工具** | 自动生成开发标注与切图 |
| **设计系统** | 维护 Design Tokens 与组件库 |

## Design Tokens

| 类型 | 说明 |
|------|------|
| **颜色** | 主色、辅助色、语义色（成功/警告/错误） |
| **字体** | 字号、字重、行高规范 |
| **间距** | 4px 基准网格系统 |
| **圆角** | 统一圆角规范（如 4px/8px/12px） |

## Model Configuration

| 配置项 | 值 |
|--------|-----|
| **default_model** | `qwen3.5` |
| **escalation_model** | `qwen3.5-coder` |
| **说明** | 日常设计说明用 default，复杂交互/动效描述用 escalation |

## Notes

- 所有设计稿必须包含状态说明（正常/hover/禁用/错误）
- 设计变更必须通知 PM 与 FE
- 视觉还原度偏差容忍度：< 2px
- 设计稿必须通过可用性审查后才交付 FE
