---
name: skill-creator-publish
description: "快速创建和发布 AI Skill 到 GitHub。根据用户需求生成标准 Skill 目录结构（SKILL.md + skill.json + scripts + marketplace.json + README），并通过 gh CLI 发布到 GitHub 仓库。"
version: "1.0.0"
author: "WorkBuddy"
created: "2026-06-20"
updated: "2026-06-20"
alwaysApply: false
keywords:
  - 创建skill
  - 发布skill
  - skill发布github
  - 创建技能
  - skill creator
  - publish skill
  - skill template
  - skill模板
  - 发布技能
  - github skill
  - codebuddy skill
  - claude code skill
  - cursor skill
---

# Skill Creator & Publisher

## 功能说明

帮助用户快速创建标准 AI Skill 并发布到 GitHub，支持 CodeBuddy、Claude Code、Cursor、Cline、Windsurf 等主流智能体。

| 功能 | 说明 |
|------|------|
| 🏗️ **创建 Skill 骨架** | 根据需求自动生成 SKILL.md + skill.json + scripts/ + marketplace.json + README |
| 📤 **发布到 GitHub** | 用 gh CLI 创建仓库、提交代码、推送 |
| ✅ **发布后验证** | clone 验证文件完整性、检查硬编码路径、检查一致性 |
| 🔄 **跨平台兼容** | 扁平目录结构，所有智能体 clone 后直接可用 |

---

## 触发场景

| 用户可能会说 | 执行操作 |
|-------------|---------|
| "帮我创建一个 skill" / "创建一个技能" | 生成 skill 骨架 |
| "帮我发布 skill 到 GitHub" / "发布到仓库" | 创建 GitHub 仓库并推送 |
| "帮我创建并发布一个 skill" | 创建 + 发布一条龙 |

---

## 工作流

### 第一步：确认需求

向用户了解以下信息：
- **Skill 名称**：英文短名（如 `pdf-merger`、`data-cleaner`）
- **功能描述**：这个 skill 做什么？
- **关键词**：用户可能怎么说来触发？（列 5-10 个）
- **是否需要脚本**：需要 Python 脚本还是纯指令型 skill？
- **GitHub 用户名**：发布到哪个账号下？

### 第二步：生成 Skill 骨架

在工作目录下创建以下文件结构（**扁平结构，不要嵌套**）：

```
<skill-name>/
├── SKILL.md                          # Skill 说明（跨平台通用）
├── skill.json                        # 机器可读配置
├── scripts/                          # 脚本目录（可选）
│   └── main.py                       # 主脚本（可选）
├── .codebuddy-plugin/
│   └── marketplace.json              # CodeBuddy 插件市场清单
├── README.md                         # 完整教程（含各 IDE 安装说明）
├── LICENSE                           # MIT 许可证
└── .gitignore
```

#### SKILL.md 模板

```yaml
---
name: <skill-name>
description: "<功能描述>"
version: "1.0.0"
author: "<作者>"
created: "<日期>"
updated: "<日期>"
alwaysApply: false
keywords:
  - <关键词1>
  - <关键词2>
  - ...
---

# <Skill 标题>

## 功能说明
<功能描述表格>

## 触发场景
<用户可能说的话 → 执行操作表格>

## 工作流
<使用步骤>
```

#### skill.json 模板

```json
{
  "name": "<skill-name>",
  "display_name": "<显示名>",
  "description": "<描述>",
  "version": "1.0.0",
  "author": "<作者>",
  "license": "MIT",
  "repository": "https://github.com/<username>/<skill-name>",
  "category": "<分类>",
  "keywords": ["<关键词>"]
}
```

#### marketplace.json 模板

```json
{
  "name": "<skill-name>-marketplace",
  "description": "<描述>",
  "owner": { "name": "<作者>" },
  "plugins": [
    {
      "name": "<skill-name>",
      "description": "<描述>",
      "source": ".",
      "version": "1.0.0",
      "author": { "name": "<作者>" },
      "license": "MIT",
      "category": "<分类>",
      "keywords": ["<关键词>"]
    }
  ]
}
```

#### README.md 必须包含

1. 项目简介
2. 安装说明（含各 IDE 路径表）
3. "最简单方式"（告诉 AI 助手仓库地址）
4. 使用方法
5. 项目结构
6. 许可证

各 IDE 的 Skill 目录：

| IDE | Skill 目录 |
|-----|-----------|
| CodeBuddy | `.codebuddy/skills/<skill-name>/` |
| Claude Code | `.claude/skills/<skill-name>/` |
| Cursor | `.cursor/skills/<skill-name>/` |
| Windsurf | `.windsurf/skills/<skill-name>/` |
| Cline | `.cline/skills/<skill-name>/` |
| 通用 | `.agents/skills/<skill-name>/` |

### 第三步：发布到 GitHub

> ⚠️ **确认 GitHub 认证**：需要用户已通过 `gh auth login` 登录，或提供 Token。

```bash
cd <skill-name>
git init
git add -A
git commit -m "Initial release: <skill-name> v1.0.0"
gh repo create <skill-name> --public --description "<描述>" --source . --push
```

如果 gh repo create 失败（Token 权限不足），用 API 方式：
```bash
gh api -X POST /user/repos -f name="<skill-name>" -f description="<描述>" -f private=false
git remote add origin https://github.com/<username>/<skill-name>.git
git push -u origin master
```

### 第四步：发布后验证

```bash
# clone 验证
git clone https://github.com/<username>/<skill-name>.git /tmp/verify
# 检查文件完整性
find /tmp/verify -not -path '*/.git/*' -type f | sort
# 检查硬编码路径（不应有绝对路径）
grep -rn "绝对路径检测" /tmp/verify/SKILL.md
# 检查一致性
# 仓库名 = SKILL.md name = skill.json name
# 版本号一致
```

---

## 重要注意事项

1. **扁平目录结构**：SKILL.md 和 scripts/ 放在仓库根目录，不要嵌套到 plugins/ 下
2. **无硬编码路径**：所有路径用相对路径（如 `scripts/xxx.py`），不要用系统绝对路径
3. **双向兼容**：skill.json 和 marketplace.json 都要有，分别给通用智能体和 CodeBuddy 用
4. **keywords 必填**：SKILL.md frontmatter 必须有 keywords 列表，提高触发命中率
5. **alwaysApply: false**：按需触发，不常驻
6. **MIT 许可证**：默认使用 MIT
7. **README 含 IDE 路径表**：让用户一眼知道装到哪

---

## 已知限制

| 限制 | 说明 |
|------|------|
| GitHub 认证 | 需要用户提前 `gh auth login` 或提供 Token |
| 仓库创建权限 | Token 需要有 repo 权限（Classic Token，不是 Fine-grained） |
| 仅支持 GitHub | 暂不支持 Gitee 等其他平台 |
