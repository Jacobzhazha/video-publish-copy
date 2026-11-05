#!/usr/bin/env python3
"""Validate all stored cases and their deliberate draft/final distinction."""
import json
from pathlib import Path
import sys
from check_publication import check, PLACEHOLDER_PATTERN


def main():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'examples/manifest.json').read_text(encoding='utf8'))
    failed=[]; summaries=[]
    for item in manifest:
        directory=root/'examples'/item['id']
        path=directory/item['output']
        try:
            text=path.read_text(encoding='utf8')
            assert (directory/item['input']).is_file()
            assert json.loads((directory/'case.json').read_text(encoding='utf8'))==item
        except (OSError,AssertionError,ValueError) as exc:
            failed.append('{}: {}'.format(item['id'],exc)); continue
        errors=check(text,item['platforms'],item['avoid_titles'],item['complete'])
        pending=PLACEHOLDER_PATTERN.findall(text)
        if not item['complete'] and not pending: errors.append('缺失信息案例应保留待补项')
        if not item['complete'] and not check(text,item['platforms'],item['avoid_titles'],True):
            errors.append('缺失信息草稿应被最终稿检查拦下')
        summaries.append({'id':item['id'],'ok':not errors,'platforms':len(item['platforms']),'complete':item['complete'],'pending':len(pending)})
        failed.extend(item['id']+': '+error for error in errors)
    print(json.dumps({'ok':not failed,'cases':len(manifest),'platform_outputs':sum(x['platforms'] for x in summaries),'results':summaries,'problems':failed},ensure_ascii=False,indent=2))
    return bool(failed)


if __name__=='__main__': sys.exit(main())
