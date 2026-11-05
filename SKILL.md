---
name: skill-creator-publish
description: 生成标准 Agent Skill 仓库骨架并发布到 GitHub。当用户说"帮我创建一个 skill""把这个做成技能""把 skill 发布到 GitHub"时使用。生成 SKILL.md、install.md（一句话安装）、README、skill.json、marketplace.json，用 gh CLI 建仓推送并验证。Create an Agent Skill repository skeleton and publish it to GitHub.
license: MIT
metadata:
  author: Liangchao Deng (smiler488)
  version: "1.1.0"
  keywords: [创建skill, 发布skill, 创建技能, skill creator, publish skill, skill template]
---

# Skill 创建与发布

把用户的需求变成一个可以直接安装的 Agent Skill 仓库，并发布到 GitHub。发布后，用户只要对任何智能体说一句"请根据 …/install.md，安装 <名称>"就能装上。

## 何时使用

| 用户说 | 做什么 |
| --- | --- |
| "帮我创建一个 skill / 技能，功能是…" | 第 1–3 步 |
| "把这个 skill 发布到 GitHub" | 第 4–5 步 |
| "创建并发布一个 skill" | 全部步骤 |

## 工作流程

### 1. 问清需求

需要以下信息，缺哪项问哪项：

- **名称**：小写字母、数字、连字符，例如 `pdf-merger`，同时作为仓库名和目录名；
- **触发场景**：用户会怎么说、在什么情况下用。这会写进 `description`，是智能体判断要不要加载的唯一依据，不超过 1024 个字符；
- **步骤和边界**：具体怎么做、哪些事不能做或要先确认；
- **是否需要脚本**：纯指令型还是需要 `scripts/`；
- **GitHub 账号**和作者名。

### 2. 生成骨架

```bash
python <本 skill 目录>/scripts/create_skill.py \
  --name <名称> --description "<触发场景>" \
  --author "<作者>" --github-user <GitHub 账号> --keywords "<关键词1>,<关键词2>"
```

在当前目录生成 `<名称>/`：`SKILL.md`、`install.md`、`README.md`、`skill.json`、`.codebuddy-plugin/marketplace.json`、`scripts/`、`LICENSE`、`.gitignore`。已有文件不会被覆盖（加 `--force` 才会）。名称不合规或描述太长时，脚本会直接报错。

### 3. 补全内容

- 按第 1 步收集的信息填写 `SKILL.md` 的"When to use / Workflow / Limits"，删掉注释。
- 需要脚本就放进 `scripts/`，并在 SKILL.md 里写清什么时候、怎么调用。
- README 写清用法示例。
- 本地自测：复制到 `~/.claude/skills/<名称>/`（或用户所用工具的 skills 目录），新开会话，用一句相关请求和一句无关请求各测一次。

### 4. 发布到 GitHub

先确认用户已执行过 `gh auth login`。推送前全文搜索密钥（API Key、Token、`.env`），发现就停下来告诉用户。

```bash
cd <名称>
git init -b main
git add -A
git commit -m "Initial release: <名称> v1.0.0"
gh repo create <GitHub 账号>/<名称> --public --description "<一句话简介>" --source . --push
git tag v1.0.0 && git push --tags
```

默认分支必须是 `main`，否则 `install.md` 里的链接会失效。

### 5. 验证

```bash
git clone --depth 1 https://github.com/<GitHub 账号>/<名称>.git /tmp/verify-<名称>
python <本 skill 目录>/scripts/create_skill.py --help >/dev/null   # 脚本仍可用
grep -rnE '/Users/|/home/[a-z]|[A-Z]:\\' /tmp/verify-<名称> --exclude-dir=.git   # 不应有本机绝对路径
```

再检查三处名称一致：仓库名 = SKILL.md 的 `name` = skill.json 的 `name`；并在浏览器里打开 `https://raw.githubusercontent.com/<GitHub 账号>/<名称>/main/install.md`，确认能访问。最后把一句话安装指令发给用户。

## 边界与注意

- 未经用户确认，不创建公开仓库、不推送。
- 只把元数据（作者、版本、关键词）写在 `metadata` 下；frontmatter 顶层只用 `name`、`description`、`license` 等标准字段。
- token 需要 repo 权限。`gh repo create` 失败时，告诉用户原因，不要自己换其他凭据重试。
- 目前只支持 GitHub。

## 文件

| 文件 | 用途 |
| --- | --- |
| `scripts/create_skill.py` | 骨架生成器 |
| `install.md` | 本 skill 自己的安装说明 |
