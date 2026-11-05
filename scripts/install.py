#!/usr/bin/env python3
"""Install the minimal skill locally without changing client configuration."""
import argparse
from pathlib import Path
import shutil
import sys

AGENTS = {'codex': '.agents', 'claude': '.claude', 'cursor': '.cursor', 'gemini': '.gemini', 'copilot': '.github'}
NAME = 'video-publish-copy'


def install(source, parent):
    source, parent = Path(source).resolve(), Path(parent).expanduser().resolve()
    destination = parent / NAME
    required = ['LICENSE', 'SKILL.md', 'references/platform-rules.md', 'references/examples.md', 'scripts/check_publication.py', 'agents/openai.yaml']
    for name in required:
        if not (source / name).is_file():
            raise ValueError('缺少技能文件：' + name)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('目标已存在，未覆盖：' + str(destination))
    parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()  # Exclusive creation: do not merge into an existing skill.
    try:
        for name in required:
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, target)
    except Exception:
        shutil.rmtree(destination)  # Only this invocation's newly created destination.
        raise
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', required=True, choices=AGENTS)
    parser.add_argument('--scope', choices=['user','project'], default='user')
    parser.add_argument('--project', type=Path, help='项目根目录，scope=project 时必填')
    args = parser.parse_args(argv)
    if args.scope == 'project' and args.project is None:
        parser.error('--scope project 需要 --project')
    if args.scope == 'user' and args.project is not None:
        parser.error('--project 只与 --scope project 一起使用')
    directory = AGENTS[args.agent]
    if args.scope == 'user' and args.agent == 'copilot': directory = '.copilot'
    root = args.project.expanduser() if args.scope == 'project' else Path.home()
    try:
        destination = install(Path(__file__).resolve().parents[1], root / directory / 'skills')
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print('已安装：' + str(destination))
    return 0


if __name__ == '__main__': sys.exit(main())
