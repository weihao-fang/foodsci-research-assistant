# 六入口与内部模块

公开版0.8.1默认提供总入口与五个任务入口。只安装总Skill时，下面内部模块均随包可读；套件增加五个可分别选择的同级入口，不重复资源。

| 入口 | 按本次任务读取的内部模块 |
| --- | --- |
| foodsci-research-assistant | 总路由，继承已完成记录，按需联动 |
| foodsci-literature | [检索核验](literature.md)或[综述整理撰写](literature-review.md) |
| foodsci-experimental-design | [研究拆解与规划](research-planning.md)或[具体实验设计](experimental-design.md) |
| foodsci-data-analysis | [数据分析](data-analysis.md)、[图表](figure-evidence.md) |
| foodsci-writing | [写作](writing.md)或[专业润色](polishing.md)，按主题读[领域规则](domain-writing.md) |
| foodsci-peer-review | [专业审稿](peer-review.md)或[投稿检查](submission-review.md) |

总入口自动按任务选择需要的阶段，不要求用户逐一报名字。写综述时复用真实文献记录，综合并形成正文，再做专业润色；数据到稿件使用实际分析→写作→润色。单段编辑直接处理，不重新检索、计算或审稿。纯生物主题不强加食品用途。

0.6.0的foodsci-literature-review并入literature，research-planning并入experimental-design，polishing并入writing，submission-review并入peer-review，插件start在公开版由总入口承担。内部文档保留，因此合并入口不删除能力。升级时整体选择一种安装方式并核对版本，避免混装旧名副本。

当前宿主支持技能调度时按名称调用；否则读取内部指引继续执行。安装ZIP并不等于联网、执行脚本或原生导入已经成功，按实际环境验证。
