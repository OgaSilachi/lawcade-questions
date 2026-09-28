# Client Case Portal

A single-file, low-code web page that gives a client a private place to follow
their case: where it stands, what has happened, what happens next, what you need
from them, shared documents, and how to reach your team.

## Why this exists

Your internal strategy dashboard (settlement ranges, deposition plans, walk-away
numbers) is privileged attorney work product and must never be shown to a client.
This portal is the client-safe counterpart: plain language, status only, no strategy.

## How to use it (no coding)

1. Open `index.html` in any text editor.
2. Find the `CONFIG` object near the top of the `<script>` block.
3. Change the text values: firm name, case title, summary, stages, timeline,
   upcoming dates, tasks, documents, contacts, FAQ. That is the whole page.
4. Save. Double-click the file to preview it in a browser.

Copy this file once per client and edit the `CONFIG` for each matter.

## How to put it online (pick one)

- **Easiest / free:** create a repo, drop this file in, turn on GitHub Pages.
- **Drag-and-drop:** Netlify Drop or Cloudflare Pages (upload the file, get a link).
- **Low-code builders:** Softr, Carrd, or Notion + a share link if you prefer a
  builder UI. You can also embed this file's markup in a Webflow/Wix HTML block.
- **Inside your practice tools:** MyCase and similar platforms already offer a
  built-in client portal. If you use theirs, this file is still useful as the
  status/roadmap page you share as a link.

## Keeping it private

- Share the link only with the client. Do not index it publicly.
- For real privacy, host it behind a login (Netlify Identity, Cloudflare Access,
  or your practice-management portal) rather than a plain public URL.
- The checklist checkboxes are saved only in the client's own browser. Nothing
  is transmitted to the firm.

## What NOT to put in here

Never paste internal strategy: settlement floors/ceilings, deposition or
cross-examination plans, assessments of the other side's credibility, or anything
you would not want the opposing party to read. Keep those in the internal
dashboard only.
