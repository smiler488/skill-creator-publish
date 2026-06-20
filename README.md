# Skill Creator & Publisher

> 快速创建标准 AI Skill 并发布到 GitHub。根据需求自动生成完整目录结构，一键推送仓库。
>
> 支持 CodeBuddy、Claude Code、Cursor、Cline、Windsurf 等主流 AI 编程智能体。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🏗️ **创建 Skill 骨架** | 自动生成 SKILL.md + skill.json + scripts/ + marketplace.json + README + LICENSE |
| 📤 **发布到 GitHub** | 用 gh CLI 创建仓库、提交代码、推送 |
| ✅ **发布后验证** | clone 验证文件完整性、检查硬编码路径、检查一致性 |
| 🔄 **跨平台兼容** | 扁平目录结构，所有智能体 clone 后直接可用 |
| 📋 **标准模板** | 内含 SKILL.md/skill.json/marketplace.json/README 标准模板 |

## 📦 安装

### 通用前置依赖

```bash
# 需要 GitHub CLI
gh auth login
```

### 最简单的方式：告诉你的 AI 助手

> 帮我安装 Skill 创建与发布工具，仓库地址：https://github.com/smiler488/skill-creator-publish

### 手动安装

将本仓库克隆到你项目下的 Skill 目录，不同 IDE 对应的路径：

| IDE | Skill 目录 |
|-----|-----------|
| CodeBuddy | `.codebuddy/skills/skill-creator-publish/` |
| Claude Code | `.claude/skills/skill-creator-publish/` |
| Cursor | `.cursor/skills/skill-creator-publish/` |
| Windsurf | `.windsurf/skills/skill-creator-publish/` |
| Cline | `.cline/skills/skill-creator-publish/` |
| 通用 | `.agents/skills/skill-creator-publish/` |

```bash
git clone https://github.com/smiler488/skill-creator-publish.git .cursor/skills/skill-creator-publish
```

只要目录下有 `SKILL.md`，Agent 下次启动就会自动加载这个 Skill。

### CodeBuddy 插件市场安装

```bash
/plugin marketplace add smiler488/skill-creator-publish
/plugin install skill-creator-publish@skill-creator-publish-marketplace
```

### 独立使用

```bash
# 生成 skill 骨架
python scripts/create_skill.py --name my-skill --description "功能描述" --author "作者" --keywords "关键词1,关键词2"
```

## 🚀 使用方法

### 方式一：通过 AI 助手（推荐）

对 AI 助手说："帮我创建一个 skill，功能是 XXX" 或 "帮我创建并发布一个 skill 到 GitHub"。

AI 助手会：
1. 确认 skill 名称、描述、关键词
2. 生成完整目录结构
3. 创建 GitHub 仓库并推送
4. 验证发布结果

### 方式二：命令行独立使用

```bash
# Step 1: 生成 skill 骨架
python scripts/create_skill.py \
  --name my-skill \
  --description "我的技能描述" \
  --author "我的名字" \
  --keywords "关键词1,关键词2,关键词3"

# Step 2: 编辑生成的 SKILL.md 补充工作流
# Step 3: 在 scripts/ 下添加脚本
# Step 4: 替换 README.md 中的 <username>

# Step 5: 发布到 GitHub
cd my-skill
git init
git add -A
git commit -m "Initial release: my-skill v1.0.0"
gh repo create my-skill --public --description "我的技能描述" --source . --push
```

## 📁 项目结构

```
skill-creator-publish/
├── SKILL.md                          # Skill 说明文件（跨平台通用）
├── skill.json                        # 机器可读配置
├── scripts/
│   └── create_skill.py               # Skill 骨架生成器
├── .codebuddy-plugin/
│   └── marketplace.json              # CodeBuddy 插件市场清单
├── README.md
├── LICENSE
└── .gitignore
```

## 📋 生成的 Skill 标准结构

使用本工具创建的 skill 会包含以下文件：

| 文件 | 作用 | 说明 |
|------|------|------|
| `SKILL.md` | 跨平台 Skill 说明 | 所有智能体通过 YAML frontmatter 识别 |
| `skill.json` | 机器可读配置 | 名称、版本、关键词 |
| `scripts/` | 脚本目录 | Python 脚本（可选） |
| `.codebuddy-plugin/marketplace.json` | CodeBuddy 插件市场 | 支持 `/plugin install` |
| `README.md` | 项目说明 | 含各 IDE 安装路径表 |
| `LICENSE` | MIT 许可证 | 开源协议 |
| `.gitignore` | Git 忽略 | 排除缓存文件 |

## ⚠️ 注意事项

| 事项 | 说明 |
|------|------|
| GitHub 认证 | 需要提前 `gh auth login` 或提供 Token |
| Token 权限 | 需要 Classic Token（有 repo 权限），Fine-grained 可能无法创建仓库 |
| 扁平目录 | SKILL.md 放仓库根目录，不要嵌套到 plugins/ 下 |
| 无硬编码路径 | 所有路径用相对路径（`scripts/xxx.py`） |
| keywords 必填 | SKILL.md frontmatter 必须有 keywords 列表 |

## 📄 许可证

MIT License — 详见 [LICENSE](LICENSE)
