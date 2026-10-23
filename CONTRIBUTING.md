# 反馈与贡献

优先提交能复现问题的最小脱敏例子：当前版本、宿主及版本、调用入口、输入、预期、实际输出。文献问题附可公开访问的来源和具体定位；计算问题附字段、单位、独立单位与最小合成数据。不要上传未发表全文、受试者信息、合作方机密或密钥。

在仓库 Issues 中选择错误报告或功能建议。说明问题影响，不用先提出完整实现。方法、证据、计算或安装有误均欢迎反馈；单一示例不能直接推广为整体准确率。

## 修改哪个文件

| 修改目标 | 位置 |
| --- | --- |
| 总入口和阶段路由 | skills/foodsci-research-assistant/SKILL.md |
| 文献、实验、分析、写作或审稿规则 | 总Skill的references目录 |
| 新增实验方法 | [ADD_METHOD.md](skills/foodsci-research-assistant/references/ADD_METHOD.md)与方法模板 |
| 子入口范围 | skills下五个任务入口的SKILL.md |
| 豆包普通聊天适配 | adapters/doubao/FoodSci-豆包聊天版.md |
| 构建、验证 | tools目录 |

每个变更说明解决什么具体问题、实际验证了什么、仍未验证什么。复杂指引使用独立原始输入做前向任务，再核对输出；不要仅靠关键词匹配认定能力已通过。修复只覆盖有依据的问题，保留无关代码与规则。

```text
python -m pip install -r requirements-dev.txt
python -B -m unittest discover -s skills/foodsci-research-assistant/tests -v
python -B -m unittest discover -s tests -v
python -B tools/build.py
python -B tools/validate.py
```

遵循[非商业学习科研许可](LICENSE)，保留[第三方通知](THIRD_PARTY_NOTICES.md)。提交内容前确认有权提供相应材料，不替作者补造方法、文献、统计或伦理信息。
