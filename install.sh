#!/usr/bin/env bash
# install.sh -- symlink kr-brand-decks skills into ~/.claude/skills so Claude Code
# discovers them. Usage:
#   ./install.sh                 # link ALL company skills
#   ./install.sh samsung-semi sk-hynix   # link only the named ones
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"

if [ "$#" -gt 0 ]; then
  slugs=("$@")
else
  slugs=()
  for d in "$REPO"/skills/deck-*/; do
    slugs+=("$(basename "$d" | sed 's/^deck-//')")
  done
fi

n=0
for s in "${slugs[@]}"; do
  src="$REPO/skills/deck-$s"
  if [ ! -d "$src" ]; then
    echo "skip: no skill deck-$s" >&2
    continue
  fi
  ln -sfn "$src" "$DEST/deck-$s"
  echo "linked  deck-$s  ->  $DEST/deck-$s"
  n=$((n + 1))
done

echo ""
echo "Installed $n skill(s) into $DEST"
echo "Restart Claude Code (or /reload-plugins) to pick them up."
echo "Engine lives at: $REPO/_engine  (skills call it by relative path)."
