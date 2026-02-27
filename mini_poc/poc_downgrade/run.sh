#!/usr/bin/env bash
set -euo pipefail

OUT="out/mini_poc/poc_downgrade"
mkdir -p "$OUT"

echo "[*] downgrade mini-poc (stub)" | tee "$OUT/log.txt"
echo "[OK] finished" | tee "$OUT/result.txt"
