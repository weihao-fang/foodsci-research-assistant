# 新增实验方法入口

“实验设计”是统一入口，含材料/体外实验、3D打印、发酵、斑马鱼/小鼠、功能评价、保鲜贮藏及生产放大。完整范围以[方法目录](methods.md)为准；后续方法也放在这一入口下，不必为每个实验新建 Skill。

## 直接在对话中提出需求

可以这样说：

> 在实验设计中新增乳化稳定性方法。我会提供采用的文献和实验记录，请帮我填写方法模板，列出分组、对照、原始数据格式、公式及质控，并标出待核验项。

在当前对话提供方法正文、文献或记录后，助手可据此进行设计和审核，并说明实际读取范围。仅在对话中上传方法不会自动修改已安装的 Skill，也不保证新对话记住该方法。

## 保存为后续可用的方法

以下路径和命令均以独立 Skill 的 `foodsci-research-assistant` 根目录为起点；该目录直接包含 `SKILL.md`。

1. 复制 `assets/method-template.md`，保存为 `references/emulsion-stability.md`。文件名可替换为其他清楚、唯一的小写英文名称；新方法正文中的同目录链接使用文件名，例如 `ADD_METHOD.md`。
2. 填写研究问题、所需输入、独立重复、对照、依据来源、公式单位、干扰检查和结论边界。未查阅的文献标为未核验；未核验的方法保持“草稿，尚未核验”。
3. 打开 [方法目录](methods.md)，复制已有表格的一行，按“方法标识、范围与路由、随包数值程序”三列替换内容。新增链接使用 `emulsion-stability.md`。不要删除模拟消化或 RAW264.7 条目。
4. 按该方法的验收记录检查来源和计算，核对本目录链接与方法登记，并运行下列现有自动测试。新方法的手算对照和实际对话验收需另行记录，不能由既有测试代替。
5. 用修改后的完整文件夹替换已安装的同名独立 Skill；或先重新打包为独立 Skill ZIP，再按宿主支持的方式安装。安装后回读 `references/emulsion-stability.md` 与 `references/methods.md`，在新对话中调用此 Skill 并运行新增方法的验收输入；如界面提示额外操作，以实际提示为准。

以乳化稳定性为例：第一列填 `emulsion-stability`；第二列将复制行中的方法名改为“乳化稳定性”，链接目标改为 `emulsion-stability.md`，范围写明“乳液形成后的稳定性设计与评价，方法草稿待核验”；第三列写“无专用脚本；按实际原始方法设计和分析”。

从 Skill 根目录运行现有自动测试：

```powershell
python -B -m unittest discover -s tests -v
```

需要 ZIP 时，在同一根目录用 PowerShell 重新打包：

```powershell
$skillSource = (Get-Location).Path
Compress-Archive -LiteralPath $skillSource -DestinationPath ..\foodsci-research-assistant-custom.zip
```

ZIP 内应为一个 `foodsci-research-assistant` 文件夹，其中直接包含 `SKILL.md`，并保留 `references/`、`scripts/`、`assets/`、`agents/` 和 `tests/`；再次打包时使用新文件名。这里是修改独立 Skill 源文件并替换安装或重新打包的流程，不依赖账户插件，也没有自动热加载。未完成替换安装时，保留源码与 ZIP，并如实标注“尚未安装更新”。

## 功能与验证边界

- **新增设计与审核指引**：一个方法文件加方法目录的一行即可，不需要改代码或新增 Skill。助手按目录定位正文；登记本身不表示方法有效或已测试。
- **同步专业审稿**：在[食品审稿检查](food-review-checks.md)添加对应主张、证据与最小修复的入口，并链接同一方法文件。新方向进入复审时沿用原问题ID和关闭标准，不另造一套门槛；分发时同步完整文件夹。
- **新增自动数值分析**：这是单独的开发工作。现有 `scripts/analyze.py` 仅接受 `raw` 和 `digestion`；抗氧化、多糖、蛋白和自定义方法不能冒充已接入该程序。需要先明确输入、公式与单位，再编写分析程序及独立的预期结果测试。
- **维护状态**：分别记录来源核验、计算核验与宿主对话验收。完成其中一项不等于另外两项完成；模板示例、合成数字和模拟验收都不能写成真实研究结果。

开始时可使用 [方法模板](../assets/method-template.md)，验收输入可参考 [实验设计与扩展用例](experimental-design-cases.md)。
