<p align="right"><a href="README.md">简体中文</a> · <b>English</b></p>

<p align="center"><img src="assets/banner.svg" alt="Video Publish Copy: one script, platform-specific publishing copy" width="100%"></p>

# Video Publish Copy

Turn a video script, voiceover or brief into **platform-specific Chinese publishing copy for Bilibili, WeChat Channels and Douyin**. Each platform gets its own title and copy, followed by a local structural check.

[Quick start](#quick-start) · [Downloads](https://github.com/Jacobzhazha/video-publish-copy/releases/latest) · [12 complete examples](examples/README.md) · [Agent installation](docs/installation.md)

## What it produces

| Platform | Editorial angle | Output |
| --- | --- | --- |
| Bilibili | Searchable subject and concrete questions | Title, conclusion-first description, 8–10 tags, optional pinned comment |
| WeChat Channels | Specific results and natural conversation | Title, short caption, hashtags |
| Douyin | Results, details and contrast | Title, short description, hashtags |

Request all three platforms or any subset. The output file is `视频发布文案.md`.

## Quick start

You need an available Agent and **Python 3.9+** to run the checker. No Python packages are required.

```bash
git clone https://github.com/Jacobzhazha/video-publish-copy.git
cd video-publish-copy
python3 scripts/install.py --agent codex
```

The installer copies only the skill files into `~/.agents/skills/video-publish-copy/`. It refuses to overwrite an existing skill. Reopen the Agent session if the skill is not visible. Use `claude`, `cursor`, `gemini` or `copilot` for another host; see the [installation guide](docs/installation.md).

Send this in Codex:

> Use $video-publish-copy to write Chinese publishing copy for Bilibili, WeChat Channels and Douyin. Save it as 视频发布文案.md.  
> Video script: A demo CSV contains six rows. Removing fully identical rows leaves four, preserving the first occurrence and the original file. Python's csv module reads and writes the files. Rows with the same name but different contents must remain.  
> Cover title: 表格去重前先留原件

Claude Code uses `/video-publish-copy`. Cursor and VS Code Copilot expose skills through the Agent chat `/` menu. Other host commands are documented in the installation guide.

## Complete examples, with inputs

There are **12 complete examples and 30 platform outputs**: 11 complete cases plus one intentional draft with missing facts. Every case contains `input.md`, the full generated `视频发布文案.md`, and `case.json` with its scope and validation settings.

| Topic | Scope | Complete case |
| --- | --- | --- |
| CSV deduplication | Three platforms | [Open](examples/01-csv-dedup/) |
| Batch file naming | Three platforms | [Open](examples/02-file-renaming/) |
| Inspecting a skill ZIP | Three platforms | [Open](examples/03-zip-inspection/) |
| Checking publishing copy | Three platforms | [Open](examples/04-caption-validation/) |
| Tomato and egg recipe | Three platforms | [Open](examples/05-tomato-eggs/) |
| Desk organization | Three platforms | [Open](examples/06-desk-reset/) |
| Adding fractions | Three platforms | [Open](examples/07-fraction-addition/) |
| Reading notes | Three platforms | [Open](examples/08-reading-notes/) |
| Mac region screenshots | Channels only | [Open](examples/09-macos-screenshot/) |
| Window-light portraits | Douyin only | [Open](examples/10-photo-exposure/) |
| JSON formatting | Bilibili only | [Open](examples/11-json-formatting/) |
| Event details missing | Three-platform draft | [Open](examples/12-event-draft/) |

## Inputs and outputs

Provide a script, voiceover or brief, plus optional platform selection and existing cover or in-video titles. The skill preserves supplied numbers, units, conditions and scope. Missing essential facts become `【待补：…】` placeholders; unnecessary missing details may be omitted.

The Agent writes the copy. Python checks it. There is no separate generation API, API-key setup or automatic social publishing.

```markdown
# Video name

## B站
### 标题
### 简介
### 标签
### 置顶评论

## 视频号
### 标题
### 文案
### 话题

## 抖音
### 标题
### 描述
### 话题
```

The Bilibili pinned comment is optional. Only requested platforms appear.

## Validate locally

```bash
python3 scripts/check_publication.py /path/to/视频发布文案.md --require-complete
python3 scripts/check_publication.py /path/to/视频发布文案.md \
  --platforms 视频号 抖音 --avoid-title 'Existing cover title' --require-complete
python3 scripts/validate_examples.py
python3 -m unittest discover -s tests -v
```

The checker covers structure, required sections, order, duplicate titles, Bilibili title length, tags, hashtags and URLs. `--json` emits structured results. Exit codes: `0` passed, `1` content problems, `2` argument or file errors. `--require-complete` rejects unfinished placeholders.

## Repository

`SKILL.md` is the entry point. `references/` holds writing guidance; `agents/openai.yaml` supplies Codex display metadata. `scripts/` provides the checker, local installer and example validation. `examples/` contains all inputs and outputs; `tests/` contains regression tests and `docs/` documents installation and usage.

## Author and license

[**Jacobzhazha**](https://github.com/Jacobzhazha)  
WeChat public account: **渣渣的赛博宇宙**

[MIT License](LICENSE) · [Contributing](CONTRIBUTING.md) · [Report an issue](https://github.com/Jacobzhazha/video-publish-copy/issues)
