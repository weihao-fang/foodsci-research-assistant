# 在 Codex 中安装 FoodSci 0.8.0

FoodSci 支持生物、食品及交叉方向的科研工作。默认安装总入口即可使用全部内部路线；需要分别点选任务时再安装六入口套件。

## 选择下载包

| 下载内容 | 适用方式 |
| --- | --- |
| [foodsci-codex-0.8.0.zip](../downloads/foodsci-codex-0.8.0.zip) | 单包：`foodsci-research-assistant` 总入口及全部资源 |
| [foodsci-suite-0.8.0.zip](../downloads/foodsci-suite-0.8.0.zip) | 六入口：总入口与五个任务子入口，共享总包资源 |
| [技能源码](../skills/foodsci-research-assistant/SKILL.md) | 在当前仓库查看技能内容与版本 |

套件包含下列六个入口。五个子入口必须与总入口安装在同一技能父目录；不能只取一个子入口后丢弃总包。

| 技能名 | 范围 |
| --- | --- |
| `foodsci-research-assistant` | 总入口，按任务选择路线 |
| `foodsci-literature` | 文献检索、核验与综述 |
| `foodsci-experimental-design` | 研究规划与实验设计 |
| `foodsci-data-analysis` | 已有数据分析与图表 |
| `foodsci-writing` | 科研起草、润色、翻译与精简 |
| `foodsci-peer-review` | 专业审稿、修订与投稿材料检查 |

## 手动安装

1. 下载一个包并解压。定位真正含有 `SKILL.md` 的技能目录。
2. 将单包中的 `foodsci-research-assistant` 目录，或套件中的全部六个技能目录，复制到用户技能目录 `$HOME/.agents/skills/`。Windows 对应当前用户主目录下的 `.agents/skills/`；可通过 `$env:USERPROFILE` 找到主目录。
3. 确认最终路径类似 `.agents/skills/foodsci-research-assistant/SKILL.md`；`references/`、`assets/` 等随总包保留。不要把整个发布包再套一层复制到技能目录。
4. 也可在某个项目内安装到项目的 `.agents/skills/`，供该项目使用。已有同名技能时先比较版本，保留自己的修改，再决定替换；不要在用户和项目目录重复放置同名版本。

上述目录来自 OpenAI 当前 [Build skills 官方文档](https://learn.chatgpt.com/docs/build-skills)。截至 2026-10-23，该页面列出用户级 `.agents/skills` 与仓库级 `.agents/skills`，并说明 Codex 会发现技能变更；未显示时重启 Codex。

## 直接在Codex中安装（推荐）

打开Codex，将下面整段发给它；公开仓库不要求申请FoodSci账号或购买本项目授权：

```text
请使用 $skill-installer 安装这个 GitHub Skill：
https://github.com/weihao-fang/foodsci-research-assistant/tree/main/skills/foodsci-research-assistant
保留全部参考、脚本和样例；先检查本机安装目标和已有同名版本。
安装后读取SKILL.md，确认版本为0.8.0并报告实际路径。
```

只有仓库中确实存在相应版本标签时才指定该标签；初次发布可从实际存在的默认分支安装。

官方支持用 `$skill-installer` 从其他仓库下载技能。需要六入口时可发送：

```text
请使用 $skill-installer，从 weihao-fang/foodsci-research-assistant 的main分支安装：
skills/foodsci-research-assistant
skills/foodsci-literature
skills/foodsci-experimental-design
skills/foodsci-data-analysis
skills/foodsci-writing
skills/foodsci-peer-review
将六个目录放在同一技能父目录，检查已有版本，并确认资源引用有效。
```

已有旧版时，安装器可能因同名目录存在而停止；这用于保护已有文件。可让Codex先比较版本与自定义内容，再将旧目录备份到技能发现目录外，安装新目录并迁回需要保留的方法。不要把不同版本混合覆盖，具体迁移见[升级说明](UPGRADING.md)。

注意安装器的版本差异：本次核对的预装安装器仍默认写入 `$CODEX_HOME/skills`，通常是 `~/.codex/skills`；这与当前官方列出的手动目录不同。让安装器报告实际路径，安装后检查 Codex 是否发现该技能；不要仅凭“文件已复制”判断加载成功。此观察只代表本次核对环境，不保证所有客户端使用同一默认值。

## 检查是否可用

在 Codex 中显式调用 `$foodsci-research-assistant`，要求它说明实际读取的 `SKILL.md` 路径，并让它完成一个短任务，例如：

> 使用 FoodSci：我有三次独立培养，每次三个复孔。请说明实验单位和汇总方式，再列出开展统计分析前缺少的信息。不要生成实验结果。

验收时检查技能是否被发现、是否实际读取总包资源、是否区分独立培养与复孔。套件还应选一个子入口，确认它能找到同级总包。若未显示，先重启，再检查目录层级、文件名和同名版本。

安装不会自动赋予联网、文件访问、Python、数据库或仪器权限。只有实际运行过的计算才能称为结果；没有数据时交付方案，没有联网时将实时文献及期刊规范标为未外部核验。脚本的适用范围与输入要求以总包实际说明为准。

本教程根据官方文档和包结构编写。公开仓库下载、文件安装和客户端实际发现应分别核对；文件复制成功不代表完整加载验收。实际验证范围见[验证记录](VALIDATION.md)，更多平台区别见[豆包使用说明](INSTALL_DOUBAO.md)。

本项目授权用于非商业学习与科研，具体条款见 [LICENSE](../LICENSE)；第三方适配内容保留各自许可，见[第三方通知](../THIRD_PARTY_NOTICES.md)。
