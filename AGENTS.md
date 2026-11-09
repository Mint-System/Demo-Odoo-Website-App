# AGENTS.md

Note: @Clanker refers to the "ai agent" (you) who is working on this task.

## General agent guidance

This section outlines the universal rules and expectations for any LLM agent working within this repository.

**Safety and Quality First:** The highest priority is to produce secure, well-documented, and high-quality code. Do not introduce vulnerabilities, hardcoded secrets, or unreadable code.

**Propose a Plan:** For any new task, first provide a brief plan of action. This plan should clearly outline the intended changes and the rationale behind them.

**Maintain Context:** Before making any changes, an agent must read and understand the relevant files, including the project's main documentation and existing code structure.

**Be Sparse:** Only introduce new code if needed. Comment only what is worth commenting. When testing focus on the business use case. When writing documentations keep the explanation to a minimum.

**Never Commit:** Do not run `git commit`, `git push`, or any other version control write operation. Only the author is allowed to commit changes. You may stage files, run diffs, and prepare commit messages, but the actual commit and push must be done by the author.

## Project structure

```text
.
├── pricelist-importer.html   # CSV pricelist importer app (HTML/CSS/JS)
├── snippet.html              # legacy pricelist editor snippet
├── input/                    # sample vendor pricelists
├── output/                   # UI screenshots per step
├── scripts/
│   ├── publish_pricelist_importer.py  # publishes the importer page
│   └── publish.py                     # legacy publisher
├── tmp/                      # scratch scripts, never committed
└── task                      # task runner
```

## Common tasks

- `./task publish-pricelist-importer` – create or update the "Pricelist Importer" website page from `pricelist-importer.html`.
- `./task publish-app` – legacy publisher for `snippet.html` (pinned to the old Odoo 16 view id).
- Verify a published page with `curl -s http://localhost:8069/pricelist-importer`.

### Odoo view arch gotchas

Odoo validates view arch as **XML**, not HTML. Inside `<script>` blocks in a snippet:

- escape every `<` as `&lt;` and every `&&` as `&amp;&amp;`;
- self-close void tags (`<input ... />`);
- avoid HTML entities such as `&nbsp;` (use `&#160;`).

`scripts/publish_pricelist_importer.py` normalises void tags and boolean attributes, but `<` inside scripts must be escaped in the source file.

## Environment & tooling


### Temporary files

When creating temporary files and scripts, use the `./tmp` directory.

### Taskfile

This project uses the <https://taskfile.build/> standard.

The `./task` file is a bash script that provides all functions necessary to work with this project.

Always try to run a command with the `./task` file script.

### Session Info (Pi harness)

Inside the **Pi** harness, session details are exposed as environment variables:

- `PI_MODEL` – model ID, e.g. `deepseek-v4-1-flash-1017`
- `PI_PROVIDER` – provider, e.g. `mistral`
- `PI_REASONING_LEVEL` – e.g. `off`
- `PI_SESSION_ID` – e.g. `01a1a57c-a4b1-777f-ac7b-6b912be9400a`
- `PI_SESSION_FILE` – path to the session log, e.g. `/home/janikvonrotz/.pi/agent/sessions/--home-janikvonrotz-Odoo-Build--/2026-11-04T07-36-11-698Z_01a1a57c-a4b1-777f-ac7b-6b912be9400a.jsonl`
- `AI_AGENT` – e.g. `Pi`
- `PI_CODING_AGENT` – e.g. `true`

The session log at `$PI_SESSION_FILE` is a JSONL file. Each assistant message carries token usage in `message.usage` (`input` and `output`). When completing a prompt file, extract the model and cumulative token counts from these sources:

```bash
jq -s '[.[] | select(.type == "message" and .message.usage) | .message.usage]
  | {input: (map(.input) | add // 0), output: (map(.output) | add // 0)}' "$PI_SESSION_FILE"
```

This prints the totals, e.g. `{"input": 19876, "output": 1064}`.

### Encrypted secrets

All required env vars are stored in `secrets.env`. You can load the env vars like this:

```bash
eval "$(task show-dotenv secrets)"
```

Set `SOPS_AGE_KEY_FILE=/home/$USER/.config/sops/age/keys.txt` to decrypt.

### New tools

Do not automatically install new software packages. Always ask for permission.

## Coding conventions


### Prompt lifecycle

Tasks are tracked in `prompt.md` with a frontmatter state of `draft`, `wip`, `review`, `completed` or `cancelled`.

When the author tells you to stop (e.g. "stop" or "continue later"), preserve your work in progress:

- Add a `## WIP` section to `prompt.md` and capture the current progress there.
- Set the frontmatter state to `wip`.
- Store the prompt with `./task commit-prompt`.

When you resume work on a `wip` prompt, read the `## WIP` section and continue from there.

### General

**Avoid try catch:** Prefer default values or default params over try catch statements.
