#!/usr/bin/env bash
#
# fetch_reference.sh
#
# Shallow-clones every git-hosted entry in MANIFEST.json at its pinned ref
# into ./samples/<id>-<name>/. Non-git entries (documentation pages, asset
# libraries such as Poly Haven / Kenney, the WCAG spec, the ISO catalogue
# record) are listed but NOT fetched by this script — visit their repo_url
# directly.
#
# ------------------------------------------------------------------------
# DISK WARNING — READ BEFORE RUNNING
# ------------------------------------------------------------------------
# Several entries are LARGE even as shallow (--depth 1) clones because the
# pinned ref's tree itself is heavy (bundled example/test assets):
#
#   REF-02  glTF-Sample-Assets   ~1.6+ GB   (multi-GB full history; the
#                                            tree at a single commit is
#                                            still hundreds of MB because
#                                            every sample model's binary
#                                            assets live directly in-tree)
#   REF-03  glTF-Sample-Viewer   ~300-500 MB shallow (submodule assets)
#   REF-07  three.js             ~150-200 MB shallow (examples/ textures)
#   REF-08  Babylon.js           ~150-250 MB shallow (playground assets)
#   REF-09  playcanvas/engine    ~50-100 MB shallow
#   REF-12  godotengine/godot    ~300-400 MB shallow (source only)
#
# Everything else (validators, docs pages, Blender add-on, KTX-Software,
# the two Godot demo-project subfolders) is small (a few MB to ~50 MB).
#
# Run with --small to SKIP any entry estimated over ~200 MB.
# This script does NOT delete or overwrite anything already cloned.
#
# Usage:
#   ./fetch_reference.sh            # fetch everything (can be many GB)
#   ./fetch_reference.sh --small    # skip entries estimated > ~200 MB
#
# Requires: git, python3, jq (optional — python3 fallback is used if
# jq is not installed), du, curl.
# ------------------------------------------------------------------------

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SCRIPT_DIR}/MANIFEST.json"
SAMPLES_DIR="${SCRIPT_DIR}/samples"
SMALL_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --small)
      SMALL_ONLY=true
      ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Usage: $0 [--small]" >&2
      exit 1
      ;;
  esac
done

if [[ ! -f "$MANIFEST" ]]; then
  echo "ERROR: MANIFEST.json not found at $MANIFEST" >&2
  exit 1
fi

mkdir -p "$SAMPLES_DIR"

# Approximate shallow-clone size in MB per repo id, used only to decide
# whether --small should skip it. These are estimates, not guarantees.
declare -A APPROX_MB=(
  [REF-01]=20
  [REF-02]=1700
  [REF-03]=400
  [REF-04]=5
  [REF-05]=60
  [REF-06]=15
  [REF-07]=180
  [REF-08]=200
  [REF-09]=80
  [REF-10]=10
  [REF-11]=10
  [REF-12]=350
)

# Non-git entries (documentation URLs / asset libraries) — informational
# only, this script does not fetch them.
NON_GIT_IDS="REF-13 REF-14 REF-15 REF-16 REF-17 REF-18 REF-19"

echo "=================================================================="
echo " URM reference-sample fetcher"
echo " Manifest: $MANIFEST"
echo " Target:   $SAMPLES_DIR"
echo " Mode:     $([ "$SMALL_ONLY" = true ] && echo 'SMALL (skip >~200MB)' || echo 'FULL (all sizes)')"
echo "=================================================================="

# Extract git entries (id, name, repo_url, ref) as TSV using python3 (jq
# not assumed present).
ENTRIES_TSV="$(python3 - "$MANIFEST" <<'PYEOF'
import json, sys
data = json.load(open(sys.argv[1]))
for e in data:
    url = e.get("repo_url", "")
    if "github.com" not in url:
        continue
    print(f"{e['id']}\t{e['name']}\t{url}\t{e['ref']}")
PYEOF
)"

CLONED_COUNT=0
SKIPPED_LARGE=0
SKIPPED_EXISTING=0
FAILED_COUNT=0

sanitize() {
  # Replace spaces, slashes, parens with hyphens for a filesystem-safe dir name.
  echo "$1" | tr ' /()&' '-----' | tr -s '-'
}

while IFS=$'\t' read -r id name url ref; do
  [[ -z "$id" ]] && continue

  safe_name="$(sanitize "$name")"
  dest="${SAMPLES_DIR}/${id}-${safe_name}"

  approx_mb="${APPROX_MB[$id]:-100}"

  if [[ "$SMALL_ONLY" = true && "$approx_mb" -gt 200 ]]; then
    echo "[SKIP-LARGE] $id ($name) ~${approx_mb} MB estimated, exceeds --small threshold"
    SKIPPED_LARGE=$((SKIPPED_LARGE + 1))
    continue
  fi

  if [[ -d "$dest/.git" ]]; then
    echo "[SKIP-EXISTS] $id ($name) already present at $dest"
    SKIPPED_EXISTING=$((SKIPPED_EXISTING + 1))
    # Still print the pinned SHA for verification even if skipped.
    actual_sha="$(git -C "$dest" rev-parse HEAD 2>/dev/null || echo 'unknown')"
    echo "  pinned ref: $ref | HEAD SHA: $actual_sha"
    continue
  fi

  echo "[CLONE] $id ($name) @ $ref -> $dest"
  mkdir -p "$dest"

  # Shallow clone at the pinned ref. Works for both branch names, tags,
  # and full commit SHAs (SHA case needs a full fetch of that commit,
  # so we fall back accordingly).
  if git clone --quiet --depth 1 --branch "$ref" "$url" "$dest" 2>/dev/null; then
    :
  else
    # ref is likely a raw commit SHA rather than a branch/tag name.
    rm -rf "$dest"
    mkdir -p "$dest"
    git init --quiet "$dest"
    (
      cd "$dest"
      git remote add origin "$url"
      git fetch --quiet --depth 1 origin "$ref"
      git checkout --quiet FETCH_HEAD
    ) || {
      echo "  [FAILED] could not fetch $id at ref $ref" >&2
      FAILED_COUNT=$((FAILED_COUNT + 1))
      continue
    }
  fi

  actual_sha="$(git -C "$dest" rev-parse HEAD 2>/dev/null || echo 'unknown')"
  echo "  pinned ref: $ref | cloned HEAD SHA: $actual_sha"
  CLONED_COUNT=$((CLONED_COUNT + 1))

done <<< "$ENTRIES_TSV"

echo ""
echo "=================================================================="
echo " Non-git reference entries (visit URL directly, not cloned):"
for id in $NON_GIT_IDS; do
  entry_line="$(python3 - "$MANIFEST" "$id" <<'PYEOF'
import json, sys
data = json.load(open(sys.argv[1]))
target = sys.argv[2]
for e in data:
    if e["id"] == target:
        print(f"  {e['id']}: {e['name']} -> {e['repo_url']}")
        break
PYEOF
)"
  echo "$entry_line"
done

echo ""
echo "=================================================================="
echo " Summary"
echo "   Cloned this run:      $CLONED_COUNT"
echo "   Skipped (existing):   $SKIPPED_EXISTING"
echo "   Skipped (--small):    $SKIPPED_LARGE"
echo "   Failed:                $FAILED_COUNT"

if [[ -d "$SAMPLES_DIR" ]]; then
  TOTAL_SIZE="$(du -sh "$SAMPLES_DIR" 2>/dev/null | cut -f1)"
  echo "   Total disk used (samples/): $TOTAL_SIZE"
else
  echo "   Total disk used (samples/): 0 (nothing cloned)"
fi
echo "=================================================================="
