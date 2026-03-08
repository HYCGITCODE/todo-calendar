# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

---

## API Keys & Environment

### Tavily Search

| 配置项 | 值 |
|--------|-----|
| **API Key** | `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` |
| **环境变量** | `TAVILY_API_KEY` |
| **安装位置** | `~/.openclaw/workspace/skills/tavily-tool/` |

**配置命令**:
```bash
# Gateway 环境变量配置
openclaw gateway env set TAVILY_API_KEY="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"
```

**使用示例**:
```bash
node skills/tavily-tool/scripts/tavily_search.js --query "best rust http client" --max_results 5
```

---

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
