#!/usr/bin/env python3
"""
Skill 骨架生成器
用法: python create_skill.py --name my-skill --description "功能描述" --author "作者"

在工作目录下生成标准 Skill 目录结构：
  my-skill/
  ├── SKILL.md
  ├── skill.json
  ├── scripts/
  ├── .codebuddy-plugin/marketplace.json
  ├── README.md
  ├── LICENSE
  └── .gitignore
"""

import argparse
import json
import os
from datetime import date


def create_skill(name, description, author, keywords, category="效率工具"):
    """生成 skill 骨架"""
    today = date.today().isoformat()
    skill_dir = os.path.join(".", name)
    os.makedirs(os.path.join(skill_dir, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(skill_dir, ".codebuddy-plugin"), exist_ok=True)

    # scripts/ 占位文件（确保 git 能跟踪空目录）
    with open(os.path.join(skill_dir, "scripts", ".gitkeep"), "w") as f:
        f.write("# 此目录用于存放脚本文件\n")

    # SKILL.md
    kw_lines = "\n".join(f"  - {kw}" for kw in keywords)
    skill_md = f"""---
name: {name}
description: "{description}"
version: "1.0.0"
author: "{author}"
created: "{today}"
updated: "{today}"
alwaysApply: false
keywords:
{kw_lines}
---

# {name}

## 功能说明

{description}

## 触发场景

| 用户可能会说 | 执行操作 |
|-------------|---------|
| "触发关键词1" | 执行操作1 |

## 工作流

### 第一步：确认需求

### 第二步：执行操作

### 第三步：返回结果

## 已知限制

| 限制 | 说明 |
|------|------|
| （待补充） | |
"""
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)

    # skill.json
    skill_json = {
        "name": name,
        "display_name": name,
        "description": description,
        "version": "1.0.0",
        "author": author,
        "license": "MIT",
        "repository": f"https://github.com/<username>/{name}",
        "category": category,
        "keywords": keywords,
    }
    with open(os.path.join(skill_dir, "skill.json"), "w", encoding="utf-8") as f:
        json.dump(skill_json, f, ensure_ascii=False, indent=2)

    # marketplace.json
    marketplace = {
        "name": f"{name}-marketplace",
        "description": f"{description}",
        "owner": {"name": author},
        "plugins": [{
            "name": name,
            "description": description,
            "source": ".",
            "version": "1.0.0",
            "author": {"name": author},
            "license": "MIT",
            "category": category,
            "keywords": keywords,
        }],
    }
    with open(os.path.join(skill_dir, ".codebuddy-plugin", "marketplace.json"), "w", encoding="utf-8") as f:
        json.dump(marketplace, f, ensure_ascii=False, indent=2)

    # README.md
    readme = f"""# {name}

> {description}
>
> 支持 CodeBuddy、Claude Code、Cursor、Cline、Windsurf 等主流 AI 编程智能体。

## 📦 安装

### 通用前置依赖

```bash
# 如果有 Python 依赖，在这里列出
# pip install xxx
```

### 最简单的方式：告诉你的 AI 助手

> 帮我安装 {name}，仓库地址：https://github.com/<username>/{name}

### 手动安装

将本仓库克隆到你项目下的 Skill 目录，不同 IDE 对应的路径：

| IDE | Skill 目录 |
|-----|-----------|
| CodeBuddy | `.codebuddy/skills/{name}/` |
| Claude Code | `.claude/skills/{name}/` |
| Cursor | `.cursor/skills/{name}/` |
| Windsurf | `.windsurf/skills/{name}/` |
| Cline | `.cline/skills/{name}/` |
| 通用 | `.agents/skills/{name}/` |

```bash
git clone https://github.com/<username>/{name}.git .cursor/skills/{name}
```

只要目录下有 `SKILL.md`，Agent 下次启动就会自动加载这个 Skill。

## 🚀 使用方法

（待补充具体使用说明）

## 📁 项目结构

```
{name}/
├── SKILL.md              # Skill 说明文件（跨平台通用）
├── skill.json            # 机器可读配置
├── scripts/              # 脚本目录
├── .codebuddy-plugin/
│   └── marketplace.json  # CodeBuddy 插件市场清单
├── README.md
├── LICENSE
└── .gitignore
```

## 📄 许可证

MIT License — 详见 [LICENSE](LICENSE)
"""
    with open(os.path.join(skill_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    # LICENSE
    license_text = f"""MIT License

Copyright (c) {today[:4]} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    with open(os.path.join(skill_dir, "LICENSE"), "w", encoding="utf-8") as f:
        f.write(license_text)

    # .gitignore
    gitignore = """__pycache__/
*.pyc
*.pyo
.DS_Store
*.tmp
*.log
.env
"""
    with open(os.path.join(skill_dir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore)

    print(f"✅ Skill 骨架已生成: {skill_dir}/")
    print(f"   文件列表:")
    for root, dirs, files in os.walk(skill_dir):
        for fname in sorted(files):
            rel = os.path.relpath(os.path.join(root, fname), skill_dir)
            print(f"   {rel}")
    print(f"\n下一步:")
    print(f"  1. 编辑 SKILL.md 补充具体工作流")
    print(f"  2. 在 scripts/ 下添加脚本")
    print(f"  3. 替换 README.md 中的 <username>")
    print(f"  4. cd {skill_dir} && git init && git add -A && git commit -m 'Initial release'")
    print(f"  5. gh repo create {name} --public --source . --push")


def main():
    parser = argparse.ArgumentParser(description="Skill 骨架生成器")
    parser.add_argument("--name", "-n", required=True, help="Skill 名称（英文短名）")
    parser.add_argument("--description", "-d", required=True, help="功能描述")
    parser.add_argument("--author", "-a", default="WorkBuddy", help="作者")
    parser.add_argument("--keywords", "-k", default="", help="关键词，逗号分隔")
    parser.add_argument("--category", "-c", default="效率工具", help="分类")
    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()] if args.keywords else [args.name]
    create_skill(args.name, args.description, args.author, keywords, args.category)


if __name__ == "__main__":
    main()
