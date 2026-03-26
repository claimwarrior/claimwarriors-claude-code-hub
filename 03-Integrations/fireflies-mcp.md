# Integration: Fireflies MCP

**Status**: Active -- fully configured and working
**MCP Server**: `fireflies`

## What It Connects To

Fireflies.ai -- meeting recording and transcription service. All strategy calls between Ben and Jo are recorded here.

## Available Capabilities

- `fireflies_get_transcripts` -- Search meetings by date, keyword, participant
- `fireflies_get_transcript` -- Get full transcript for a specific meeting
- `fireflies_get_summary` -- Get AI-generated summary (keywords, action items, overview)
- `fireflies_get_active_meetings` -- Check for live meetings
- `fireflies_get_user` -- User account info
- `fireflies_get_user_contacts` -- Contact list
- `fireflies_get_usergroups` -- User groups
- `fireflies_search` -- Full-text search across transcripts
- `fireflies_share_meeting` / `fireflies_revoke_meeting_access` -- Sharing management
- `fireflies_move_meeting` -- Organize meetings into channels
- `fireflies_list_channels` / `fireflies_get_channel` -- Channel management

## Key Use Cases for CW

1. **Meeting Notes** -- Pull transcripts and summaries from Ben/Jo calls for vault documentation
2. **Knowledge Base Building** -- Extract business context, decisions, and action items from recorded calls
3. **Decision Tracking** -- Search past calls for when/why specific decisions were made

## Already Used For

- Extracted March 24 and March 25 2026 call transcripts to build this vault
- Will continue to be used for documenting future strategy calls

## Source

Active MCP integration. Used during vault creation March 25 2026.
