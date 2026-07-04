---
name: stepwise-explanations
description: Break long explanations, reports, tutorials, implementation walkthroughs, and multi-step reasoning into short readable chunks with explicit pause points. Use when the user asks for step-by-step explanation, says long answers are hard to read, asks to proceed slowly, or when an answer would otherwise require substantial scrolling.
---

# Stepwise Explanations

Use this skill to pace long answers so the user can read and retain each part before moving on.

## Core Rule

For any answer that would be long, multi-step, or conceptually dense, do not deliver the whole explanation at once.

Instead:

1. Start with a short roadmap.
2. Explain only the first chunk.
3. Stop and ask whether to continue.
4. Continue one chunk at a time after the user confirms.

## Chunk Size

Keep each chunk small enough to fit on one screen:

- Aim for 150-300 words.
- Use at most 3-5 bullets.
- Include only one main idea per chunk.
- Avoid long tables unless the user explicitly asks for them.
- Prefer compact code snippets over full files.

## Opening Pattern

Begin with a roadmap like:

```text
I will explain this in 5 parts:
1. What problem we are solving
2. How the variables are generated
3. How the estimation works
4. What the figures mean
5. What we learn

I will start with Part 1 and pause before Part 2.
```

Then give Part 1 only.

## Pause Pattern

End each chunk with a simple continuation question:

```text
Say "continue" and I will explain Part 2.
```

Do not continue automatically unless the user has clearly asked for the full report in one message.

## When User Asks "Step by Step"

Treat "step by step" literally:

- Explain one step.
- State why it matters.
- Give a minimal example if useful.
- Pause.

## When User Asks for a File

If the user asks for a Markdown file, report, guide, or long written artifact:

- It is acceptable to write the full file.
- In the chat response, give only the file path and a short summary.
- Do not paste the full file content unless requested.

## Exceptions

You may answer normally when:

- The answer is short.
- The user explicitly asks for everything at once.
- The user asks for a complete artifact to be written to disk.
- A safety, correctness, or approval issue requires immediate complete context.

## Style

Use clear headings, short paragraphs, and plain language.

Prefer:

```text
Part 1: The causal question
...
Say "continue" and I will explain Part 2.
```

Avoid:

```text
Here is a full 20-section explanation...
```
