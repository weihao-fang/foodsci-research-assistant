# Scientific系列能力的食品生物适配

0.8.0于2026-10-23选读Scientific Agent Skills的相关方法，将其改写为食品、生物及交叉研究的决策规范。方法已在本包内，不要求另装整套来源技能。这里只记录实际采用的机制，不把来源库规模、热门程度或自述性能当成FoodSci的验证结果。

## 从通用科研方法到领域工作流

| 实际选读的来源 | 本次采用与落点 |
| --- | --- |
| scientific-critical-thinking、hypothesis-generation、scientific-brainstorming | 先界定问题与推断类型，比较主要竞争解释，以能区分解释的试验推进研究；见[实验拆解](research-decomposition.md)与[方法决策](scientific-methods.md) |
| experimental-design、statistical-power | 混料约束、过程因素与裂区层级；按有意义效应或精度规划独立样本量；见[实验设计](experimental-design.md) |
| exploratory-data-analysis、statistical-analysis、scientific-visualization | 数据字典/来源、独立单位、设计匹配的比较、效应与不确定性、图表证据与可复现运行；见[分析流程](analysis-workflow.md)及[证据图表](figure-evidence.md) |
| scikit-bio、bulk-rnaseq | 组成型菌群与RNA计数分流、ID与注释版本、距离/离散程度、分组验证和多重性；只采用实际问题所需部分，见[方法决策](scientific-methods.md) |
| literature-review、citation-management、research-lookup | 分块检索、题录与全文支持分开、同研究多报告、可追溯证据包与不可合并判断；见[文献核验](literature.md)与[综合方法](synthesis-methods.md) |
| scientific-writing，并结合原有humanizer及anti-defensive-writing | 先锁定真实结果再组织论证，按实际研究证据逐连接综合（食品研究如材料/过程/结构/消化/模型），精修后反向核对科学含义；见[写作](writing.md)、[润色](polishing.md)及[领域表达](domain-writing.md) |
| database-lookup与官方领域资源 | 稳定ID、版本、查询条件、字段与计量基础；把外部注释转为本研究可验证的问题，见[食品—生物证据桥](food-bio-resources.md) |

食品适配的特色示例包括三条主线：结构—加工—消化—功能、发酵—代谢—宿主响应、保鲜—贮藏—生产放大。这些示例不限定可处理的任务；实际任务只验证需要的连接，纯生物研究使用自身模型，不强加食品用途。资源名录、领域术语和机制示意图均不等于实测证据。

## 取舍与运行范围

不复制原多代理编排、付费后端、固定工作量、质量总分或统一论文模板。样本量不写惯例n；不以零检索命中证明首创，不用显著性计票，不把注释/预测当验证。来源中的软件依赖、文件格式能力及研究引擎没有因改写指引而随本包安装。

本次没有迁入第三方程序、数据库、图表或大段原文。固定数值脚本保持RAW264.7与模拟消化的原范围；其他统计及组学需由宿主按真实数据实际执行。真实任务的文件、联网、认证与软件能力分别检查。保留有意义的阴性结果、因果范围和统计不确定性，表达精简按[用户原始规则](style-rules.md)执行。

## 可追溯出处

方法源库：[K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills)，[仓库许可](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/LICENSE.md)为MIT。本次选读的本机scikit-bio技能另声明BSD-3-Clause；本包只独立概括其方法并引用官方API，不携带其程序或文本副本。所用软件与数据库仍按各自许可处理，不能用源库总许可覆盖全部外部资源。

来源论文：Kassis, T., Agarwal, V., He, Y., Patel, D., & Brueckner, A. M. (2026). *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*. [arXiv:2609.00065v2](https://arxiv.org/abs/2609.00065v2)，[DOI](https://doi.org/10.48550/arXiv.2609.00065)。本次核对书目与摘要，不将其文档研究当成FoodSci任务性能证明。

NIST、scikit-bio、DESeq2和scikit-learn官方方法链接在[方法页](scientific-methods.md)逐项列出；FoodOn、FDC、UniProt、dbCAN、QIIME 2、MetaboLights、GNPS、ZFIN、MGI及INFOGEST出处在[资源页](food-bio-resources.md)就近列出。未取得的许可或读取失败如实标记。原Nature/Academic方法脉络见[历史来源](research-capabilities.md)，第三方通知见[许可归属](third-party-notices.md)。
