# Project: Knowledge Base Ingestion

**Status**: Phase 1 -- In progress
**Priority**: Critical -- everything else depends on this
**Owner**: Ben
**Phase**: 1 (Foundation)

## What It Does

Teaches Claude everything about Claim Warriors by ingesting all available data: contracts, call recordings, transcripts, and operational knowledge. This creates the foundation that every future AI agent draws from.

## Why It's Critical

Jo's core directive: "Teach Claude what this business is. Once we have that understanding, then we can build everything else."

Without business context, AI agents produce generic output. With 788+ contracts and thousands of call recordings worth of context, agents produce claim-type-specific, operationally relevant output.

## Data Sources

### Completed Contracts (788+)
- Location: GHL -> Payments -> All Documents -> Contracts -> Completed
- Contains: Customer info, claim type, claim value, contract terms
- Access: Navigate to each customer, view their full record

### Call Recordings
- Location: Under each customer in GHL (hover over customer name -> click -> calls)
- Volume: Multiple calls per customer, some with 5+ calls
- Intake calls: Usually first call over 5 minutes
- Quality: GHL's built-in transcription is "garbage" -- need Whisper or better transcriber
- Approach: Identify intake calls (first substantive call per customer)

### Unsigned Leads (~796)
- Location: GHL -> Payments -> Contracts -> Not Signed
- Future use: Outreach bot data. Not needed for Phase 1 but should be noted

### Fireflies Recordings
- Location: Fireflies MCP
- Contains: Strategy calls between Ben and Jo
- Use: Understanding business context, priorities, operational challenges

## Ingestion Strategy

### Step 1: Structured Data
- Pull all completed contract data from GHL via MCP
- Categorize by claim type (water, fire, roof, misc) and status (denied, underpaid, new)
- Store structured knowledge in this Obsidian vault

### Step 2: Call Transcripts
- For each completed contract, pull the call recording
- Transcribe using Whisper (better quality than GHL's transcriber)
- Feed transcripts to Claude organized by claim type
- Extract: sales patterns, objections, customer language, key qualification questions

### Step 3: Knowledge Synthesis
- Claude analyzes all data and produces:
  - Intake scripts per claim type + status (9 combinations)
  - Qualification criteria per claim type
  - Common objections and responses
  - Red flags that indicate a garbage claim
  - Patterns in successful vs. failed claims

### Step 4: Store in Vault
- Generated scripts go in [[../04-Scripts/_index|04-Scripts]]
- Qualification criteria and patterns go in [[../00-Company/claim-types|claim-types]]
- Everything feeds back into this vault as permanent reference

## Challenges

- **Volume**: 788 contracts x multiple calls each = potentially thousands of recordings
- **Quality**: GHL transcripts are low quality, need re-transcription
- **Token management**: Can't feed everything into one context window. Need chunking strategy
- **Time**: Ben estimated 2-3 days to build the ingestion pipeline and have initial results

## Timeline

- **Target**: Thursday March 27, 2026 -- knowledge base learned, first scripts generated
- **Jo's request**: Scripts ready for review by Thursday so she can give feedback

## Source

- Ben/Jo call, March 24 2026 -- "AI Next Steps" (extensive discussion)
- Ben/Jo call, March 25 2026 -- confirmed priority
