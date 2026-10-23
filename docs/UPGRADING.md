# 更新与维护

## 使用者更新

1. 在[CHANGELOG](../CHANGELOG.md)查看行为变化和验证范围。
2. 备份旧包及自行新增方法，确认当前实际安装路径和版本。
3. 选择单总Skill或六入口套件，完整替换对应文件夹。不要把不同版本文件混合覆盖；首次替换旧副本的操作由使用者明确选择。
4. 确认入口读取0.8.0，运行一个小任务和必要的离线样例。

项目级与用户级可能同时发现同名Skill。以技能列表和实际读取路径为准，不假定它们会自动合并。豆包新聊天需重新提供聊天规范；原生工作技能的更新方式以实际界面为准。

## 0.6到0.7入口迁移

| 原入口 | 公开版入口 |
| --- | --- |
| foodsci-start、总Skill | foodsci-research-assistant |
| foodsci-literature、foodsci-literature-review | foodsci-literature |
| foodsci-research-planning、foodsci-experimental-design | foodsci-experimental-design |
| foodsci-data-analysis | foodsci-data-analysis |
| foodsci-writing、foodsci-polishing | foodsci-writing |
| foodsci-peer-review、foodsci-submission-review | foodsci-peer-review |

内部模块未删除：总Skill可继续处理旧任务，只是独立选择的入口减少。原私人插件和公开分发版本分别维护，不因本仓库更新自动修改别人的安装或账户。

从旧多入口安装迁移时，先备份并确认来源，再由使用者将旧版 `foodsci-start`、`foodsci-literature-review`、`foodsci-research-planning`、`foodsci-polishing`、`foodsci-submission-review` 独立目录移出宿主技能发现目录。同名保留入口也应整目录替换为同版本。仅复制六个新目录不会自动停用旧入口；若旧名来自已安装插件，应在宿主中停用对应旧插件，不能直接删除其缓存。

## 维护者发新版

0.8.0沿用0.7的六入口结构；原有自定义方法可在备份后迁回总Skill，先核对新增Scientific决策和资源解释规则是否与自定义内容冲突。旧的0.7下载ZIP继续保留，当前推荐文件及SHA256SUMS指向0.8。

完整资源只维护在 `skills/foodsci-research-assistant/`，五个薄入口引用它，不复制长正文。修改VERSION、六个Skill的metadata.version和薄入口依赖版本，再记录变更；历史来源版本字段不随发布号冒充更新。

新增方法先按[方法入口](../skills/foodsci-research-assistant/references/ADD_METHOD.md)补指导与来源。新增计算必须实现数据契约、可复现代码和有意义数值测试。豆包轻量规范同步共同规则，不承诺其具有文件系统或脚本工具。

按[贡献说明](../CONTRIBUTING.md)完成回归、结构和真实任务核对，然后运行 `python -B tools/build.py`。同版本生成文件会重建；要保留旧包，请先升版本。SHA256SUMS随构建更新。CI验证不自动创建公开Release，发布由维护者明确执行。

已有GitHub仓库按正常Git流程查看差异、选择本次修改文件提交，再推送main；`tools/publish_github.py`只用于新建仓库，不用于升级已存在的origin。推送后核对实际Actions结果、下载包和版本。不要把本机work目录、登录配置或私有测试回执作为项目内容上传。
