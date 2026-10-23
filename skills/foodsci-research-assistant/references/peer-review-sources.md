# 专业审稿模块的依据和适用范围

整理日期2026-10-18。这里记录设计来源与实际读到的一手依据，不能代替新任务的文献检索、当前指南或全文核验。

## 吸收的本机技能机制

- **nature-reviewer**：从SKILL.md及technical-concern-taxonomy.md吸收稳定问题ID、claim/evidence定位、Major/Minor与Blocking分开、缺失/未评估状态、无问题配额及隔离报告冻结后汇总。保留实际优点，不为“严厉”而造问题。
- **academic-paper-reviewer**：从SKILL.md、peer_review_report_template.md及re_review_mode_protocol.md吸收领域/方法/统计等分工、不同证据类型的定位、定性有据的判断，以及固定原问题和关闭标准、先查修稿再核对回复的复审闭环。

本模块用自己的简洁流程实现这些原则，不依赖安装来源Skill，不复制其全套调度/schema，不强制三席/五席、虚构身份、主观置信分、录用概率或自动判决。Nature式广泛跨学科意义不自动成为食品专业期刊门槛。来源技能并非Nature或其他出版社对本模块的官方认可。

## 本轮实际读取的一手来源

| 来源 | 本轮实际范围（2026-10-18） | 支持的用途及限制 |
| --- | --- | --- |
| [Food Chemistry官方期刊介绍](https://shop.elsevier.com/journals/food-chemistry/0308-8146) | Elsevier Shop完整Description；ScienceDirect aims-and-scope入口403 | 食品化学/生物化学、分析与食品相关性的范围判断。没有取得完整当前作者指南，不生成字数、图件或AI政策等硬性要求 |
| [Food Hydrocolloids官方期刊介绍](https://shop.elsevier.com/journals/food-hydrocolloids/0268-005X) | Elsevier Shop完整Description；ScienceDirect范围入口403 | 胶体来源/性质、足以评价与重复的理化特征及相应解释；该刊范围不可套到所有食品期刊，不推出统一纯度门槛或全套表征清单 |
| [INFOGEST作者机构原文PDF](https://infogest.hub.inrae.fr/content/download/342/2720?version=1) | Brodkorb等2019，含存档封面的25页PDF；本轮读取第2–7页及20–21页，第7页截图复核 | 静态分阶段方法、终点及消化液衔接细胞的模型限制。DOI为10.1038/s41596-018-0119-1；未证明这是始终最新版本，不能等同人体吸收或完整生理动力学 |
| [ATCC RAW264.7 TIB-71官方说明PDF](https://www.atcc.org/atcc/productsheetpdf/generatehtmlpdf/tib-71) | 身份/用途与培养说明可读，产品网页工具访问失败；PDF截图失败 | 说明小鼠来源研究模型身份。活力、干扰、内毒素及机制检查为按主张的审查判断，不是该产品页提供了全部食品实验阈值 |
| [FDA BAM Chapter3当前版本入口](https://www.fda.gov/food/laboratory-methods-food/bam-chapter-3-aerobic-plate-count) | 实际打开入口链接的[PDF](https://www.fda.gov/media/191248/download?attachment=)，封面/修订史为January2026；核读第1、3–9页 | 好氧平板计数的版本、取样/计数和报告可追溯性；搜索标题残留旧日期未被当作当前版本。APC不等于全部病原阴性，BAM不是通用地区/食品法规限量 |
| [ICMJE稿件准备建议](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html) | Data Collection and Measurements、Statistics、Results、Discussion | 借鉴可评价的统计报告、效应与不确定性、主要/次要终点和不过度解释原则；医学期刊建议不是食品期刊当然强制格式，未取得原始数据不能声称已复算 |

食品检查还复用本包现有蛋白、多糖、抗氧化、消化和RAW方法模块中的已记录来源。新任务要核验具体参数、声称当前政策/法规或确认首次发现时，应实际读取相应原始方法和当前官方依据，并记录本次范围。本轮未单独核验感官标准、各地食品限量或期刊完整AI政策，不虚构这类要求。

## 0.4.0新增领域的共用依据

实验设计与审稿共用同一份方法正文，避免两处保留不同参数或门槛。各文件末尾分别记录2026-10-18实际读到的一手来源、范围和访问限制：[食品3D打印](food-3d-printing.md)、[发酵](fermentation.md)、[斑马鱼与小鼠](animal-models.md)、[功能评价](functional-evaluation.md)、[保鲜贮藏](preservation-storage.md)、[食品生产](production-scaleup.md)。

来源支持研究设计与有边界的审查判断，不表示作者采用该方法、模型已在本产品验证，或当前地区动物审批、食品功能声称、生产及标签法规已确认合规。不能把食品用菌鉴别写成益生功效确认，把模型/品质结果写成人体或安全期限证明。
