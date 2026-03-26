# Integration: Go High Level MCP

**Status**: Available -- needs configuration for CW-specific use cases
**MCP Server**: `Ghl-mcp-claim-warrior`

## What It Connects To

Go High Level -- the CRM, phone system, and sales pipeline for Claim Warriors.

## Available Capabilities

Based on the configured MCP tools:

### Contacts
- `contacts_get-contacts` -- Search/list contacts
- `contacts_get-contact` -- Get single contact details
- `contacts_create-contact` -- Create new contact
- `contacts_update-contact` -- Update contact fields
- `contacts_upsert-contact` -- Create or update contact
- `contacts_add-tags` / `contacts_remove-tags` -- Manage contact tags
- `contacts_get-all-tasks` -- Get tasks for a contact

### Conversations
- `conversations_search-conversation` -- Find conversations
- `conversations_get-messages` -- Read messages in a conversation
- `conversations_send-a-new-message` -- Send message to contact

### Opportunities (Pipeline)
- `opportunities_search-opportunity` -- Search pipeline opportunities
- `opportunities_get-opportunity` -- Get opportunity details
- `opportunities_update-opportunity` -- Update opportunity
- `opportunities_get-pipelines` -- List pipelines and stages

### Calendars
- `calendars_get-calendar-events` -- Get calendar events
- `calendars_get-appointment-notes` -- Get notes from appointments

### Payments
- `payments_list-transactions` -- List transactions
- `payments_get-order-by-id` -- Get order details

### Social Media
- Social media posting tools available (create, edit, get posts)

### Other
- `locations_get-location` -- Get location/account info
- `locations_get-custom-fields` -- List custom fields (important for intake AI)
- `emails_create-template` / `emails_fetch-template` -- Email templates
- `blogs_*` -- Blog management tools

## Key Use Cases for CW

1. **Intake AI Bot** -- `contacts_update-contact` to fill custom fields in real-time during calls
2. **Call Summary Push** -- `contacts_update-contact` to update summary fields
3. **Knowledge Base Ingestion** -- `contacts_get-contacts` + `conversations_get-messages` to pull customer data and call history
4. **Lead Pre-qualification** -- `opportunities_update-opportunity` to update pipeline stage based on AI rating
5. **Custom Fields Discovery** -- `locations_get-custom-fields` to understand what fields exist and how they map to intake questions

## Configuration Notes

- Phone numbers are purchased through GHL (Twilio under the hood)
- GHL's built-in transcriber is poor quality -- use Whisper for re-transcription
- Workflows 851/852/853 handle call summaries (currently broken -- see [[../02-Projects/call-summary-workflow]])

## Source

MCP tools discovered via tool search. Use cases from Ben/Jo calls March 24-25 2026.
