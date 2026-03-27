# Project: Knowledge Base Creation -- Operational Runbook

**Status**: Step 3 in progress (transcription)
**Priority**: Critical -- foundation for all AI agents
**Owner**: Ben
**Phase**: 1 (Foundation)
**Strategic doc**: [[knowledge-base-ingestion]] (the "why" and methodology)

## Quick Start (for Claude Code sessions)

This is the operational runbook. A fresh Claude Code session should be able to read this and immediately run the next batch.

### Prerequisites

- Python: `C:\Users\benelk\AppData\Local\Programs\Python\Python312\python.exe`
- Scripts: `C:\Users\benelk\Documents\claimwarriors-claude-code-hub\src\`
- Env file: `C:\Users\benelk\Documents\claudeclaw\.env`
- Required env vars: `CLAIM_WARRIOR_GHL_API_KEY`, `GROQ_API_KEY`

### Step A: Extract completed-contract contact IDs

Run once (or re-run to refresh). Outputs one contact ID per line to stdout.

```bash
cd C:\Users\benelk\Documents\claimwarriors-claude-code-hub\src
C:\Users\benelk\AppData\Local\Programs\Python\Python312\python.exe extract_contract_contacts.py "$CLAIM_WARRIOR_GHL_API_KEY" > C:\Users\benelk\AppData\Local\Temp\ghl_completed_contract_contacts.txt
```

This pages through the GHL Documents API (`GET /proposals/document?status[]=completed`) and extracts recipient contact IDs. As of March 26, 2026: 790 completed contracts.

### Step B: Run transcription pipeline (batch of 50)

```bash
cd C:\Users\benelk\Documents\claimwarriors-claude-code-hub\src
C:\Users\benelk\AppData\Local\Programs\Python\Python312\python.exe transcribe_calls.py --env-file C:\Users\benelk\Documents\claudeclaw\.env --contact-ids C:\Users\benelk\AppData\Local\Temp\ghl_completed_contract_contacts.txt --batch-size 50 --processed-ids C:\Users\benelk\AppData\Local\Temp\ghl_processed_ids.txt --processed-contacts C:\Users\benelk\AppData\Local\Temp\ghl_processed_contacts.txt
```

The script outputs JSON lines to stdout. Each line is one transcribed call. Insert into Supabase using the MCP or pipe to a loader.

**To insert results into Supabase:** The script prints JSON lines to stdout. Use the Supabase MCP `execute_sql` tool to insert each line, or redirect stdout to a file and batch-insert:

```bash
... > C:\Users\benelk\AppData\Local\Temp\ghl_transcription_batch.jsonl
```

Then read the JSONL file and insert each row into the `GHL Call Transcripts` table via Supabase MCP.

### Re-running is safe

- **Message-level dedup**: `--processed-ids` file tracks every message ID already handled (transcribed, skipped as voicemail, etc.)
- **Contact-level dedup**: `--processed-contacts` file tracks contacts whose calls have been fully scanned
- **Supabase dedup**: Table has a unique constraint on `ghl_message_id` -- duplicate inserts are no-ops
- Run the same command repeatedly. It picks up where it left off.

## Current Status (as of March 26, 2026)

| Metric | Value |
|--------|-------|
| Completed contracts in GHL | 790 |
| Unique contacts (estimated) | TBD -- need to run Step A with new filter |
| Contacts transcribed | 1 (William Gardner) |
| Calls in Supabase | 5 |
| Errors | 0 |

**IMPORTANT**: The old contact IDs file at `ghl_completed_contact_ids.txt` (562 contacts) is STALE -- it was the unfiltered full contact list. Step A above generates the correct filtered list from completed contracts only. The new file is named `ghl_completed_contract_contacts.txt` to avoid confusion.

## The 6-Step Pipeline

### Step 1: Map GHL call data -- DONE
Explored GHL API. Call recordings live under conversations > messages (TYPE_CALL). Recording download endpoint: `GET /conversations/messages/{messageId}/locations/{locationId}/recording`.

### Step 2: Build extraction script -- DONE
Two scripts in `src/`:
- `extract_contract_contacts.py` -- pages through completed contracts, outputs contact IDs
- `transcribe_calls.py` -- downloads recordings, transcribes via Groq Whisper, outputs JSONL

### Step 3: Transcribe and store -- IN PROGRESS
Pipeline proven end-to-end. Need to scale from 1 contact to all ~790 contracts worth of contacts.

Each batch run:
1. Pulls next N unprocessed contacts
2. For each contact: finds conversation, fetches TYPE_CALL messages
3. Skips voicemails and non-completed calls
4. Downloads WAV, transcribes via Groq Whisper (`whisper-large-v3`)
5. Outputs JSON, deletes local WAV
6. Tracks progress in processed-ids files

### Step 4: Write extraction rubric -- NOT STARTED
A Gemini Flash prompt defining what patterns to mine from transcripts:
- Objections raised and how handled
- Qualification questions asked and when
- Close attempts and what led to them
- Openers and customer responses
- Claim type signals and type-specific details
- Red flags (old claims, low value, prior adjusters)
- Information collection patterns
- Customer emotional state and rep response

### Step 5: Gemini Flash batch extraction -- NOT STARTED
Batch 20-30 transcripts at a time through Gemini Flash (cheap, 1M context). Store structured extractions in a second Supabase table (`call_extractions` or similar).

### Step 6: Claude synthesis -- NOT STARTED
Distill all Gemini extractions into:
- 4-6 conversation archetypes
- 10-15 recurring objection/response pairs
- Qualification patterns per claim type
- Few-shot examples from real calls
- Two intake scripts (denied + new/underpaid)

## Supabase Table: GHL Call Transcripts

**Project**: Claim Warrior (`upbbqaqnegncoetxuhwk`)

| Column | Type | Nullable | Notes |
|--------|------|----------|-------|
| id | bigint | NO | Auto-increment PK |
| ghl_contact_id | text | NO | GHL contact ID |
| call_date | timestamptz | NO | When the call happened |
| transcript | text | YES | Full transcript text |
| created_at | timestamptz | YES | Row creation time |
| ghl_message_id | text | YES | Unique constraint -- dedup key |
| duration | integer | YES | Call duration in seconds |
| direction | text | YES | inbound or outbound |
| call_status | text | YES | "completed" for real calls |
| conversation_id | text | YES | GHL conversation ID |

## API Reference

### GHL Documents (completed contracts)
- `GET https://services.leadconnectorhq.com/proposals/document`
- Params: `locationId=L58ZxauomnryKcGf1IjZ`, `status[]=completed`, `limit=20`, `skip=N`
- Auth: `Authorization: Bearer pit-...` + `Version: 2021-07-28`
- Response: `{ documents: [...], total: 790 }`
- Contact ID is in `documents[].recipients[].id`

### GHL Conversations
- Search: `GET /conversations/search?locationId=...&contactId=...`
- Messages: `GET /conversations/{id}/messages?type=TYPE_CALL&limit=100`
- Recording: `GET /conversations/messages/{msgId}/locations/{locId}/recording`

### Groq Whisper
- `POST https://api.groq.com/openai/v1/audio/transcriptions`
- Model: `whisper-large-v3`
- Auth: `Bearer {GROQ_API_KEY}`

## Filtering Logic

1. **Completed contracts only**: Contact IDs extracted from GHL documents API with `status[]=completed`
2. **Calls only, no voicemails**: Script checks `meta.call.status` -- only processes `"completed"` calls
3. **All durations**: No minimum duration filter -- every completed call is processed regardless of length
