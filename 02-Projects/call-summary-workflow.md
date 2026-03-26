# Project: Call Summary Workflow Fix

**Status**: Needs fix
**Priority**: High -- currently broken
**Owner**: Ben
**Phase**: 2 (Front Office AI)

## The Problem

The current GHL automation (workflows 851, 852, 853) generates call summaries using ChatGPT, but it's broken:

1. **Creates duplicate summaries** -- Every call creates a new summary entry instead of updating the existing one. A single customer can have 5+ separate summary entries
2. **No single source of truth** -- Multiple summary fields exist (summary, damage summary, lead summary, claim summary) and it's unclear which is canonical
3. **Summaries don't push to software** -- After a customer signs, the summary should become the first comment in Claim Warriors software. This doesn't happen

## Desired Behavior

### During Sales Process
- One summary document per customer
- Each call updates the existing summary (appends new info, doesn't create a new one)
- Summary includes: call date, key topics discussed, customer's claim details, next steps
- Summary is continuously updated as more calls happen with the same customer

### After Contract Signing
- The complete summary is pushed to Claim Warriors software as the first comment on the new claim
- Data flow: GHL summary -> Airtable -> Supabase (Claim Warriors software comment)
- This gives the back office immediate context without having to listen to calls

## Technical Approach

1. Identify the existing GHL workflows (851, 852, 853) and understand current logic
2. Fix: single summary field per contact, updated on each call (not new entry)
3. Improve: use Claude instead of ChatGPT for better summary quality (optional -- Jo said summarization works fine with any AI)
4. Add: trigger that pushes summary to CW software when contract status changes to "signed"

## Dependencies

- [ ] Access to GHL workflow editor to review current automations
- [ ] Understand the data flow from GHL -> Airtable -> Supabase for new claims
- [ ] Determine which summary field is the canonical one (or create a new one)

## Source

- Ben/Jo call, March 24 2026 -- "AI Next Steps"
