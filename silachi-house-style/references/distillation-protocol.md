# DISTILL: how the Silachi style is born and evolves

The goal is a style that is measurably the firm's own, built from documents the Partner already approved, not from Claude's defaults. DISTILL never changes `firm.json` without the Partner's approval.

## Step 1: Collect the approved set

Ask for 3 to 5 documents the Partner considers the firm's best work, in `.docx` form (a PDF tells you nothing about styles or numbering). Mix types if possible: one agreement, one client letter or memo, one filing. Record which ones the Partner loves and which are merely acceptable.

## Step 2: Fingerprint

```bash
python3 scripts/fingerprint.py approved/*.docx --json fingerprint.json
```

Read the consensus table. It measures: fonts and sizes by share of characters, body alignment, leading, space after, first-line indent, how headings are dressed, which numbering formats are in use, colors, tables and borders, sentence length, em-dash count, typed numbering, defined terms, and whether there is a signature page.

Also fingerprint `assets/directions` output if useful, but the approved set is the evidence.

## Step 3: Interview the Partner (five questions, one message)

1. When a client opens this, what should they feel in the first three seconds? (Pick: protected, impressed, informed, in good hands, other.)
2. Which of the approved documents is closest to "this is us," and what one thing about it would you change?
3. Point to the gallery (`scripts/gallery.py`): which direction is closest, and which is furthest from you?
4. Is there anything a judge, client, or opposing counsel has ever complimented or criticized about how your documents look or read?
5. Any hard constraints: a color that must or must not appear, a font the office lacks, a format a client demands?

## Step 4: Synthesize (the prompt Claude runs on itself)

> Using the fingerprint, the interview, and the current `firm.json`, propose the smallest set of numeric changes that moves the house style toward what the Partner already approves, while keeping the 80/20 balance (80% Judicial Prestige: serif voice, small-caps articles, earned hierarchy, justified text; 20% Boardroom Minimalist: sans labels, air, the At-a-Glance panel). Keep all five signature marks. For each change, state the current value, the proposed value, the evidence (a fingerprint number or an interview answer), and what the reader will notice. Do not propose anything that would put a non-Red-Book look on a court filing. Do not exceed eight changes in one round.

Present the result as a table:

| Setting | Now | Proposed | Evidence | Reader notices |
|---|---|---|---|---|

## Step 5: Show, do not tell

Write the proposal as a direction preset, e.g. `assets/directions/7-proposed-v1.1.json`, and run the gallery with the Partner's own content so the current house style and the proposal sit side by side. Show the image.

## Step 6: Approve and lock

Only after the Partner says yes:

1. Apply the changes to `assets/firm.json` and bump `version`.
2. Update the matching numbers in `references/house-style.md` and add a changelog row: version, date, what changed, why.
3. Delete the proposal preset (or rename it to keep as history).
4. Rebuild the sample and run `scripts/audit.py` to confirm it still clears.

## Distinctiveness, honestly

No one can prove a style is "statistically distinct from every firm." What makes this one distinct is the combination: oxblood rule above small-caps Roman articles, the sans eyebrow, the At-a-Glance panel on page 1, and run-in bold small-caps sections. Most firms use Times New Roman, centered bold caps headings, and no summary panel. Keep the combination and the style stays recognizably Silachi.
