#!/usr/bin/env bash
# install_fonts.sh -- install Pretendard (free KR font) so decks render cleanly.
# WHY: without a real KR font installed, LibreOffice/PowerPoint substitute the font
# name "Pretendard" with whatever it finds -- often a BRUSH/handwriting font -- which
# is exactly the "손글씨" (handwriting) look you want to avoid. Installing Pretendard
# fixes every deck at once.
set -euo pipefail

VER="v1.3.9"
BASE="https://raw.githubusercontent.com/orioncactus/pretendard/${VER}/packages/pretendard/dist/public/static"

case "$(uname -s)" in
  Darwin) DEST="$HOME/Library/Fonts" ;;
  *)      DEST="$HOME/.fonts" ;;
esac
mkdir -p "$DEST"

n=0
for f in Pretendard-Regular.otf Pretendard-Medium.otf Pretendard-SemiBold.otf Pretendard-Bold.otf; do
  if curl -fsSL "$BASE/$f" -o "$DEST/$f" && [ -s "$DEST/$f" ]; then
    echo "installed $f"
    n=$((n + 1))
  else
    echo "failed: $f" >&2
  fi
done

# refresh font cache (Linux / fontconfig; harmless if fc-cache absent)
command -v fc-cache >/dev/null 2>&1 && fc-cache -f "$DEST" >/dev/null 2>&1 || true

echo ""
echo "Installed $n Pretendard weight(s) into $DEST"
echo "Verify:  fc-match Pretendard   (should print a Pretendard file)"
echo "Now re-render your decks and the handwriting substitution is gone."
