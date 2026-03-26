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

## Why This Matters for AI

Each claim type + status combination needs:
1. A specific **intake script** (how the AI talks to the customer)
2. A specific **nurture sequence** (follow-up messaging if they don't sign)
3. Different **qualification criteria** (what makes it worth pursuing)
4. Different **back office workflow** (what the team needs to do)

The goal is for Claude to learn from 788+ completed contracts and generate scripts per combination:
- Denied + Water
- Denied + Roof
- Denied + Fire
- Underpaid + Water
- Underpaid + Roof
- Underpaid + Fire
- New + Water
- New + Roof
- New + Fire

## Source

Information extracted from:
- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
