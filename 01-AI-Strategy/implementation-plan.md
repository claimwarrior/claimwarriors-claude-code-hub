# Implementation Plan -- What Jo Is Waiting For

This document describes everything Joseph expects to come out of the AI initiative, organized as concrete deliverables. Revised March 26 based on expert pipeline advice and scope clarification.

---

## Deliverable 1: The Knowledge Base (Foundation for Everything Else)

### What Jo Said
"Teach Claude what this business is. Go to payments, completed contracts, find every customer, listen to all the phone calls. Separate the data into water, roof, fire, miscellaneous. Once we have that understanding, then we can build everything else."

### What This Actually Means
Claude needs to ingest all 788+ completed contracts and their associated call recordings from Go High Level. The goal is for Claude to internalize how Claim Warriors operates deeply enough that its outputs sound like they came from someone who's worked there for a year.

What Claude needs to learn:
- What does a typical water damage intake call sound like vs. a roof or fire call?
- What does a denied claim customer say vs. a new/underpaid claim customer?
- What questions do successful reps ask that lead to signed contracts?
- What are the common objections and how do the best reps handle them?
- What information do reps collect, in what order?
- What language do customers use when describing their situation?
- What patterns separate high-value claims from garbage claims?

### Extraction Pipeline

Based on expert advice from Mark Kashef and Matthew Snow (Early AI-dopters community), the pipeline is:

**Step 1: Extract audio from GHL**
- Use GHL API to pull call recordings from all 788 completed contracts
- Focus on substantive calls (5+ minutes) -- skip missed calls, voicemails, sub-minute callbacks

**Step 2: Transcribe with Whisper or Groq**
- GHL's built-in transcriber is too low quality
- Use Whisper-based transcription or Groq's free tier
- Output: clean text transcripts per call

**Step 3: Define extraction rubric**
- NOT manual labeling of individual calls (all 788 contracts are successful deals -- they're inherently "good" calls)
- Instead, define WHAT patterns to mine for:
  - Every objection raised and how it was handled
  - Every qualification question asked and when in the call
  - Every close attempt (successful or not) and what led to it
  - Every opener and how the customer responded
  - Claim type identification and type-specific details discussed
  - Red flags mentioned (old claims, low value, prior adjusters)
  - Information collection patterns (what fields, what order)

**Step 4: Batch process with Gemini Flash**
- Batch 20-30 transcripts at a time
- Gemini Flash: cheap, 1M context window, handles the volume
- Prompt: "Given this rubric, extract every instance of [pattern] from these transcripts"
- Mine for specific patterns, NOT generic summaries
- Don't burn Claude tokens on extraction -- save Claude for synthesis

**Step 5: Synthesis pass with Claude**
- Take all extracted patterns from Gemini Flash batches
- Claude distills them into:
  - Conversation archetypes (likely 4-6 distinct types)
  - Recurring objection/response pairs (likely 10-15)
  - Qualification patterns per claim type
  - Few-shot examples from real calls (for use in AI agent prompts)
- This is where Claude's reasoning quality matters

**Step 6: Generate deliverables**
- Scripts, qualification criteria, rating framework, nurture content
- Each grounded in real patterns from actual CW calls
- Few-shot examples embedded in prompts so AI agents sound authentic

### What Done Looks Like
- Claude can describe how a water damage intake call flows differently from a roof call
- Claude can identify which claim types close best and why
- Claude can explain what separates a $500k real claim from garbage
- Structured knowledge is saved in this vault so future agents inherit it without re-ingesting
- Extracted patterns and archetypes stored as permanent reference

### Dependencies
- Access to all 788 completed contracts in GHL (via GHL MCP)
- Access to call recordings under each customer
- Gemini Flash API access for batch processing
- Whisper or Groq for transcription

---

## Deliverable 2: Intake Scripts

### What Jo Said
"Give us scripts of intake for denied claims and for new or underpaid claims."

### What This Actually Means
Jo needs two intake scripts, not nine. The claim status drives the conversation -- a denied claim customer is in a completely different emotional state than someone with a new claim. The claim type (water, fire, roof, misc) adds specific context within each script, but doesn't change the fundamental conversation structure.

**Script A: Denied Claim Intake**
For customers whose insurance company has already denied their claim. These customers are frustrated, skeptical, and often desperate. The conversation needs to:
- Acknowledge their frustration without being sycophantic
- Quickly assess if the denial is worth fighting (not all are)
- Collect specific information about the denial (reason, timeline, what they've tried)
- Explain what CW can do that's different from what they've already tried
- Handle objections specific to denied claims ("I already tried fighting it", "my lawyer said it's hopeless", "how is a public adjuster different?")
- Adapt qualification and red flags based on claim type (water denial has different patterns than roof denial)

**Script B: New or Underpaid Claim Intake**
For customers with a fresh claim or one where insurance paid too little. These customers are anxious, confused, or angry about being shortchanged. The conversation needs to:
- Assess the gap between what they got and what the damage is actually worth
- Qualify whether the gap is large enough to justify CW's involvement
- Collect damage details and insurance response information
- Explain CW's value proposition (we fight for the difference)
- Handle objections specific to new/underpaid ("my insurance company said this is all they'll pay", "how much do you charge?", "I already have a contractor estimate")
- Adapt details based on claim type (water damage underpayment looks different than fire)

Each script includes **claim-type-specific sections** so the rep (or AI) can pivot based on whether it's water, fire, roof, or misc. But the core flow is the same -- the status drives the script, the type adds context.

### What Done Looks Like
- 2 complete scripts that Jo can read and say "this sounds like how my best rep talks"
- Each script has claim-type-specific branches (not separate scripts, just sections that adapt)
- Scripts include real objection/response pairs extracted from actual CW calls (few-shot examples)
- Scripts are specific enough to be loaded directly into an AI voice agent
- Jo reviews, provides feedback, iterate

### Dependencies
- Deliverable 1 (knowledge base) must be complete
- Jo's review cycle -- he needs to read each script and approve or request changes

---

## Deliverable 3: Qualification Criteria and Red Flags

### What Jo Said
"We had customers come in and say my claim is worth $500k. And then back office worked for 15 hours, which is money to me, at $50, that's a lot of cash. Just to realize the claim is garbage."

### What This Actually Means
From 788 completed contracts and their outcomes, identify what patterns predict a claim's actual value and viability. This directly saves money by preventing the back office from wasting hours on bad claims.

What Claude needs to identify:

1. **Early warning signals** -- What does a customer say during intake that correlates with a garbage claim? Phrases, amounts, timelines, situations
2. **Claim value predictors** -- What factors predict whether a claim is worth $100k or $10k? Description of damage, time since loss, insurance company, policy type
3. **Disqualification criteria** -- Hard rules per claim type: if X is true, don't take it
4. **Soft warnings** -- Yellow flags: inflated damage, multiple prior adjusters, insurance already made final offer

### What Done Looks Like
- Clear criteria per claim type: "Here's what makes a water damage claim worth pursuing vs. garbage, and how to tell in the first 5 minutes"
- Criteria are specific and testable, not vague
- These feed directly into the rating system and the intake scripts

### Dependencies
- Deliverable 1 (knowledge base)
- Outcome data on which contracts resulted in high payouts vs. low/no payouts (if available in GHL or Airtable)

---

## Deliverable 4: Rating System

### What Jo Said
"AI would help us put together a rating for the claim, a rating for the lead, a rating for the call, the dollar amount, and give us a good description of what we need to do to get this claim to become successful."

### What This Actually Means
Every customer interaction produces a structured assessment with four components:

**Lead Rating (1-10)** -- Is this person worth pursuing? Policyholder? Legitimate claim? Ready to sign or shopping around?

**Call Rating (1-10)** -- Was this call productive? Did we get the info we needed? Red flags? Follow-up needed?

**Claim Rating (1-10)** -- Is this claim viable? Estimated value, recovery likelihood, complexity, red flags

**Dollar Amount Estimate** -- Range, not a single number. E.g., "$45k-$80k based on described water damage to first floor." Compared against insurance payment if underpaid.

**Action Summary** -- Specific next step: "Send contract immediately", "Follow up in 2 days with water damage nurture content", "Disqualify -- claim too old", "Escalate to senior rep"

### What Done Looks Like
- Rating framework with clear criteria for each score level
- Can be applied by AI automatically after every call
- Action summary specific enough that anyone reading it knows what to do next
- Ratings stored in GHL custom fields

### Dependencies
- Deliverable 1 (knowledge base)
- Deliverable 3 (qualification criteria)
- GHL custom fields for storing ratings

---

## Deliverable 5: Claim Success Playbooks

### What Jo Said
"Give us a good description of what we need to do to get this claim to become successful."

### What This Actually Means
For every claim that passes qualification, AI produces a playbook for the back office:

1. **What data do we have and what's missing?** -- Pictures, estimates, denial letter, coverage letter
2. **What will the insurance company argue?** -- Pre-existing damage, wear and tear, policy exclusions
3. **What's our negotiation position?** -- What are we asking for, what evidence supports it
4. **Recommended path** -- Direct negotiation, attorney, re-inspection, state complaint
5. **Timeline estimate** -- How long this type of claim typically takes

### What Done Looks Like
- Per claim type template that AI fills in with customer-specific details
- Back office reads it and knows exactly what to do without starting from scratch

### Dependencies
- Deliverable 1, Deliverable 3
- Back office process knowledge

---

## Deliverable 6: Operational Improvement Recommendations

### What Jo Said
"Is there any way to also ask Claude to give us other ideas how to improve operations based on the data it sees? I'm putting this on you."

### What This Actually Means
Ongoing responsibility. After ingesting call data, produce a "State of Operations" report covering: bottlenecks, wasted effort patterns, missed opportunities, script gaps, process inefficiencies, and team performance patterns.

### What Done Looks Like
- 5-10 specific, actionable recommendations with evidence from the data
- Each includes: problem, how we found it, impact, potential fix
- Recurring output as new data comes in

### Dependencies
- Deliverable 1 (knowledge base)

---

## Deliverable 7: Personalized Nurture Content

### What Jo Said
"If you're a water customer, I'm sending you basic information. But I would want Claude to send: hey, you have a water damage, here's some context."

### What This Actually Means
Replace generic GHL follow-up sequences with claim-type-specific nurture content:

1. **Educational content** -- Claim-type-specific information that positions CW as the expert
2. **Do/don't guidance** -- Specific to the claim type
3. **Social proof** -- Relevant reviews and success stories
4. **Urgency triggers** -- Deadlines, statutes of limitation, policy expiration
5. **Re-engagement messaging** -- Different approaches for ghosted, thinking, or lost leads

### What Done Looks Like
- 4-6 nurture messages per claim type
- Ready to load into GHL workflow automations
- Jo approves tone and content before going live

### Dependencies
- Deliverable 1, existing GHL workflows reviewed

---

## Priority Order

1. **Knowledge Base** -- everything else depends on this
2. **Intake Scripts** (2 scripts with claim-type branches) -- Jo's primary ask
3. **Qualification Criteria / Red Flags** -- directly saves money
4. **Rating System** -- applies qualification criteria structurally
5. **Operational Recommendations** -- quick win after data analysis
6. **Nurture Content** -- high impact, not blocking anything
7. **Claim Success Playbooks** -- back office value, can come later

---

## What's NOT in This Plan (Separate Projects)

Implementation projects that USE these deliverables but are separate builds:

- Intake AI Voice Bot, Live Call Listener, Call Summary Workflow Fix
- AI Customer Service Rep, Contract Automation, Slack Bot Integration
- RingCentral Data Extraction, Image Analysis with Gemini

These are documented in `02-Projects/` individually.
