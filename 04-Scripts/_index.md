# Scripts

This folder contains AI-generated intake and communication scripts for Claim Warriors.

## How Scripts Are Generated

1. Call recordings are extracted from GHL (788+ completed contracts)
2. Transcribed with Whisper or Groq (not GHL's built-in transcriber)
3. Batched through Gemini Flash (20-30 transcripts per batch) to mine specific patterns against a defined rubric
4. Claude synthesizes extracted patterns into archetypes, objection/response pairs, and few-shot examples
5. Scripts are generated grounded in real CW call patterns
6. Jo reviews each script and provides feedback
7. Approved scripts are used by AI agents (intake bot, outreach bot) and human reps

## Script Structure

Two intake scripts, each with claim-type-specific branches:

### Script A: Denied Claim Intake
Handed off to: Low-Level Rep ($10-$12/hr)
Goal: Sign at 15%-20%

For customers whose insurance company has denied their claim. The more transactional path. Covers:
- Acknowledging frustration, assessing if denial is worth fighting
- Denied-claim-specific qualification questions
- Objection handling for denied scenarios
- Claim-type branches (water/fire/roof/misc) for type-specific details and red flags

**File**: `intake-denied.md` (TBD -- pending knowledge base completion)

### Script B: New or Underpaid Claim Intake
Handed off to: Sam / Account Manager ($25/hr)
Goal: Sign claim + sales valuation

For customers with a fresh claim or insurance underpayment. The more complex path -- requires assessing claim value and building a case for CW involvement. Covers:
- Assessing the gap between payout and actual damage value
- Performing sales valuation (what is CW's potential fee?)
- New/underpaid-specific qualification questions
- Objection handling for underpayment scenarios
- Claim-type branches (water/fire/roof/misc) for type-specific details and red flags

**File**: `intake-new-underpaid.md` (TBD -- pending knowledge base completion)

## Why Two Scripts, Not Nine

The claim STATUS (denied vs. new/underpaid) drives the conversation structure -- the customer's emotional state, objections, and qualification path are fundamentally different. The claim TYPE (water, fire, roof, misc) adds context within each script but doesn't change the core flow. Separate sections inside each script handle type-specific details.

## Additional Script Types (Future)

### Nurture Scripts
Claim-type-specific follow-up sequences for customers who don't sign on the first call. See Deliverable 7 in the [[../01-AI-Strategy/implementation-plan|implementation plan]].

### Outreach Scripts
For the denied claims outreach bot to re-contact ~796 unsigned leads. Different tone -- re-engagement, not first contact.

## Status

**Not yet generated.** Waiting on:
- [ ] Knowledge base ingestion (Deliverable 1)
- [ ] Pattern extraction pipeline (Gemini Flash batches)
- [ ] Claude synthesis pass
- [ ] Jo's review and feedback
