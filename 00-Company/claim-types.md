# Claim Types

## By Type of Loss

### Water Damage
- Most common claim type
- Includes pipe bursts, flooding, storm water intrusion, mold from water
- Insurance companies frequently underpay water claims
- Requires specific documentation of affected areas and remediation costs

### Roof Damage
- Wind, hail, storm damage to roofing
- Often requires inspection to verify extent of damage
- Insurance companies may claim pre-existing wear vs. storm damage
- Photo evidence is critical

### Fire Damage
- Structure fires, smoke damage, related water damage from firefighting
- Often high-value claims
- Requires detailed documentation of all affected areas and contents

### Miscellaneous
- Catch-all for claims that don't fit neatly into water/roof/fire
- May include vandalism, theft, or other covered perils

## By Claim Status

### New Claims
- Fresh claims where the customer hasn't yet filed or just filed with their insurance
- Intake process focuses on documenting damage early
- Goal: get ahead of the insurance company's assessment

### Denied Claims
- Insurance company has denied the claim entirely
- Customer needs help reopening or disputing the denial
- Requires different sales approach -- customer is frustrated and skeptical
- Specific scripts needed for denied claim intake

### Underpaid Claims
- Insurance company paid something, but significantly less than the actual damage
- Most common scenario
- Sales pitch: "Your claim is worth $X but they only paid you $Y -- we'll fight for the difference"
- Requires showing the gap between payment and actual value

## How This Maps to AI Deliverables

Claim types serve as the **knowledge layer** -- they add context and specificity to everything the AI produces. But they don't each get their own script.

**Scripts are driven by claim STATUS** (denied vs. new/underpaid):
- 2 intake scripts, each with claim-type-specific branches inside
- The customer's emotional state and objection patterns differ by status, not by type
- See [[../04-Scripts/_index]] for script structure

**Claim types add context WITHIN each script:**
- Type-specific qualification questions (water has different red flags than roof)
- Type-specific objection handling (denial reasons differ by claim type)
- Type-specific nurture content (water customers get water-specific follow-up)
- Type-specific playbooks for back office

**Claim types also drive:**
- Qualification criteria per type (what makes a water claim garbage vs. valuable)
- Nurture content per type (educational content, urgency triggers)
- Back office playbooks per type (negotiation approach, documentation needs)

## Source

Information extracted from:
- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
