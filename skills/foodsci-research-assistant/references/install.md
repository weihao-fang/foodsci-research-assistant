# 安装与第一次使用（0.8.0）

Codex单包解压后得到foodsci-research-assistant，将整个文件夹复制到项目的.agents/skills/或用户的.agents/skills/。最终须为.agents/skills/foodsci-research-assistant/SKILL.md，不要只复制SKILL.md，也不要多套ZIP外层目录。新技能若未出现，重新开启会话。

六入口套件则把外层目录内的六个技能文件夹一起复制到同一个技能目录；五个薄入口需要同版本总文件夹。单包已包含全部指引，不要求安装其余入口。选择一种方式，避免同名旧版本重复发现。

也可在Codex中发送：“请使用$skill-installer安装https://github.com/weihao-fang/foodsci-research-assistant/tree/main/skills/foodsci-research-assistant，保留完整资源，检查已有版本并确认安装0.8.0。”安装器实际目录以其提示为准；部分版本使用.codex/skills，安装后核对技能列表与实际读取路径。

豆包工作有官方技能机制，但本包ZIP导入规范与兼容性没有实机验证。只在账户提供明确上传技能入口且界面接受本包格式时试导入并实际调用。豆包普通聊天使用另附的自包含聊天文本，在当前界面支持格式时上传，否则粘贴正文并明确要求本次按该规则执行；这不等于持久安装或本地脚本能力。

可先请求：“使用FoodSci，将我给的三项结果整理成主张证据表，再写一个短结果段，保留数字、独立单位、阴性结果和必要限定。”没有数据时可做方案，不声称计算成功；没有联网时只处理已有资料，不声称文献已外部核验。

配套脚本需Python3.10+，只用标准库。先定位本Skill文件夹，再在自己的工作区保存新结果：

```text
python -B scripts/run_workflow.py --config assets/examples/workflow.json --output-dir ABSOLUTE_NEW_RESULTS_DIR
```

输出目录必须不存在，不向已安装Skill目录保存科研结果。合成RAW示例85%/独立n=2、消化15 mg/L/独立n=2只用于软件验证，非法DOI保持未核验与待复核。

按[新增方法入口](ADD_METHOD.md)扩展方法。版本副本不会自动同步，更新时保留自己新增的方法和旧包，完整替换后核对名称、版本和一个小任务。完整官方平台说明与升级文档位于公开仓库docs目录，不依赖创建者私人账户。
