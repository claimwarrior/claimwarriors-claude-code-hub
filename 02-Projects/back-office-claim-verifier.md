# Project: Back Office Claim Verifier

**Status**: Planned
**Priority**: High (Phase 3)
**Owner**: Ben
**Phase**: 3 (Back Office AI)

## What It Does

An AI system that analyzes claim data -- pictures, estimates, customer statements, and sales call information -- to rate claim viability before the back office invests hours of work. Also identifies what's missing from estimates and highlights discrepancies.

## Why It Matters

The single biggest waste at Claim Warriors: back office works 15+ hours at ~$50/hr on a claim, only to discover it's garbage. This verifier catches bad claims early and tells the team exactly what to focus on.

> "We had customers come in and say, hey, my claim is worth $500k. And then back office worked for 15 hours just to realize the claim is garbage." -- Jo

## Two Functions

### 1. Claim Rating (Pre-Work)
Before the back office starts, AI reviews all available data and produces:
- **Claim viability score** -- is this claim worth pursuing?
- **Estimated value range** -- based on damage type, photos, and customer statements
- **Red flags** -- inconsistencies between what customer said and what photos show
- **Recommendation** -- proceed, proceed with caution, or flag for review

### 2. Estimate Gap Analysis (During Work)
Once the team has written their estimate, AI compares it against:
- The insurance company's payment/assessment
- Industry standards for that type of damage
- Historical data from similar claims in the CW database

Output: a list of items that were missed, undervalued, or overlooked, with suggested negotiation points.

## Technical Approach

### Image Analysis
- **Gemini** for analyzing damage photos -- cheap, excellent at visual tasks
- Input: customer-uploaded photos of property damage
- Output: damage type identification, severity assessment, estimated repair scope

### Data Analysis
- **Claude** for comparing estimates, identifying gaps, reasoning about claim value
- Input: CW estimate, carrier estimate, call transcripts, customer data
- Output: gap analysis report, negotiation talking points

## Dependencies

- [ ] Knowledge base built (Phase 1) -- needs to understand claim types and valuation patterns
- [ ] Image upload workflow established (customers need to send photos during intake)
- [ ] Historical claim data accessible for comparison (Supabase MCP)
- [ ] Gemini API integrated for image analysis

## Open Questions

- At what point in the sales process do we ask for pictures? Currently not collected during intake
- How do we get Xactimate estimate data into a format AI can analyze?
- What threshold for the viability score triggers a "don't work this claim" flag?

## Source

- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation" (primary discussion)
- Ben/Jo call, March 24 2026 -- mentioned briefly
