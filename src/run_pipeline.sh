#!/bin/zsh
#
# Full transcription pipeline — launch once, processes ALL contacts and calls.
#
# Extract contacts → split across parallel workers → transcribe ALL calls →
# insert into Supabase → repeat until every contact is done.
#
# Usage:
#   ./src/run_pipeline.sh [NUM_WORKERS]
#
# Default: 4 parallel workers. Each worker processes its chunk of contacts
# until all calls are transcribed. Progress is tracked per-worker so it
# survives interrupts — just re-run to resume.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_DIR/.env"

NUM_WORKERS="${1:-2}"
CALLS_PER_ROUND=100  # How many calls each worker does per loop iteration

DATA_DIR="$PROJECT_DIR/pipeline_data"
mkdir -p "$DATA_DIR"

CONTACT_IDS_FILE="$DATA_DIR/contact_ids.txt"
LOG_DIR="$DATA_DIR/logs"
mkdir -p "$LOG_DIR"

echo "=== Claim Warriors Full Transcription Pipeline ==="
echo "Workers: $NUM_WORKERS"
echo "Data dir: $DATA_DIR"
echo "Started: $(date)"
echo ""

# ── Step 1: Extract contact IDs (skip if already done) ──
if [ ! -f "$CONTACT_IDS_FILE" ] || [ ! -s "$CONTACT_IDS_FILE" ]; then
    echo "[Step 1] Extracting contact IDs from completed contracts..."
    GHL_KEY=$(grep '^CLAIM_WARRIOR_GHL_API_KEY=' "$ENV_FILE" | cut -d'=' -f2-)
    python3 "$SCRIPT_DIR/extract_contract_contacts.py" "$GHL_KEY" > "$CONTACT_IDS_FILE" 2>"$LOG_DIR/extract.log"
    TOTAL=$(wc -l < "$CONTACT_IDS_FILE" | tr -d ' ')
    echo "  Extracted $TOTAL unique contact IDs"
else
    TOTAL=$(wc -l < "$CONTACT_IDS_FILE" | tr -d ' ')
    echo "[Step 1] Contact IDs already extracted ($TOTAL contacts). Skipping."
fi
echo ""

# ── Step 2: Split contacts into chunks (only if not already split) ──
NEED_SPLIT=false
for i in $(seq 0 $((NUM_WORKERS - 1))); do
    if [ ! -f "$DATA_DIR/worker_${i}_contacts.txt" ]; then
        NEED_SPLIT=true
        break
    fi
done

if $NEED_SPLIT; then
    echo "[Step 2] Splitting $TOTAL contacts across $NUM_WORKERS workers..."
    LINES_PER_CHUNK=$(( (TOTAL + NUM_WORKERS - 1) / NUM_WORKERS ))

    # Use gsplit if available (macOS), otherwise split
    if command -v gsplit &>/dev/null; then
        SPLIT_CMD=gsplit
    else
        SPLIT_CMD=split
    fi

    $SPLIT_CMD -l "$LINES_PER_CHUNK" -d -a 1 "$CONTACT_IDS_FILE" "$DATA_DIR/chunk_"

    for i in $(seq 0 $((NUM_WORKERS - 1))); do
        CHUNK_SRC="$DATA_DIR/chunk_$i"
        CHUNK_DST="$DATA_DIR/worker_${i}_contacts.txt"
        if [ -f "$CHUNK_SRC" ]; then
            mv "$CHUNK_SRC" "$CHUNK_DST"
            COUNT=$(wc -l < "$CHUNK_DST" | tr -d ' ')
            echo "  Worker $i: $COUNT contacts"
        fi
    done
else
    echo "[Step 2] Workers already have contact chunks. Resuming."
    for i in $(seq 0 $((NUM_WORKERS - 1))); do
        F="$DATA_DIR/worker_${i}_contacts.txt"
        if [ -f "$F" ]; then
            TOTAL_C=$(wc -l < "$F" | tr -d ' ')
            DONE_C=0
            if [ -f "$DATA_DIR/worker_${i}_processed_contacts.txt" ]; then
                DONE_C=$(wc -l < "$DATA_DIR/worker_${i}_processed_contacts.txt" | tr -d ' ')
            fi
            echo "  Worker $i: $DONE_C/$TOTAL_C contacts done"
        fi
    done
fi
echo ""

# ── Step 3: Loop until all contacts are processed ──
ROUND=0
while true; do
    ROUND=$((ROUND + 1))

    # Check how many contacts are left across all workers
    ALL_DONE=true
    for i in $(seq 0 $((NUM_WORKERS - 1))); do
        WORKER_CONTACTS="$DATA_DIR/worker_${i}_contacts.txt"
        WORKER_DONE="$DATA_DIR/worker_${i}_processed_contacts.txt"
        if [ ! -f "$WORKER_CONTACTS" ]; then continue; fi

        TOTAL_C=$(wc -l < "$WORKER_CONTACTS" | tr -d ' ')
        DONE_C=0
        if [ -f "$WORKER_DONE" ]; then
            DONE_C=$(wc -l < "$WORKER_DONE" | tr -d ' ')
        fi
        if [ "$DONE_C" -lt "$TOTAL_C" ]; then
            ALL_DONE=false
            break
        fi
    done

    if $ALL_DONE; then
        echo "[Round $ROUND] All contacts fully processed!"
        break
    fi

    echo "[Round $ROUND] Launching $NUM_WORKERS workers ($CALLS_PER_ROUND calls each)..."

    # Launch workers in parallel
    WORKER_PIDS=()
    for i in $(seq 0 $((NUM_WORKERS - 1))); do
        WORKER_CONTACTS="$DATA_DIR/worker_${i}_contacts.txt"
        WORKER_OUTPUT="$DATA_DIR/worker_${i}_output.jsonl"
        WORKER_PROCESSED_MSGS="$DATA_DIR/worker_${i}_processed_msgs.txt"
        WORKER_PROCESSED_CONTACTS="$DATA_DIR/worker_${i}_processed_contacts.txt"
        WORKER_LOG="$LOG_DIR/worker_${i}_round_${ROUND}.log"

        if [ ! -f "$WORKER_CONTACTS" ]; then continue; fi

        # Skip if this worker is fully done
        TOTAL_C=$(wc -l < "$WORKER_CONTACTS" | tr -d ' ')
        DONE_C=0
        if [ -f "$WORKER_PROCESSED_CONTACTS" ]; then
            DONE_C=$(wc -l < "$WORKER_PROCESSED_CONTACTS" | tr -d ' ')
        fi
        if [ "$DONE_C" -ge "$TOTAL_C" ]; then
            echo "  Worker $i: already done, skipping"
            continue
        fi

        python3 "$SCRIPT_DIR/transcribe_calls.py" \
            --env-file "$ENV_FILE" \
            --contact-ids "$WORKER_CONTACTS" \
            --batch-size "$CALLS_PER_ROUND" \
            --processed-ids "$WORKER_PROCESSED_MSGS" \
            --processed-contacts "$WORKER_PROCESSED_CONTACTS" \
            >> "$WORKER_OUTPUT" \
            2>"$WORKER_LOG" &

        WORKER_PIDS+=($!)
        echo "  Worker $i started (PID $!), $DONE_C/$TOTAL_C contacts done"
    done

    # Wait for all workers
    FAILED=0
    for PID in "${WORKER_PIDS[@]}"; do
        if ! wait "$PID" 2>/dev/null; then
            FAILED=$((FAILED + 1))
        fi
    done

    if [ "$FAILED" -gt 0 ]; then
        echo "  WARNING: $FAILED worker(s) had errors this round (check logs)"
    fi

    # Insert this round's results into Supabase
    MERGED="$DATA_DIR/round_${ROUND}.jsonl"
    for i in $(seq 0 $((NUM_WORKERS - 1))); do
        WORKER_OUTPUT="$DATA_DIR/worker_${i}_output.jsonl"
        if [ -f "$WORKER_OUTPUT" ] && [ -s "$WORKER_OUTPUT" ]; then
            cat "$WORKER_OUTPUT" >> "$MERGED"
            : > "$WORKER_OUTPUT"
        fi
    done

    if [ -f "$MERGED" ] && [ -s "$MERGED" ]; then
        ROWS=$(wc -l < "$MERGED" | tr -d ' ')
        echo "  Inserting $ROWS transcriptions into Supabase..."
        python3 "$SCRIPT_DIR/supabase_insert.py" \
            --env-file "$ENV_FILE" \
            --jsonl "$MERGED" \
            2>"$LOG_DIR/insert_round_${ROUND}.log"
        INSERTED=$(grep -c "Inserted" "$LOG_DIR/insert_round_${ROUND}.log" 2>/dev/null || echo 0)
        echo "  Supabase insert done ($INSERTED new rows)"
    else
        echo "  No new transcriptions this round"
    fi

    # Progress summary
    TOTAL_MSGS=0
    TOTAL_CONTACTS_DONE=0
    for i in $(seq 0 $((NUM_WORKERS - 1))); do
        F="$DATA_DIR/worker_${i}_processed_msgs.txt"
        G="$DATA_DIR/worker_${i}_processed_contacts.txt"
        if [ -f "$F" ]; then TOTAL_MSGS=$((TOTAL_MSGS + $(wc -l < "$F" | tr -d ' '))); fi
        if [ -f "$G" ]; then TOTAL_CONTACTS_DONE=$((TOTAL_CONTACTS_DONE + $(wc -l < "$G" | tr -d ' '))); fi
    done
    echo "  Progress: $TOTAL_CONTACTS_DONE/$TOTAL contacts done, $TOTAL_MSGS messages processed"
    echo ""
done

# ── Final Summary ──
echo ""
echo "=== Pipeline Complete ==="
echo "Finished: $(date)"
TOTAL_MSGS=0
TOTAL_CONTACTS_DONE=0
for i in $(seq 0 $((NUM_WORKERS - 1))); do
    F="$DATA_DIR/worker_${i}_processed_msgs.txt"
    G="$DATA_DIR/worker_${i}_processed_contacts.txt"
    if [ -f "$F" ]; then TOTAL_MSGS=$((TOTAL_MSGS + $(wc -l < "$F" | tr -d ' '))); fi
    if [ -f "$G" ]; then TOTAL_CONTACTS_DONE=$((TOTAL_CONTACTS_DONE + $(wc -l < "$G" | tr -d ' '))); fi
done
echo "Total contacts processed: $TOTAL_CONTACTS_DONE/$TOTAL"
echo "Total call messages processed: $TOTAL_MSGS"
echo "All transcriptions have been inserted into Supabase."
