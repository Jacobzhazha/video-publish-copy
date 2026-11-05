"""Behavioral regression tests for the publication checker."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_publication.py'
spec = importlib.util.spec_from_file_location('checker', SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
BASE = '''# 一个视频

## B站
### 标题
Python整行去重怎么保留顺序
### 简介
只删除整行完全相同的记录。
### 标签
Python，CSV，去重，数据清洗，表格整理，标准库，文件处理，编程教程

## 视频号
### 标题
表格重复记录该怎么删？
### 文案
先留原文件，再比较整行。你按什么判断重复？
### 话题
#Python #表格整理

## 抖音
### 标题
同名记录先别删
### 描述
整行不一样，就先留着。
### 话题
#数据清洗 #Python
'''


class PublicationTests(unittest.TestCase):
    def rejects(self, value, **kwargs):
        self.assertTrue(checker.check(value, **kwargs))

    def test_full_copy(self):
        self.assertEqual([], checker.check(BASE, expected_platforms=list(checker.PLATFORM_ORDER), require_complete=True))

    def test_single_platform(self):
        self.assertEqual([], checker.check('# 视频\n\n' + BASE.split('## 视频号')[1].split('## 抖音')[0].join(['## 视频号','']), expected_platforms=['视频号']))

    def test_empty(self): self.rejects('')
    def test_missing_video_name(self): self.rejects(BASE.replace('# 一个视频', '# '))
    def test_wrong_first_heading(self): self.rejects(BASE.replace('# 一个视频', '说明文字'))
    def test_two_video_names(self): self.rejects(BASE + '\n# 第二个视频\n')
    def test_unknown_platform(self): self.rejects(BASE.replace('## 抖音', '## 其他'))
    def test_duplicate_platform(self): self.rejects(BASE + '\n## 视频号\n### 标题\n新标题\n')
    def test_duplicate_section(self): self.rejects(BASE.replace('### 简介', '### 标题\n重复标题\n### 简介'))
    def test_missing_required_section(self): self.rejects(BASE.replace('### 简介\n只删除整行完全相同的记录。', ''))
    def test_empty_required_section(self): self.rejects(BASE.replace('只删除整行完全相同的记录。', ''))
    def test_unknown_section(self): self.rejects(BASE.replace('### 简介', '### 步骤'))
    def test_section_order(self): self.rejects(BASE.replace('### 标题\nPython整行去重怎么保留顺序\n### 简介\n只删除整行完全相同的记录。', '### 简介\n先给结论。\n### 标题\nPython整行去重怎么保留顺序'))
    def test_platform_order(self): self.rejects('# 视频\n' + BASE[BASE.index('## 抖音'):] + BASE[BASE.index('## B站'):BASE.index('## 抖音')])
    def test_scope_extra_platforms(self): self.rejects(BASE, expected_platforms=['B站'])
    def test_scope_missing_platforms(self): self.rejects(BASE[:BASE.index('## 视频号')], expected_platforms=['B站','视频号'])
    def test_empty_optional_section(self): self.rejects(BASE.replace('## 视频号', '### 置顶评论\n\n## 视频号'))
    def test_optional_section(self): self.assertEqual([], checker.check(BASE.replace('## 视频号', '### 置顶评论\n先备份再修改。\n\n## 视频号')))
    def test_title_with_only_punctuation(self): self.rejects(BASE.replace('同名记录先别删', '！？'))
    def test_multiline_title(self): self.rejects(BASE.replace('同名记录先别删', '同名记录\n先别删'))
    def test_bilibili_title_limit(self): self.rejects(BASE.replace('Python整行去重怎么保留顺序', '字'*81))
    def test_bilibili_title_boundary(self): self.assertEqual([], checker.check(BASE.replace('Python整行去重怎么保留顺序', '字'*80)))
    def test_too_few_tags(self): self.rejects(BASE.replace('，编程教程', ''))
    def test_too_many_tags(self): self.rejects(BASE.replace('，编程教程', '，编程教程，例子一，例子二，例子三'))
    def test_duplicate_tags_casefold(self): self.rejects(BASE.replace('，CSV', '，python'))
    def test_english_comma(self): self.rejects(BASE.replace('Python，CSV', 'Python,CSV'))
    def test_empty_tag(self): self.rejects(BASE.replace('Python，CSV', 'Python，，CSV'))
    def test_tag_hashtag(self): self.rejects(BASE.replace('Python，CSV', '#Python，CSV'))
    def test_topic_prose(self): self.rejects(BASE.replace('#Python #表格整理', '#Python 欢迎来看'))
    def test_empty_topics(self): self.rejects(BASE.replace('#Python #表格整理', ''))
    def test_duplicate_topics(self): self.rejects(BASE.replace('#Python #表格整理', '#Python #python'))
    def test_attached_topics(self): self.rejects(BASE.replace('#Python #表格整理', '#Python#表格整理'))
    def test_duplicate_titles_casefold(self): self.rejects(BASE.replace('Python整行去重怎么保留顺序', 'ABC').replace('同名记录先别删', 'a b c！'))
    def test_cover_title(self): self.rejects(BASE, avoid_titles=['同名记录，先别删！'])
    def test_links(self):
        for url in ['https://example.com', 'HTTP://example.com', 'ftp://example.net', 'www.example.cn', 'example.org', '[入口](https://example.com)']:
            with self.subTest(url=url): self.rejects(BASE.replace('只删除整行完全相同的记录。', url))
    def test_placeholder_draft(self): self.assertEqual([], checker.check(BASE.replace('只删除整行完全相同的记录。', '【待补：活动日期】')))
    def test_placeholder_final(self): self.rejects(BASE.replace('只删除整行完全相同的记录。', '【待补：活动日期】'), require_complete=True)
    def test_orphan_content(self): self.rejects(BASE.replace('# 一个视频', '# 一个视频\n额外说明'))
    def test_orphan_section(self): self.rejects(BASE.replace('# 一个视频', '# 一个视频\n### 说明\n额外说明'))
    def test_deep_heading(self): self.rejects(BASE + '\n#### 提醒\n内容\n')
    def test_cli_exit_codes_and_bom(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'copy.md'
            path.write_text(BASE, encoding='utf-8-sig')
            good=subprocess.run([sys.executable,str(SCRIPT),str(path),'--json'],capture_output=True,text=True)
            self.assertEqual(0,good.returncode); self.assertIn('"ok": true',good.stdout)
            path.write_text(BASE.replace('#Python #表格整理','无话题'),encoding='utf8')
            self.assertEqual(1,subprocess.run([sys.executable,str(SCRIPT),str(path)],capture_output=True).returncode)
            self.assertEqual(2,subprocess.run([sys.executable,str(SCRIPT),str(path)+'missing'],capture_output=True).returncode)
            path.write_bytes(b'\xff\xfe\xff')
            self.assertEqual(2,subprocess.run([sys.executable,str(SCRIPT),str(path)],capture_output=True).returncode)


if __name__ == '__main__': unittest.main()
