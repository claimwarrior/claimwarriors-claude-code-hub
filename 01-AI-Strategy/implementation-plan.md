# Implementation Plan -- What Jo Is Waiting For

This document describes everything Joseph expects to come out of the AI initiative, organized as concrete deliverables with enough detail that you can start mapping implementation in your head. No code specs here -- just what needs to exist, what it needs to do, and what "done" looks like.

---

## Deliverable 1: The Knowledge Base (Foundation for Everything Else)

### What Jo Said
"Teach Claude what this business is. Go to payments, completed contracts, find every customer, listen to all the phone calls. Separate the data into water, roof, fire, miscellaneous. Once we have that understanding, then we can build everything else."

### What This Actually Means
Claude needs to ingest every completed contract (788+) and their associated call recordings from Go High Level. Not just skim them -- actually learn:

- What does a typical water damage intake call sound like?
- What does a denied claim customer say vs. a new claim customer?
- What questions do successful reps ask that lead to signed contracts?
- What are the common objections per claim type?
- What information do reps collect, and in what order?
- When do deals fall apart, and why?
- What language do customers use when describing their situation?

The output isn't a database -- it's Claude having internalized enough context that when you ask it "write me a denied water damage intake script," it produces something that sounds like it came from someone who's worked at Claim Warriors for a year.

### What Done Looks Like
- Claude can accurately describe the difference between how a water damage intake call flows vs. a roof damage call
- Claude can identify which claim types have the highest close rate and why
- Claude can explain what makes a claim worth $500k vs. $50k based on patterns it learned
- The structured knowledge is saved in this vault so future agents inherit it without re-ingesting

### Dependencies
- Access to all 788 completed contracts in GHL (via GHL MCP)
- Access to call recordings under each customer
- A transcription solution better than GHL's built-in one (Whisper or similar)
- A chunking strategy because you can't feed 788 contracts into one context window

---

## Deliverable 2: Intake Scripts (9 Combinations)

### What Jo Said
"Give us scripts of intake for denied claims and for new or underpaid claims." And separately: "Once we have the knowledge base, then we say build me this script, build me this script, build me this script."

### What This Actually Means
Jo needs a complete intake script for every combination of claim type and claim status. Each script is what the AI intake bot (or a human rep) follows when talking to a customer for the first time.

The matrix:

| | Water | Roof | Fire | Misc |
|---|---|---|---|---|
| **Denied** | Script needed | Script needed | Script needed | Script needed |
| **Underpaid** | Script needed | Script needed | Script needed | Script needed |
| **New** | Script needed | Script needed | Script needed | Script needed |

Each script needs to cover:

1. **Opening** -- How to greet the customer. Tone varies: a denied claim customer is frustrated and skeptical ("my insurance screwed me"), a new claim customer is anxious and confused ("I just had a flood, what do I do?"), an underpaid customer is angry ("they only gave me $10k on a $100k claim")
2. **Qualification questions** -- The specific questions to determine if this claim is worth pursuing. These differ by type: a water damage claim has different red flags than a roof claim. The questions should be ordered so the most disqualifying ones come first (don't waste 20 minutes before finding out the claim is garbage)
3. **Information collection** -- What data to gather and in what order: customer name, address, insurance company, claim number, type of loss, date of loss, estimated damage, amount paid, policy details. This maps directly to GHL custom fields
4. **Objection handling** -- Responses to common pushback per scenario. "How much do you charge?" "Why should I trust you?" "My insurance company said they'd handle it." "I already have a public adjuster." These are different per claim type and status
5. **Transition to contract** -- How to move from qualification to "let's get you signed up." The trigger point, the language, the urgency framing
6. **Disqualification path** -- How to gracefully end the call if the claim isn't worth pursuing. What to say, whether to refer elsewhere, how to leave the door open

### What Done Looks Like
- 9 complete scripts (or 12 if misc is split further) that Jo can read, review, and say "this sounds like how my best rep talks"
- Scripts are specific enough to be loaded directly into an AI voice agent as conversation instructions
- Scripts reference real patterns from actual CW calls, not generic sales language
- Jo provides feedback, scripts get iterated

### Dependencies
- Deliverable 1 (knowledge base) must be complete -- scripts are generated FROM this data
- Jo's review cycle -- she needs to read each script and approve or request changes

---

## Deliverable 3: Qualification Criteria and Red Flags

### What Jo Said
"We had customers come in and say my claim is worth $500k. And then back office worked for 15 hours, which is money to me, at $50, that's a lot of cash. Just to realize the claim is garbage."

### What This Actually Means
From 788 completed contracts and their outcomes, Claude needs to learn what patterns predict a claim's actual value and viability. This is the most important analytical output -- it directly saves money by preventing the back office from wasting hours on bad claims.

What Claude needs to identify:

1. **Early warning signals** -- What does a customer say during intake that correlates with the claim being garbage? Are there phrases, claim amounts, timelines, or situations that experienced reps recognize as red flags?
2. **Claim value predictors** -- What factors during the intake call predict whether a claim is actually worth $100k or $10k? Customer's description of damage? How long ago the loss happened? Type of insurance company? Policy type?
3. **Disqualification criteria** -- Hard rules: if X is true, don't take the claim. What are these for each claim type? Maybe: claim is older than X years, damage is below $X threshold, customer already has a PA, etc.
4. **Soft warnings** -- Not disqualifiers but yellow flags: customer seems to be inflating damage, multiple adjusters have already looked at it, insurance company already made a final offer, etc.

### What Done Looks Like
- A clear document per claim type that says: "Here's what makes a water damage claim worth pursuing, here's what makes it garbage, and here's how to tell the difference in the first 5 minutes of the call"
- Criteria are specific and testable -- not "the claim should be viable" but "if the date of loss is more than 3 years ago AND the customer has already received a final settlement, this is likely not worth pursuing"
- These criteria feed directly into the rating system (Deliverable 4) and the intake scripts (Deliverable 2)

### Dependencies
- Deliverable 1 (knowledge base)
- Ideally: outcome data on which completed contracts resulted in high payouts vs. low/no payouts. If that data exists in GHL or Airtable, it massively improves the analysis

---

## Deliverable 4: Rating System

### What Jo Said
"AI would help us put together a rating for the claim, a rating for the lead, a rating for the call, the dollar amount, and give us a good description of what we need to do to get this claim to become successful."

### What This Actually Means
Every customer interaction should produce a structured assessment. Not just "this lead is good" -- a multi-dimensional rating that tells the team exactly where this claim stands and what to do next.

The rating system has four components:

**Lead Rating** -- How valuable is this person as a potential customer?
- Are they the policyholder?
- Do they have a legitimate claim?
- Are they ready to sign or just shopping around?
- How responsive are they?
- Score: 1-10 with clear criteria for each score range

**Call Rating** -- How productive was this specific call?
- Did we get all the information we needed?
- Did the customer engage or resist?
- Were there red flags in what they said?
- Is follow-up needed, and for what?
- Score: 1-10 with clear criteria

**Claim Rating** -- How viable is this claim?
- Estimated true value based on what we know
- Likelihood of successful recovery
- Complexity level (straightforward vs. will need attorney)
- Red flags from qualification criteria (Deliverable 3)
- Score: 1-10 with clear criteria

**Dollar Amount Estimate** -- What's this claim likely worth?
- Based on claim type, damage description, customer statements, and any photos
- Range, not a single number (e.g., "$45k-$80k based on described water damage to first floor")
- Compared against what insurance already paid (if underpaid)

**Action Summary** -- What needs to happen next?
- "Send contract immediately -- high-value, ready to sign"
- "Follow up in 2 days -- interested but wants to think about it. Send water damage nurture content"
- "Disqualify -- claim is too old, damage is minimal, not worth back office time"
- "Escalate to senior rep -- complex claim, potential attorney involvement"

### What Done Looks Like
- A clear rating framework document that defines every score level for every dimension
- Rating can be applied by AI automatically after every call (or during the call)
- The action summary is specific enough that whoever reads it knows exactly what to do next without re-listening to the call
- Ratings are stored in GHL (custom fields or notes) so the team can sort and prioritize

### Dependencies
- Deliverable 1 (knowledge base) -- ratings need to be calibrated against real outcomes
- Deliverable 3 (qualification criteria) -- feeds directly into the claim rating component
- GHL custom fields need to exist for storing ratings

---

## Deliverable 5: Claim Success Playbooks

### What Jo Said
"Give us a good description of what we need to do to get this claim to become successful."

### What This Actually Means
This goes beyond the rating. For every claim that passes qualification, the AI should produce a playbook -- a specific set of steps for the back office to follow to maximize the chance of a successful settlement.

Each playbook covers:

1. **What data do we have and what's missing?** -- Pictures? Estimates? Denial letter? Coverage letter? What do we still need from the customer?
2. **What's the insurance company likely to argue?** -- Based on claim type and carrier patterns, what objections will the carrier raise? Pre-existing damage? Wear and tear? Policy exclusions?
3. **What's our negotiation position?** -- Based on the damage type and value, what are we asking for? What evidence supports it?
4. **What's the recommended path?** -- Direct negotiation? Bring in attorney? Request re-inspection? File complaint with state insurance board?
5. **Timeline estimate** -- How long does this type of claim typically take to resolve?

### What Done Looks Like
- Per claim type, a template playbook that the AI fills in with specific details for each customer
- After intake, AI generates: "This is a denied water damage claim estimated at $85k. Customer has photos and a denial letter. Insurance company is State Farm. Recommended path: request re-inspection, prepare supplemental estimate focusing on hidden moisture damage. Typical resolution: 60-90 days. Missing: independent moisture reading report -- ask customer to schedule."
- Back office team reads this and knows exactly what to do without starting from scratch

### Dependencies
- Deliverable 1 (knowledge base)
- Deliverable 3 (qualification criteria)
- Back office process knowledge -- may need to interview the team or pull from existing documentation

---

## Deliverable 6: Operational Improvement Recommendations

### What Jo Said
"Is there any way to also ask Claude to give us other ideas how to improve operations based on the data it sees? I'm putting this on you -- come to me with, hey, I'm seeing this opportunity here, do you want to implement this or not?"

### What This Actually Means
This is an ongoing responsibility, not a one-time deliverable. Once Claude has ingested all the call data and understands the business, it should produce a report of observed patterns and improvement opportunities.

Things Claude should look for:

1. **Bottlenecks** -- Where are deals getting stuck? Is there a point in the process where customers consistently drop off? Is there a claim type that takes disproportionately long to resolve?
2. **Wasted effort patterns** -- Beyond just garbage claims, are reps spending time on activities that don't lead to conversions? Are certain questions being asked repeatedly that could be pre-answered?
3. **Missed opportunities** -- Are there things customers say that indicate upsell potential? Are there claim types with high win rates that CW isn't actively pursuing?
4. **Script gaps** -- Are reps handling certain objections poorly? Are there common customer questions that reps don't have good answers for?
5. **Process inefficiencies** -- Are there manual steps that could be automated? Are there data entry patterns that cause errors downstream?
6. **Team performance patterns** -- Without naming individuals, are there patterns in what separates high-performing calls from low-performing ones?

### What Done Looks Like
- A "State of Operations" report generated after the knowledge base ingestion
- 5-10 specific, actionable recommendations with evidence from the data
- Each recommendation includes: what the problem is, how we found it, what the impact is, and what the fix could be
- This becomes a recurring output -- every time significant new data is ingested, Claude produces updated observations

### Dependencies
- Deliverable 1 (knowledge base) -- can't make recommendations without data
- Access to outcome data (which claims resulted in payouts, which didn't)

---

## Deliverable 7: Personalized Nurture Content

### What Jo Said
"If you're a water customer, I'm sending you basic information. But I would want Claude to send: hey, you have a water damage, here's some context. How to make sure you don't get screwed by the insurance company for water damage. Make sure you stop talking to them. Here's our reviews."

### What This Actually Means
The current follow-up sequences in GHL are generic -- every customer gets the same content regardless of their claim type. Jo wants claim-type-specific nurture sequences that feel relevant and build trust.

For each claim type (water, fire, roof, denied, underpaid, new), Claude should generate:

1. **Educational content** -- "5 things water damage claimants don't know about their policy." "Why your insurance company's first offer on a roof claim is almost always too low." Content that positions CW as the expert and makes the customer feel like they need help
2. **Do/don't guidance** -- "Don't talk to your insurance company without representation." "Don't sign anything they send you." "Do document everything with photos." Specific to the claim type
3. **Social proof** -- Which reviews, testimonials, or case studies are most relevant for this claim type? A water damage customer wants to hear about water damage wins
4. **Urgency triggers** -- Deadlines, statute of limitations, policy expiration -- whatever creates legitimate urgency for this specific claim type
5. **Re-engagement messaging** -- For customers who went cold. Different for "they ghosted after first call" vs. "they said they'd think about it" vs. "they went with someone else"

These get loaded into GHL workflows as claim-type-specific drip sequences.

### What Done Looks Like
- 4-6 nurture messages per claim type (potentially more for denied claims since those customers need more convincing)
- Messages are written in a tone consistent with how CW actually talks to customers
- Content is factually accurate for each claim type (water damage has different legal/policy nuances than roof damage)
- Messages are ready to be loaded into GHL workflow automations
- Current generic workflows get replaced with these targeted ones

### Dependencies
- Deliverable 1 (knowledge base)
- Existing GHL workflows need to be reviewed to understand current automation structure
- Jo's approval on tone and content before going live

---

## Priority Order

Based on what Jo emphasized and what blocks what:

1. **Knowledge Base** -- everything else depends on this
2. **Intake Scripts** -- Jo specifically said "by Thursday give me scripts"
3. **Qualification Criteria / Red Flags** -- directly saves money (stops garbage claims)
4. **Rating System** -- applies the qualification criteria in a structured way
5. **Operational Recommendations** -- quick win once the data is analyzed
6. **Nurture Content** -- high impact but not blocking anything else
7. **Claim Success Playbooks** -- most valuable for back office but can come after front office is sorted

---

## What's NOT in This Plan (Separate Projects)

These are things Jo mentioned but they're implementation projects, not knowledge base outputs:

- **Intake AI Voice Bot** -- uses the scripts but is a separate build
- **Live Call Listener** -- technical project, depends on GHL capabilities
- **Call Summary Workflow Fix** -- GHL automation work
- **AI Customer Service Rep** -- separate bot build
- **Contract Automation** -- future enhancement
- **Slack Bot Integration** -- depends on Slack being set up
- **RingCentral Data Extraction** -- separate integration work
- **Image Analysis with Gemini** -- back office tool, separate build

These are documented in `02-Projects/` individually. This plan focuses on what Claude needs to LEARN and PRODUCE from the call data -- the intellectual output that feeds everything else.
