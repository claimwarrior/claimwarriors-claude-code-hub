# Integration: RingCentral

**Status**: No MCP available -- manual or custom API integration needed
**MCP Server**: None (as of March 2026)

## What It Connects To

RingCentral -- phone system used by back office for carrier/insurance company communications.

## Current State

- Back office uses RingCentral to call and negotiate with insurance carriers
- RingCentral has a built-in AI summarization tool that generates call summaries
- These summaries currently stay inside RingCentral -- not connected to CW software

## Desired State

- Extract AI-generated summaries from RingCentral
- Push summaries into Claim Warriors software as comments/notes on the claim
- Give AI access to carrier communication data for negotiation assistance

## Integration Approach

Since no MCP exists, options are:
1. **RingCentral API** -- Custom integration to pull call data and summaries
2. **N8N workflow** -- Build an N8N automation that polls RingCentral and pushes to Supabase
3. **Manual export** -- Team manually copies summaries (not ideal, but works as interim)

## Priority

Low -- this is a Phase 4 item. Core front office AI comes first. But noting it here so it doesn't get lost.

## Source

- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
