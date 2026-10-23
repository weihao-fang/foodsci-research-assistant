# 综述、领域写作与润色的来源和适配

核对日期：2026-10-22。本版在原0.5.0机制上新增综述和润色，并将研究规划、实验设计、数据分析、写作等任务分为子技能。以下是程序性做法的审计与重写，不把来源名称作为期刊认可、模型性能或领域知识验证的证明。运行需要的规则已随包提供。

| 来源 | 实际采用的做法 | FoodSci落点 |
| --- | --- | --- |
| `nature-writing`、`nature-polishing`及其直接引用的综述/术语/讨论资料 | 按文章任务先修论证再改句；主张—证据—范围；综述按问题比较；术语数字锁定，定向复核改动 | [科研写作](writing.md)、[专业润色](polishing.md) |
| `academic-paper`的文献策略与修订资料 | 文献矩阵、阅读范围、主题综合、争议与有依据的作者判断、局部修订 | [综述整理](literature-review.md) |
| Scientific Agent Skills的`literature-review`、`scientific-writing`、`scientific-critical-thinking` | 检索/筛选执行台账；record/report/study区分；按结局和设计比较证据；成稿与来源定位保持对应 | [综合方法](synthesis-methods.md)、证据模板 |
| Scientific Agent Skills的`bulk-rnaseq`、`pathway-enrichment`、`scikit-bio`、`experimental-design`、`analytical-method-validation`相关段落 | 生物/技术重复、批次、RNA与蛋白层级、富集背景与方法、菌群与数量、检测用途和基质等专门语义 | [领域写作](domain-writing.md) |
| `anti-defensive-writing`的适用部分与用户原文 | 明确真实贡献，围绕证据组织，删除假想反对意见与无信息自我削弱；不写实验流水账 | [去防御规则](style-rules.md) |
| `humanizer` v3.1.0 | 删除无信息强调、重复结尾、假对立、虚构权威和聊天残留，保留作者事实与风格 | 同上；嵌入流程时直接交付最终稿 |

以上本地来源按实际正文和相关引用读取，未遍历整个科学Skill库，也没有迁入其外部服务、付费依赖、固定代理数或成熟领域计算引擎。FoodSci原有十二项方法与交叉桥接构成食品适配基础；新增领域写作围绕实际测量、比较及推断类型优化文字，不预填剂量、阈值或机制。

## 采用时修正的边界

保留重要的阴性、不利与异质结果；不采用“只保留优势”“不说输”、事后更换比较口径或删除不利实验证据。人类风格规则不能把科学上的 `associated with`、`may`、负号、区间或基因命名当作可删除套话。不以误差条重叠判断统计显著性，不作AI检测规避或期刊接收承诺。

系统与范围综述按其实际完成程度报告；PRISMA是报告规范，不能自动证明检索完备或研究质量。GRADE需按适用比较/结局评证据体，不给所有食品/材料论文套统一单篇等级。原来源中的自然科学语料建议不等于现行期刊政策，期刊要求须另查当前官方指南。

## 本轮重新打开的公开来源

- [Scientific Agent Skills官方仓库](https://github.com/K-Dense-AI/scientific-agent-skills)：仓库说明原名Claude Scientific Skills，提供科学研究与沟通类技能。本包选读相关能力，不复述其用户数或整体性能宣传。
- [literature-review源文件](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/literature-review/SKILL.md)与[scientific-writing源文件](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-writing/SKILL.md)：在线正文与本地相关版本交叉核查；链接为可变化main分支，本次快照审计日期如上。
- [PRISMA 2020](https://www.prisma-statement.org/prisma-2020)、[PRISMA-ScR](https://www.prisma-statement.org/scoping)：根据实际综述类型选择报告指引。
- [Cochrane第12章](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-12)：有依据地分组和报告不可合并的证据，不按统计显著性计票。
- [Cochrane第14章](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-14)：按比较/结局评估证据体确定性。

Science领域扩展资料主要为本地正文的选读，未把其源台账中全部外部文献重新核验。实际执行任务仍需核对新的论文、数据和所用规范。作者身份、实测数据、论点支持与元数据核验分开记录；只报告真正完成的检索、筛选、分析、修改与检查。

## 第三方署名

Scientific Agent Skills：K-Dense Inc.，源库[MIT许可](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/LICENSE.md)。humanizer：本地源许可标示 Copyright (c) 2025 Siqi Chen，MIT。相关许可通知见[第三方通知](third-party-notices.md)。Nature、Academic和anti-defensive来源用于分析工作方法，正文为FoodSci重新编写；用户要求加入的规则按用户原文保留。
