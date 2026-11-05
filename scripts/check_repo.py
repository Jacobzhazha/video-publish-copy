#!/usr/bin/env python3
"""Offline repository checks: local links, case artifacts and public-file hygiene."""
import csv
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


def main():
    root=Path(__file__).resolve().parents[1]
    problems=[]; link_count=0
    for path in root.rglob('*'):
        if not path.is_file() or any(part in {'.git','__pycache__','.venv','work','dist'} for part in path.relative_to(root).parts): continue
        if path.suffix not in {'.md','.py','.json','.yml','.yaml','.svg'} and path.name not in {'LICENSE','.gitignore'}: continue
        text=path.read_text(encoding='utf8')
        if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,}|/(?:Users|home)/[^/]+/',text):
            problems.append(str(path.relative_to(root))+': 发现疑似凭证或私人绝对路径')
        if path.suffix != '.md': continue
        outside_code=re.sub(r'```.*?```','',text,flags=re.S)
        targets=re.findall(r'\[[^\]]*\]\(([^)]+)\)',outside_code)+re.findall(r'(?:src|href)="([^"]+)"',outside_code)
        for target in targets:
            target=target.strip().split(' "',1)[0]
            if re.match(r'^[a-z][a-z0-9+.-]*:',target,re.I) or target.startswith('#'): continue
            target=unquote(target.split('#',1)[0])
            if target and not (path.parent/target).exists(): problems.append(str(path.relative_to(root))+': 链接目标不存在 '+target)
            link_count+=1
    skill=(root/'SKILL.md').read_text(encoding='utf8')
    if not re.match(r'^---\nname: video-publish-copy\ndescription: .+?\n',skill): problems.append('技能 frontmatter 缺少 name 或 description')
    rows=list(csv.DictReader((root/'examples/01-csv-dedup/source.csv').open(encoding='utf8')))
    expected=list(csv.DictReader((root/'examples/01-csv-dedup/expected.csv').open(encoding='utf8')))
    unique=list(dict.fromkeys(tuple(row.items()) for row in rows))
    if len(rows)!=6 or len(expected)!=4 or unique != [tuple(row.items()) for row in expected]: problems.append('CSV 案例事实与原始数据不符')
    source=json.loads((root/'examples/11-json-formatting/source.json').read_text())
    if source != json.loads((root/'examples/11-json-formatting/expected.json').read_text()): problems.append('JSON 排版改变了数据')
    for problem in problems: print('- '+problem)
    print('仓库检查{}；{} 个本地链接。'.format('失败' if problems else '通过',link_count))
    return bool(problems)


if __name__=='__main__': sys.exit(main())
