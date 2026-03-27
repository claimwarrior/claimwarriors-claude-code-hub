"""Extract all unique contact IDs from completed contracts in GHL."""

import requests
import sys
import time


GHL_API = "https://services.leadconnectorhq.com"
LOC_ID = "L58ZxauomnryKcGf1IjZ"


def main():
    api_key = sys.argv[1]
    headers = {
        "Authorization": api_key,
        "Version": "2021-07-28",
        "Accept": "application/json",
    }

    contact_ids = set()
    offset = 0
    page = 0

    while True:
        resp = requests.get(
            f"{GHL_API}/proposals/document",
            headers=headers,
            params={
                "locationId": LOC_ID,
                "status": "completed",
                "limit": 20,
                "skip": str(offset),
            },
        )
        if resp.status_code != 200:
            print(f"Error {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
            break

        data = resp.json()
        docs = data.get("documents", [])
        if not docs:
            break

        for doc in docs:
            for r in doc.get("recipients", []):
                cid = r.get("id")
                if cid:
                    contact_ids.add(cid)

        page += 1
        offset += len(docs)
        total = data.get("total", 0)
        print(
            f"Page {page}: {len(docs)} docs, {len(contact_ids)} unique contacts ({offset}/{total})",
            file=sys.stderr,
            flush=True,
        )

        if offset >= total:
            break

        time.sleep(0.3)

    print(f"\nTotal completed contracts: {offset}", file=sys.stderr)
    print(f"Unique contact IDs: {len(contact_ids)}", file=sys.stderr)

    # Output contact IDs to stdout (one per line)
    for cid in sorted(contact_ids):
        print(cid)


if __name__ == "__main__":
    main()
