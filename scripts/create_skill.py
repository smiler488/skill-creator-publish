#!/usr/bin/env python3
"""
Generate the skeleton of an Agent Skill repository.

    python scripts/create_skill.py --name pdf-merger \
        --description "Merge PDF files. Use when the user asks to combine PDFs." \
        --author "Your Name" --github-user yourname --keywords "pdf,merge"

Creates ./<name>/ with:

    SKILL.md                        frontmatter per the Agent Skills format
    install.md                      one-sentence install instructions for AI assistants
    README.md                       usage and install for humans
    skill.json                      machine-readable metadata
    .codebuddy-plugin/marketplace.json
    scripts/.gitkeep
    LICENSE (MIT), .gitignore

Existing files are never overwritten unless --force is given.

Author: Liangchao Deng (邓良超)
License: MIT
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

SKILL_DIRS = [
    ("Claude Code", "~/.claude/skills/"),
    ("Codex", "~/.codex/skills/"),
    ("WorkBuddy / CodeBuddy", "~/.workbuddy/skills/"),
    ("Cursor", "~/.cursor/skills/"),
    ("Gemini CLI", "~/.gemini/skills/"),
]

MIT = """MIT License

Copyright (c) {year} {author}

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


def yaml_str(s):
    """Quote a string for YAML. JSON strings are valid YAML scalars."""
    return json.dumps(s, ensure_ascii=False)


def git_user():
    try:
        out = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, timeout=5)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def skill_md(name, description, author, keywords, today):
    kw = "\n".join(f"    - {yaml_str(k)}" for k in keywords)
    return f"""---
name: {name}
description: {yaml_str(description)}
license: MIT
metadata:
  author: {yaml_str(author)}
  version: "1.0.0"
  created: "{today}"
  keywords:
{kw}
---

# {name}

<!-- One or two sentences: what problem this skill solves. -->

## When to use

<!-- What the user says or does when this skill should load. Be concrete. -->

## Workflow

1. ...
2. ...

## Limits

<!-- What not to do, what needs the user's confirmation, how to recover from errors. -->

## Files

- `scripts/` - scripts called from the workflow above (say when and how)
"""


def install_md(name, user):
    rows = "\n".join(f"| {tool} | `{path}` |" for tool, path in SKILL_DIRS)
    raw = f"https://raw.githubusercontent.com/{user}/{name}/main/install.md"
    return f"""# {name} install instructions (for AI assistants)

> Users only need to say: `Install {name} following {raw}`
> 用户只需说：`请根据 {raw}，安装 {name}。`

You are an AI assistant asked to install the Agent Skill `{name}`. Use the defaults below without asking at every step. Ask the user only if the target folder already exists and is not a git clone of this repository. Report the result in one or two sentences.

## 1. Target folder

| Tool | User-level skills folder |
| --- | --- |
{rows}

For a single project use `<project>/.claude/skills/` (or the project folder of the tool in use). Set `TARGET=<skills folder>/{name}`; the folder name must equal `name` in SKILL.md.

## 2. Download

```bash
git clone --depth 1 https://github.com/{user}/{name}.git "$TARGET"
# already installed: git -C "$TARGET" pull --ff-only
```

Without git (macOS / Linux):

```bash
mkdir -p "$TARGET"
curl -fsSL https://codeload.github.com/{user}/{name}/tar.gz/refs/heads/main | tar -xz --strip-components=1 -C "$TARGET"
```

Without git (Windows PowerShell): download `https://codeload.github.com/{user}/{name}/zip/refs/heads/main`, extract it, and copy the contents of `{name}-main` into `$TARGET`.

## 3. Check

`TARGET/SKILL.md` exists and its frontmatter has `name: {name}`.

## 4. Tell the user

Give the install path and say that the skill is available in a new session.

Chat-only assistants: read https://raw.githubusercontent.com/{user}/{name}/main/SKILL.md into the conversation and follow it.

Uninstall: delete `TARGET`.
"""


def readme_md(name, description, user):
    rows = "\n".join(f"| {tool} | `{path}{name}/` |" for tool, path in SKILL_DIRS)
    return f"""# {name}

{description}

## Install

Tell your AI assistant:

```text
Install {name} following https://raw.githubusercontent.com/{user}/{name}/main/install.md
```

Or clone it into the skills folder of your tool:

| Tool | Folder |
| --- | --- |
{rows}

```bash
git clone --depth 1 https://github.com/{user}/{name}.git ~/.claude/skills/{name}
```

Start a new session afterwards.

## Use

<!-- Example requests and what the skill does with them. -->

## Files

| Path | Purpose |
| --- | --- |
| `SKILL.md` | instructions the assistant loads |
| `install.md` | install instructions for AI assistants |
| `scripts/` | helper scripts |
| `skill.json`, `.codebuddy-plugin/marketplace.json` | metadata for skill marketplaces |

## License

MIT, see [LICENSE](LICENSE).
"""


def write(path, text, force, created):
    if path.exists() and not force:
        print(f"  keep existing {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    created.append(path)


def create_skill(name, description, author, keywords, category, user, out_dir=".", force=False):
    if not NAME_RE.match(name) or len(name) > 64:
        raise SystemExit(f"Invalid name {name!r}: use lowercase letters, digits and single hyphens, max 64 characters.")
    if len(description) > 1024:
        raise SystemExit(f"Description is {len(description)} characters; the limit is 1024.")

    today = date.today().isoformat()
    root = Path(out_dir) / name
    created = []
    meta = {
        "name": name,
        "display_name": name,
        "description": description,
        "version": "1.0.0",
        "author": author,
        "license": "MIT",
        "repository": f"https://github.com/{user}/{name}",
        "category": category,
        "keywords": keywords,
    }
    marketplace = {
        "name": f"{name}-marketplace",
        "description": description,
        "owner": {"name": author},
        "plugins": [{
            "name": name, "description": description, "source": ".", "version": "1.0.0",
            "author": {"name": author}, "license": "MIT", "category": category, "keywords": keywords,
        }],
    }

    write(root / "SKILL.md", skill_md(name, description, author, keywords, today), force, created)
    write(root / "install.md", install_md(name, user), force, created)
    write(root / "README.md", readme_md(name, description, user), force, created)
    write(root / "skill.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n", force, created)
    write(root / ".codebuddy-plugin" / "marketplace.json",
          json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n", force, created)
    write(root / "scripts" / ".gitkeep", "", force, created)
    write(root / "LICENSE", MIT.format(year=today[:4], author=author), force, created)
    write(root / ".gitignore", "__pycache__/\n*.pyc\n.DS_Store\n*.log\n.env\n", force, created)

    print(f"Skeleton in {root}/ ({len(created)} files written)")
    for p in created:
        print(f"  {p.relative_to(root)}")
    print("\nNext:")
    print("  1. fill in the workflow in SKILL.md and the usage section in README.md")
    print(f"  2. cd {root} && git init -b main && git add -A && git commit -m 'Initial release'")
    print(f"  3. gh repo create {user}/{name} --public --source . --push")
    return root


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate an Agent Skill repository skeleton.")
    ap.add_argument("--name", "-n", required=True, help="skill name, lowercase-with-hyphens")
    ap.add_argument("--description", "-d", required=True,
                    help="when the skill should be used (max 1024 characters)")
    ap.add_argument("--author", "-a", default=None, help="author name (default: git user.name)")
    ap.add_argument("--github-user", "-u", default="<username>", help="GitHub account for URLs")
    ap.add_argument("--keywords", "-k", default="", help="comma-separated keywords")
    ap.add_argument("--category", "-c", default="productivity", help="marketplace category")
    ap.add_argument("--out", "-o", default=".", help="parent folder (default: current folder)")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    args = ap.parse_args(argv)

    author = args.author or git_user() or "<author>"
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()] or [args.name]
    create_skill(args.name, args.description, author, keywords, args.category,
                 args.github_user, args.out, args.force)


if __name__ == "__main__":
    sys.exit(main())
