# Integration: Supabase MCP

**Status**: Available
**MCP Server**: `Supabase-claim-warrior`

## What It Connects To

Supabase (PostgreSQL) -- the database powering the Claim Warriors software application.

## Available Capabilities

### Database
- `execute_sql` -- Run SQL queries against the CW database
- `list_tables` -- List all tables
- `apply_migration` -- Apply database migrations
- `list_migrations` -- View migration history
- `list_extensions` -- List PostgreSQL extensions

### Project Management
- `list_projects` / `get_project` -- Project info
- `get_project_url` -- Get Supabase project URL
- `list_organizations` / `get_organization` -- Org info

### Edge Functions
- `list_edge_functions` / `get_edge_function` / `deploy_edge_function` -- Serverless functions

### Branching
- `list_branches` / `create_branch` / `merge_branch` / `reset_branch` / `rebase_branch` / `delete_branch` -- Database branching

### Other
- `get_logs` -- Application logs
- `get_advisors` -- Performance advisors
- `search_docs` -- Search Supabase documentation
- `generate_typescript_types` -- Generate TypeScript types from DB schema

## Key Use Cases for CW

1. **AI Customer Service Rep** -- `execute_sql` to query claim status, comments, assignments for customer inquiries
2. **Call Summary Push** -- `execute_sql` to insert the call summary as a comment on the claim record
3. **Claim Verifier** -- `execute_sql` to pull historical claim data for comparison
4. **Knowledge Base Ingestion** -- `list_tables` + `execute_sql` to understand the full CW data model
5. **Back Office Tools** -- Query estimates, carrier responses, file uploads for AI analysis

## Important Notes

- This is the PRODUCTION database. Be careful with write operations
- The VP R&D owns the CW codebase. AI strategy decisions are ours, but software changes go through them
- Recommended for dev/testing environments, not direct production writes without review

## Source

MCP tools discovered via tool search. Context from Ben/Jo calls March 24-25 2026.
