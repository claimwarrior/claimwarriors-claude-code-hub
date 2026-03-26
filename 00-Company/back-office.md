# Back Office -- Claims Processing & Operations

## What the Back Office Does

Once a customer signs a contract, the claim moves to the back office. This team does the heavy lifting -- inspections, estimates, negotiations with insurance carriers, and final settlement.

## Current Workflow

1. Claim data arrives from front office (GHL -> Airtable -> Claim Warriors software)
2. Back office team reviews the claim
3. Adjusters inspect the property and document damages
4. Team writes estimates using tools like Xactimate
5. Submit claim/estimate to insurance carrier
6. Negotiate with carrier (phone calls via RingCentral, emails via Outlook)
7. Resolve the claim -- settlement, supplemental payment, or escalation to attorney

## Key Pain Points

### Wasted Time on Bad Claims
- Biggest cost center: back office works 15+ hours on a claim at ~$50/hr, only to discover it's garbage
- No early-warning system to flag low-value or fraudulent claims before work begins
- Example: customer says claim is worth $500k, back office discovers it's worth nothing after extensive work

### Manual Estimate Review
- Adjusters manually compare their estimates against what the insurance company paid
- No AI assistance to highlight what was missed in the carrier's estimate
- No automated comparison between Claim Warriors' assessment and the carrier's assessment

### Communication Bottlenecks
- Consultants advise on routing (inspection, attorney, direct negotiation) via calls
- These routing decisions could be partially automated
- Internal team communication is manual -- could be handled by Slack bots

### Carrier Communication
- Negotiation emails are written manually
- RingCentral calls with carriers have AI summarization (built-in) but that data doesn't feed back into Claim Warriors software
- No AI-assisted negotiation based on claim data, pictures, and carrier responses

## AI Opportunities (Back Office)

1. **Claim Verifier** -- AI reviews pictures, estimates, and customer data to rate claim viability before back office starts work
2. **Estimate Gap Analysis** -- AI compares Claim Warriors' estimate vs. carrier's estimate, highlights what was missed
3. **Negotiation Email Generator** -- AI drafts carrier negotiation emails using pictures, call data, estimates, and carrier responses
4. **RingCentral Data Extraction** -- Pull AI summaries from carrier calls into Claim Warriors software
5. **Internal Task Automation** -- Slack bots that route and execute tasks between team members

## Source

Information extracted from:
- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
