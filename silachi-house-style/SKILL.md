---
name: silachi-house-style
description: "The Silachi Prestige Standard (SLF-HS-001): Silachi Law Firm's own document look and voice, 80% Judicial Prestige and 20% Boardroom Minimalist, locked into a .docx builder so every agreement, client memo, case report, proposal, and firm guide comes out identical and unmistakably Silachi. Four modes: BUILD a document in house style, AUDIT a draft against it, show the GALLERY of style directions, and DISTILL the firm's approved documents to evolve the style. Use whenever the user asks for anything in house style, the Silachi look, firm style, our template, a client-facing agreement, engagement agreement, term sheet, advisory memo, case report, or proposal; asks to make a document look like the firm, check a document against house style, tune or evolve the style, compare style options, or see a gallery; or uploads approved documents and asks what makes them work. Court filings stay with slf-red-book; this skill then applies only its voice rules."
---

# Silachi House Style

The firm's sixth style, born from a gallery of five. Claude has no style gallery and drifts to a generic AI look unless it is locked in. This skill is the lock: the look lives in `assets/firm.json`, the rules live in `references/house-style.md`, and the scripts make it impossible to drift.

## Step 0: route the document

Decide the bucket before touching anything. See `references/house-style.md` Section 0.

| The document is... | Do this |
|---|---|
| A court filing (pleading, motion, order, discovery, disclosure, brief) | Hand layout to `slf-red-book` and `slf-signature-block`. From this skill apply only the voice rules: run `audit.py --voice-only`. Never put Garamond or oxblood on a filing. |
| A letter, demand, or records request | Red Book letter overrides govern layout. Apply voice rules only (`--voice-only`). |
| An agreement, engagement agreement, term sheet, client memo, case report, strategy briefing, proposal, firm guide, or playbook | Full house style. Use BUILD. |

If unsure, ask the user which bucket. If the document may become a court exhibit that will be photocopied, set `"court_safe": true` (all black, same layout).

## Mode 1: BUILD

1. Read `references/house-style.md` (the canon) and `references/content-schema.md` (the input format).
2. Write the document's words as a content JSON file. The words follow Section 9 voice rules. Use the sample `assets/sample_engagement.json` as the pattern.
3. Build:
   ```bash
   python3 scripts/build.py content.json "OUTPUT.docx"
   ```
4. Audit, and fix every FAIL before delivering:
   ```bash
   python3 scripts/audit.py "OUTPUT.docx"
   ```
   Unresolved `[PLACEHOLDER]` tokens fail on purpose. A template may ship with them; a client document may not.
5. Render page 1 and look at it (`soffice --headless --convert-to pdf`, then `pdftoppm -r 70 -png -f 1 -l 1`). Check the five signature marks in Section 1 of the canon are all visible.
6. Name the file per `slf-naming-conventions` if that skill is available.

Never hand-format a house-style document in Word XML or with the generic docx skill. The builder is the only way in, because the builder is what keeps the style locked.

## Mode 2: AUDIT

```bash
python3 scripts/audit.py draft.docx            # full house style
python3 scripts/audit.py filing.docx --voice-only   # court filings and letters
```

Report the table to the user. FAIL means fix before it leaves the office. WARN means look and decide.

## Mode 3: GALLERY

When the user wants to see options, compare looks, or is unsure what they like:

```bash
python3 scripts/gallery.py assets/sample_engagement.json OUT_DIR
```

This builds the same content in all six directions in `assets/directions/` (Texas Sovereign, Boardroom Minimalist, Judicial Prestige, Legacy Brief, Modern Counsel, Silachi Prestige) and writes `OUT_DIR/gallery.png`, a side-by-side contact sheet of page 1. Show the user the image. Pass the user's own content file instead of the sample to see their real document in every direction.

To try a new direction, add a JSON file to `assets/directions/` holding only the values that differ from `firm.json`. Knobs: `fonts`, `colors`, `page`, `panel` (At-a-Glance on or off), `body.align` (`justify` or `left`), `article.align` (`left` or `center`), `article.case` (`smallcaps` or `caps`), `article.font` (`sans` to use the sans face), `article.bold`, `article.underline`, `article.rule`, `article.double_rule`, plus every size and spacing value.

## Mode 4: DISTILL (how the style evolves and stays personal)

Run when the user uploads approved documents, says "make it more us," or wants to tune the style. Follow `references/distillation-protocol.md` exactly. In short: fingerprint the approved documents with `scripts/fingerprint.py`, interview the Partner with five questions, propose specific numeric changes to `firm.json` as a diff with a reason for each, render the before and after in the gallery, and change nothing until the Partner approves. Then bump the version and log it in the canon's changelog.

## Hard rules

- The five signature marks (canon Section 1) appear on every full house-style document.
- Two typefaces only: Garamond and Gill Sans MT. Four colors only, oxblood on marks and never on sentences.
- Numbers are never typed. The I / A / 1 list is the only list.
- No em dashes or en dashes anywhere in prose. This applies to Claude's chat replies about the document too.
- No invented facts, figures, names, or citations go into a document to fill a gap. Use a `[BRACKETED PLACEHOLDER]` and list it for the user.
- `firm.json` changes only through DISTILL with Partner approval.

## Files

- `references/house-style.md`: the canon, SLF-HS-001
- `references/content-schema.md`: content JSON format for BUILD
- `references/distillation-protocol.md`: the DISTILL procedure and the synthesis prompt
- `assets/firm.json`: every locked value the builder reads
- `assets/directions/`: the six gallery presets
- `assets/sample_engagement.json`: a placeholder engagement agreement
- `scripts/build.py`, `scripts/audit.py`, `scripts/gallery.py`, `scripts/fingerprint.py`

Scripts need `python-docx`; GALLERY also needs LibreOffice, `pdftoppm`, and Pillow. Rendered previews substitute fonts when Garamond and Gill Sans are not installed, so judge spacing and structure from previews and judge typefaces in Word.
