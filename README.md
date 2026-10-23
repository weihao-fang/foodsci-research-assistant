<img src="assets/icon.svg" width="76" height="76" alt="FoodSci 图标">

# FoodSci Research Assistant

**面向食品、生物及交叉研究的证据驱动科研 Skill。**

围绕 **食品基质 → 加工与发酵 → 结构与消化 → 生物响应** 组织研究，将文献、实验和数据连接成可检验的科学论证。可从任一环节进入，也适用于独立的生物学课题。

**0.8.0** · Codex Skill / 六入口套件 / 豆包聊天版 · 非商业学习与科研

[立即下载](docs/DOWNLOADS.md) · [Codex 安装](docs/INSTALL_CODEX.md) · [豆包使用](docs/INSTALL_DOUBAO.md) · [功能与研究场景](docs/FEATURES.md)

## 为食品与生物研究建立专业主线

| 研究主线 | FoodSci 的专业落点 |
| --- | --- |
| **结构—加工—消化—功能** | 连接蛋白、多糖、食品材料与3D打印，区分结构表征、消化暴露与功能证据，确定最值得补充的对照与终点。 |
| **发酵—代谢—宿主响应** | 串联菌株、底物转化、代谢与菌群信息，处理组学注释、批次与组成型数据，明确细胞、斑马鱼和小鼠证据的解释层级。 |
| **保鲜—贮藏—生产放大** | 围绕时间、温度、配方与工艺组织设计，识别重复测量、独立生产批次、代理指标和真实应用终点。 |

Scientific Agent Skills 的设计、分析与科学交流方法已转化为领域决策规范。FoodOn、FoodData Central、UniProt、dbCAN、QIIME 2、MetaboLights、GNPS、ZFIN/MGI等资源用于规范术语、注释与验证路径；[资源手册](skills/foodsci-research-assistant/references/food-bio-resources.md)说明具体用途、来源及适用边界。

## 一套技能，贯通研究与成稿

**证据检索与综述综合 · 课题拆解与实验设计 · 数据分析与科研图表 · 中英文论文写作与精修 · 专业审稿与修订。**

总入口按任务衔接相关模块，保留来源、实验单位和结果定位。既可推演整项研究，也可只完成一张证据表、一段 Results 或一条审稿回复。[完整功能](docs/FEATURES.md) · [合成任务演示](docs/QUICKSTART.md) · [能力来源](skills/foodsci-research-assistant/references/scientific-adaptation.md)

看两份0.8.0实际交付的**合成示例**：[48份配方—加工—贮藏试验怎样排班](examples/formulation-design/output.md)；[湿基升高、干基降低，怎样计算并写成英文Results](examples/processing-analysis/output.md)。它们是SYNTHETIC测试，不是真实科研发现。

## 在 Codex 中安装

将下面内容直接发给 Codex：

```text
请使用 $skill-installer 安装这个 GitHub Skill：
https://github.com/weihao-fang/foodsci-research-assistant/tree/main/skills/foodsci-research-assistant
保留全部参考、脚本和样例；如有旧版，先检查安装路径和版本再更新。
安装后确认读取的版本是0.8.0，并报告实际安装路径。
```

安装后这样开始：

```text
使用 $foodsci-research-assistant：
我研究发酵植物蛋白，已有文献和预实验结果。
请梳理“加工—结构—消化—功能”的证据链，提出最有判别力的下一步实验，
并将现有结果写成一段英文 Results。只采用实际材料，不补造结果。
```

也可[下载单Skill包](downloads/foodsci-codex-0.8.0.zip?raw=true)手动安装；需要独立选择任务入口时使用[六入口套件](downloads/foodsci-suite-0.8.0.zip?raw=true)。[安装、更新与故障检查](docs/INSTALL_CODEX.md)遵循[OpenAI官方技能说明](https://learn.chatgpt.com/docs/build-skills)。

## 验证与持续更新

检索、计算和文件处理使用宿主实际具备的工具。固定脚本提供RAW264.7与模拟消化的有限描述汇总；其他统计需匹配真实数据并实际运行。资源手册提供查询与解释规则，不附带第三方数据库或账号连接。豆包提供自包含聊天文本，原生技能导入仍待实机验证。

[验证记录](docs/VALIDATION.md) · [更新日志](CHANGELOG.md) · [升级说明](docs/UPGRADING.md) · [方法扩展](skills/foodsci-research-assistant/references/ADD_METHOD.md)

欢迎用最小脱敏例子[反馈问题](CONTRIBUTING.md)。Star方便下次找到，Watch可按自己的偏好接收更新。原创部分限非商业学习与科研，见[LICENSE](LICENSE)；[第三方材料](THIRD_PARTY_NOTICES.md)保留原有许可。
