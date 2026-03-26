# Project: AI Customer Service Rep

**Status**: Planned
**Priority**: Medium-High
**Owner**: Ben
**Phase**: 2 (Front Office AI)

## What It Does

A front-office AI bot that handles routine customer support inquiries. Connected to GHL and the Claim Warriors software, it can look up claim status, provide updates, and escalate complex issues to the back office via Slack tickets.

## Why It Matters

- Customers call in asking for status updates -- currently handled by human reps
- Frees up reps to focus on sales instead of support
- Provides faster response times for routine questions
- Creates a clear escalation path (AI -> Slack ticket -> back office)

## How It Works

1. Customer calls in with a support question
2. AI identifies the customer (phone number lookup in GHL)
3. AI reads claim data from Claim Warriors software (Supabase MCP)
4. AI reads recent comments, status updates, and notes
5. AI summarizes the claim status and communicates it to the customer in plain language
6. If the customer's issue requires action:
   - AI opens a Slack ticket in the appropriate channel
   - Ticket includes: customer info, claim ID, issue description, urgency level
   - Back office picks up the ticket
7. If additional information is needed from the customer, AI collects it and attaches to the ticket

## Integration Points

- **GHL** -- Customer lookup, contact info, call history
- **Supabase (CW Software)** -- Claim status, comments, assignments, file history
- **Slack** -- Ticket creation for back office escalation
- **Airtable** -- Additional claim data if needed

## Dependencies

- [ ] Knowledge base built (Phase 1) -- bot needs to understand claim terminology
- [ ] Slack channels set up for AI-generated tickets
- [ ] Supabase MCP configured for claim data reads
- [ ] Define: what questions can AI answer vs. what requires human escalation

## Open Questions

- What's the boundary between "AI can handle this" and "route to human"?
- Should the bot be voice only, or also handle text/chat through GHL?
- What Slack channel structure for AI-generated tickets? One channel per claim type? One general?

## Source

- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
