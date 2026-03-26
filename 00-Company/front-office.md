# Front Office -- Sales & Customer Support

## Sales Process

### Current Flow
1. Lead comes in (inbound call, marketing, referral)
2. Sales rep picks up via Go High Level phone system
3. Rep asks qualifying questions and fills out custom fields in GHL manually during the call
4. Rep sends contract during or after the call (currently manual)
5. After call: ChatGPT generates a summary via GHL automation (workflow 851/852/853)
6. If customer signs, data flows from GHL to Airtable to Claim Warriors software (Supabase)

### Custom Fields Collected During Sales Call
- Customer first name, last name, contact info
- Type of loss (water, fire, roof, misc)
- Claim status (denied, underpaid, new)
- Customer's estimated claim value (e.g., $100k)
- Amount already paid by insurance (e.g., $10k)
- Remaining amount (e.g., $90k)
- Personal property claims (separate from structure)
- Insurance company name

### Known Pain Points
- Reps fill fields manually -- slow, error-prone
- Contract sent manually -- sometimes during call, sometimes after, sometimes delayed
- Call summaries are broken -- workflow creates multiple duplicate summaries instead of updating one
- No pictures collected during sales (customer isn't asked for photos of damage)
- No AI pre-qualification -- garbage claims slip through to back office
- GHL's built-in transcriber is "garbage" -- too many errors to be useful
- Voicemail calls get billed by AI calling tools

### IVR / Call Routing
- GHL has an IVR automation that rings all available reps
- When all reps are busy, calls currently go unanswered or to voicemail
- Opportunity: AI intake agent picks up overflow calls

## Customer Support

### Current State
- Customers call in with status questions
- Reps look up claim info manually, relay updates
- No self-service or automated status updates
- Back office communication about claim progress is manual

### Desired State
- AI customer service rep handles routine inquiries
- Bot reads claim data from Claim Warriors software and GHL
- Summarizes status and gives meaningful updates to customers
- If additional info is needed, opens a ticket on Slack for back office
- Escalates complex issues to human reps

## Source

Information extracted from:
- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
