# Backlog -- Future AI Projects

These projects were discussed but are not immediate priorities. They'll become relevant after Phases 1-3 are complete.

## Denied Claims Outreach Bot

**What**: AI-powered outreach to the ~796 customers who were sent contracts but didn't sign
**How**: Personalized text and call campaigns based on claim type. AI contacts them, re-engages, and tries to bring them back
**Why**: Large untapped pool of warm leads. Different approach needed per claim type
**When**: After intake AI and knowledge base are solid

## Email AI

**What**: AI that monitors the Outlook inbox, handles routine emails, and drafts carrier negotiation emails
**How**: Outlook MCP for email access. Claude for drafting. Human approval before sending important emails
**Why**: Team spends time on repetitive email communication. AI can handle routine responses and draft complex negotiations
**When**: After core front office AI is deployed

## Contract Automation

**What**: Auto-send contracts during sales calls when all required fields are filled
**How**: Once AI fills all GHL custom fields (via intake bot or live listener), automatically trigger contract creation and sending
**Why**: Eliminates manual contract sending. Faster close during the call
**When**: After AI field-filling is proven reliable. Requires high confidence in data accuracy

## Voice Cloning (Rio)

**What**: Clone the voice of a former sales rep named Rio for use in AI voice agents
**How**: Use Rio's recorded calls as training data for voice synthesis. Apply to intake bot and outreach bot
**Why**: Familiar voice for returning customers. Professional, proven sales voice
**When**: After intake bot is working with a default voice. This is an enhancement

## Internal Slack Bots

**What**: AI bots on Slack that automate task routing, claims triage, and team communication
**How**: Slack integration + Claude. Bots pick up tasks, route them to appropriate team members, and handle internal communication
**Why**: Currently Jo's consultants advise on routing (inspection, attorney, negotiation) via phone calls. Much of this could be automated
**Example**: Consultant tells Jo "this needs to go to inspection, this needs to go to attorney" -- a bot could do that analysis and routing
**When**: After Slack is set up and the team is using it daily

## Carrier Call Data Extraction

**What**: Pull AI-generated summaries from RingCentral carrier calls and feed them into Claim Warriors software
**How**: RingCentral has built-in AI summarization. Extract those summaries and push to Supabase as comments or notes on the claim
**Why**: Carrier call data currently stays siloed in RingCentral. Back office has to manually reference it
**When**: After core integrations are working. May require custom RingCentral API work (no MCP available as of March 2026)

## Source

All items from:
- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
