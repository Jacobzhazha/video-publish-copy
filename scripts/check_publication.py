#!/usr/bin/env python3
"""Validate video publishing copy. Python 3.9+, standard library only."""
import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata

PLATFORM_SECTIONS = {
    "B站": ("标题", "简介", "标签", "置顶评论"),
    "视频号": ("标题", "文案", "话题"),
    "抖音": ("标题", "描述", "话题"),
}
PLATFORM_ORDER = tuple(PLATFORM_SECTIONS)
URL_PATTERN = re.compile(
    r"(?:[a-z][a-z0-9+.-]*://|www\.|mailto:|"
    r"\b(?:[a-z0-9-]+\.)+(?:com|cn|net|org|io|ai|dev|app|co|me|edu|gov)\b)", re.I
)
PLACEHOLDER_PATTERN = re.compile(r"【待补[^】]*】")


def normalize_for_compare(value):
    return "".join(c for c in value if unicodedata.category(c)[0] in "LN").casefold()


def parse_md(text):
    """Compatibility helper: return title and ordered platform-section text lines."""
    title, platforms, _ = _parse(text)
    return title, platforms


def _parse(text):
    title = None
    platforms = {}
    errors = []
    current_platform = current_section = None
    h1_count = 0
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r"^(#{1,6})(?:\s+(.*)|\s*)$", line)
        if match:
            level, name = len(match[1]), (match[2] or "").strip()
            if level == 1:
                h1_count += 1
                if h1_count > 1:
                    errors.append("第 {} 行：只能有一个一级标题".format(number))
                if not name:
                    errors.append("视频名不能为空")
                if title is None:
                    title = name
                current_platform = current_section = None
            elif level == 2:
                if name in platforms:
                    errors.append("第 {} 行：平台章节重复「{}」".format(number, name))
                current_platform, current_section = name, None
                platforms.setdefault(name, {})
            elif level == 3:
                if current_platform is None:
                    errors.append("第 {} 行：小节必须放在平台章节内".format(number))
                else:
                    if name in platforms[current_platform]:
                        errors.append("第 {} 行：小节重复「{} / {}」".format(number, current_platform, name))
                    current_section = name
                    platforms[current_platform].setdefault(name, [])
            else:
                errors.append("第 {} 行：不支持四级及更深的标题".format(number))
        elif line.strip():
            if current_platform is None or current_section is None:
                errors.append("第 {} 行：内容应放在平台小节内".format(number))
            else:
                platforms[current_platform][current_section].append(line)
    return title, platforms, errors


def section_text(platforms, platform, section):
    return "\n".join(platforms.get(platform, {}).get(section, [])).strip()


def check(text, expected_platforms=None, avoid_titles=(), require_complete=False):
    """Return actionable problems; an empty list means structural checks passed."""
    problems = []
    first = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not first.startswith("# "):
        problems.append("首个非空行应为一级标题（# 视频名）")
    title, platforms, parse_errors = _parse(text)
    problems.extend(parse_errors)
    if not title:
        problems.append("缺少有效视频名（# 视频名）")
    present = [p for p in platforms if p in PLATFORM_ORDER]
    if not present:
        problems.append("未找到任何平台章节")
    canonical = [p for p in PLATFORM_ORDER if p in present]
    if present != canonical:
        problems.append("平台顺序应为 B站、视频号、抖音（只保留需要的平台）")
    if expected_platforms is not None and set(present) != set(expected_platforms):
        problems.append("平台范围不符：需要 {}，实际 {}".format("、".join(expected_platforms), "、".join(present)))
    for platform, sections in platforms.items():
        if platform not in PLATFORM_SECTIONS:
            problems.append("未知平台章节「{}」".format(platform))
            continue
        allowed = PLATFORM_SECTIONS[platform]
        required = allowed[:3]
        for section in required:
            if section not in sections:
                problems.append("{} 缺少必填小节「{}」".format(platform, section))
        if list(sections) != [s for s in allowed if s in sections]:
            problems.append("{} 小节未知或顺序错误，应依次为 {}".format(platform, "、".join(allowed)))
        for section in sections:
            if not section_text(platforms, platform, section):
                problems.append("{} 的「{}」内容为空".format(platform, section))
        heading = section_text(platforms, platform, "标题")
        if heading and ("\n" in heading or not normalize_for_compare(heading)):
            problems.append("{} 发布标题应为一行有效文字".format(platform))
        if platform == "B站":
            if len(heading) > 80:
                problems.append("B站标题最多 80 字，当前 {} 字".format(len(heading)))
            value = section_text(platforms, platform, "标签")
            tags = [t.strip() for t in value.split("，") if t.strip()]
            if not 8 <= len(tags) <= 10:
                problems.append("B站标签应为 8–10 个，当前 {} 个".format(len(tags)))
            if any(x in value for x in (",", "\n", "#")) or "，，" in value or value.endswith("，"):
                problems.append("B站标签应用中文逗号分隔，不含换行、# 或空标签")
            normalized = [normalize_for_compare(t) for t in tags]
            if len(set(normalized)) != len(normalized):
                problems.append("B站标签重复（忽略大小写、空白和标点）")
        else:
            value = section_text(platforms, platform, "话题")
            parts = value.split()
            if not parts or any(not re.fullmatch(r"#[\w\u3400-\u9fff]+", part) for part in parts):
                problems.append("{} 话题只写 #话题，用空格分隔".format(platform))
            normalized = [normalize_for_compare(t) for t in parts]
            if len(set(normalized)) != len(normalized):
                problems.append("{} 话题重复".format(platform))
    seen = {}
    avoided = {normalize_for_compare(t) for t in avoid_titles}
    for platform in present:
        value = section_text(platforms, platform, "标题")
        normalized = normalize_for_compare(value)
        if not normalized:
            continue
        if normalized in seen:
            problems.append("{} 与 {} 的标题去除标点、空白和大小写后相同".format(seen[normalized], platform))
        seen[normalized] = platform
        if normalized in avoided:
            problems.append("{} 发布标题与封面或片内标题重复".format(platform))
    if URL_PATTERN.search(text):
        problems.append("发布文案包含网址或外部链接")
    if require_complete and PLACEHOLDER_PATTERN.search(text):
        problems.append("成稿仍含待补占位项")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="视频发布文案.md")
    parser.add_argument("--platforms", nargs="+", choices=PLATFORM_ORDER, help="要求输出的平台，可指定多个")
    parser.add_argument("--avoid-title", action="append", default=[], help="不得重复的封面/片内标题，可多次指定")
    parser.add_argument("--require-complete", action="store_true", help="拒绝待补占位项")
    parser.add_argument("--json", action="store_true", help="输出可供 CI 使用的 JSON")
    args = parser.parse_args(argv)
    try:
        content = args.path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        if args.json:
            print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        else:
            print("无法读取文件：{}".format(exc), file=sys.stderr)
        return 2
    problems = check(content, args.platforms, args.avoid_title, args.require_complete)
    pending = PLACEHOLDER_PATTERN.findall(content)
    if args.json:
        print(json.dumps({"ok": not problems, "problems": problems, "pending": pending}, ensure_ascii=False, indent=2))
    elif problems:
        print("发现 {} 处问题：".format(len(problems)))
        for problem in problems:
            print("- " + problem)
    else:
        print("检查通过" + ("（草稿含 {} 个待补项）".format(len(pending)) if pending else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
