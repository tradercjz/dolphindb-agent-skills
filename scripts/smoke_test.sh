#!/usr/bin/env bash
# End-to-end smoke test for dolphindb-agent-skills.
#
# What this does:
#   1. Creates a throwaway venv at /tmp/ddb-venv.
#   2. Installs the repo in editable mode.
#   3. Runs the _patch_skill_connection unit tests.
#   4. Drives the interactive installer non-interactively (via `expect`)
#      against a sandbox project at /tmp/ddb-sandbox, feeding in test
#      connection values.
#   5. Hard-checks that the shipped default values (127.0.0.1 / 8848 /
#      admin / 123456) are completely absent from the patched SKILL.md,
#      and that the new values are present.
#
# Usage:
#     bash scripts/smoke_test.sh [HOST] [PORT] [USER] [PASSWD]
#
# Defaults mirror the user's real setup; override on the command line
# if you want to smoke-test against a different server. The installer
# only asks for these values — it does NOT try to reach the server,
# so any syntactically valid value will pass the test.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="/tmp/ddb-venv"
SANDBOX="/tmp/ddb-sandbox"

HOST="${1:-192.168.100.43}"
PORT="${2:-8742}"
USER_="${3:-admin}"
PASSWD="${4:-DolphinDB123456}"

echo "============================================================"
echo " dolphindb-agent-skills smoke test"
echo "------------------------------------------------------------"
echo "  repo    : $REPO_ROOT"
echo "  venv    : $VENV"
echo "  sandbox : $SANDBOX"
echo "  DDB     : $USER_@$HOST:$PORT  (password hidden)"
echo "============================================================"

# ── 0. prerequisites ────────────────────────────────────────────
command -v expect >/dev/null 2>&1 || {
    echo "❌ 'expect' is required. Install with:  brew install expect"
    exit 1
}

# ── 1. venv + editable install ─────────────────────────────────
if [ ! -d "$VENV" ]; then
    echo "[1/5] Creating venv at $VENV"
    python3 -m venv "$VENV"
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -e "$REPO_ROOT"
echo "[1/5] ✅ editable install done"

# ── 2. unit tests for _patch_skill_connection ──────────────────
echo "[2/5] Running patch unit tests"
python - <<PYEOF
import sys, tempfile, shutil, types
from pathlib import Path
ROOT = Path("$REPO_ROOT")
sys.path.insert(0, str(ROOT / "src"))
stub = types.ModuleType("questionary")
stub.Style = type("S", (), {"__init__": lambda self, *a, **k: None})
for n in ("text", "select", "confirm", "password", "checkbox", "Choice"):
    setattr(stub, n, lambda *a, **k: None)
sys.modules["questionary"] = stub
from dolphindb_skill_installer.main import _patch_skill_connection
def run(h,p,u,w):
    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / "SKILL.md"
        shutil.copy(ROOT / "skills/dolphindb-runtime/SKILL.md", dst)
        _patch_skill_connection(dst, h, p, u, w)
        return dst.read_text()
t = run("192.168.100.43", "8742", "myuser", "S3cret!")
assert "127.0.0.1" not in t and "8848" not in t
assert 's.connect("192.168.100.43", 8742, "myuser", "S3cret!")' in t
t = run("10.0.0.5", "8903", "joe", "admin")
assert 's.connect("10.0.0.5", 8903, "joe", "admin")' in t
t = run("10.0.0.5", "8903", "123456", "hunter2")
assert 's.connect("10.0.0.5", 8903, "123456", "hunter2")' in t
print("  patch unit tests OK")
PYEOF
echo "[2/5] ✅ unit tests passed"

# ── 3. clean sandbox ────────────────────────────────────────────
rm -rf "$SANDBOX"
mkdir -p "$SANDBOX"
echo "[3/5] ✅ sandbox reset at $SANDBOX"

# ── 4. drive installer via expect ───────────────────────────────
echo "[4/5] Driving installer interactively (via expect)"
expect <<EXPECT_EOF
set timeout 30
log_user 1
spawn -noecho env -i HOME=$HOME PATH=$PATH bash -c "cd $SANDBOX && dolphindb-agent-skills"

# Step 1: Tool selector — default is the first entry (Claude Code). Enter.
expect "Choose one tool"
send "\r"

# Step 2: Install into project directory? (Y/n) → Enter = Y
expect "Install skills into this project directory"
send "\r"

# Step 3: checkbox. Both skills default-checked. Enter confirms.
expect "Choose skills"
send "\r"

# Step 5: connection info (no yes/no prompt anymore; straight into fields)
expect "DDB host:"
send "$HOST\r"
expect "DDB port:"
send "$PORT\r"
expect "DDB user:"
send "$USER_\r"
expect "DDB password:"
send "$PASSWD\r"

expect eof
EXPECT_EOF
echo "[4/5] ✅ installer finished"

# ── 5. hard-check produced files ────────────────────────────────
echo "[5/5] Hard-checking produced skill files"
SKILL="$SANDBOX/.claude/skills/dolphindb-runtime/SKILL.md"
KB="$SANDBOX/.claude/skills/dolphindb/SKILL.md"

[ -f "$SKILL" ] || { echo "❌ missing $SKILL"; exit 1; }
[ -f "$KB" ]    || { echo "❌ missing $KB";    exit 1; }

fail=0

# default HOST/PORT must be gone
for bad in "127.0.0.1" "8848"; do
    if grep -q "$bad" "$SKILL"; then
        echo "  ❌ default '$bad' still present in $SKILL"
        fail=1
    fi
done

# default PASSWD must be gone (unless the user deliberately kept it)
if [ "$PASSWD" != "123456" ] && grep -q "\"123456\"" "$SKILL"; then
    echo "  ❌ default password still present in $SKILL"
    fail=1
fi

# new values must appear in at least one s.connect(...)
if ! grep -q "s.connect(\"$HOST\", $PORT, \"$USER_\", \"$PASSWD\"" "$SKILL"; then
    echo "  ❌ patched s.connect line not found in $SKILL"
    echo "     (expected: s.connect(\"$HOST\", $PORT, \"$USER_\", \"$PASSWD\", ...))"
    fail=1
fi

# knowledge skill must be untouched (still contains its name frontmatter)
grep -q "^name: dolphindb$" "$KB" || { echo "  ❌ dolphindb KB looks corrupted"; fail=1; }

if [ $fail -eq 0 ]; then
    echo "[5/5] ✅ all assertions passed"
    echo ""
    echo "============================================================"
    echo " 🎉 smoke test passed — skill is ready to publish"
    echo "============================================================"
    echo "  Patched connect lines in dolphindb-runtime:"
    grep -n "s.connect" "$SKILL" | sed 's/^/    /'
else
    echo ""
    echo "❌ smoke test FAILED — see messages above"
    exit 1
fi
