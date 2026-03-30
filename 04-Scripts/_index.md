# Scripts

This folder contains AI-generated intake scripts, qualification frameworks, and reference materials for Claim Warriors. All content synthesized from 2,800+ successful sales calls (28 batch reports).

## How Scripts Were Generated

1. Call recordings extracted from GHL (788+ completed contracts)
2. Transcribed with Whisper/Groq
3. Batched through Gemini Flash to mine specific patterns against a defined extraction rubric
4. Claude synthesized extracted patterns into archetypes, objection/response pairs, and few-shot examples
5. Scripts generated grounded in real CW call patterns
6. **Status**: Generated. Awaiting Jo's review and feedback.

## Files in This Folder

### Foundation Documents (read these first)
- **[[conversation-archetypes]]** -- 5 distinct conversation patterns that cover ~100% of CW calls
- **[[objection-response-pairs]]** -- 12 objection types ranked by frequency, with real rep quotes and resolution rates
- **[[qualification-sequences]]** -- Question sequences per claim type (water/roof/fire/misc) in the order top reps actually use
- **[[rating-signals]]** -- Framework for scoring leads, calls, and claims (1-10 scales + hard disqualifiers)
- **[[few-shot-examples]]** -- 24 real call excerpts for embedding in AI agent prompts

### Intake Scripts
- **[[intake-denied]]** -- Script A: Denied claim intake. For low-level rep ($10-12/hr). Goal: sign at 15-20%.
- **[[intake-new-underpaid]]** -- Script B: New/underpaid claim intake. For Sam / Account Manager ($25/hr). Goal: sign + sales valuation. Includes sales valuation cheat sheet.

## Why Two Scripts, Not Nine

The claim STATUS (denied vs. new/underpaid) drives the conversation structure -- the customer's emotional state, objections, and qualification path are fundamentally different. The claim TYPE (water, fire, roof, misc) adds context within each script but doesn't change the core flow. Separate sections inside each script handle type-specific details.

## How to Use These

### For Human Reps
Read the script matching your role. Reference the objection-response pairs and few-shot examples as training material. The scripts are structured as a conversation flow — follow the phases in order.

### For AI Agents
Load the relevant script as the primary prompt. Embed 3-5 few-shot examples from [[few-shot-examples]] to set the tone. Use [[rating-signals]] for post-call scoring. Use [[qualification-sequences]] for type-specific question logic.

### For Jo's Review
Start with [[conversation-archetypes]] to see if the patterns ring true. Then read both intake scripts. The question to answer: "Does this sound like how my best rep talks?"

## Additional Script Types (Future)

### Nurture Scripts
Claim-type-specific follow-up sequences for customers who don't sign on the first call. See Deliverable 7 in the [[../01-AI-Strategy/implementation-plan|implementation plan]].

### Outreach Scripts
For the denied claims outreach bot to re-contact ~796 unsigned leads. Different tone -- re-engagement, not first contact.

## Status

- [x] Knowledge base ingestion (Deliverable 1)
- [x] Pattern extraction pipeline (Gemini Flash batches — 28 batches, 2,800+ calls)
- [x] Claude synthesis pass
- [ ] Jo's review and feedback
- [ ] Iterate scripts based on feedback
