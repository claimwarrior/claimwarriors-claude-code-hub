"""
GHL Call Recording Transcription Pipeline
==========================================

Downloads call recordings from GoHighLevel and transcribes them via Groq Whisper.
Outputs JSON results to stdout for insertion into Supabase via MCP.

Only processes contacts with completed contracts.
Only processes completed calls (no voicemails).

Usage:
    python transcribe_calls.py --env-file /path/to/.env --contact-ids /path/to/ids.txt --batch-size 10

The script:
1. Loads the list of contact IDs with completed contracts
2. For each contact, searches for their conversation in GHL
3. Fetches TYPE_CALL messages from that conversation
4. Skips voicemails and non-completed calls
5. Downloads the recording WAV for completed calls
6. Transcribes via Groq Whisper
7. Outputs JSON lines to stdout (one per transcribed call)
8. Deletes the local WAV after transcription

Each output line is a JSON object:
{
    "ghl_message_id": "...",
    "ghl_contact_id": "...",
    "conversation_id": "...",
    "call_date": "...",
    "duration": 123,
    "direction": "inbound|outbound",
    "call_status": "completed",
    "transcript": "..."
}
"""

import argparse
import json
import os
import sys
import tempfile
import time
import requests


GHL_API_BASE = "https://services.leadconnectorhq.com"
GHL_API_VERSION = "2021-07-28"
GROQ_API_BASE = "https://api.groq.com/openai/v1"
LOCATION_ID = "L58ZxauomnryKcGf1IjZ"


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


def load_ids_file(filepath):
    """Load a set of IDs from a text file (one per line)."""
    if not filepath or not os.path.exists(filepath):
        return set()
    with open(filepath, "r") as f:
        return set(line.strip() for line in f if line.strip())


def save_processed_id(filepath, msg_id):
    """Append a processed message ID to the tracking file."""
    if not filepath:
        return
    with open(filepath, "a") as f:
        f.write(msg_id + "\n")


def ghl_headers(api_key):
    return {
        "Authorization": api_key,
        "Version": GHL_API_VERSION,
        "Accept": "application/json",
    }


def find_conversation_for_contact(api_key, contact_id):
    """Search for a conversation by contact ID."""
    params = {
        "locationId": LOCATION_ID,
        "contactId": contact_id,
        "limit": 1,
    }
    resp = requests.get(
        f"{GHL_API_BASE}/conversations/search",
        headers=ghl_headers(api_key),
        params=params,
    )
    resp.raise_for_status()
    convos = resp.json().get("conversations", [])
    return convos[0] if convos else None


def fetch_call_messages(api_key, conversation_id, last_message_id=None):
    """Fetch TYPE_CALL messages from a conversation."""
    params = {"type": "TYPE_CALL", "limit": 100}
    if last_message_id:
        params["lastMessageId"] = last_message_id

    resp = requests.get(
        f"{GHL_API_BASE}/conversations/{conversation_id}/messages",
        headers=ghl_headers(api_key),
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


def download_recording(api_key, message_id, output_path):
    """Download call recording WAV from GHL."""
    url = f"{GHL_API_BASE}/conversations/messages/{message_id}/locations/{LOCATION_ID}/recording"
    resp = requests.get(url, headers=ghl_headers(api_key), stream=True)
    if resp.status_code == 404:
        return False
    resp.raise_for_status()

    content_type = resp.headers.get("content-type", "")
    if "audio" not in content_type and "octet-stream" not in content_type:
        return False

    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    # Verify file has actual content
    if os.path.getsize(output_path) < 1000:
        return False

    return True


def transcribe_with_groq(groq_key, audio_path):
    """Transcribe audio file using Groq Whisper API."""
    with open(audio_path, "rb") as f:
        resp = requests.post(
            f"{GROQ_API_BASE}/audio/transcriptions",
            headers={"Authorization": f"Bearer {groq_key}"},
            files={"file": ("recording.wav", f, "audio/wav")},
            data={
                "model": "whisper-large-v3",
                "response_format": "json",
                "language": "en",
            },
        )
    resp.raise_for_status()
    return resp.json().get("text", "")


def log(msg):
    """Log to stderr so stdout stays clean for JSON output."""
    print(msg, file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser(description="GHL Call Transcription Pipeline")
    parser.add_argument(
        "--env-file",
        required=True,
        help="Path to .env file with API keys",
    )
    parser.add_argument(
        "--contact-ids",
        required=True,
        help="Path to file with contact IDs (one per line) -- only these contacts are processed",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of calls to transcribe per run (default: 10)",
    )
    parser.add_argument(
        "--processed-ids",
        default=None,
        help="Path to file tracking already-processed message IDs",
    )
    parser.add_argument(
        "--processed-contacts",
        default=None,
        help="Path to file tracking fully-scanned contact IDs (all their calls done)",
    )
    args = parser.parse_args()

    # Load config
    env = load_env(args.env_file)
    ghl_key = env.get("CLAIM_WARRIOR_GHL_API_KEY")
    groq_key = env.get("GROQ_API_KEY")

    if not ghl_key:
        log("ERROR: CLAIM_WARRIOR_GHL_API_KEY not found in .env")
        sys.exit(1)
    if not groq_key:
        log("ERROR: GROQ_API_KEY not found in .env")
        sys.exit(1)

    # Load contact IDs (completed contracts only)
    all_contact_ids = []
    with open(args.contact_ids, "r") as f:
        all_contact_ids = [line.strip() for line in f if line.strip()]
    log(f"Loaded {len(all_contact_ids)} contact IDs from completed contracts")

    # Load already-processed tracking
    processed_msg_ids = load_ids_file(args.processed_ids)
    processed_contact_ids = load_ids_file(args.processed_contacts)
    log(f"Already processed: {len(processed_msg_ids)} messages, {len(processed_contact_ids)} contacts fully done")

    transcribed_count = 0
    skipped_count = 0
    error_count = 0
    contacts_scanned = 0

    for contact_id in all_contact_ids:
        if transcribed_count >= args.batch_size:
            break

        # Skip contacts we've fully processed
        if contact_id in processed_contact_ids:
            continue

        contacts_scanned += 1

        # Find this contact's conversation
        try:
            convo = find_conversation_for_contact(ghl_key, contact_id)
        except requests.exceptions.HTTPError as e:
            if e.response and e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 60))
                log(f"  Rate limited on conversation search. Waiting {retry_after}s...")
                time.sleep(retry_after)
                continue
            log(f"  Error finding conversation for {contact_id}: {e}")
            error_count += 1
            continue

        if not convo:
            # No conversation for this contact -- mark as done
            if args.processed_contacts:
                with open(args.processed_contacts, "a") as f:
                    f.write(contact_id + "\n")
            processed_contact_ids.add(contact_id)
            continue

        convo_id = convo["id"]
        contact_name = convo.get("contactName", "Unknown")
        log(f"[Contact {contacts_scanned}] {contact_name} ({contact_id}) -- conversation {convo_id}")

        # Fetch all TYPE_CALL messages for this contact
        contact_had_new_calls = False
        last_msg_id = None
        has_more = True

        while has_more and transcribed_count < args.batch_size:
            try:
                messages, has_more, last_msg_id = fetch_call_messages(
                    ghl_key, convo_id, last_msg_id
                )
            except requests.exceptions.HTTPError as e:
                if e.response and e.response.status_code == 429:
                    retry_after = int(e.response.headers.get("Retry-After", 60))
                    log(f"  Rate limited. Waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                log(f"  Error fetching messages: {e}")
                error_count += 1
                break

            for msg in messages:
                if transcribed_count >= args.batch_size:
                    break

                msg_id = msg["id"]
                call_meta = msg.get("meta", {}).get("call", {})
                call_status = call_meta.get("status", "")
                duration = call_meta.get("duration")
                direction = msg.get("direction", "")
                date_added = msg.get("dateAdded", "")

                # Skip if already processed
                if msg_id in processed_msg_ids:
                    skipped_count += 1
                    continue

                # Only process completed calls -- skip voicemails, no-answer, etc.
                if call_status != "completed":
                    skipped_count += 1
                    processed_msg_ids.add(msg_id)
                    save_processed_id(args.processed_ids, msg_id)
                    continue

                # Download and transcribe
                contact_had_new_calls = True
                tmp_wav = os.path.join(tempfile.gettempdir(), f"ghl_{msg_id}.wav")
                try:
                    log(f"  [{transcribed_count + 1}/{args.batch_size}] {msg_id} ({duration}s, {direction})")
                    has_recording = download_recording(ghl_key, msg_id, tmp_wav)

                    if not has_recording:
                        log(f"    No recording available, skipping.")
                        skipped_count += 1
                        processed_msg_ids.add(msg_id)
                        save_processed_id(args.processed_ids, msg_id)
                        continue

                    log(f"    Transcribing...")
                    transcript = transcribe_with_groq(groq_key, tmp_wav)

                    result = {
                        "ghl_message_id": msg_id,
                        "ghl_contact_id": contact_id,
                        "conversation_id": convo_id,
                        "call_date": date_added,
                        "duration": duration,
                        "direction": direction,
                        "call_status": "completed",
                        "transcript": transcript,
                    }
                    print(json.dumps(result), flush=True)

                    processed_msg_ids.add(msg_id)
                    save_processed_id(args.processed_ids, msg_id)
                    transcribed_count += 1
                    log(f"    Done ({len(transcript)} chars)")

                except requests.exceptions.HTTPError as e:
                    log(f"    HTTP error: {e}")
                    error_count += 1
                    if e.response and e.response.status_code == 429:
                        retry_after = int(e.response.headers.get("Retry-After", 60))
                        log(f"    Rate limited. Waiting {retry_after}s...")
                        time.sleep(retry_after)
                    continue
                except Exception as e:
                    log(f"    Error: {e}")
                    error_count += 1
                    continue
                finally:
                    if os.path.exists(tmp_wav):
                        os.remove(tmp_wav)

            time.sleep(0.5)

        # If we processed all messages for this contact and didn't hit batch limit,
        # mark the contact as fully done
        if not has_more and transcribed_count < args.batch_size:
            if args.processed_contacts:
                with open(args.processed_contacts, "a") as f:
                    f.write(contact_id + "\n")
            processed_contact_ids.add(contact_id)

        time.sleep(0.3)

    log(f"\n--- Summary ---")
    log(f"Contacts scanned: {contacts_scanned}")
    log(f"Calls transcribed: {transcribed_count}")
    log(f"Calls skipped (voicemail/no-answer/already done): {skipped_count}")
    log(f"Errors: {error_count}")


if __name__ == "__main__":
    main()
