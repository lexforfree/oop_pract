#!/usr/bin/env bash
# Прогоняет все demo_*.py через python и через mypy, печатая оба вывода
# рядом - лучший способ увидеть разрыв между "выполнится" и "типобезопасно".
set -u
cd "$(dirname "$0")"

files=(
  demo_invariant_ok.py
  demo_invariant_fail.py
  demo_covariant_ok.py
  demo_covariant_fail.py
  demo_contravariant_ok.py
  demo_contravariant_fail.py
  demo_producer_consumer.py
)

for f in "${files[@]}"; do
  echo "=============================================================="
  echo "FILE: $f"
  echo "--------------------------------------------------------------"
  echo "--- mypy $f ---"
  mypy "$f" --config-file mypy.ini
  echo
  echo "--- python $f ---"
  python3 "$f"
  echo
done