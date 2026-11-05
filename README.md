# skill-creator-publish

English | [中文](README.zh-CN.md)

An Agent Skill that turns "I want a skill that does X" into a GitHub repository anyone can install with one sentence. It asks for the missing details, generates the skeleton (SKILL.md, install.md, README, skill.json, a CodeBuddy marketplace file, LICENSE), creates the repository with GitHub CLI, and checks the published result.

## Install

Tell your assistant:

```text
Install skill-creator-publish following https://raw.githubusercontent.com/smiler488/skill-creator-publish/main/install.md
```

Or by hand (Claude Code shown; see `install.md` for other tools):

```bash
git clone --depth 1 https://github.com/smiler488/skill-creator-publish.git ~/.claude/skills/skill-creator-publish
```

Publishing needs [GitHub CLI](https://cli.github.com) and `gh auth login`.

CodeBuddy marketplace:

```text
/plugin marketplace add smiler488/skill-creator-publish
/plugin install skill-creator-publish@skill-creator-publish-marketplace
```

## Use

Ask in plain words, e.g. "create a skill that merges PDF files and publish it to my GitHub". Nothing is pushed before you confirm.

The generator also works on its own:

```bash
python scripts/create_skill.py --name pdf-merger \
  --description "Merge PDF files. Use when the user asks to combine PDFs." \
  --author "Your Name" --github-user yourname --keywords "pdf,merge"
```

It checks the name (lowercase, digits, hyphens) and the 1024-character description limit, and never overwrites existing files unless you pass `--force`.

## Generated layout

```
pdf-merger/
├── SKILL.md                        name / description / license; author, version, keywords under metadata
├── install.md                      install instructions written for AI assistants
├── README.md
├── skill.json
├── .codebuddy-plugin/marketplace.json
├── scripts/
├── LICENSE                         MIT
└── .gitignore
```

## Changes in this revision

- Generated SKILL.md files put `version`, `author`, `keywords` and `alwaysApply` at the top level of the frontmatter, which the Agent Skills format does not define. They are now under `metadata`.
- Descriptions with quotes broke the YAML. Values are now quoted safely.
- Every new skill gets an `install.md`, so it can be installed with one sentence.
- Name and description are validated, and existing files are kept unless `--force` is given.
- The default author is your git user name instead of a tool name. Instructions push to `main`, which the raw install links rely on.
- The post-publish path check was a placeholder that matched nothing. It now looks for `/Users/`, `/home/…` and `C:\` paths.

## License

MIT, see [LICENSE](LICENSE). Liangchao Deng (邓良超).
