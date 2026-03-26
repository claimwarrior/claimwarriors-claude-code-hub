# Tools & Platforms

## Core Stack

### Go High Level (GHL)
- **Role**: CRM, phone system, sales pipeline, marketing automation, contract sending
- **Used by**: Front office (sales reps, customer support)
- **Key features used**: IVR/call routing, custom fields, workflows (automations), payment/contracts, call recording
- **Phone numbers**: Purchased directly through GHL (uses Twilio under the hood)
- **MCP available**: Yes -- GHL MCP for reading/writing contacts, opportunities, conversations
- **Pain points**: Built-in transcriber is low quality. Call summaries workflow creates duplicates

### Airtable
- **Role**: Data bridge between GHL and Claim Warriors software
- **Used by**: Operations, data sync
- **Key features used**: Tables for claims, customers, pipeline tracking
- **MCP available**: Yes -- Airtable MCP for reading/writing records
- **Data flow**: GHL -> Airtable -> Claim Warriors (Supabase)

### Claim Warriors Software (Supabase)
- **Role**: Core business application for claims management
- **Built with**: React, TypeScript, Supabase (PostgreSQL)
- **Used by**: Back office, management
- **Key features**: Claim tracking, comments, file uploads, team assignments, status tracking
- **MCP available**: Yes -- Supabase MCP for direct DB access
- **Note**: This is the custom software Ben built. The VP R&D owns the codebase

### RingCentral
- **Role**: Phone system for back office / carrier communications
- **Used by**: Back office team for negotiating with insurance carriers
- **Key features**: Call recording, built-in AI summarization
- **MCP available**: No (as of March 2026)
- **Opportunity**: Extract AI summaries and feed into Claim Warriors software

### Outlook
- **Role**: Email communication with carriers, customers, attorneys
- **Used by**: Entire team
- **MCP available**: Yes -- Outlook MCP for email read/write
- **Opportunity**: AI-assisted email drafting for carrier negotiations

### Slack
- **Role**: Internal team communication (being set up)
- **Used by**: Will be used by entire team + AI bots
- **Key plans**: Dedicated channels for AI projects, bot-driven task automation, ticket creation from AI customer service rep
- **Opportunity**: AI bots that execute tasks, route work, and update team members

### Fireflies.ai
- **Role**: Meeting recording and transcription
- **Used by**: Ben, Jo, for external and internal calls
- **MCP available**: Yes -- Fireflies MCP for transcript retrieval, search, and sharing
- **Data**: All Ben/Jo strategy calls are recorded here

## AI Tools

### Claude (Anthropic)
- **Role**: Primary AI engine for all AI initiatives
- **Access**: Anthropic subscription (not API -- cost savings)
- **Implementation**: Claude Code + Claude Claw for persistent conversational agent
- **Why Claude**: Best at script writing, complex reasoning, tool use, and code generation

### Gemini (Google)
- **Role**: Image analysis (damage photos, estimates)
- **Why Gemini**: Cheap, excellent at visual analysis, multimodal
- **Use case**: Analyze property damage pictures to validate claim values during intake

### Whisper (OpenAI)
- **Role**: Speech-to-text transcription
- **Use case**: Transcribe GHL call recordings (replacing GHL's poor built-in transcriber)
- **Note**: May use as part of data ingestion pipeline for teaching Claude the business

## Deployment

### Claude Claw
- Persistent Claude Code wrapper with conversational layer (Telegram/Discord)
- Runs on a dedicated machine (currently Ben's computer, needs permanent home)
- Chosen over OpenClaw for: security (no third-party skills marketplace), cost (uses Anthropic subscription), and integration (same machine as development)
- See [[../05-Decisions/2026-03-24-claude-claw-over-openclaw]]

## Source

Information extracted from:
- Ben/Jo call, March 24 2026 -- "AI Next Steps"
- Ben/Jo call, March 25 2026 -- "More Details About AI Implementation"
