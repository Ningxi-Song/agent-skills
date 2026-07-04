# Agent Skills

A collection of reusable agent skills for AI-powered coding assistants (opencode, Claude Code, Codex, etc.).

## Structure

```
skills/
├── economics/              Economics research & presentation
│   ├── econ-regression-table
│   ├── econ-summary-stats
│   └── beamer-presentation
├── engineering/            Software engineering practices
│   ├── diagnose
│   ├── tdd
│   ├── improve-codebase-architecture
│   └── zoom-out
├── planning/               Project management & planning
│   ├── to-issues
│   ├── to-prd
│   ├── triage
│   ├── grill-me
│   └── grill-with-docs
└── meta/                   Skill & agent management
    ├── caveman
    ├── find-skills
    ├── write-a-skill
    ├── setup-matt-pocock-skills
    └── stepwise-explanations
```

## Skills

### economics/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| **econ-regression-table** | Format regression tables to economics journal standards | Willie Song |
| **econ-summary-stats** | Produce summary statistics tables with sample transparency and balance tests | Willie Song |
| **beamer-presentation** | Design academic Beamer slides with conclusion-driven titles and one-point-per-slide | Willie Song |

### engineering/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| **diagnose** | Disciplined diagnosis loop for hard bugs and performance regressions | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **tdd** | Test-driven development with red-green-refactor loop | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **improve-codebase-architecture** | Find deepening opportunities in a codebase | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **zoom-out** | Zoom out for broader context / higher-level perspective | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |

### planning/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| **to-issues** | Break a plan/spec/PRD into independently-grabbable issues | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **to-prd** | Turn conversation context into a PRD | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **triage** | Triage issues through a state machine | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **grill-me** | Interview the user relentlessly about a plan or design | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **grill-with-docs** | Grilling session that challenges your plan against existing domain model | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |

### meta/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| **caveman** | Ultra-compressed communication mode. Cuts token usage ~75% | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **find-skills** | Helps users discover and install agent skills | Vercel Labs, imported from [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| **write-a-skill** | Create new agent skills with proper structure | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **setup-matt-pocock-skills** | Sets up Agent skills block in AGENTS.md/CLAUDE.md | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| **stepwise-explanations** | Break long answers into small readable chunks with pause points | Willie Song |

## Attribution

Creator/source labels are based on this repository's commit history and the local skill installer lock file used to import upstream skills. The economics skills and `stepwise-explanations` were authored in this repository by Willie Song. The Matt Pocock skills were imported and reorganized from `mattpocock/skills`. `find-skills` was imported from `vercel-labs/skills`.

## Usage

Clone into `~/.agents/skills/` and any compatible agent will auto-discover them.

```bash
git clone https://github.com/Ningxi-Song/agent-skills.git ~/.agents/skills
```
