# AI Roadmap

## Phase 1 -- Foundation (Now)

**Status**: In progress (March 2026)

### Build the Knowledge Base (Extraction Pipeline)
- [ ] Extract call recordings from GHL API (focus on 5+ minute substantive calls)
- [ ] Transcribe with Whisper or Groq (not GHL's built-in transcriber)
- [ ] Define extraction rubric (objections, qualifications, closes, openers, red flags)
- [ ] Batch process 20-30 transcripts at a time through Gemini Flash
- [ ] Claude synthesis pass -- distill patterns into archetypes and few-shot examples
- [ ] Store structured knowledge in this Obsidian vault

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
- [ ] Generate 2 intake scripts (denied + new/underpaid) with claim-type branches
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
