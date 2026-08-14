# Agent Skills

A collection of reusable agent skills for AI-powered coding assistants (opencode, Claude Code, Codex, etc.).

## Structure

```
beamer-skills/          Beamer & LaTeX/TikZ skills
├── beamer-format
├── verify-tikz-layout
├── beamer-live-draft
├── tests/verify-tikz-layout
└── docs/superpowers
economics/              Economics research
├── econ-regression-table
├── econ-summary-stats
└── preliminary-data-audit
engineering/            Software engineering practices
├── diagnose
├── tdd
├── improve-codebase-architecture
├── project-hygiene
└── zoom-out
planning/               Project management & planning
├── to-issues
├── to-prd
├── triage
├── grill-me
└── grill-with-docs
meta/                   Skill & agent management
├── caveman
├── find-skills
├── write-a-skill
├── setup-matt-pocock-skills
└── stepwise-explanations
```

## Skills

### beamer-skills/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| [**beamer-format**](beamer-skills/beamer-format/SKILL.md) | Design academic Beamer slides with a clean, minimal aesthetic | Willie Song |
| [**verify-tikz-layout**](beamer-skills/verify-tikz-layout/SKILL.md) | Compile, render, and visually verify TikZ layouts (including Beamer slides) | Willie Song |
| [**beamer-live-draft**](beamer-skills/beamer-live-draft/SKILL.md) | Interactive Beamer-style HTML draft editor (right-panel) + JSON→tex/PDF transpiler | Willie Song |

### economics/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| [**econ-regression-table**](economics/econ-regression-table/SKILL.md) | Format regression tables to economics journal standards | Willie Song |
| [**econ-summary-stats**](economics/econ-summary-stats/SKILL.md) | Produce summary statistics tables with sample transparency and balance tests | Willie Song |
| [**preliminary-data-audit**](economics/preliminary-data-audit/SKILL.md) | Produce a first-pass dataset audit covering introduction, structure, coverage, units, variables, and basic dimensions | Willie Song |

### engineering/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| [**diagnose**](engineering/diagnose/SKILL.md) | Disciplined diagnosis loop for hard bugs and performance regressions | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**tdd**](engineering/tdd/SKILL.md) | Test-driven development with red-green-refactor loop | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**improve-codebase-architecture**](engineering/improve-codebase-architecture/SKILL.md) | Find deepening opportunities in a codebase | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**project-hygiene**](engineering/project-hygiene/SKILL.md) | Keep mixed Git changes, duplicate files, and temporary outputs under control with risk-based audits | Willie Song |
| [**zoom-out**](engineering/zoom-out/SKILL.md) | Zoom out for broader context / higher-level perspective | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |

### planning/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| [**to-issues**](planning/to-issues/SKILL.md) | Break a plan/spec/PRD into independently-grabbable issues | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**to-prd**](planning/to-prd/SKILL.md) | Turn conversation context into a PRD | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**triage**](planning/triage/SKILL.md) | Triage issues through a state machine | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**grill-me**](planning/grill-me/SKILL.md) | Interview the user relentlessly about a plan or design | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**grill-with-docs**](planning/grill-with-docs/SKILL.md) | Grilling session that challenges your plan against existing domain model | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |

### meta/

| Skill | Description | Creator / Source |
|-------|-------------|------------------|
| [**caveman**](meta/caveman/SKILL.md) | Ultra-compressed communication mode. Cuts token usage ~75% | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**find-skills**](meta/find-skills/SKILL.md) | Helps users discover and install agent skills | Vercel Labs, imported from [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| [**write-a-skill**](meta/write-a-skill/SKILL.md) | Create new agent skills with proper structure | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**setup-matt-pocock-skills**](meta/setup-matt-pocock-skills/SKILL.md) | Sets up Agent skills block in AGENTS.md/CLAUDE.md | Matt Pocock, imported from [mattpocock/skills](https://github.com/mattpocock/skills) |
| [**stepwise-explanations**](meta/stepwise-explanations/SKILL.md) | Break long answers into small readable chunks with pause points | Willie Song |

## Attribution

Creator/source labels are based on this repository's commit history and the local skill installer lock file used to import upstream skills. The economics skills, beamer skills, and `stepwise-explanations` were authored in this repository by Willie Song. The Matt Pocock skills were imported and reorganized from `mattpocock/skills`. `find-skills` was imported from `vercel-labs/skills`.

## Usage

Clone into `~/.agents/skills/` and any compatible agent will auto-discover them.

```bash
git clone https://github.com/Ningxi-Song/agent-skills.git ~/.agents/skills
```
