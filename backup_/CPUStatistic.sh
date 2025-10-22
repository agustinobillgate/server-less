#!/bin/bash

LOG_FILE="cpu_stats.log"

# Function to read CPU stats
read_cpu() {
    read -r -a CPU < <(grep '^cpu ' /proc/stat)
    # Fields:
    # 0=cpu  1=user  2=nice  3=system  4=idle  5=iowait  6=irq  7=softirq  8=steal
    TOTAL=0
    for i in "${CPU[@]:1}"; do
        TOTAL=$((TOTAL + i))
    done
    echo "${CPU[1]} ${CPU[2]} ${CPU[3]} ${CPU[4]} ${CPU[5]} ${CPU[6]} ${CPU[7]} ${CPU[8]} $TOTAL"
}

# Initial read
read PREV_USER PREV_NICE PREV_SYS PREV_IDLE PREV_IOWAIT PREV_IRQ PREV_SOFTIRQ PREV_STEAL PREV_TOTAL < <(read_cpu)

echo "Logging CPU stats to $LOG_FILE (Press Ctrl+C to stop)"
echo "--------------------------------------------------------------------"

while true; do
    sleep 1
    read USER NICE SYS IDLE IOWAIT IRQ SOFTIRQ STEAL TOTAL < <(read_cpu)

    # Compute deltas
    DIFF_USER=$((USER - PREV_USER))
    DIFF_NICE=$((NICE - PREV_NICE))
    DIFF_SYS=$((SYS - PREV_SYS))
    DIFF_IDLE=$((IDLE - PREV_IDLE))
    DIFF_IOWAIT=$((IOWAIT - PREV_IOWAIT))
    DIFF_IRQ=$((IRQ - PREV_IRQ))
    DIFF_SOFTIRQ=$((SOFTIRQ - PREV_SOFTIRQ))
    DIFF_STEAL=$((STEAL - PREV_STEAL))
    DIFF_TOTAL=$((TOTAL - PREV_TOTAL))

    # Avoid divide by zero
    ((DIFF_TOTAL == 0)) && DIFF_TOTAL=1

    # Convert to percentages with 1 decimal place (using bc)
    US=$(echo "scale=1; 100 * $DIFF_USER / $DIFF_TOTAL" | bc)
    SY=$(echo "scale=1; 100 * $DIFF_SYS / $DIFF_TOTAL" | bc)
    NI=$(echo "scale=1; 100 * $DIFF_NICE / $DIFF_TOTAL" | bc)
    ID=$(echo "scale=1; 100 * $DIFF_IDLE / $DIFF_TOTAL" | bc)
    WA=$(echo "scale=1; 100 * $DIFF_IOWAIT / $DIFF_TOTAL" | bc)
    HI=$(echo "scale=1; 100 * $DIFF_IRQ / $DIFF_TOTAL" | bc)
    SI=$(echo "scale=1; 100 * $DIFF_SOFTIRQ / $DIFF_TOTAL" | bc)
    ST=$(echo "scale=1; 100 * $DIFF_STEAL / $DIFF_TOTAL" | bc)

    TIMESTAMP=$(date +"%Y%m%d-%H:%M:%S")

    OUTPUT=$(printf "%s %%Cpu(s): %5.1f us, %5.1f sy, %5.1f ni, %5.1f id, %5.1f wa, %5.1f hi, %5.1f si, %5.1f st" \
        "$TIMESTAMP" "$US" "$SY" "$NI" "$ID" "$WA" "$HI" "$SI" "$ST")

    echo "$OUTPUT" | tee -a "$LOG_FILE"

    # Update previous
    PREV_USER=$USER
    PREV_NICE=$NICE
    PREV_SYS=$SYS
    PREV_IDLE=$IDLE
    PREV_IOWAIT=$IOWAIT
    PREV_IRQ=$IRQ
    PREV_SOFTIRQ=$SOFTIRQ
    PREV_STEAL=$STEAL
    PREV_TOTAL=$TOTAL
done

