# Meeting Notes: Ben / Jo -- More Details About AI Implementation

**Date**: March 25, 2026
**Duration**: ~13 minutes
**Participants**: Ben (Benjamin EL KRIEFF), Jo (Digital Nomad / Speaker 1)
**Recording**: [Fireflies](https://app.fireflies.ai/view/01KMKAMQC90C3VESSPYP4AB29Q)

## Summary

Follow-up call to add detail on front office and back office AI separation. Jo provided specific examples of how AI should work in both departments, confirmed budget flexibility, and discussed additional integration points (RingCentral, Slack bots).

## Key Topics Discussed

### 1. Front Office vs. Back Office AI Separation

**Front Office AI** (Sales + Customer Support):
- Analyze calls and customer files early to estimate claim value
- Flag discrepancies between what customer claims and reality
- Save time by catching garbage claims before back office invests hours
- Ask customers for pictures during intake (not currently done)
- Use Gemini for image analysis -- "very good at it and it's cheap"

**Back Office AI** (Claims Processing):
- Verify claims by highlighting missing information in estimates
- Generate summaries to reduce manual review time
- Compare CW estimate vs. carrier estimate
- Rating system for leads, calls, and claims

### 2. Claim Rating System
- Every interaction should produce ratings:
  - Lead quality rating
  - Call quality rating
  - Claim viability rating
  - Dollar amount estimate
- Plus a description of what's needed to make the claim successful

### 3. Obsidian for Knowledge Management
- Ben introduced Obsidian as the knowledge base tool
- "Cabinet with drawers" metaphor -- organized files with a graph view showing connections
- Will be built step by step alongside AI development

### 4. AI Customer Service Rep
- Front office bot connected to GHL and Claim Warriors software
- Reads comments and data, summarizes for customers
- Opens Slack tickets when back office action is needed

### 5. RingCentral Integration
- RingCentral has built-in AI summarization for carrier calls
- Data currently siloed -- need to extract and push to CW software
- Separate from GHL (which handles customer-facing calls)

### 6. Internal Slack Bots
- Task automation between team members
- Example: consultant says "this goes to inspection, this goes to attorney" -- a bot could handle this routing
- Jo agreed to create Slack channels for AI projects

### 7. Budget Confirmation
- Jo explicitly said: "Don't think that you don't have a budget or support from me"
- Willing to spend on AI tools to move faster
- Prefers paying for tools over paying for Ben's time to build inferior alternatives

## Action Items

### Ben
- [ ] Build the foundational AI system with Obsidian knowledge base
- [ ] Prepare front office AI functions including AI customer service rep
- [ ] Explore RingCentral AI summary extraction
- [ ] Keep Thursday timeline for initial deliverables

### Jo
- [ ] Create Slack channels for AI projects
- [ ] Provide ongoing budget support for AI tools
- [ ] Notify team about AI implementation timeline

## Key Quotes

- "We had customers come in and say my claim is worth 500k. Back office worked 15 hours just to realize the claim is garbage." -- Jo
- "Don't think that you don't have a budget or support from me. If you gotta spend a hundred dollars worth of tokens, just let me know." -- Jo
- "We can use Gemini to analyze the picture. It's very good at it and it's cheap." -- Ben
- "It's not trivial. There's a lot of tools. It's very exciting." -- Ben

## Timeline

- Keep Thursday March 27 target
- Jo to be notified of any delays
- Slack channels to be set up by Jo
