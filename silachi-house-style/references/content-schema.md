# Content JSON for BUILD

The content file holds words and structure only. No fonts, sizes, or colors: those come from `assets/firm.json`.

```json
{
  "court_safe": false,
  "doc_type": "Engagement Agreement",
  "title": "Agreement for Legal Services",
  "short_title": "Engagement Agreement",
  "meta": "Prepared for Jane Doe · October 15, 2026 · Matter 18.0.00100-LIT",
  "matter_no": "18.0.00100-LIT",
  "at_a_glance": [["Client", "Jane Doe"], ["Retainer", "$5,000.00"]],
  "body": [ ...blocks... ],
  "signature": {
    "attestation": "The parties sign this Agreement to be effective on the Effective Date.",
    "parties": [{"name": "Jane Doe", "fields": ["Name", "Date"]}],
    "firm": true
  }
}
```

| Field | Required | Notes |
|---|---|---|
| `doc_type` | yes | Becomes the eyebrow above the title. Write it in title case; the style sets the caps. |
| `title` | yes | Small caps title. |
| `short_title` | no | Running header on pages 2+. Defaults to `title`. |
| `meta` | no | Italic line under the title. Separate items with ` · ` (middle dot), never a dash. |
| `matter_no` | no | Footer, left. |
| `at_a_glance` | no | 4 to 8 `[label, value]` rows. Omit for internal guides. |
| `signature` | no | Omit for memos and reports. `firm: true` adds the firm's block. |
| `court_safe` | no | `true` makes every color black. |

## Body blocks (in order)

| Block | Renders as |
|---|---|
| `{"article": "Scope of Representation"}` | Level 1: `II.` oxblood numeral, small caps, Oxblood Rule above |
| `{"section": "Included Services", "text": "..."}` | Level 2: `A.` with a bold small-caps run-in lead-in, then the text |
| `{"sub": "..."}` | Level 3: `1.` |
| `{"p": "..."}` | Plain body paragraph |
| `{"bullets": ["...", "..."]}` | Oxblood square bullets |
| `{"quote": "..."}` | Indented block quote |

Inline markup inside any text: `**bold**` and `*italic*`. Define terms as `(the “**Client**”)` with curly quotes.

Numbering restarts automatically: sections restart under each article, subsections under each section. Never type a number into the text.
