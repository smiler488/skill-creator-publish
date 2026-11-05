# skill-creator-publish 安装说明（给 AI 助手）

> 用户只需对 AI 助手说：
> `请根据 https://raw.githubusercontent.com/smiler488/skill-creator-publish/main/install.md，安装 skill-creator-publish。`

你是收到安装请求的 AI 助手。按下面的步骤把 Agent Skill `skill-creator-publish` 装到本机，用默认值直接执行，不需要每一步都征求确认。只有一种情况要先问用户：目标目录已经存在、而且不是本仓库的 git 克隆（可能是用户自己改过的版本）。装完用一两句话告诉用户结果。

## 1. 确定安装目录

按当前运行的工具选择 skills 目录；如果目录还不存在就创建它：

| 工具 | 用户级 skills 目录 |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| WorkBuddy / CodeBuddy | `~/.workbuddy/skills/` |
| Cursor | `~/.cursor/skills/` |
| Gemini CLI | `~/.gemini/skills/` |

- 用户说只在当前项目里用时，改用项目内的目录，例如 `<项目>/.claude/skills/`。
- Windows 上 `~` 指 `C:\Users\<用户名>`。
- 目标目录记为 `TARGET = <skills 目录>/skill-creator-publish`。目录名必须是 `skill-creator-publish`，和 SKILL.md 里的 `name` 一致。

## 2. 下载

**有 git 时（推荐，方便以后更新）**

```bash
git clone --depth 1 https://github.com/smiler488/skill-creator-publish.git "$TARGET"
```

如果 `TARGET` 已经是本仓库的克隆，改为更新：

```bash
git -C "$TARGET" pull --ff-only
```

**没有 git，macOS / Linux：**

```bash
mkdir -p "$TARGET"
curl -fsSL https://codeload.github.com/smiler488/skill-creator-publish/tar.gz/refs/heads/main \
  | tar -xz --strip-components=1 -C "$TARGET"
```

**没有 git，Windows PowerShell：**

```powershell
$Target = "$HOME\.claude\skills\skill-creator-publish"   # 按第 1 步换成实际目录
$Zip = "$env:TEMP\skill-creator-publish.zip"
Invoke-WebRequest https://codeload.github.com/smiler488/skill-creator-publish/zip/refs/heads/main -OutFile $Zip
Expand-Archive $Zip -DestinationPath "$env:TEMP\skill-creator-publish-src" -Force
New-Item -ItemType Directory -Force $Target | Out-Null
Copy-Item "$env:TEMP\skill-creator-publish-src\skill-creator-publish-main\*" $Target -Recurse -Force
```

## 3. 安装依赖

需要 Python 3.8 及以上（生成骨架时用）。发布到 GitHub 还需要 GitHub CLI：检查 `gh --version`，没有就提示用户按 https://cli.github.com 安装，并在用户自己的终端里执行 `gh auth login`（不要替用户输入或保存 token）。

## 4. 检查

- `TARGET/SKILL.md` 存在，开头的 frontmatter 里有 `name: skill-creator-publish`。
- 这些文件也在：`scripts/create_skill.py`、`skill.json`。

缺文件就说明下载不完整，删掉 `TARGET` 后重新执行第 2 步。

## 5. 告诉用户

报告安装路径，并提醒用户：**新开一个会话（或重启工具）后 skill 才会生效**。

用法示例："帮我创建一个 skill，功能是把多个 PDF 合并成一个"、"把这个 skill 发布到我的 GitHub"。

## 网页版助手（没有本地文件系统）

跳过安装。网页版助手无法运行脚本和 gh。把 https://raw.githubusercontent.com/smiler488/skill-creator-publish/main/SKILL.md 读进对话，按其中的结构直接在对话里写出各个文件的内容，让用户自己保存和发布。

## 卸载

删除 `TARGET` 目录即可。

---

## English

Tell your assistant: `Install skill-creator-publish following https://raw.githubusercontent.com/smiler488/skill-creator-publish/main/install.md`

1. Pick the skills folder of the running tool (table above), e.g. `~/.claude/skills/`. Set `TARGET=<folder>/skill-creator-publish`. The folder name must equal the `name` in SKILL.md.
2. `git clone --depth 1 https://github.com/smiler488/skill-creator-publish.git "$TARGET"`. If it already exists as a clone, run `git -C "$TARGET" pull --ff-only` instead. Without git, use the curl or PowerShell commands above.

   Needs Python 3.8+. Publishing needs GitHub CLI (`gh`); if missing, point the user to https://cli.github.com and ask them to run `gh auth login` themselves.
3. Check that `TARGET/SKILL.md` has `name: skill-creator-publish` and that `scripts/create_skill.py`, `skill.json` exist.
4. Tell the user where it was installed and that a new session is needed. Example: "create a skill that merges PDFs and publish it to my GitHub".

Chat-only assistants: they cannot run the script or gh; read SKILL.md from the raw URL and write the files out in the chat for the user to save.

Uninstall: delete `TARGET`.
