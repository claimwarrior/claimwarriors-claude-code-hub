# AI Roadmap

## Phase 1 -- Foundation (Now)

**Status**: In progress (March 2026)

### Build the Knowledge Base
- [ ] Ingest 788+ completed contracts from GHL (payments -> completed -> customer -> calls)
- [ ] Transcribe call recordings using Whisper (GHL's built-in transcriber is too low quality)
- [ ] Feed all data to Claude to learn about Claim Warriors' business
- [ ] Separate knowledge by claim type (water, roof, fire, misc) and claim status (denied, underpaid, new)
- [ ] Build this Obsidian vault as the structured reference layer

### Connect MCP Integrations
- [ ] GHL MCP -- read/write contacts, opportunities, conversations, custom fields
- [ ] Airtable MCP -- read/write claim records
- [ ] Supabase MCP -- direct access to Claim Warriors software DB
- [ ] Outlook MCP -- email read/write
- [ ] Fireflies MCP -- call transcripts and recordings
- [ ] Slack -- set up channels, prepare for bot integration

### Deploy Claude Claw
- [ ] Set up persistent Claude Code instance with conversational layer
- [ ] Determine permanent hosting (Ben's machine -> dedicated machine or cloud)
- [ ] Connect to all MCP integrations

**Target**: By Thursday March 27, 2026 -- knowledge base learned, first scripts generated

## Phase 2 -- Front Office AI (Next)

### Intake AI Bot
- [ ] Build AI voice agent that picks up calls via GHL
- [ ] Pre-qualifies leads using learned scripts
- [ ] Updates GHL custom fields in real-time during the call via tool calls
- [ ] Routes qualified leads to appropriate next step
- [ ] Detects voicemails and hangs up (don't bill for voicemail)

### Live Call Listener
- [ ] Research: how to join GHL calls as third-party listener
- [ ] Build AI note-taker that listens to human rep calls
- [ ] Updates GHL fields in real-time as information is discussed
- [ ] Generates/updates call summary (single document, not duplicates)

### Call Summary Fix
- [ ] Fix broken GHL workflow (851/852/853) that creates duplicate summaries
- [ ] Implement: one summary per customer, updated on each call
- [ ] After customer signs contract, push summary as first comment to Claim Warriors software

### Script Generation
- [ ] Generate intake scripts per claim type + status combination (9 combinations)
- [ ] Jo reviews and provides feedback
- [ ] Iterate scripts based on feedback

## Phase 3 -- Back Office AI (Later)

### Claim Verification
- [ ] AI analyzes pictures + estimates to rate claim viability
- [ ] Flags garbage claims before back office invests hours
- [ ] Uses Gemini for image analysis

### Estimate Gap Analysis
- [ ] Compare CW estimates vs. carrier estimates
- [ ] Highlight missing items, undervalued items, overlooked damage
- [ ] Generate summary of what to negotiate for

### Carrier Communication AI
- [ ] AI-drafted negotiation emails based on full claim data
- [ ] Extract RingCentral AI summaries and feed into CW software
- [ ] AI-assisted carrier call prep

## Phase 4 -- Outreach & Automation (Future)

### Denied Claims Outreach Bot
- [ ] Contact the ~796 unsigned customers
- [ ] Personalized outreach based on claim type
- [ ] Text and call campaigns

### Email AI
- [ ] Monitor and respond to routine emails
- [ ] Draft carrier negotiation emails
- [ ] Flag urgent communications

### Contract Automation
- [ ] Auto-send contracts during calls when all fields are filled
- [ ] Auto-populate contract with customer data

### Voice Cloning
- [ ] Clone former rep Rio's voice for AI agents
- [ ] Use for intake and outreach bots

### Internal Slack Bots
- [ ] Task automation between team members
- [ ] Claims triage and routing
- [ ] Consultant-style routing bot (inspection, attorney, negotiation)

## Source

Timeline and priorities from:
- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
