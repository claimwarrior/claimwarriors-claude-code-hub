# Scripts

This folder contains AI-generated intake and communication scripts for Claim Warriors.

## How Scripts Are Generated

1. The knowledge base is built from 788+ completed contracts and their call recordings (see [[../02-Projects/knowledge-base-ingestion]])
2. Claude analyzes the data, organized by claim type and status
3. Scripts are generated for each combination of claim type + claim status
4. Jo reviews each script and provides feedback
5. Approved scripts are used by AI agents (intake bot, outreach bot) and human reps

## Script Matrix

| | Water | Roof | Fire | Misc |
|---|---|---|---|---|
| **Denied** | TBD | TBD | TBD | TBD |
| **Underpaid** | TBD | TBD | TBD | TBD |
| **New** | TBD | TBD | TBD | TBD |

Each cell will become a script file in this folder once generated.

## Script Types

### Intake Scripts
Used by the AI intake bot and human reps during the first call with a customer. Cover:
- Greeting and introduction
- Qualification questions
- Claim-type-specific probing questions
- Objection handling
- Transition to contract discussion

### Nurture Scripts
Used for follow-up when a customer doesn't sign on the first call. Personalized by claim type:
- Claim-specific information (why water damage claims are commonly underpaid, etc.)
- Social proof (reviews, success stories)
- Urgency triggers
- Re-engagement messaging

### Outreach Scripts (Future)
Used by the denied claims outreach bot to re-contact unsigned leads. Different tone -- re-engagement rather than first contact.

## Naming Convention

Scripts will be named: `{type}-{claim-type}-{claim-status}.md`

Example: `intake-water-denied.md`, `nurture-roof-underpaid.md`

## Status

**Not yet generated.** Waiting on:
- [ ] Knowledge base ingestion (Phase 1)
- [ ] Jo's list of what scripts she wants first
- [ ] Jo's review and approval process

## Source

Script strategy from Ben/Jo calls March 24-25 2026.
