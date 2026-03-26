# Project: Image Analysis (Gemini)

**Status**: Planned
**Priority**: Medium
**Owner**: Ben
**Phase**: 3 (Back Office AI) -- but could be introduced earlier in intake

## What It Does

Uses Google's Gemini AI to analyze property damage photographs submitted by customers. Validates whether the damage matches what the customer claims, estimates severity, and helps rate claim viability.

## Why It Matters

Customers sometimes overstate their damage. Currently, the only way to verify is for back office to spend hours reviewing the claim. With image analysis, AI can flag discrepancies during or immediately after the sales call.

> "Based on the pictures, AI would identify and confirm if the claim is worth that much." -- Jo

## How It Works

1. Customer submits photos (during intake call, via text, or through a form)
2. Photos are sent to Gemini API for analysis
3. Gemini identifies:
   - Type of damage (water, fire, wind, structural)
   - Severity (minor, moderate, severe)
   - Affected areas (roof, walls, floors, contents)
   - Consistency with customer's verbal description
4. Results feed into the [[back-office-claim-verifier]] for overall claim rating
5. Flagged discrepancies are noted for the sales team or back office

## Why Gemini (Not Claude)

- Gemini is specifically strong at visual/multimodal analysis
- Significantly cheaper than Claude for image processing
- API is straightforward to integrate
- Ben already has experience with Gemini API (GOOGLE_API_KEY configured)

> "We can use Gemini to analyze the picture. It's very good at it and it's cheap." -- Ben

## Dependencies

- [ ] Establish photo collection workflow (when/how do customers submit photos?)
- [ ] Gemini API integration (API key already available)
- [ ] Define output format that feeds into claim verifier
- [ ] Training data: examples of damage types and what they look like

## Open Questions

- When in the sales process do we ask for pictures? Currently not part of intake
- Can we accept photos via text message through GHL?
- What's the minimum photo quality needed for reliable analysis?
- Should we ask for specific angles/areas, or accept whatever the customer sends?

## Source

- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
