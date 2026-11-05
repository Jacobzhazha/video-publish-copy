# 完整案例 / Complete examples

| 案例 / Case | 平台 / Scope | 输入 / Input | 完整输出 / Full output |
| --- | --- | --- | --- |
| CSV 去重教程 | B站、视频号、抖音 | [input.md](01-csv-dedup/input.md) | [视频发布文案.md](01-csv-dedup/视频发布文案.md) |
| 文件批量命名 | B站、视频号、抖音 | [input.md](02-file-renaming/input.md) | [视频发布文案.md](02-file-renaming/视频发布文案.md) |
| 技能 ZIP 检查 | B站、视频号、抖音 | [input.md](03-zip-inspection/input.md) | [视频发布文案.md](03-zip-inspection/视频发布文案.md) |
| 文案结构校验 | B站、视频号、抖音 | [input.md](04-caption-validation/input.md) | [视频发布文案.md](04-caption-validation/视频发布文案.md) |
| 家常菜教程 | B站、视频号、抖音 | [input.md](05-tomato-eggs/input.md) | [视频发布文案.md](05-tomato-eggs/视频发布文案.md) |
| 桌面整理 | B站、视频号、抖音 | [input.md](06-desk-reset/input.md) | [视频发布文案.md](06-desk-reset/视频发布文案.md) |
| 分数知识讲解 | B站、视频号、抖音 | [input.md](07-fraction-addition/input.md) | [视频发布文案.md](07-fraction-addition/视频发布文案.md) |
| 阅读笔记方法 | B站、视频号、抖音 | [input.md](08-reading-notes/input.md) | [视频发布文案.md](08-reading-notes/视频发布文案.md) |
| 仅视频号的操作教程 | 视频号 | [input.md](09-macos-screenshot/input.md) | [视频发布文案.md](09-macos-screenshot/视频发布文案.md) |
| 仅抖音的摄影知识 | 抖音 | [input.md](10-photo-exposure/input.md) | [视频发布文案.md](10-photo-exposure/视频发布文案.md) |
| 仅 B站的编程教程 | B站 | [input.md](11-json-formatting/input.md) | [视频发布文案.md](11-json-formatting/视频发布文案.md) |
| 活动信息缺失草稿 | B站、视频号、抖音（草稿） | [input.md](12-event-draft/input.md) | [视频发布文案.md](12-event-draft/视频发布文案.md) |

## 复现 / Reproduce

1. 安装技能，进入一个新的 Agent 会话。
2. 把某组 `input.md` 的完整内容交给 Agent，并让它在新目录生成 `视频发布文案.md`。不要覆盖仓库中的留存样本。
3. 使用该目录 `case.json` 记录的平台与封面标题参数检查新文件。
4. 对比事实、平台范围、标题角度和结构；文案措辞不要求逐字相同。

```bash
python3 scripts/validate_examples.py
```

可机读的案例清单见 [manifest.json](manifest.json)。
