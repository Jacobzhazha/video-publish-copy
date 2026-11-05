# Agent installation / 多 Agent 安装

[简体中文首页](../README.md) · [English README](../README.en.md)

## Install the complete skill / 安装完整技能

Clone the repository, then run the local installer. It installs the skill instructions, references, publication checker, display metadata and MIT license. It does not change models, prompts, permissions or client settings, and refuses to overwrite existing skills.

```bash
git clone https://github.com/Jacobzhazha/video-publish-copy.git
cd video-publish-copy

# Choose one / 选择一个
python3 scripts/install.py --agent codex
python3 scripts/install.py --agent claude
python3 scripts/install.py --agent cursor
python3 scripts/install.py --agent gemini
python3 scripts/install.py --agent copilot
```

For a project-scoped installation, specify the project root explicitly:

```bash
python3 scripts/install.py --agent codex --scope project --project /path/to/your/project
```

The same commands work on Windows when Git and Python are available; use `py -3` instead of `python3` if appropriate.

## Locations and invocation / 目录与调用

Copy the entire minimal skill folder if installing manually.

| Agent | Project directory | Personal directory | Invoke |
| --- | --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/video-publish-copy/` | `~/.agents/skills/video-publish-copy/` | `$video-publish-copy`; CLI/IDE skill selection through `/skills` or `$` |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/video-publish-copy/` | `~/.claude/skills/video-publish-copy/` | `/video-publish-copy` |
| [Cursor](https://cursor.com/docs/skills) | `.cursor/skills/video-publish-copy/` | `~/.cursor/skills/video-publish-copy/` | Select the skill from the Agent chat `/` menu |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | `.gemini/skills/video-publish-copy/` | `~/.gemini/skills/video-publish-copy/` | `/skills reload`, `/skills list`, then explicitly request the skill |
| [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills) | `.github/skills/video-publish-copy/` | `~/.copilot/skills/video-publish-copy/` | `/skills reload`, `/skills info video-publish-copy`; prompt with `/video-publish-copy` |

VS Code Copilot uses `.github/skills/` or `~/.copilot/skills/`; select the skill through Agent Chat's `/` menu. The Copilot CLI management commands above are not VS Code commands.

Reopen the Agent session if a new skill is not visible.

Gemini CLI also provides its own installer:

```bash
gemini skills install /absolute/path/to/video-publish-copy
gemini skills list --all
```

Use either the repository installer or the host installer. Follow the host's normal activation confirmation when shown.

