# DOI 元数据核验工具

`verify_doi.py` 仅核对用户提供的 DOI、标题、发表年份与 Crossref 返回的元数据。它不搜索替代文献，不验证全文、实验结果、引用所支持的论点、撤稿状态或研究质量。Crossref 元数据可能缺项；不一致应人工核对出版商页面和全文。Crossref 中找不到记录，也不能据此认定 DOI 或文献不存在。

要求 Python 3.10+，仅使用标准库，无需安装依赖。以下命令从Skill 根目录运行：

```powershell
python scripts/verify_doi.py --input my-references.csv --output doi-report.json
python scripts/verify_doi.py --input my-references.csv --output doi-report-online.json --online
```

默认离线：不发送请求，不产生任何 `verified_metadata` 记录。加入 `--online` 后，仅把规范化的 DOI 通过 HTTPS 发给 Crossref；CSV 中的标题、年份不会作为搜索参数发送。工具没有凭证，也没有声称已连接用户的数据库。

## 输入约定

- CSV 使用 UTF-8，可带 BOM，第一行必须有大小写精确、唯一的 `doi,title,year` 表头；额外命名列会忽略。
- 每行三项均必填；含逗号、换行或引号的标题遵循标准 CSV 引号规则。
- `doi` 接受裸 DOI、`doi:` 前缀、`https://doi.org/` 或 `http(s)://dx.doi.org/` URL；忽略大小写和两侧空格，URL 路径进行百分号解码。格式要求 `10.` 后 4–9 位数字、斜杠、非空且无空白或控制字符的后缀。此语法筛选不证明 DOI 有效。
- `title` 必须含至少一个字母或数字；比较时仅移除无属性的常见格式标签（i/b/em/strong/sub/sup/span 及 jats:italic/bold/sub/sup），解码 HTML 实体，使用 Unicode NFKC 和大小写折叠。保留正文中的比较和正负等运算符（`< > ≤ ≥ = ≠ + - − ± × ÷`），其余标点和空白折叠为空格。未知标签样式不删除，避免吞掉数学正文；复杂排版可能需要人工核对。此操作是严格的规范化比较，不使用模糊相似度，也不判断科学语义等价。
- `year` 必须是 1000–9999 的四位整数。与 Crossref `published`、`published-print`、`published-online`、`issued` 中任一年匹配即可；报告会展示所有获得的年份，便于人工区分在线和纸刊日期。
- 每次最多 500 行，至少 1 行。列数过多或单行字段无效标为 `invalid_input`；缺少/重复表头、未闭合的 CSV 引号、空文件、超量文件产生输入错误并且不开始联网。
- 输入与输出路径必须不同，输出目录须已存在；已有输出文件会被拒绝。请指定新的报告文件名以保留历史记录。

## 输出与状态

JSON 保留每行输入 `expected`、`normalized_doi`、`retrieved`、不匹配字段 `mismatches`、Crossref `evidence_url`、UTC `checked_at` 和状态计数。`checked_at` 为 `null` 表示没有执行对应请求；离线的 URL 只是计划核验的端点，不是检索证据。`row` 是 CSV 解析器的逻辑行序号（第一条数据为 2），带多行字段时不是物理文本行号。

| 状态 | 含义 |
| --- | --- |
| `not_checked_offline` | 有效输入，离线未核验 |
| `verified_metadata` | 返回 DOI 一致，且输入标题和年份匹配；范围仅为这三项元数据 |
| `metadata_mismatch` | DOI、标题或年份有不一致/缺项；见 `mismatches` 和原始返回字段 |
| `not_found` | Crossref 返回 HTTP 404；其他注册机构的 DOI 也可能出现此状态 |
| `network_error` | 网络/HTTP 错误、不可用的返回格式，或因 403/429 停止后未请求的记录；见 `reason` |
| `invalid_input` | DOI 语法、标题、年份或该行列数无效 |

同一次运行中每个规范化 DOI 只请求一次；重复行标注 `duplicate_of_row`，复用返回结果，但仍逐行比较各自提供的标题和年份。没有跨运行缓存。

联网请求串行执行，每次新请求之间至少等待 1 秒，每请求 15 秒超时，不自动重试。遇 HTTP 403/429 后停止新的网络请求，余下未请求的 DOI 标为 `network_error`，`checked_at` 为 `null`。超时和其他单条失败会被报告，随后继续处理其他 DOI。应根据失败原因稍后人工重跑。15 秒是底层网络操作超时，不是整个批次的总时限。

退出码：`0` = 所有记录的三项元数据均匹配；`1` = 报告成功写入，但含未核验、错误或不匹配项（默认离线必为 1）；`2` = 输入/输出错误。离线报告生成成功不代表文献已核验。

## 测试

```powershell
python -m unittest discover -s tests -p test_verify_doi.py -v
```

本文件对应的自动单元测试均使用明确标注的合成夹具和模拟 HTTP 传输，不访问互联网，不把合成 DOI 或标题作为真实文献证据。另在 2026-10-18 可用性验收中实际调用 Crossref，核对 INFOGEST、DPPH 与 BCA 三条真实方法文献，并检验错题名、404 及格式错误对照；该记录来自来源插件 0.2.1 的验收，不等同本 Skill 在所有 Agent 中已验收。HTTP 响应截断等单条传输失败会记为 network_error，再继续下一条，不自动重试。

## 官方依据

实现于 2026-10-18 查阅以下一手文档：

- [Crossref REST API：`/works/{doi}` 单条元数据端点](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [Crossref REST API 官方说明：DOI URL 编码、返回结构与注册机构限制](https://github.com/CrossRef/rest-api-doc)
- [Crossref：检查 HTTP 状态和缓存重复请求](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/)

接口和服务限制可能变化；本工具采用保守的串行请求速率，并在服务拒绝访问或限流时停止批次，避免以重试掩盖失败。
