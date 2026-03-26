# AI Decision Principles

These are the principles guiding AI decisions at Claim Warriors. Established during the March 24-25 2026 strategy calls.

## 1. Teach First, Build Second

Before building any AI agent, Claude needs to understand the business deeply. The knowledge base comes before any bot. Without business context, agents produce generic output. With context, they produce claim-type-specific, operationally relevant output.

> "Teach Claude what this business is. Once we have that understanding, then we separate denied, new, and underpaid claims." -- Jo

## 2. Buy Over Build (When Possible)

If a tool already exists that solves the problem, use it. Don't build from scratch what you can buy. Jo explicitly supports spending on AI tools to move faster -- paying for a tool is cheaper than paying Ben's time to build a worse version.

> "I'd rather pay a premium to an AI tool that already has everything than rather use it and try to build it out and hack it." -- Jo

## 3. Context Is Everything

An AI with context outperforms an AI without context, even if the AI itself is identical. Every agent should have access to the full business knowledge base. This is why the Obsidian vault and data ingestion pipeline are foundational -- they create the context layer that makes every future agent smarter.

> "Claude A with no context gives you decent results. Claude B with business context gives you way better results." -- Ben

## 4. Use the Right Model for the Job

- **Claude** for complex reasoning, script writing, tool use, conversation, code generation
- **Gemini** for image analysis (damage photos, estimates) -- cheap and excellent at visual tasks
- **Whisper** for transcription -- better than GHL's built-in transcriber
- **ChatGPT** fine for simple summarization (but Claude preferred for consistency)

Don't default to the biggest/most expensive model for everything. Match the model to the task.

## 5. Security Over Convenience

Chose Claude Claw over OpenClaw specifically because:
- No third-party skills marketplace (no malware risk)
- Uses Anthropic subscription (no expensive API tokens)
- Runs on a controlled machine (not exposed to untrusted code)
- See [[../05-Decisions/2026-03-24-claude-claw-over-openclaw]]

## 6. Human Oversight on High-Stakes Decisions

AI assists, humans decide -- especially for:
- Contract sending (human reviews before sending)
- Claim value assessment (AI suggests, adjuster confirms)
- Carrier negotiations (AI drafts, human sends)
- Customer escalations (AI handles routine, human handles complex)

## 7. Revenue Impact First

Every AI project should tie to one of:
- **Saving time** (reduce hours on garbage claims)
- **Saving money** (automate tasks currently done by humans)
- **Making money** (close more deals, handle more calls, reactivate unsigned leads)

If it doesn't do one of these three, question whether it's worth building.

## Source

Principles extracted from:
- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
