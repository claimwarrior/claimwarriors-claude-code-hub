"""Insert JSONL transcripts into Supabase via REST API.

Reads a JSONL file (one JSON object per line) and inserts each row into the
'GHL Call Transcripts' table in Supabase. Uses the PostgREST API with
ignore-duplicates to handle the UNIQUE constraint on ghl_message_id.

Usage:
    python supabase_insert.py --env-file /path/to/.env --jsonl /path/to/batch.jsonl

Requires CW_SUPABASE_SERVICE_ROLE_KEY in the .env file.
"""

import argparse
import json
import os
import sys
import requests

SUPABASE_URL = "https://upbbqaqnegncoetxuhwk.supabase.co"
TABLE = "GHL Call Transcripts"


def load_env(env_file):
    """Load key=value pairs from .env file."""
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


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser(description="Insert JSONL transcripts into Supabase")
    parser.add_argument(
        "--env-file",
        required=True,
        help="Path to .env file with CW_SUPABASE_SERVICE_ROLE_KEY",
    )
    parser.add_argument(
        "--jsonl",
        required=True,
        help="Path to JSONL file with transcript data",
    )
    args = parser.parse_args()

    env = load_env(args.env_file)
    service_key = env.get("CW_SUPABASE_SERVICE_ROLE_KEY")
    if not service_key:
        log("ERROR: CW_SUPABASE_SERVICE_ROLE_KEY not found in .env")
        sys.exit(1)

    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }

    rows = []
    with open(args.jsonl, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            rows.append(data)

    log(f"Loaded {len(rows)} rows from JSONL")

    inserted = 0
    skipped = 0
    errors = 0

    for i, row in enumerate(rows):
        try:
            resp = requests.post(
                f"{SUPABASE_URL}/rest/v1/{TABLE}",
                headers={
                    **headers,
                    "Prefer": "resolution=ignore-duplicates,return=minimal",
                },
                json=row,
            )
            if resp.status_code == 201:
                inserted += 1
                log(f"  [{i+1}/{len(rows)}] Inserted {row['ghl_message_id']}")
            elif resp.status_code == 200:
                skipped += 1
                log(f"  [{i+1}/{len(rows)}] Skipped (dup) {row['ghl_message_id']}")
            elif resp.status_code == 409:
                skipped += 1
                log(f"  [{i+1}/{len(rows)}] Skipped (conflict) {row['ghl_message_id']}")
            else:
                errors += 1
                log(f"  [{i+1}/{len(rows)}] Error {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            errors += 1
            log(f"  [{i+1}/{len(rows)}] Exception: {e}")

    log(f"\nInserted: {inserted}, Skipped: {skipped}, Errors: {errors}")


if __name__ == "__main__":
    main()
