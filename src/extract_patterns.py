"""
Gemini Flash Pattern Extraction — One call at a time.

Reads transcripts from Supabase, sends EACH ONE individually to Gemini Flash,
and immediately writes the extraction back to Supabase before moving on.

Usage:
    python extract_patterns.py --env-file .env --min-duration 180 --worker 0 --total-workers 4
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


def load_rubric():
    rubric_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extraction_rubric.md")
    with open(rubric_path, "r") as f:
        return f.read()


def supabase_headers(service_key):
    return {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }


def fetch_unprocessed_ids(service_key, min_duration, worker, total_workers):
    """Fetch all IDs of transcripts that need extraction, partitioned for this worker."""
    headers = supabase_headers(service_key)
    params = {
        "select": "id",
        "transcript": "not.is.null",
        "extraction": "is.null",
        "duration": f"gte.{min_duration}",
        "order": "id.asc",
        "limit": "5000",
    }
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/{TRANSCRIPTS_TABLE}",
        headers=headers,
        params=params,
    )
    resp.raise_for_status()
    all_ids = [r["id"] for r in resp.json()]
    # Partition
    return [i for i in all_ids if i % total_workers == worker]


def fetch_transcript_by_id(service_key, row_id):
    """Fetch a single transcript row."""
    headers = supabase_headers(service_key)
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/{TRANSCRIPTS_TABLE}?id=eq.{row_id}&select=id,ghl_message_id,ghl_contact_id,conversation_id,call_date,duration,direction,transcript",
        headers=headers,
    )
    resp.raise_for_status()
    rows = resp.json()
    return rows[0] if rows else None


def extract_one(api_key, rubric, transcript_row):
    """Send ONE transcript to Gemini and return the extraction."""
    t = transcript_row
    prompt = f"""{rubric}

---

Here is 1 transcript to analyze. Return a single JSON object (NOT an array).

--- TRANSCRIPT ---
ghl_message_id: {t['ghl_message_id']}
ghl_contact_id: {t['ghl_contact_id']}
duration: {t.get('duration', 'unknown')}s
direction: {t.get('direction', 'unknown')}
call_date: {t.get('call_date', 'unknown')}

{t.get('transcript', '')}

IMPORTANT: Return ONLY valid JSON. No markdown code fences, no explanation. Just ONE JSON object."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json",
        },
    }

    resp = requests.post(
        f"{GEMINI_API_BASE}/{GEMINI_MODEL}:generateContent?key={api_key}",
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=300,
    )

    if resp.status_code == 429:
        return None, "rate_limited"
    if resp.status_code >= 500:
        return None, f"server_error_{resp.status_code}"

    try:
        resp.raise_for_status()
    except Exception as e:
        return None, str(e)

    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]

    try:
        extraction = json.loads(text)
        return extraction, None
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {e}"


def save_extraction(service_key, ghl_message_id, extraction):
    """Write extraction to Supabase immediately."""
    headers = {
        **supabase_headers(service_key),
        "Prefer": "return=minimal",
    }
    resp = requests.patch(
        f"{SUPABASE_URL}/rest/v1/{TRANSCRIPTS_TABLE}?ghl_message_id=eq.{ghl_message_id}",
        headers=headers,
        json={"extraction": extraction},
    )
    return resp.status_code in (200, 204)


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--min-duration", type=int, default=180)
    parser.add_argument("--worker", type=int, default=0)
    parser.add_argument("--total-workers", type=int, default=1)
    parser.add_argument("--limit", type=int, default=0,
                        help="Max transcripts to process (0 = all)")
    args = parser.parse_args()

    env = load_env(args.env_file)
    gemini_key = env.get("CLAIM_WARRIOR_GOOGLE_API_KEY")
    supabase_key = env.get("CW_SUPABASE_SERVICE_ROLE_KEY")

    if not gemini_key or not supabase_key:
        log("ERROR: Missing GOOGLE_API_KEY or CW_SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)

    rubric = load_rubric()
    log(f"Worker {args.worker}/{args.total_workers} starting")

    # Get all IDs this worker needs to process
    my_ids = fetch_unprocessed_ids(supabase_key, args.min_duration, args.worker, args.total_workers)
    if args.limit > 0:
        my_ids = my_ids[:args.limit]
    log(f"  {len(my_ids)} transcripts to process")

    done = 0
    errors = 0

    for row_id in my_ids:
        # Fetch the full transcript
        row = fetch_transcript_by_id(supabase_key, row_id)
        if not row:
            continue

        transcript = row.get("transcript", "") or ""
        if len(transcript) < 200:
            continue

        msg_id = row["ghl_message_id"]
        duration = row.get("duration", 0)

        # Extract with Gemini — retry until success
        max_retries = 5
        extraction = None
        error = None
        for attempt in range(max_retries):
            try:
                extraction, error = extract_one(gemini_key, rubric, row)
            except Exception as e:
                extraction, error = None, f"exception: {e}"

            if not error:
                break

            if error == "rate_limited":
                log(f"  [{done}/{len(my_ids)}] {msg_id} -- rate limited, waiting 30s (attempt {attempt + 1})")
                time.sleep(30)
            elif error.startswith("server_error"):
                log(f"  [{done}/{len(my_ids)}] {msg_id} -- {error}, waiting 10s (attempt {attempt + 1})")
                time.sleep(10)
            elif "JSON parse error" in error:
                log(f"  [{done}/{len(my_ids)}] {msg_id} -- bad JSON, retrying (attempt {attempt + 1})")
                time.sleep(2)
            else:
                log(f"  [{done}/{len(my_ids)}] {msg_id} -- {error}, retrying (attempt {attempt + 1})")
                time.sleep(5)

        if error:
            log(f"  [{done}/{len(my_ids)}] {msg_id} ({duration}s) -- FAILED after {max_retries} attempts: {error}")
            errors += 1
            continue

        # Push to Supabase IMMEDIATELY
        saved = save_extraction(supabase_key, msg_id, extraction)
        done += 1

        if saved:
            log(f"  [{done}/{len(my_ids)}] {msg_id} ({duration}s) -- saved")
        else:
            log(f"  [{done}/{len(my_ids)}] {msg_id} ({duration}s) -- SAVE FAILED")
            errors += 1

    log(f"\nDone. Extracted: {done}, Errors: {errors}")


if __name__ == "__main__":
    main()
