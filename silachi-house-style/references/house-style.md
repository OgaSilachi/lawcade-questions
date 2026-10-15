# The Silachi Prestige Standard

SLF-HS-001 · Version 1.0 · Owner: Uwaoma-Silachi Nwogwugwu

The firm's sixth style. Eighty percent Judicial Prestige (editorial, law-review authority, serif voice, earned hierarchy), twenty percent Boardroom Minimalist (sans-serif labels, air, a cover summary a client can read in ten seconds). Every value below is a number, not an adjective, so two drafters produce the same page.

The exact values also live in `assets/firm.json`. The builder reads that file. When this document and `firm.json` disagree, `firm.json` wins and this document is out of date.

## 0. Precedence (read first)

| Document | What governs |
|---|---|
| Anything filed with a court (pleadings, motions, orders, discovery, disclosures, briefs) | The Red Book (`slf-red-book`, FIRM-OPS-009) and `slf-signature-block`. This standard adds nothing. Courts get Times New Roman, black, RB-100 to RB-700. |
| Letters, demands, records requests | Red Book Partner overrides for letters (letterhead built from the firm's last sent letter). This standard governs only the body voice rules in Section 9. |
| Client agreements, engagement agreements, settlement term sheets, client advisory memos, case reports, strategy briefings, proposals, firm guides, playbooks | **This standard, in full.** |

If a request is ambiguous, ask which bucket it falls in. Never put Garamond or oxblood on a court filing.

## 1. The five signature marks

These five marks are what make a page read as Silachi from across a conference table. A document missing any of them is not in house style.

1. **The Oxblood Rule.** A 0.75 pt rule in Silachi Oxblood (`#5C1A1B`) sits above every Article heading, full text width, 4 pt gap to the heading text.
2. **The Eyebrow.** Every title and every signature page opens with a small sans-serif label above it: Gill Sans MT, 8.5 pt, ALL CAPS, tracked +1.5 pt, oxblood.
3. **Small-Caps Articles.** Article headings are Garamond small caps, 14 pt, with the Roman numeral in oxblood.
4. **The At-a-Glance Panel.** Page 1 of every agreement and memo carries a two-column summary table (label / term) with hairline rules only. Clients read this first; judges reading an exhibit see the deal in one look.
5. **The Run-In Section.** Second-level sections open with a bold small-caps lead-in ending in a period, and the text runs on in the same paragraph. This is the F-pattern anchor: the eye drops down the left edge reading only the lead-ins.

## 2. Page

- Letter, 8.5 x 11. One section, with Different First Page on.
- Margins: 1.0" top and bottom, 1.15" left and right (the extra 0.15" is the air).
- Header 0.5", footer 0.5" from edge.

## 3. Type

| Role | Font | Size | Other |
|---|---|---|---|
| Body | Garamond | 12.5 pt | Ink `#1A1A1A`, justified, exactly 17 pt leading, 0 pt before, 9 pt after, widow and orphan control on |
| Title | Garamond | 26 pt | Small caps, letter spacing +0.5 pt, left aligned |
| Subtitle / meta line | Garamond | 11 pt | Italic, gray `#5F5F5F` |
| Eyebrow | Gill Sans MT | 8.5 pt | ALL CAPS, tracked +1.5 pt, oxblood |
| Article (Level 1) | Garamond | 14 pt | Small caps, tracked +0.75 pt, numeral in oxblood, Oxblood Rule above, 22 pt before, 8 pt after, keep with next |
| Section (Level 2) | Garamond | 12.5 pt | Run-in bold small-caps lead-in, number at 0", text at 0.5" |
| Subsection (Level 3) | Garamond | 12.5 pt | Number at 0.5", text at 1.0", no lead-in |
| Table label column | Gill Sans MT | 8.5 pt | ALL CAPS, tracked +1 pt, gray |
| Table value column | Garamond | 12 pt | Ink |
| Header / footer | Gill Sans MT | 8 pt | Tracked +1 pt, gray |
| Block quote | Garamond | 12 pt | 0.75" left and right, exactly 15 pt leading |

Only two typefaces ever: Garamond and Gill Sans MT. Fallbacks if a machine lacks them: EB Garamond, then Times New Roman; Gill Sans Nova, then Calibri.

## 4. Color

| Token | Hex | Use |
|---|---|---|
| Ink | `#1A1A1A` | All body text |
| Oxblood | `#5C1A1B` | Eyebrows, Article numerals, Oxblood Rule. Nothing else. |
| Graphite | `#5F5F5F` | Meta lines, table labels, header and footer |
| Hairline | `#BFBFBF` | Table rules |

Oxblood never colors a full sentence. **Court-safe mode** (`"court_safe": true` in the content file) turns every color to black for any document that may become a court exhibit and must photocopy cleanly.

## 5. Numbering (locked)

One Word multilevel list, defined once, wired to the heading styles. Numbers are never typed.

| Level | Format | Example | Number position | Text position |
|---|---|---|---|---|
| 1 Article | Upper Roman + period | `I.` | 0" | 0.5" |
| 2 Section | Upper letter + period | `A.` | 0" | 0.5" |
| 3 Subsection | Decimal + period | `1.` | 0.5" | 1.0" |

Level 2 restarts under each Article. Level 3 restarts under each Section. Cross references read `Section II.B.3`.

## 6. Page 1 anatomy

1. Eyebrow (document type, e.g. ENGAGEMENT AGREEMENT).
2. Title in small caps.
3. Meta line in italic graphite: `Prepared for [Client] · [Month D, YYYY] · Matter [No.]` (middle dots, never dashes).
4. Oxblood Rule.
5. At-a-Glance panel (4 to 8 rows).
6. Body begins.

First-page header: `SILACHI LAW FIRM, PLLC` in Gill Sans, tracked +3 pt, centered, with `11800 Magnolia Parkway, Suite 2117 · Manvel, Texas 77578` beneath it in graphite.

Pages 2+: header reads `SILACHI LAW FIRM, PLLC` at left and the short title at right. Footer reads the matter number at left and `Page X of Y` at right, both live fields.

## 7. Defined terms

Defined at first use in parentheses with curly quotes and bold: (the “**Client**”). After that, capitalized, never bold. No "hereinafter."

## 8. Signature page (locked)

- The last body paragraph ends the text; then a centered italic line: *[Signature page follows.]*
- Hard page break.
- Eyebrow `SIGNATURE PAGE`, then the attestation sentence.
- A borderless two-column table, one party per cell, rows set to not break across pages. Each cell: party name in small caps, 30 pt of space, a 2.75" signature line, then `Name:`, `Title:`, `Date:`.
- The firm's cell uses `THE SILACHI LAW FIRM, PLLC`, `By: Uwaoma-Silachi Nwogwugwu`, `Texas State Bar No. 24118480`.
- Nothing else on the signature page.

## 9. Voice (applies to every firm document, court filings included)

- No em dashes and no en dashes in prose. Use a comma, colon, semicolon, or parentheses.
- Sentences average 22 words or fewer. No sentence over 40.
- Lead with the conclusion, then the reason.
- No "hereinafter," "witnesseth," "said" as an adjective, or "and/or."
- Numbers: words for one through nine, digits from 10, always digits for money, dates, and percentages. Money as `$12,500.00` in agreements.
- Dates as `October 15, 2026`.
- No italics for emphasis. Bold only for defined terms and lead-ins.

## 10. What the style forbids

- Any third typeface. Any color outside Section 4.
- Typed numbering, manual tabs to fake indents, empty paragraphs for spacing.
- Centered body text. Underlined headings (that is the Red Book court look; it stays in court).
- Tables with vertical borders.
- A signature block that can split across pages.

## Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-15 | Birth of the standard. Values seeded from the 80/20 Judicial Prestige / Boardroom Minimalist synthesis. Run DISTILL on the firm's approved documents to tune them. |
