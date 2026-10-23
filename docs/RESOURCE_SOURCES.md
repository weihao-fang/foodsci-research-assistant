# 食品—生物资源的使用与来源

FoodSci 将外部专业资源转化为研究工作流中的查询规则、数据字段和解释边界：统一食品与加工术语，核对组成和蛋白身份，把多糖利用预测接到实际发酵测量，把组学注释接到标准品与模型验证。具体操作见[食品—生物证据桥](../skills/foodsci-research-assistant/references/food-bio-resources.md)和[可填写资源台账](../skills/foodsci-research-assistant/assets/resource-ledger-template.csv)。

以下状态于 **2026-10-23** 核查官方公开说明。它们是外部来源，并未随技能安装；数据查询、文件下载、软件运行和相应认证需要在具体任务中实际执行。开放阅读、开放数据许可与开源代码分别核对。

| 类型 | 官方资源与归属 | 本次采用的内容 | 许可/访问处理 |
|---|---|---|---|
| 术语本体 | [FoodOn / FoodOntology](https://github.com/FoodOntology/foodon) | 食品身份、加工状态和可比较性映射 | 本体 CC BY 4.0；保留版本/术语 ID |
| 食品组成数据 | [USDA FoodData Central](https://fdc.nal.usda.gov/api-guide/) | 食品类型、营养素单位与计量基准 | 数据 CC0；API 需要 key |
| 蛋白知识 | [UniProt Consortium](https://www.uniprot.org/api-documentation/support-data) | 序列版本、物种、成熟链及证据注释 | 数据库 CC BY 4.0；REST 公开读取 |
| 软件/酶知识 | [run_dbcan 团队](https://github.com/bcb-unl/run_dbcan) / [CAZy](https://www.cazy.org/) | 酶家族、底物预测及验证边界 | dbCAN 代码 GPL-3.0；配套库/CAZy 许可单独核对，未确认项记 unknown |
| 分析软件 | [QIIME 2](https://library.qiime2.org/docs) | 样品元数据、流程 provenance 与菌群分析边界 | q2-dada2 为 BSD-3-Clause；插件/参考分类库各有许可 |
| 研究数据仓储 | [EMBL-EBI MetaboLights](https://www.ebi.ac.uk/training/online/courses/metabolights-quick-tour/getting-data-from-metabolights/) | 样品—assay—代谢物映射、公开数据复用 | 逐研究核对许可与公开状态；私有数据需授权 |
| 谱图数据/平台 | [GNPS / UC San Diego](https://ccms-ucsd.github.io/GNPSDocumentation/spectrumcuration/) | 谱库匹配、证据等级与注释可追溯性 | 直接贡献谱默认 CC0；导入第三方谱库逐库核对 |
| 模型生物知识 | [ZFIN](https://zfin.org/downloads) | 斑马鱼阶段、基因型、表型及处理条件 | 公开 TSV；本次许可页未成功读取，整体再分发许可未确认 |
| 模型生物知识 | [MGI / The Jackson Laboratory](https://www.informatics.jax.org/mgihome/other/copyright.shtml) | 小鼠等位基因、背景和表型证据 | 数据/注释 CC BY 4.0；图片另查版权 |
| 共识方法论文 | [INFOGEST / Brodkorb 等，2019](https://www.nature.com/articles/s41596-018-0119-1) | 静态消化的参数记录和推论范围 | 引用方法；不收录原文或附件，不推定附件可再分发 |

这些规则为本项目重新组织的工作方法。未复制第三方软件、整库数据、网页正文或受限图片；第三方名称、ID 与方法保留其原有来源和归属。项目的非商用许可适用于本项目原创部分，不改变外部资源的许可。
