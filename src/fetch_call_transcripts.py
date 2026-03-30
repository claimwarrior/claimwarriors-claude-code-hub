"""
GHL Call Transcript Fetcher
============================

Fetches call transcripts directly from GHL's transcription API and upserts
them into Supabase. No audio download or local transcription needed.

Only processes contacts with completed contracts.
Only processes completed calls (no voicemails).

Usage:
    python fetch_call_transcripts.py --env-file /path/to/.env --contact-ids /path/to/ids.txt --batch-size 100
"""

import argparse
import json
import os
import sys
import time
import requests


GHL_API_BASE = "https://services.leadconnectorhq.com"
GHL_API_VERSION = "2021-07-28"
LOCATION_ID = "L58ZxauomnryKcGf1IjZ"
SUPABASE_URL = "https://upbbqaqnegncoetxuhwk.supabase.co"
SUPABASE_TABLE = "GHL Call Transcripts"


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


def load_ids_file(filepath):
    if not filepath or not os.path.exists(filepath):
        return set()
    with open(filepath, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_processed_id(filepath, id_val):
    if not filepath:
        return
    with open(filepath, "a") as f:
        f.write(id_val + "\n")


def ghl_headers(api_key):
    return {
        "Authorization": api_key,
        "Version": GHL_API_VERSION,
        "Accept": "application/json",
    }


def ghl_request(url, api_key, params=None, max_retries=5):
    """Make a GHL API request with retry on 429."""
    for attempt in range(max_retries):
        resp = requests.get(url, headers=ghl_headers(api_key), params=params)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 10 * (attempt + 1)))
            log(f"    GHL 429, waiting {wait}s...")
            time.sleep(wait)
            continue
        return resp
    return resp


def find_conversation_for_contact(api_key, contact_id):
    resp = ghl_request(
        f"{GHL_API_BASE}/conversations/search",
        api_key,
        params={"locationId": LOCATION_ID, "contactId": contact_id, "limit": 1},
    )
    resp.raise_for_status()
    convos = resp.json().get("conversations", [])
    return convos[0] if convos else None


def fetch_call_messages(api_key, conversation_id, last_message_id=None):
    params = {"type": "TYPE_CALL", "limit": 100}
    if last_message_id:
        params["lastMessageId"] = last_message_id
    resp = ghl_request(
        f"{GHL_API_BASE}/conversations/{conversation_id}/messages",
        api_key,
        params=params,
    )
    resp.raise_for_status()
    data = resp.json()
    messages_data = data.get("messages", {})
    return (
        messages_data.get("messages", []),
        messages_data.get("nextPage", False),
        messages_data.get("lastMessageId"),
    )


def fetch_transcript(api_key, location_id, message_id):
    """Fetch transcript from GHL's transcription API.

    Returns a formatted string with speaker labels (Channel 1 / Channel 2).
    """
    resp = ghl_request(
        f"{GHL_API_BASE}/conversations/locations/{location_id}/messages/{message_id}/transcription",
        api_key,
    )
    if resp.status_code in (404, 422):
        return None
    resp.raise_for_status()
    data = resp.json()

    if not data or not isinstance(data, list):
        return None

    lines = []
    for sentence in data:
        channel = sentence.get("mediaChannel", 0)
        text = sentence.get("transcript", "").strip()
        if text:
            lines.append(f"[Speaker {channel}]: {text}")

    return "\n".join(lines) if lines else None


def upsert_to_supabase(service_key, row):
    """Upsert a transcript row into Supabase (overwrite existing on ghl_message_id conflict)."""
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?on_conflict=ghl_message_id",
        headers=headers,
        json=row,
    )
    if resp.status_code in (200, 201):
        return True
    log(f"    Supabase error {resp.status_code}: {resp.text[:200]}")
    return False


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser(description="GHL Call Transcript Fetcher")
    parser.add_argument("--env-file", required=True)
    parser.add_argument("--contact-ids", required=True)
    parser.add_argument("--batch-size", type=int, default=100,
                        help="Max contacts to process per run")
    parser.add_argument("--processed-ids", default=None)
    parser.add_argument("--processed-contacts", default=None)
    args = parser.parse_args()

    env = load_env(args.env_file)
    ghl_key = env.get("CLAIM_WARRIOR_GHL_API_KEY")
    supabase_key = env.get("CW_SUPABASE_SERVICE_ROLE_KEY")

    if not ghl_key:
        log("ERROR: CLAIM_WARRIOR_GHL_API_KEY not found in .env")
        sys.exit(1)
    if not supabase_key:
        log("ERROR: CW_SUPABASE_SERVICE_ROLE_KEY not found in .env")
        sys.exit(1)

    with open(args.contact_ids, "r") as f:
        all_contact_ids = [line.strip() for line in f if line.strip()]
    log(f"Loaded {len(all_contact_ids)} contact IDs")

    processed_msg_ids = load_ids_file(args.processed_ids)
    processed_contact_ids = load_ids_file(args.processed_contacts)
    log(f"Already processed: {len(processed_msg_ids)} messages, {len(processed_contact_ids)} contacts")

    fetched_count = 0
    skipped_count = 0
    error_count = 0
    contacts_done = 0

    for contact_id in all_contact_ids:
        if contacts_done >= args.batch_size:
            break

        if contact_id in processed_contact_ids:
            continue

        try:
            convo = find_conversation_for_contact(ghl_key, contact_id)
        except Exception as e:
            log(f"  Error finding conversation for {contact_id}: {e}")
            error_count += 1
            continue

        if not convo:
            save_processed_id(args.processed_contacts, contact_id)
            processed_contact_ids.add(contact_id)
            continue

        convo_id = convo["id"]
        contact_name = convo.get("contactName", "Unknown")
        log(f"[{contacts_done + 1}] {contact_name} ({contact_id})")

        last_msg_id = None
        has_more = True

        while has_more:
            try:
                messages, has_more, last_msg_id = fetch_call_messages(
                    ghl_key, convo_id, last_msg_id
                )
            except Exception as e:
                log(f"  Error fetching messages: {e}")
                error_count += 1
                break

            for msg in messages:
                msg_id = msg["id"]
                call_meta = msg.get("meta", {}).get("call", {})
                call_status = call_meta.get("status", "")
                duration = call_meta.get("duration")
                direction = msg.get("direction", "")
                date_added = msg.get("dateAdded", "")

                if msg_id in processed_msg_ids:
                    skipped_count += 1
                    continue

                if call_status != "completed":
                    skipped_count += 1
                    processed_msg_ids.add(msg_id)
                    save_processed_id(args.processed_ids, msg_id)
                    continue

                try:
                    transcript = fetch_transcript(ghl_key, LOCATION_ID, msg_id)

                    if not transcript:
                        log(f"  {msg_id} ({duration}s) -- no transcript available")
                        skipped_count += 1
                        processed_msg_ids.add(msg_id)
                        save_processed_id(args.processed_ids, msg_id)
                        continue

                    row = {
                        "ghl_message_id": msg_id,
                        "ghl_contact_id": contact_id,
                        "conversation_id": convo_id,
                        "call_date": date_added,
                        "duration": duration,
                        "direction": direction,
                        "call_status": "completed",
                        "transcript": transcript,
                    }

                    if upsert_to_supabase(supabase_key, row):
                        fetched_count += 1
                        log(f"  {msg_id} ({duration}s) -- upserted ({len(transcript)} chars)")
                    else:
                        error_count += 1

                    processed_msg_ids.add(msg_id)
                    save_processed_id(args.processed_ids, msg_id)

                except Exception as e:
                    log(f"  {msg_id} error: {e}")
                    error_count += 1

            time.sleep(0.3)

        if not has_more:
            save_processed_id(args.processed_contacts, contact_id)
            processed_contact_ids.add(contact_id)
            contacts_done += 1
            log(f"  Contact done ({contacts_done}/{args.batch_size})")

        time.sleep(0.2)

    log(f"\n--- Summary ---")
    log(f"Contacts done: {contacts_done}")
    log(f"Calls fetched & upserted: {fetched_count}")
    log(f"Skipped: {skipped_count}")
    log(f"Errors: {error_count}")


if __name__ == "__main__":
    main()
