"""
Cross-platform transcription pipeline.

Usage:
    Mac:     python3 src/run_pipeline.py --machine 1 --of 2 --workers 4
    Windows: python  src/run_pipeline.py --machine 2 --of 2 --workers 4

--machine N --of M: splits the contact list into M equal partitions and
processes partition N. This lets multiple machines work on different contacts
with no overlap.

Each machine creates its own pipeline_data/ folder locally (gitignored).
Progress is tracked per-worker and survives restarts.
"""

import argparse
import os
import subprocess
import sys
import time


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


def extract_contacts(script_dir, ghl_key, output_file, log_file):
    """Run extract_contract_contacts.py and save contact IDs."""
    print(f"[Step 1] Extracting contact IDs from completed contracts...")
    result = subprocess.run(
        [sys.executable, os.path.join(script_dir, "extract_contract_contacts.py"), ghl_key],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:500]}")
        sys.exit(1)
    with open(output_file, "w") as f:
        f.write(result.stdout)
    with open(log_file, "w") as f:
        f.write(result.stderr)
    count = len([l for l in result.stdout.strip().split("\n") if l.strip()])
    print(f"  Extracted {count} unique contact IDs")
    return count


def split_contacts(all_contacts, machine, total_machines):
    """Return this machine's partition of the contact list."""
    chunk_size = len(all_contacts) // total_machines
    remainder = len(all_contacts) % total_machines
    start = 0
    for i in range(1, machine):
        start += chunk_size + (1 if i <= remainder else 0)
    size = chunk_size + (1 if machine <= remainder else 0)
    return all_contacts[start:start + size]


def main():
    parser = argparse.ArgumentParser(description="Cross-platform transcription pipeline")
    parser.add_argument("--machine", type=int, default=1, help="This machine's number (1-indexed)")
    parser.add_argument("--of", type=int, default=1, dest="total_machines", help="Total number of machines")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers on this machine")
    parser.add_argument("--calls-per-round", type=int, default=100, help="Calls each worker processes per round")
    args = parser.parse_args()

    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    env_file = os.path.join(project_dir, ".env")
    data_dir = os.path.join(project_dir, "pipeline_data")
    log_dir = os.path.join(data_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    env = load_env(env_file)
    ghl_key = env.get("CLAIM_WARRIOR_GHL_API_KEY")
    if not ghl_key:
        print("ERROR: CLAIM_WARRIOR_GHL_API_KEY not found in .env")
        sys.exit(1)

    print(f"=== Claim Warriors Transcription Pipeline ===")
    print(f"Machine: {args.machine} of {args.total_machines}")
    print(f"Workers: {args.workers} | Calls per round: {args.calls_per_round}")
    print(f"Data dir: {data_dir}")
    print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Step 1: Extract all contact IDs
    all_contacts_file = os.path.join(data_dir, "contact_ids.txt")
    if not os.path.exists(all_contacts_file) or os.path.getsize(all_contacts_file) == 0:
        extract_contacts(script_dir, ghl_key, all_contacts_file, os.path.join(log_dir, "extract.log"))
    else:
        print(f"[Step 1] Contact IDs already extracted. Skipping.")

    with open(all_contacts_file) as f:
        all_contacts = [l.strip() for l in f if l.strip()]
    print(f"  Total contacts: {len(all_contacts)}")

    # Step 2: Get this machine's partition
    my_contacts = split_contacts(all_contacts, args.machine, args.total_machines)
    print(f"  This machine's contacts: {len(my_contacts)} (partition {args.machine}/{args.total_machines})")
    print()

    # Step 3: Split into worker chunks
    print(f"[Step 2] Setting up {args.workers} workers...")
    worker_chunks = []
    chunk_size = len(my_contacts) // args.workers
    remainder = len(my_contacts) % args.workers
    start = 0
    for i in range(args.workers):
        size = chunk_size + (1 if i < remainder else 0)
        worker_chunks.append(my_contacts[start:start + size])
        start += size

    prefix = f"m{args.machine}_"
    for i, chunk in enumerate(worker_chunks):
        chunk_file = os.path.join(data_dir, f"{prefix}worker_{i}_contacts.txt")
        # Only write if not already exists (preserve across restarts)
        if not os.path.exists(chunk_file):
            with open(chunk_file, "w") as f:
                f.write("\n".join(chunk) + "\n")
        count = sum(1 for l in open(chunk_file) if l.strip())
        done = 0
        done_file = os.path.join(data_dir, f"{prefix}worker_{i}_processed_contacts.txt")
        if os.path.exists(done_file):
            done = sum(1 for l in open(done_file) if l.strip())
        print(f"  Worker {i}: {done}/{count} contacts done")
    print()

    # Step 3: Loop until all contacts processed
    round_num = 0
    while True:
        round_num += 1

        # Check if all done
        all_done = True
        for i in range(args.workers):
            contacts_file = os.path.join(data_dir, f"{prefix}worker_{i}_contacts.txt")
            done_file = os.path.join(data_dir, f"{prefix}worker_{i}_processed_contacts.txt")
            total = sum(1 for l in open(contacts_file) if l.strip())
            done = 0
            if os.path.exists(done_file):
                done = sum(1 for l in open(done_file) if l.strip())
            if done < total:
                all_done = False
                break

        if all_done:
            print(f"[Round {round_num}] All contacts fully processed!")
            break

        print(f"[Round {round_num}] Launching {args.workers} workers...")

        # Launch workers
        processes = []
        for i in range(args.workers):
            contacts_file = os.path.join(data_dir, f"{prefix}worker_{i}_contacts.txt")
            processed_msgs = os.path.join(data_dir, f"{prefix}worker_{i}_processed_msgs.txt")
            processed_contacts = os.path.join(data_dir, f"{prefix}worker_{i}_processed_contacts.txt")
            output_file = os.path.join(data_dir, f"{prefix}worker_{i}_output.jsonl")
            worker_log = os.path.join(log_dir, f"{prefix}worker_{i}_round_{round_num}.log")

            # Skip if done
            total = sum(1 for l in open(contacts_file) if l.strip())
            done = 0
            if os.path.exists(processed_contacts):
                done = sum(1 for l in open(processed_contacts) if l.strip())
            if done >= total:
                print(f"  Worker {i}: done, skipping")
                continue

            log_fh = open(worker_log, "w")
            out_fh = open(output_file, "a")
            p = subprocess.Popen(
                [
                    sys.executable,
                    os.path.join(script_dir, "transcribe_calls.py"),
                    "--env-file", env_file,
                    "--contact-ids", contacts_file,
                    "--batch-size", str(args.calls_per_round),
                    "--processed-ids", processed_msgs,
                    "--processed-contacts", processed_contacts,
                ],
                stdout=out_fh,
                stderr=log_fh,
            )
            processes.append((i, p, log_fh, out_fh, done, total))
            print(f"  Worker {i} started (PID {p.pid}), {done}/{total} contacts done")

        # Wait for all
        failed = 0
        for i, p, log_fh, out_fh, _, _ in processes:
            ret = p.wait()
            log_fh.close()
            out_fh.close()
            if ret != 0:
                print(f"  Worker {i} FAILED (exit code {ret})")
                failed += 1
            else:
                print(f"  Worker {i} finished")

        # Progress summary
        total_msgs = 0
        total_contacts_done = 0
        total_contacts = 0
        for i in range(args.workers):
            msgs_file = os.path.join(data_dir, f"{prefix}worker_{i}_processed_msgs.txt")
            done_file = os.path.join(data_dir, f"{prefix}worker_{i}_processed_contacts.txt")
            contacts_file = os.path.join(data_dir, f"{prefix}worker_{i}_contacts.txt")
            if os.path.exists(msgs_file):
                total_msgs += sum(1 for l in open(msgs_file) if l.strip())
            if os.path.exists(done_file):
                total_contacts_done += sum(1 for l in open(done_file) if l.strip())
            total_contacts += sum(1 for l in open(contacts_file) if l.strip())
        print(f"  Progress: {total_contacts_done}/{total_contacts} contacts, {total_msgs} messages processed")
        if failed:
            print(f"  WARNING: {failed} worker(s) failed (check logs)")
        print()

    # Final summary
    print()
    print(f"=== Pipeline Complete ===")
    print(f"Finished: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    total_msgs = 0
    total_contacts_done = 0
    for i in range(args.workers):
        msgs_file = os.path.join(data_dir, f"{prefix}worker_{i}_processed_msgs.txt")
        done_file = os.path.join(data_dir, f"{prefix}worker_{i}_processed_contacts.txt")
        if os.path.exists(msgs_file):
            total_msgs += sum(1 for l in open(msgs_file) if l.strip())
        if os.path.exists(done_file):
            total_contacts_done += sum(1 for l in open(done_file) if l.strip())
    print(f"Contacts processed: {total_contacts_done}/{len(my_contacts)}")
    print(f"Messages processed: {total_msgs}")


if __name__ == "__main__":
    main()
