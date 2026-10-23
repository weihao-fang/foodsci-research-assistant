# 下载 FoodSci 0.8.0

第一次使用Codex，选单Skill包即可；想单独选择任务入口再选六入口套件。豆包普通聊天选聊天版。所有包共享本版规则，按[许可](../LICENSE)用于非商业学习科研。

| 你的环境 | 下载 | 使用方法 |
| --- | --- | --- |
| Codex，一个总入口 | [标准单Skill ZIP](../downloads/foodsci-codex-0.8.0.zip?raw=true) | 解压后整体复制总文件夹，见[Codex教程](INSTALL_CODEX.md) |
| Codex，分别选择任务入口 | [六入口套件 ZIP](../downloads/foodsci-suite-0.8.0.zip?raw=true) | 六个文件夹一起安装，五个任务入口共享总资源 |
| 豆包普通聊天 | [聊天文本包 ZIP](../downloads/foodsci-doubao-chat-0.8.0.zip?raw=true)、[Markdown](../downloads/FoodSci-豆包聊天版.md?raw=true)、[TXT](../downloads/FoodSci-豆包聊天版.txt?raw=true) | 上传界面允许的格式，否则粘贴；见[豆包教程](INSTALL_DOUBAO.md) |
| 支持Agent Plugins格式的环境 | [插件包 ZIP](../downloads/foodsci-plugin-0.8.0.zip?raw=true) | 包含六个技能；不是可执行安装程序，也不包含marketplace注册 |

豆包工作官方有技能机制，本包原生导入兼容仍待实机核验。账户有明确技能导入入口且接受标准结构时可按界面尝试单Skill包；普通聊天附件上传不等于永久安装。

## 从GitHub下载

点击上表的实际文件链接。若打开的是文件预览页，点击页面的Download/下载按钮。也可以在仓库首页用Code→Download ZIP下载全部源码，安装时只取`skills`内的对应文件夹，避免多套一层仓库目录。不要仅复制SKILL.md而漏掉references、assets、scripts。

本仓库在未上传前，本地文件不是公开网址；不会要求访问创建者的私人插件账号。更新版下载仍以当前仓库及维护者实际Release为准，不使用虚构的最新版本链接。

## 完整性校验与重建

[SHA256SUMS](../downloads/SHA256SUMS)列出当前包及聊天文本的哈希。Windows可运行`Get-FileHash -Algorithm SHA256 文件路径`，macOS/Linux可运行`shasum -a 256 文件路径`后对照。哈希证明文件完整性，不证明科研结论正确。

维护者修改源文件后运行`python -B tools/build.py`重建ZIP与SHA256SUMS，勿直接改压缩包。升级与旧入口合并见[UPGRADING](UPGRADING.md)。
