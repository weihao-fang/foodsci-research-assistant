<img src="assets/icon.svg" width="76" height="76" alt="FoodSci 图标">

# FoodSci Research Assistant

**论文润色、文献综述、实验设计与数据分析，一套生物食品科研 Skill。**

从一段原稿、一项课题或一份数据开始，按你手头的材料推进科研工作。纯生物、纯食品或新的交叉需求都可从同一入口处理，无需先匹配预设工作流。

**0.8.1** · Codex Skill / 六入口套件 / 豆包聊天版 · 非商业学习与科研

[立即下载](docs/DOWNLOADS.md) · [Codex 安装](docs/INSTALL_CODEX.md) · [豆包使用](docs/INSTALL_DOUBAO.md) · [功能与研究场景](docs/FEATURES.md)

<a id="先看一个短例子"></a>

## 先看三个使用例子

以下均为合成或虚构教学演示，每例附原始材料与交付结果。选一个与你手头工作接近的任务，安装后就能试。

### 1. 贴一段论文，得到中英文定稿

**这样问：**“使用FoodSci润色这段Results，交付中英文定稿，保留数据和科学含义，删去套话。”

**原稿节选：**

> 值得注意的是，在本研究中，我们对4°C贮藏7天后的草莓样品进行了失重率的测定，结果发现与未涂膜组相比，采用壳聚糖—果胶涂膜的处理组失重率从7.2%降低到了4.8%，这表明这种涂膜处理在降低贮藏期间失重率方面具有一定的积极作用。

**中文定稿节选：**

> 在4°C贮藏7天后，壳聚糖—果胶涂膜组草莓的平均失重率为4.8%，低于未涂膜组的7.2%。

**英文定稿节选：**

> After storage at 4°C for 7 days, mean mass loss was lower in strawberries coated with chitosan–pectin (4.8%) than in uncoated strawberries (7.2%).

删去套话，先给结果；三个独立配对批次的均值口径保留在[完整中英文稿](examples/polishing-quickstart/output.md)中。**[拿这份原稿试一次](examples/polishing-quickstart/input.md)**

### 2. 提出一个课题，得到关键对照与实验方案

**这样问：**“我想减少燕麦发酵凝胶第14天的离水，又不能太硬。请按给定设备和48份上限，设计关键对照并排班。”

| 你要解决的问题 | 示例方案中的具体安排 |
| --- | --- |
| 配方怎么比较？ | 选择3个合法混料点，粉料合计保持100%，与2个加热温度交叉比较。 |
| 发酵还是酸化起作用？ | 每个配方设置活菌发酵与同配方乳酸酸化比较，先验证酸度与加液质量的匹配条件。 |
| 有限设备怎么排？ | 匹配验证通过后，4天×每天2轮×每轮6份，共48份；跨日平衡加热温度的先后。 |
| 最后按什么筛选？ | 以第14天离水为主要终点，同时检查硬度是否处于0.8–1.8 N。 |

这是一份尚未开展的候选设计，附前置验证条件、独立单位、取样和分析口径。**[查看原始条件](examples/formulation-design/input.md)** · [看本次精简方案](examples/formulation-design/quick-output.md)

### 3. 上传一份数据，得到可复算的专业判断

**这样问：**“请分析这4批苹果渣浆的Folin读数，检查‘加热提高酚类含量’的判断，并给我英文Results和补实验建议。”

**SYNTHETIC数据已实际运行代码复算：**

| 同一份数据的表达基础 | 加热相对对照的组均值变化 |
| --- | ---: |
| 每克湿浆料 | **+20.5%** |
| 每克干物质 | **−4.3%** |

独立n=4个配对批次，技术复孔先平均；变化为`100×(加热组均值/对照组均值−1)`。

湿基升高、干基降低，计量基础改变了判断；这些结果尚不能证明结合态酚类释放。[完整计算、英文Results与后续实验](examples/processing-analysis/output.md) · **[原始数据](examples/processing-analysis/task-b-raw.csv)** · [实验记录](examples/processing-analysis/task-b-analysis.md)

从你手头的一段文字或脱敏数据开始：**[安装到Codex](docs/INSTALL_CODEX.md)** · [豆包聊天使用](docs/INSTALL_DOUBAO.md) · [选择下载包](docs/DOWNLOADS.md)

## 具体能帮你做什么？

| 功能 | 能帮你完成的工作 |
| --- | --- |
| **文献搜集与核验** | 设计检索式、筛选相关论文，核对DOI与题录，整理可追溯的文献和证据表。 |
| **综述整理与撰写** | 按主题梳理研究进展，比较一致与矛盾证据，形成综述提纲、对比表和正文。 |
| **课题拆解与规划** | 拆解论文的实验与证据链，提炼研究问题，形成研究路线与关键判别试验。 |
| **实验设计与优化** | 规划因素、对照、独立重复与取样终点，形成实验方案、质量控制和预定分析。 |
| **数据分析与科研图表** | 检查原始数据、单位与批次，选择统计方法，按实际工具计算、作图并交付代码。 |
| **中英文论文写作** | 根据已有证据起草或重组摘要、引言、方法、结果、讨论及图注。 |
| **论文润色与翻译** | 优化中英文逻辑、术语和表达，翻译或压缩正文，删除冗余与过度防御性表述。 |
| **专业审稿与投稿修改** | 检查创新依据、方法统计与主张证据，形成修改清单、审稿回复和投稿材料。 |

这些功能已整合在总Skill中，六入口套件另提供五个任务入口，方便单独调用。检索、核验和计算按当前可用工具执行；未列出的生物、食品及交叉科研需求也可直接提出。[查看功能、入口与典型交付](docs/FEATURES.md)

## 通用科研入口，保留食品与生物专长

下面三条是特色研究示例，用于展示专业适配。方法目录、资源清单和六个任务入口均不限制主题范围；未列出的科研需求直接按研究对象、材料、数据类型和目标产物处理。

| 研究主线 | FoodSci 的专业落点 |
| --- | --- |
| **结构—加工—消化—功能** | 连接蛋白、多糖、食品材料与3D打印，区分结构表征、消化暴露与功能证据，确定最值得补充的对照与终点。 |
| **发酵—代谢—宿主响应** | 串联菌株、底物转化、代谢与菌群信息，处理组学注释、批次与组成型数据，明确细胞、斑马鱼和小鼠证据的解释层级。 |
| **保鲜—贮藏—生产放大** | 围绕时间、温度、配方与工艺组织设计，识别重复测量、独立生产批次、代理指标和真实应用终点。 |

Scientific Agent Skills 的设计、分析与科学交流方法已转化为领域决策规范。FoodOn、FoodData Central、UniProt、dbCAN、QIIME 2、MetaboLights、GNPS、ZFIN/MGI等资源用于规范术语、注释与验证路径；[资源手册](skills/foodsci-research-assistant/references/food-bio-resources.md)说明具体用途、来源及适用边界。

## 从单项任务到整项研究

总入口按任务组合相关方法，保留来源、实验单位和结果定位。既可组织整项研究，也可只完成一次新方法分析、一份课题申请、一段 Results 或一条审稿回复。没有专门模块时，直接运用适用科研方法与实际可用工具推进，不要求先新增Skill或登记方法。[完整功能](docs/FEATURES.md) · [合成任务演示](docs/QUICKSTART.md) · [能力来源](skills/foodsci-research-assistant/references/scientific-adaptation.md)

看实际交付的**合成示例**：[目录外的细胞生物学计算、英文Results与课题申请文字](examples/cell-biology/output.md)；[48份配方—加工—贮藏试验排班](examples/formulation-design/output.md)；[湿基升高、干基降低的计算与英文Results](examples/processing-analysis/output.md)。它们是SYNTHETIC测试，不是真实科研发现，也不限定可处理的方向。

## 在 Codex 中安装

将下面内容直接发给 Codex：

```text
请使用 $skill-installer 安装这个 GitHub Skill：
https://github.com/weihao-fang/foodsci-research-assistant/tree/main/skills/foodsci-research-assistant
保留全部参考、脚本和样例；如有旧版，先检查安装路径和版本再更新。
安装后确认读取的版本是0.8.1，并报告实际安装路径。
```

安装后这样开始：

```text
使用 $foodsci-research-assistant：
我的研究问题是【问题】，现有材料是【文件或数据】，这次需要【具体交付】。
请按实际研究对象、数据和可用工具选择方法，直接完成本次工作。
未列在方法目录中的需求也按任务处理，不强套示例工作流，不补造结果。
```

也可[下载单Skill包](downloads/foodsci-codex-0.8.1.zip?raw=true)手动安装；需要独立选择任务入口时使用[六入口套件](downloads/foodsci-suite-0.8.1.zip?raw=true)。[安装、更新与故障检查](docs/INSTALL_CODEX.md)遵循[OpenAI官方技能说明](https://learn.chatgpt.com/docs/build-skills)。

## 验证与持续更新

检索、计算和文件处理使用宿主实际具备的工具。固定脚本提供RAW264.7与模拟消化的有限描述汇总；其他统计需匹配真实数据并实际运行。资源手册提供查询与解释规则，不附带第三方数据库或账号连接。豆包提供自包含聊天文本，原生技能导入仍待实机验证。

[验证记录](docs/VALIDATION.md) · [更新日志](CHANGELOG.md) · [升级说明](docs/UPGRADING.md) · [方法扩展](skills/foodsci-research-assistant/references/ADD_METHOD.md)

欢迎用最小脱敏例子[反馈问题](CONTRIBUTING.md)。Star方便下次找到，Watch可按自己的偏好接收更新。原创部分限非商业学习与科研，见[LICENSE](LICENSE)；[第三方材料](THIRD_PARTY_NOTICES.md)保留原有许可。
