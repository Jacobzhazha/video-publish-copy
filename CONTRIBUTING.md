# 贡献指南 / Contributing

欢迎改进文案生成行为、平台写法和检查器。提交问题时提供可公开的最小输入、实际输出、期望行为、Agent 与版本；请删除私人材料和凭证。

调整规则时同步更新 `SKILL.md`、相关参考文档与受影响的示例。检查器只验证明确规则，不用机械匹配替代事实或文案质量判断。新增行为检查请使用真实失败输入作为回归案例。

提交前运行：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_examples.py
python3 scripts/check_repo.py
```

新案例保留完整输入、完整输出与 `case.json`，在 `examples/manifest.json` 登记。若修改公共安装行为，保持不覆盖已有技能目录。

English contributions are welcome. Include a minimal reproducible input and full output, update affected guidance, and run the checks above. Keep complete example inputs and outputs.
