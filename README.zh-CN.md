# skill-creator-publish

[English](README.md) | 中文

一个 Agent Skill：把"我想要一个能做 X 的 skill"变成一个任何人一句话就能安装的 GitHub 仓库。它会：

- 先问清缺少的信息；
- 生成骨架：SKILL.md、install.md、README、skill.json、CodeBuddy 插件市场文件和 LICENSE；
- 用 GitHub CLI 创建仓库；
- 检查发布结果。

我自己的 skill（pptx-zh2en、research-integrity-review 等）都是用它发布的，所以每个仓库的结构一致，也都带有能用的 `install.md`。

## 安装

对 AI 助手说：

```text
请根据 https://raw.githubusercontent.com/smiler488/skill-creator-publish/main/install.md，安装 skill-creator-publish。
```

也可以手动安装（这里以 Claude Code 为例，其他工具的目录见 `install.md`）：

```bash
git clone --depth 1 https://github.com/smiler488/skill-creator-publish.git ~/.claude/skills/skill-creator-publish
```

发布功能需要先安装 [GitHub CLI](https://cli.github.com)，并执行 `gh auth login` 登录。

通过 CodeBuddy 插件市场安装：

```text
/plugin marketplace add smiler488/skill-creator-publish
/plugin install skill-creator-publish@skill-creator-publish-marketplace
```

## 使用

直接用自然语言说，比如"帮我创建一个合并 PDF 的 skill，并发布到我的 GitHub"。在你确认之前，不会推送任何东西。

生成器也可以单独使用：

```bash
python scripts/create_skill.py --name pdf-merger \
  --description "合并 PDF 文件。当用户要求把多个 PDF 合成一个时使用。" \
  --author "你的名字" --github-user yourname --keywords "pdf,合并"
```

脚本会检查名称（只能用小写字母、数字和连字符）以及描述是否超过 1024 个字符；已有的文件不会被覆盖，除非加上 `--force`。

## 生成的结构

```
pdf-merger/
├── SKILL.md                        顶层只有 name / description / license；作者、版本、关键词放在 metadata 下
├── install.md                      写给智能体看的安装说明
├── README.md
├── skill.json
├── .codebuddy-plugin/marketplace.json
├── scripts/
├── LICENSE                         MIT
└── .gitignore
```

## 本次修订

- 原来生成的 SKILL.md 把 `version`、`author`、`keywords`、`alwaysApply` 放在 frontmatter 顶层，这些字段不在 Agent Skills 规范里。现在统一放到 `metadata` 下。
- 描述里带引号时会把 YAML 弄坏，现在会做安全转义。
- 每个新生成的 skill 都会带 `install.md`，可以一句话安装。
- 增加名称和描述的校验；已有文件默认保留，加 `--force` 才覆盖。
- 默认作者从工具名改为你的 git 用户名；发布说明改为推送到 `main` 分支，因为 raw 安装链接依赖这个分支名。
- 发布后检查绝对路径的命令原来是个占位符，什么都匹配不到；现在会查找 `/Users/`、`/home/…` 和 `C:\` 形式的路径。

## 许可证

MIT，见 [LICENSE](LICENSE)。邓良超（Liangchao Deng）。
