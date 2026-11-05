# 输入

请用 $video-publish-copy 只写 B站标题、简介和标签，置顶评论按需。
封面标题：把嵌套数据摊开看
口播稿：一行 JSON 不好读，可以用 Python 自带的 json 模块重新排版。json.loads 解析字符串，再用 json.dumps 设置 ensure_ascii=False 和 indent=2，中文直接显示，嵌套层级有缩进。重新排版只改变空白表示，示例里的对象字段和值没有变化。遇到不合法 JSON，要先修语法，格式化不会自动修数据。
本案例附带 source.json 和 expected.json，是实际运行 Python 生成的演示数据；不要写成修好了任何接口故障。
