# Project: Knowledge Base Ingestion

**Status**: Phase 1 -- In progress
**Priority**: Critical -- everything else depends on this
**Owner**: Ben
**Phase**: 1 (Foundation)

## What It Does

Teaches Claude everything about Claim Warriors by extracting patterns from 788+ completed contracts and their call recordings. Creates the foundation that every future AI agent draws from.

## Why It's Critical

Jo's core directive: "Teach Claude what this business is. Once we have that understanding, then we can build everything else."

Without business context, AI agents produce generic output. With patterns extracted from hundreds of real calls, agents produce scripts grounded in what actually worked.

## Data Sources

### Completed Contracts (788+)
- Location: GHL -> Payments -> All Documents -> Contracts -> Completed
- Contains: Customer info, claim type, claim value, contract terms
- Access: GHL MCP or GHL API

### Call Recordings
- Location: Under each customer in GHL
- Volume: Multiple calls per customer, focus on substantive calls (5+ minutes)
- Quality: GHL's built-in transcription is too low quality -- need Whisper or Groq
- Key insight: All 788 contracts are COMPLETED deals, so all calls are inherently "successful"

### Unsigned Leads (~796)
- Location: GHL -> Payments -> Contracts -> Not Signed
- Future use: Outreach bot data. Not needed for Phase 1

## Extraction Pipeline

Based on expert advice (Mark Kashef, Matthew Snow -- Early AI-dopters community). Revised from original approach.

### Step 1: Extract Audio
- Pull call recordings from GHL via API
- Focus on intake calls (first substantive call per customer, 5+ minutes)
- Skip missed calls, voicemails, sub-minute callbacks

### Step 2: Transcribe
- Use Whisper-based transcription or Groq's free tier
- NOT GHL's built-in transcriber (too many errors)
- Output: clean text transcripts per call

### Step 3: Define Extraction Rubric
- No manual labeling of individual calls needed (all are successful deals)
- Define WHAT patterns to mine for:
  - Every objection raised and how it was handled
  - Every qualification question asked and when in the call
  - Every close attempt and what led to it
  - Every opener and customer response
  - Claim type identification and type-specific details
  - Red flags mentioned (old claims, low value, prior adjusters)
  - Information collection patterns (what fields, what order)
  - Customer emotional state and how rep responded

### Step 4: Batch Process with Gemini Flash
- Batch 20-30 transcripts at a time
- Gemini Flash: cheap, 1M context window
- Prompt: "Given this rubric, extract every instance of [pattern]"
- Mine for specific patterns, NOT generic summaries
- Save Claude tokens for synthesis -- Gemini handles the bulk extraction

### Step 5: Synthesis with Claude
- Take all extracted patterns from Gemini batches
- Distill into:
  - Conversation archetypes (expected: 4-6 distinct types)
  - Recurring objection/response pairs (expected: 10-15)
  - Qualification patterns per claim type
  - Few-shot examples from real calls
- Claude's reasoning quality matters here -- this is where the intelligence happens

### Step 6: Generate Outputs
- 2 intake scripts (denied + new/underpaid) with claim-type branches
- Qualification criteria per claim type
- Rating system framework
- Operational improvement recommendations
- Nurture content per claim type
- All grounded in real patterns, with few-shot examples embedded

## Why Not Manual Labeling?

Mark Kashef and Matthew Snow recommended labeling 20-30% of calls before processing. We're skipping this because:
1. All 788 contracts are completed deals -- they're all "successful" calls
2. We define the rubric (what to extract) without needing per-call labels
3. Jo IS the feedback loop -- he'll review scripts and iterate
4. Labeling 150+ calls would delay delivery by days for marginal first-draft improvement

## Why Gemini Flash, Not Claude, for Extraction?

- Gemini Flash: $0.075/1M input tokens, 1M context window
- Claude: $3/1M input tokens, 200k context window
- Extraction is pattern matching, not complex reasoning
- Save Claude for the synthesis pass where reasoning quality actually matters
- 40x cost difference for the bulk processing step

## Challenges

- **Volume**: 788 contracts x multiple calls = potentially thousands of recordings
- **Audio extraction**: Need to figure out GHL API call recording access
- **Transcription cost/time**: Large volume, need efficient pipeline
- **Gemini Flash prompt engineering**: Rubric needs to be precise to get useful extractions

## Timeline

- **Original target**: Thursday March 27, 2026
- **Revised**: Pipeline needs to be built first. Realistic: extraction pipeline this week, first script outputs early next week

## Operational Runbook

For the hands-on "how to run it" guide with exact commands, current status, and Supabase schema, see [[knowledge-base-creation]].

## Source

- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- confirmed priority
- Mark Kashef & Matthew Snow -- pipeline methodology (Early AI-dopters, March 2026)
