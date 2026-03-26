# Front Office -- Sales & Customer Support

## Sales Process

### Current Flow
1. Lead comes in (inbound call, marketing, referral)
2. Sales rep picks up via Go High Level phone system
3. Rep asks qualifying questions and fills out custom fields in GHL manually during the call
4. Rep sends contract during or after the call (currently manual)
5. After call: ChatGPT generates a summary via GHL automation (workflow 851/852/853)
6. If customer signs, data flows from GHL to Airtable to Claim Warriors software (Supabase)

### Step 2: Initial Intake / Pre-Qualification

Owner: AI or Low-Level Sales Rep

This is the first structured interaction with a new lead. The goal is to collect baseline information and route the customer to the right person based on claim stage.

**Data collected during pre-qualification:**
- Customer first name, last name, contact info (phone, email)
- Address
- Homeowner vs. Renter (hard disqualifier -- renters typically can't file property insurance claims)
- Type of damage (water, fire, roof, misc)
- Date of loss
- Claim stage (denied, new, underpaid)

**After pre-qualification, route by claim stage:**

| Path | Owner | Pay | Goal |
|------|-------|-----|------|
| Denied claim | Low-Level Rep | $10-$12/hr | Sign at 15%-20% |
| New / Underpaid claim | Sam / Account Manager | $25/hr | Sign claim + sales valuation |

The denied path is more transactional -- get the signature at a set rate. The new/underpaid path requires actual sales skill -- the rep needs to assess what the claim is worth and build a case for why CW should take it on, which is why it goes to a higher-paid Account Manager.

### Additional Fields Collected During Full Sales Call
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
- No homeowner vs. renter check -- renters slip through and waste time

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
