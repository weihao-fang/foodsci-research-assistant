# 建立GitHub仓库与上传

本目录就是完整仓库内容，上传后README会成为首页。源码、下载包、非商业许可、使用教程、演示、反馈表与离线CI均已放在对应位置。不要把创建者工作目录或私人账号回执一起上传。

## 用GitHub CLI新建并上传

安装Git及[官方GitHub CLI](https://cli.github.com/)，在本项目根目录执行：

```text
gh auth login --web --git-protocol https --scopes workflow
python -B tools/publish_github.py
python -B tools/publish_github.py --execute
```

第一条在GitHub官方页面授权，不要把密码、PAT或登录凭证贴到聊天或Issues。第二条只是预览；第三条会验证文件、建立初始本地提交，并在已登录用户下创建公开的foodsci-research-assistant仓库且推送。该脚本只负责新仓库，遇到同名仓库或已有origin不会覆盖。出错后先检查远程实际状态，不盲目重试创建。

## 网页上传

也可在[GitHub新建页](https://github.com/new?name=foodsci-research-assistant&visibility=public)选择公开仓库。已有本项目README、LICENSE和gitignore时，不再让GitHub额外初始化同名文件。创建后在Add file→Upload files上传本目录内文件与文件夹；确认隐藏.github配置也进入仓库，避免把仓库外层再套一层。Git命令行推送更便于完整保留目录。

发布后检查README下载链接、Codex文档、豆包聊天文件，以及Actions实际结果。可在About添加food-science、biology、research、agent-skills、codex等与内容相符的主题；不要把未验证平台或准确率作为宣传标签。

## 发布正式版本

在Releases创建与VERSION一致的版本标签，例如v0.8.0，附CHANGELOG摘要和downloads内的ZIP及SHA256SUMS。未真正创建标签前，安装者可以下载已提交的文件或选择实际存在的分支，不应使用不存在的版本链接。

留住访客靠具体交付：保持下载入口显眼、演示可读、最小试用可完成；持续记录修复和真实限制，并回复可复现问题。Star/Watch可作为自愿的返回或更新方式，不设置下载门槛。
