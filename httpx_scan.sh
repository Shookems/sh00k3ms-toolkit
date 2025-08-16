#!/bin/bash

# Prompt for input
read -p "Enter a single endpoint (e.g., https://example.com) or path to file with targets: " input

# Timestamp for output file
timestamp=$(date +"%Y%m%d_%H%M%S")
output_file="httpx_results_$timestamp.txt"

# Check if input is a file
if [[ -f "$input" ]]; then
    echo "[*] Running httpx scan on file: $input"
    cat "$input" | httpx -title -tech-detect -status-code -server -tls -favicon -hash -json -o "$output_file"
else
    echo "[*] Running httpx scan on single endpoint: $input"
    echo "$input" | httpx -title -tech-detect -status-code -server -tls -favicon -hash -json -o "$output_file"
fi

# Pretty print summary
echo "[*] Scan complete. Output saved to $output_file"
jq -r '.url + " | " + (.status_code|tostring) + " | " + (.title // "No Title") + " | " + (.tech // [] | join(", "))' "$output_file"

