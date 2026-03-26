# Project: Live Call Listener

**Status**: Research needed
**Priority**: High
**Owner**: Ben
**Phase**: 2 (Front Office AI)

## What It Does

An AI agent that joins live calls between human sales reps and customers as a silent third-party listener. It transcribes the conversation in real-time, fills GHL custom fields as information is mentioned, and generates/updates the call summary.

## Why It Matters

- Reps currently fill fields manually during calls -- slow and error-prone
- Contracts need to be sent during the call, which requires fields to be filled
- Call summaries are generated after the call -- but they should be building in real-time
- Frees reps to focus on the conversation instead of data entry

## How It Works (Proposed)

1. Sales call comes in via GHL IVR
2. Human rep picks up
3. AI listener auto-joins the call as a third participant (silent/muted)
4. AI transcribes the conversation in real-time
5. As key information is mentioned (name, claim type, values), AI updates GHL fields via API
6. After call ends, AI finalizes the summary and updates the single summary document

## Technical Challenge

This is the biggest unknown. How do we get an AI to join a live GHL call as a third-party listener?

### Possible Approaches
1. **GHL conference/3-way call** -- Have the IVR ring both the human rep AND an AI "user". AI joins as second participant. Need to verify if GHL supports this
2. **Twilio-level integration** -- GHL uses Twilio under the hood. May be able to intercept the audio stream at the Twilio layer
3. **RingCentral-style approach** -- Some tools (like RingCentral) have built-in call recording with AI. Could we tap into GHL's recording stream in real-time?
4. **Post-call processing** -- Fallback: don't listen live, but process the recording immediately after the call ends. Less ideal (can't fill fields during the call) but much simpler

## Dependencies

- [ ] Research: Can GHL support 3-way calls with an AI participant?
- [ ] Research: Can we access the Twilio audio stream under GHL?
- [ ] GHL MCP must be configured for real-time field updates
- [ ] Knowledge base built so AI knows which fields to fill based on conversation content

## Open Questions

- Is real-time field filling during a human call technically feasible with GHL?
- If not, is near-real-time (processing in chunks every 10-15 seconds) acceptable?
- What's the fallback if live listening isn't possible? Post-call processing?

## Source

- Ben/Jo call, March 24 2026 -- "AI Next Steps" (extensive discussion on this feature)
