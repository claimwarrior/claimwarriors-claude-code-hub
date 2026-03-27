---
name: cw-insert-transcript
description: |
  Claim Warriors transcript insertion pipeline. Extracts call recordings
  from GoHighLevel for completed-contract customers, transcribes them via
  Groq Whisper, and inserts transcripts into Supabase.

  Use this skill when user says:
  - "run the transcription pipeline"
  - "transcribe CW calls"
  - "insert transcripts"
  - "run a batch of transcriptions"
  - "extract and transcribe calls"
---

# CW Insert Transcript Pipeline

End-to-end pipeline: GHL completed contracts -> contact IDs -> call recordings -> Groq Whisper transcription -> Supabase storage.

## Prerequisites

- Python: `C:\Users\benelk\AppData\Local\Programs\Python\Python312\python.exe`
- Scripts: `C:\Users\benelk\Documents\claimwarriors-claude-code-hub\src\`
- Env file: `C:\Users\benelk\Documents\claudeclaw\.env` (needs `CLAIM_WARRIOR_GHL_API_KEY`, `GROQ_API_KEY`, `CW_SUPABASE_SERVICE_ROLE_KEY`)
- Supabase project: `upbbqaqnegncoetxuhwk` (Claim Warrior)
- Supabase table: `GHL Call Transcripts`

## How to Run

When invoked, ask the user for a batch size (default 10). The batch size represents the number of **unique contacts** to process -- all calls for each contact are transcribed. Then execute all three phases in sequence. Do not stop between phases unless there's an error.

### Phase 1: Extract Contact IDs

Extract contact IDs from completed contracts in GHL. This generates the filtered list of customers to process.

Read the .env file with the Read tool, extract the `CLAIM_WARRIOR_GHL_API_KEY` value (it includes the `Bearer ` prefix), and pass it directly to the Python command:

```bash
cd C:\Users\benelk\Documents\claimwarriors-claude-code-hub\src && C:\Users\benelk\AppData\Local\Programs\Python\Python312\python.exe extract_contract_contacts.py "<GHL_API_KEY_FROM_ENV>" > C:\Users\benelk\AppData\Local\Temp\ghl_completed_contract_contacts.txt
```

After Phase 1 completes, report how many unique contact IDs were extracted.

### Phase 2: Transcribe Calls

Run the transcription pipeline with the requested batch size. The batch size controls how many **contacts** to process -- all calls for each contact are transcribed regardless of count.

```bash
cd C:\Users\benelk\Documents\claimwarriors-claude-code-hub\src && C:\Users\benelk\AppData\Local\Programs\Python\Python312\python.exe transcribe_calls.py --env-file C:\Users\benelk\Documents\claudeclaw\.env --contact-ids C:\Users\benelk\AppData\Local\Temp\ghl_completed_contract_contacts.txt --batch-size <BATCH_SIZE> --processed-ids C:\Users\benelk\AppData\Local\Temp\ghl_processed_ids.txt --processed-contacts C:\Users\benelk\AppData\Local\Temp\ghl_processed_contacts.txt > C:\Users\benelk\AppData\Local\Temp\ghl_transcription_batch.jsonl
```

Progress logs go to stderr (visible in terminal). The script handles:
- Rate limiting (auto-retry with backoff)
- Skipping voicemails and non-completed calls
- Skipping already-processed messages (via processed-ids file)
- Deleting WAV files after transcription

After Phase 2 completes, report how many contacts were processed and total calls transcribed.

### Phase 3: Insert into Supabase

Use the Python REST API insertion script. This bypasses the Supabase MCP size limit that truncates long transcripts.

```bash
cd C:\Users\benelk\Documents\claimwarriors-claude-code-hub\src && C:\Users\benelk\AppData\Local\Programs\Python\Python312\python.exe supabase_insert.py --env-file C:\Users\benelk\Documents\claudeclaw\.env --jsonl C:\Users\benelk\AppData\Local\Temp\ghl_transcription_batch.jsonl
```

Requires `CW_SUPABASE_SERVICE_ROLE_KEY` in the .env file. Get it from Supabase dashboard > Project Settings > API > service_role key.

**IMPORTANT:** Do NOT use the Supabase MCP `execute_sql` for inserting transcripts -- it has a ~3000 character query parameter limit that silently truncates long transcripts.

After Phase 3, report:
- Total calls inserted
- Any duplicates skipped (ON CONFLICT)
- Verify totals using the Supabase MCP: `mcp__Supabase-claim-warrior__execute_sql` with `SELECT COUNT(*) FROM "GHL Call Transcripts";`

## Resumability

Everything is resumable. Re-running the skill:
- Phase 1: Re-extracts the full contact list (fast, ~1-2 min)
- Phase 2: Skips already-processed messages and contacts via tracking files
- Phase 3: Supabase dedup via ON CONFLICT on ghl_message_id (ignore-duplicates)

## Tracking Files

| File | Purpose |
|------|---------|
| `ghl_completed_contract_contacts.txt` | Contact IDs from completed contracts (regenerated each run) |
| `ghl_processed_ids.txt` | Message IDs already processed (append-only) |
| `ghl_processed_contacts.txt` | Contacts fully scanned (all their calls done) |
| `ghl_transcription_batch.jsonl` | Latest batch output (overwritten each run) |

All in `C:\Users\benelk\AppData\Local\Temp\`.

## Supabase Table Schema

| Column | Type | Notes |
|--------|------|-------|
| id | bigint | Auto-increment PK |
| ghl_contact_id | text | NOT NULL |
| call_date | timestamptz | NOT NULL |
| transcript | text | nullable |
| created_at | timestamptz | default now() |
| ghl_message_id | text | UNIQUE constraint -- dedup key |
| duration | integer | seconds |
| direction | text | inbound/outbound |
| call_status | text | "completed" |
| conversation_id | text | GHL conversation ID |

## Full Runbook

For background context, methodology, and the full 6-step pipeline plan (including Gemini Flash extraction and Claude synthesis -- steps 4-6 not yet implemented), see:
`C:\Users\benelk\Documents\claimwarriors-claude-code-hub\02-Projects\knowledge-base-creation.md`
