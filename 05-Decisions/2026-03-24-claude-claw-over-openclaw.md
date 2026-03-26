# Decision: Claude Claw Over OpenClaw

**Date**: March 24, 2026
**Decision by**: Ben
**Status**: Decided

## Context

We needed a persistent AI system that could be "always on" -- connected to all business tools via MCP, accessible via conversational interface (Telegram/Discord), and capable of autonomous task execution.

Two options were evaluated:
1. **OpenClaw** -- Open source framework, viral adoption, large skills marketplace
2. **Claude Claw** -- Claude Code wrapper built by a trusted developer, runs natively on Claude

## Decision

**Claude Claw** was chosen over OpenClaw.

## Reasoning

### Security
- OpenClaw has a public skills marketplace where anyone can publish skills
- Multiple incidents of malware-infected skills being published (keyloggers, credential scrapers)
- Users who installed these skills had their private data compromised
- Claude Claw has no third-party marketplace -- only skills we create ourselves

### Cost
- OpenClaw cannot use the Anthropic subscription token (Claude subscription) -- this is a terms of service violation
- Using OpenClaw with Claude requires the Anthropic API, which costs ~5x more than the subscription
- Claude Claw uses the Anthropic subscription directly -- significantly cheaper
- Jo is paying for Ben's time + tools. No reason to pay 5x more for the same AI

### Integration
- Claude Claw runs on the same machine where the Claim Warriors codebase lives
- This means it already has access to everything: the CW software, MCP integrations, vault, etc.
- OpenClaw would require deploying on a separate machine, creating synchronization problems between OpenClaw and the CW development environment

### Familiarity
- Ben already uses Claude Code extensively and is building Claude Claw for personal use
- Same mental model, same tools, same workflow -- no additional learning curve

## Trade-offs

### What We Lose
- OpenClaw's large community and skills marketplace (but this is also the security risk)
- OpenClaw's broader model support (can use any LLM, not just Claude)

### What We Gain
- Security (no untrusted third-party code)
- Cost efficiency (subscription vs. API pricing)
- Integration simplicity (same machine, same tools)
- Consistency (one platform for development and AI operations)

## Deployment Plan

1. ~~Start on Ben's personal computer~~ (current temporary setup)
2. Move to dedicated always-on machine (Mac Mini, VPS, or similar)
3. Both Ben and Jo need access to the machine/instance

## Source

- Ben/Jo call, March 24 2026 -- "AI Next Steps" (detailed discussion at ~23:49 mark)
