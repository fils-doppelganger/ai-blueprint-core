# FAIR Assessor — a Hermes Skill

This folder contains a small **Hermes Agent skill** that evaluates how well a web
resource (a dataset page, data portal, or repository) aligns with a set of
**FAIR principles** (Findable, Accessible, Interoperable, Reusable). You point it
at a starting URL and a FAIR "blueprint" document, and it produces a structured
alignment report.

If you've never used Hermes before, this README explains what's here, what Hermes
is, how to install it, and how to run this skill yourself.

## What's in this folder

| File | What it is |
|------|------------|
| [`SKILL.md`](./SKILL.md) | The skill itself — instructions Hermes follows when assessing a resource. |
| [`FAIR-assessment-ImmPort-SDY2968-2026-06-09.md`](./FAIR-assessment-ImmPort-SDY2968-2026-06-09.md) | An **example output**: a real assessment of the ImmPort study SDY2968 against the NIAID Blueprint v2. |

## What is Hermes?

[Hermes Agent](https://hermes-agent.nousresearch.com) (by Nous Research) is a
command-line AI agent. Like other agentic coding/research tools, it can read
files, browse the web, and run multi-step tasks on your behalf.

A **skill** is a reusable, packaged set of instructions (a `SKILL.md` file plus
optional resources) that teaches the agent how to do one specific job well. When a
skill is installed, Hermes loads it automatically and you invoke it as a slash
command (e.g. `/fair-assessment`). This is the same "Agent Skills" concept used
across modern agent tooling.

- Skills overview & hub: <https://hermes-agent.nousresearch.com/docs/skills>
- Writing your own skill: <https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills>

## How this skill works

The full procedure is in [`SKILL.md`](./SKILL.md), but in short the agent:

1. **Takes two inputs** — a starting URL (the resource to assess) and a FAIR
   blueprint (a URL or local file). In the example, the blueprint is the
   [NIAID Blueprint v2](https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md).
2. **Crawls the page and its key first-level links** using
   [Firecrawl](https://www.firecrawl.dev/), which renders JavaScript-heavy data
   portals into clean Markdown that the agent can actually read.
3. **Compares the content** against each FAIR principle, gathering direct quotes
   as evidence.
4. **Writes a report** with an overall alignment score, a per-principle
   breakdown, identified gaps, and prioritized recommendations.

See the [example report](./FAIR-assessment-ImmPort-SDY2968-2026-06-09.md) for what
the finished output looks like.

> **Note on Firecrawl:** This skill declares `requires_toolsets: [web]` and relies
> on Firecrawl for clean page extraction. You'll need a `FIRECRAWL_API_KEY` (or a
> self-hosted `FIRECRAWL_API_URL`) configured in Hermes. See the
> [Hermes web/tools configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration).

## Installing Hermes

**Linux / macOS / WSL2 / Termux:**

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

**Windows (PowerShell):**

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Then reload your shell (`source ~/.zshrc` or `source ~/.bashrc`).

Full getting-started guide:
<https://hermes-agent.nousresearch.com/docs/getting-started/quickstart>

## Running this skill

Because this skill lives locally in this repo, the simplest path is to start
Hermes from this directory so it can pick up the local `SKILL.md`:

```bash
cd skills/hermes/fair-assessor
hermes
```

Then invoke it as a slash command and give it your inputs, for example:

```
/fair-assessment Assess https://www.immport.org/shared/study/SDY2968/summary
against the NIAID Blueprint at
https://raw.githubusercontent.com/go-fair-us/ai-blueprint-core/refs/heads/master/docs/NIAID_Blueprint_v2_26Sep2025_forExternal.md
```

Hermes will crawl, evaluate, and write a report like the example included here.

You can also browse and install skills from the Hermes Skills Hub:

```bash
hermes skills browse
hermes skills search fair
hermes skills install <source/path>
```

## Learn more

- Hermes Agent home: <https://hermes-agent.nousresearch.com>
- Getting started: <https://hermes-agent.nousresearch.com/docs/getting-started/quickstart>
- Skills hub & docs: <https://hermes-agent.nousresearch.com/docs/skills>
- Creating skills: <https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills>
- Firecrawl: <https://www.firecrawl.dev/>
- NIAID Blueprint (this project): see the repository root `CLAUDE.md` and `docs/`.
