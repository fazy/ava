#!/usr/bin/env bash

set -euo pipefail

# Try out various scenarios
# Automates generating the output but requires manual verification for now
#
# >-- NB. Running the tests uses credits and may incur charges --<

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd "$SCRIPT_DIR/.."
source .venv/bin/activate

IFS=$'\n'
parameters="$(cat << EOF
default         ping.txt    default-ping.txt
code-love       code.py     code-love.txt
code-doc        code.py     code-doc.txt
code-review     code.py     code-review.txt
code-summary    code.py     code-summary.txt
text-love       text.txt    text-love.txt
text-review     text.txt    text-review.txt
text-summary    text.txt    text-summary.txt
EOF
)"

for parameter in $parameters; do
    profile="$(echo "$parameter" | awk '{print $1}')"
    in_file="$(echo "$parameter" | awk '{print $2}')"
    out_file="$(echo "$parameter" | awk '{print $3}')"
    echo python ava/ava.py \
        --profile-dir example-profiles \
        --profile "$profile" \
        --in-file test/input/"$in_file" \
        --out-file test/output/"$out_file"
done
