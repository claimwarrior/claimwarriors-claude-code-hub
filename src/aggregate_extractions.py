"""
Gemini Flash Aggregation — batch summarize extractions into pattern reports.

Reads all extractions from Supabase, batches them into groups of 100,
and sends each batch to Gemini to produce a pattern summary report.
Saves reports as markdown files.

Usage:
    python aggregate_extractions.py --env-file .env --batch-size 100 --worker 0 --total-workers 4
"""

import argparse
import json
import os
import sys
import time
import requests


SUPABASE_URL = "https://upbbqaqnegncoetxuhwk.supabase.co"
TRANSCRIPTS_TABLE = "GHL Call Transcripts"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_MODEL = "models/gemini-2.5-flash"

AGGREGATION_PROMPT = """You are analyzing pattern extractions from successful sales calls at Claim Warriors, a public adjusting firm that fights insurance companies for homeowners.

Each extraction contains structured data about one call: objections raised, qualification questions, openers, close attempts, red flags, value signals, emotional dynamics, and claim type details.

Your job: AGGREGATE patterns across all the extractions below. Rank by frequency. Include exact quotes as evidence.

## Produce a report with these sections:

### 1. Claim Type & Status Distribution
- Count of each claim type (water, roof, fire, misc, unknown)
- Count of each claim status (new, denied, underpaid, unknown)
- Count of each call purpose (intake, follow_up, negotiation_update, document_collection, other)

### 2. Top Objections (ranked by frequency)
For each objection pattern:
- The objection category and typical phrasing (exact quotes)
- How many times it appeared
- The most effective response strategy with exact quote examples
- Whether it was typically resolved

### 3. Qualification Question Patterns
- Most common questions asked, grouped by purpose (assess_value, assess_viability, collect_info, identify_type, red_flag_check)
- Typical question order/flow for each claim type
- Key questions that separate good claims from bad

### 4. Opener Patterns
- Most common rep openers with exact quotes
- Customer initial tone distribution
- Which openers led to the best customer engagement

### 5. Close Attempt Patterns
- Types of closes used (direct_ask, assumptive, summary, urgency, trial)
- Success rate patterns — what close types worked best
- What typically preceded a successful close
- Exact quotes from successful closes

### 6. Red Flags
- Most common red flag categories
- How reps typically handled each type
- Which red flags killed deals vs. were manageable

### 7. Value Signals
- How claim values are discussed
- Common value ranges by claim type
- How reps assess and communicate value

### 8. Emotional Dynamics
- Most common initial customer states
- Most common turning points (what shifted the customer)
- Most effective empathy moments (exact quotes)
- Pattern: initial state → turning point → final state

### 9. Type-Specific Insights
For each claim type (water, roof, fire, misc):
- Unique patterns specific to this type
- Type-specific qualification questions
- Type-specific objections

### 10. Key Takeaways
- Top 5 patterns that explain why these calls succeeded
- Most important skills/techniques observed
- Biggest differences between claim types

---

Here are {count} call extractions to analyze:

{extractions}

Produce the report now. Be specific — use exact quotes and counts, not vague summaries."""


def load_env(env_file):
    env = {}
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                env[key.strip()] = val.strip()
    return env


def supabase_headers(service_key):
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }


def fetch_all_extractions(service_key):
    """Fetch all extractions from Supabase."""
    headers = supabase_headers(service_key)
    all_rows = []
    offset = 0
    limit = 1000

    while True:
        resp = requests.get(
            f"{SUPABASE_URL}/rest/v1/{TRANSCRIPTS_TABLE}",
            headers={**headers, "Range": f"{offset}-{offset + limit - 1}"},
            params={
                "select": "id,ghl_message_id,ghl_contact_id,duration,extraction",
                "extraction": "not.is.null",
                "order": "id.asc",
            },
        )
        if resp.status_code == 416:
            break
        resp.raise_for_status()
        rows = resp.json()
        if not rows:
            break
        all_rows.extend(rows)
        offset += limit

    return all_rows


def call_gemini(api_key, prompt, max_retries=5):
    """Call Gemini with retry logic."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "text/plain",
        },
    }

    for attempt in range(max_retries):
        try:
            resp = requests.post(
                f"{GEMINI_API_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=600,
            )
        except Exception as e:
            log(f"    Request error (attempt {attempt + 1}): {e}")
            time.sleep(10 * (attempt + 1))
            continue

        if resp.status_code == 429:
            log(f"    Rate limited, waiting 30s (attempt {attempt + 1})")
            time.sleep(30)
            continue
        if resp.status_code >= 500:
            log(f"    Server error {resp.status_code}, waiting 10s (attempt {attempt + 1})")
            time.sleep(10)
            continue

        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    return None


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--worker", type=int, default=0)
    parser.add_argument("--total-workers", type=int, default=1)
    args = parser.parse_args()

    env = load_env(args.env_file)
    gemini_key = env.get("CLAIM_WARRIOR_GOOGLE_API_KEY")
    supabase_key = env.get("CW_SUPABASE_SERVICE_ROLE_KEY")

    if not gemini_key or not supabase_key:
        log("ERROR: Missing API keys")
        sys.exit(1)

    # Output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    reports_dir = os.path.join(project_dir, "pipeline_data", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Fetch all extractions
    log("Fetching all extractions from Supabase...")
    all_rows = fetch_all_extractions(supabase_key)
    log(f"  {len(all_rows)} extractions fetched")

    # Split into batches
    batches = []
    for i in range(0, len(all_rows), args.batch_size):
        batches.append(all_rows[i:i + args.batch_size])
    log(f"  {len(batches)} batches of ~{args.batch_size}")

    # This worker's batches
    my_batches = [(i, b) for i, b in enumerate(batches) if i % args.total_workers == args.worker]
    log(f"  Worker {args.worker}/{args.total_workers}: {len(my_batches)} batches to process")

    done = 0
    errors = 0

    for batch_idx, batch in my_batches:
        batch_num = batch_idx + 1
        report_file = os.path.join(reports_dir, f"batch_{batch_num:02d}.md")

        # Skip if already done
        if os.path.exists(report_file) and os.path.getsize(report_file) > 500:
            log(f"  [Batch {batch_num}] Already done, skipping")
            done += 1
            continue

        # Build extractions text
        extractions_text = ""
        for row in batch:
            ext = row["extraction"]
            if isinstance(ext, str):
                ext = json.loads(ext)
            extractions_text += f"\n--- Extraction (id={row['id']}, duration={row.get('duration', '?')}s) ---\n"
            extractions_text += json.dumps(ext, indent=2) + "\n"

        prompt = AGGREGATION_PROMPT.format(
            count=len(batch),
            extractions=extractions_text,
        )

        total_chars = len(prompt)
        log(f"  [Batch {batch_num}] {len(batch)} extractions, {total_chars:,} chars (~{total_chars // 4:,} tokens)")

        report = call_gemini(gemini_key, prompt)

        if not report:
            log(f"  [Batch {batch_num}] FAILED after retries")
            errors += 1
            continue

        # Save report
        with open(report_file, "w") as f:
            f.write(f"# Batch {batch_num} — {len(batch)} calls analyzed\n\n")
            f.write(report)

        done += 1
        log(f"  [Batch {batch_num}] Saved ({len(report):,} chars)")

    log(f"\nDone. Reports: {done}, Errors: {errors}")


if __name__ == "__main__":
    main()
