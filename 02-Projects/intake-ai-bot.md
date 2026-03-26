# Project: Intake AI Bot

**Status**: Phase 2 -- Planned
**Priority**: High -- first AI agent to deploy
**Owner**: Ben
**Phase**: 2 (Front Office AI)

## What It Does

An AI voice agent that picks up inbound sales calls via Go High Level, pre-qualifies the lead by asking intake questions, and fills out GHL custom fields in real-time during the call using tool calls.

## Why It Matters

- Handles overflow calls when human reps are busy (currently those calls go unanswered)
- Pre-qualifies leads before routing to human reps
- Fills GHL fields automatically -- no manual data entry
- Operates 24/7 without breaks

## How It Works

1. Inbound call hits GHL IVR
2. If all human reps are busy, call routes to AI intake agent
3. AI greets customer, asks qualifying questions based on learned scripts
4. As customer answers, AI makes GHL API tool calls to update custom fields in real-time:
   - First name, last name, contact info
   - Type of loss (water, fire, roof, misc)
   - Claim status (denied, underpaid, new)
   - Estimated claim value
   - Amount paid by insurance
5. AI rates the lead quality based on responses
6. If qualified, routes to next step (contract or human callback)
7. If not qualified, handles gracefully

## Technical Requirements

- Voice AI agent with GHL integration
- Real-time tool calls to GHL API during conversation
- Voicemail detection -- must identify when it's talking to a machine and hang up (avoid billing)
- Scripts per claim type + status combination (generated from knowledge base)
- Call recording for quality assurance

## Dependencies

- [ ] Knowledge base must be built first (Phase 1) -- scripts are generated from this
- [ ] GHL MCP must be configured for read/write
- [ ] Jo must review and approve generated scripts before going live
- [ ] Voicemail detection logic must be tested

## Open Questions

- Can we use Rio's cloned voice for the agent? (Future enhancement)
- What's the handoff flow when AI qualifies a lead but no human rep is available?
- Should AI attempt to send contract, or always route to human for that step?

## Timeline

Originally discussed as "ready by tomorrow" (March 25) for the pure AI version. Pushed to after knowledge base is built (Thursday March 27 target).

## Source

- Ben/Jo call, March 24 2026 -- "AI Next Steps" (primary discussion)
- Ben/Jo call, March 25 2026 -- confirmed priority
