---
name: foodsci-peer-review
description: "审查生物食品稿件的主张、贡献、实验统计和证据，进行逐项修订复审，并按任务核对目标期刊规范与投稿材料。"
metadata:
  version: "0.7.0"
  requires-foodsci-research-assistant: "0.7.0"
---

# FoodSci 审稿与投稿

本入口属于FoodSci六入口套件，依赖同级同版本 `foodsci-research-assistant` 总文件夹，不能单独取走。只安装总文件夹也可完成所有任务。

科学贡献、主张、方法统计与修订复审读取[专业审稿](../foodsci-research-assistant/references/peer-review.md)；期刊规范、材料或作者回复读取[投稿检查](../foodsci-research-assistant/references/submission-review.md)。只需格式检查时不强制科学外审；科学审稿也不默认联网查所有期刊。依据作者实际修改与来源回复，不把计划当完成；具体改句应用[专业润色](../foodsci-research-assistant/references/polishing.md)。

按用户本次目标读取相关模块并完成实际交付，共享来源/主张/实验/数据/图ID。没有独立调度接口时直接应用包内规则，不声称有未运行的后台代理；只要局部任务就完成该部分。不要加载全部方法、补造来源/数据或上传私有资料到无关服务。
