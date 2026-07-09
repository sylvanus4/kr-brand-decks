# Security

This repository is a collection of **Claude Code / Cursor skills that generate
PowerPoint (.pptx) files locally**. It is designed to be safe to install and run.
Security here is enforced by code and CI, not just claimed in prose.

## What these skills do — and do NOT do

| | |
|---|---|
| ✅ Run fully **locally** | `python-pptx` + `matplotlib` build slides on your machine. |
| ✅ **No data exfiltration** | Nothing you type is sent anywhere. There is no telemetry, no analytics, no phone-home. |
| ✅ **No secrets required** | The core deck generator needs no API key, no login, no network. |
| ⚙️ **Optional** AI hero images | Only if *you* set `OPENAI_API_KEY`. Without it, image slots degrade to placeholders. This is the **only** optional outbound call, and it is off by default. |
| ⚙️ **Optional** icon fetch | Line icons (if enabled) are fetched from the public Lucide GitHub raw URLs. Off by default; the sample decks use native shapes, no fetch. |
| 🚫 No logo files | We ship brand **color palettes** only. No company logo image is bundled. |
| 🚫 No shell/exec of untrusted input | The engine reads JSON specs and writes a .pptx. It does not eval or execute spec content. |

## Permissions each skill needs

- **Read/Write files** in the skill's own folder (spec, palette, `examples/`).
- **Run `python3`** to invoke `_engine/render_deck.py`.
- **Run `soffice` (LibreOffice)** *only if you pass `--pdf`* to export a PDF.

That's the full surface. No elevated permissions, no background daemons.

## Supply-chain hygiene (enforced in CI)

- **Secret scanning**: `gitleaks` + `pre-commit` run on every push/PR. The biggest risk
  in any skill marketplace is a secret leaking into a script — this is blocked at commit time.
- **No large binaries / private keys**: `detect-private-key` and a large-file guard run pre-commit.
- **Manifest validation**: `tools/validate_marketplace.py` (zero-dependency) verifies every
  plugin manifest and that each skill has a `SKILL.md` before merge.
- **Porting gate**: skills are authored to be free of absolute personal paths, `.venv`
  hardcodes, and repo-private script coupling, so they run on any machine.

## Reporting

Found something? Open a GitHub issue (omit any secret) or contact the maintainer.
