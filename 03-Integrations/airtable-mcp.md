# Integration: Airtable MCP

**Status**: Available
**MCP Server**: `airtable-claim-warrior`

## What It Connects To

Airtable -- the data bridge between Go High Level and the Claim Warriors software.

## Role in the Data Flow

```
GHL (Sales) -> Airtable (Bridge) -> Supabase (CW Software)
```

Airtable sits in the middle. When data changes in GHL (new contract signed, status update), it flows through Airtable and into the Claim Warriors software.

## Available Capabilities

- `list_bases` -- List available Airtable bases
- `list_tables` -- List tables in a base
- `describe_table` -- Get table schema and field info
- `list_records` / `search_records` / `get_record` -- Read data
- `create_record` / `update_records` / `delete_records` -- Write data
- `create_table` / `update_table` -- Schema management
- `create_field` / `update_field` -- Field management
- `list_comments` / `create_comment` -- Record comments
- `upload_attachment` -- File attachments

## Key Use Cases for CW

1. **Knowledge Base Ingestion** -- Pull all claim records to understand business data
2. **Call Summary Push** -- After summary is generated in GHL, push to Airtable which syncs to CW software
3. **Data Sync Monitoring** -- Verify data flows correctly from GHL through Airtable to Supabase
4. **Claim Type Analysis** -- Pull records grouped by claim type for pattern analysis

## Notes

- Ben has previously used Airtable MCP when building the CW software (familiar with the schema)
- Need to map: which Airtable tables/fields correspond to which CW software tables

## Source

MCP tools discovered via tool search. Context from Ben/Jo calls March 24-25 2026.
