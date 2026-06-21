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
    └── setup-matt-pocock-skills
```

## Skills

### economics/

| Skill | Description |
|-------|-------------|
| **econ-regression-table** | Format regression tables to economics journal standards |
| **econ-summary-stats** | Produce summary statistics tables with sample transparency and balance tests |
| **beamer-presentation** | Design academic Beamer slides with conclusion-driven titles and one-point-per-slide |

### engineering/

| Skill | Description |
|-------|-------------|
| **diagnose** | Disciplined diagnosis loop for hard bugs and performance regressions |
| **tdd** | Test-driven development with red-green-refactor loop |
| **improve-codebase-architecture** | Find deepening opportunities in a codebase |
| **zoom-out** | Zoom out for broader context / higher-level perspective |

### planning/

| Skill | Description |
|-------|-------------|
| **to-issues** | Break a plan/spec/PRD into independently-grabbable issues |
| **to-prd** | Turn conversation context into a PRD |
| **triage** | Triage issues through a state machine |
| **grill-me** | Interview the user relentlessly about a plan or design |
| **grill-with-docs** | Grilling session that challenges your plan against existing domain model |

### meta/

| Skill | Description |
|-------|-------------|
| **caveman** | Ultra-compressed communication mode. Cuts token usage ~75% |
| **find-skills** | Helps users discover and install agent skills |
| **write-a-skill** | Create new agent skills with proper structure |
| **setup-matt-pocock-skills** | Sets up Agent skills block in AGENTS.md/CLAUDE.md |

## Usage

Clone into `~/.agents/skills/` and any compatible agent will auto-discover them.

```bash
git clone https://github.com/Ningxi-Song/agent-skills.git ~/.agents/skills
```
