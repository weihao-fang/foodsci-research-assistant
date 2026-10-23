# 演示：离线 RAW 与模拟消化描述汇总

**以下输入与数值均为 SYNTHETIC 软件测试样例。本页的样例数值来自既有 0.6.0 离线工作流运行，不是科研发现，也不代表本次 0.7.0 新行为验证。当前版实际软件检查见[验证记录](../VALIDATION.md)。**

## 样例做什么

一个配置依次运行三项固定任务：RAW264.7 描述汇总、模拟消化描述汇总和离线 DOI 状态检查。它不联网，不执行文献检索、综述、写作或审稿，也不生成 P 值、功效和机制判断。

输入均随总入口提供：

- [工作流配置](../../skills/foodsci-research-assistant/assets/examples/workflow.json)
- [RAW 合成 CSV](../../skills/foodsci-research-assistant/assets/examples/SYNTHETIC_raw.csv)
- [消化合成 CSV](../../skills/foodsci-research-assistant/assets/examples/SYNTHETIC_digestion.csv)
- [DOI 合成 CSV](../../skills/foodsci-research-assistant/assets/examples/SYNTHETIC_doi.csv)

CSV 列含义、独立单位与计算前提见[数据契约](../../skills/foodsci-research-assistant/references/data-contract.md)。RAW 参考组在配置中显式为 `control`。

## 在自己的电脑复现

准备 Python 3.10+，在解压后的仓库根目录运行：

```powershell
python -B skills/foodsci-research-assistant/scripts/run_workflow.py --config skills/foodsci-research-assistant/assets/examples/workflow.json --output-dir demo-results
```

`demo-results` 必须是尚不存在的新目录；重复试用时换一个新目录名，保留已有运行记录。固定脚本只用 Python 标准库，不需要模型 API 密钥。

## 阅读输出时看什么

| 文件 | 样例预期与含义 |
| --- | --- |
| `raw-summary.json` | treatment 平均归一化值 85%，独立 n=2；技术孔不会增加独立 n |
| `digestion-summary.json` | 描述性均值 15 mg/L，独立 n=2；不是推断统计或人体吸收结果 |
| `doi-status.json` | 合成非法 DOI 保留 `invalid_input` 等逐记录问题状态，不写成已核验 |
| `run-report.json` | 工作流可为 `completed`，同时 `needs_review=true`，DOI 任务为 `needs_review` |

进程成功说明规定的任务得到了报告，不能说明 DOI 合法或文献已核验。应阅读逐记录状态；本演示的非法 DOI 是预期测试输入，不需要改成真实文献来让报告“全绿”。

## 换成自己的数据

先核对列映射、单位、空白、稀释、参考组与独立实验单位，保留原文件。脚本只直接读取约定 CSV；Excel 或仪器表要先有依据地转换，不默改原件。不同参考组或归一化目的分成不同任务。

此工作流只自动处理 RAW 和消化的有限描述性统计。其他方法按[数据分析指引](../../skills/foodsci-research-assistant/references/data-analysis.md)结合真实设计和可用工具执行；尚未运行时只能交付计划或待运行代码。

[返回快速试用](../QUICKSTART.md) · [返回首页](../../README.md)
