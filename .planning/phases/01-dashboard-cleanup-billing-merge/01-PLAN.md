---
phase: 01
phase_name: Dashboard Cleanup + Billing Merge
plan_number: 01
plan_name: Single-Wave Sequential Execution
wave: 1
depends_on: []
autonomous: true
files_modified:
  - index.html
  - data/billing.json
  - data/project_status.json
  - README.md
  - PRICING_CALCULATIONS.md
  - REVISED_PRICING.md
  - _archive/PRICING_CALCULATIONS.md
  - _archive/REVISED_PRICING.md
requirements_addressed:
  - W1-polish
  - W2-data-consolidation
  - W3-billing-module
must_haves:
  - Branch feature/dashboard-cleanup-billing-merge contains all changes
  - No CLAUDE.md or memory file modifications
  - No ~/maplemoon-website touches
  - No Vercel deploy triggered
  - No invoices drafted or sent
  - Dashboard loads at localhost:8765 with no JS console errors after each task
spec_reference: docs/superpowers/specs/2026-05-28-dashboard-cleanup-billing-merge-design.md
---

<phase_context>
**Phase:** 01 — Dashboard Cleanup + Billing Merge
**Spec:** `docs/superpowers/specs/2026-05-28-dashboard-cleanup-billing-merge-design.md`
**Goal:** Clean up cruft accumulated across 20+ commits, consolidate scattered pricing markdowns, add a new Billing tab that surfaces AFQA / Shopify / Photoshoot scopes with mates-rate-aware display. Ship as a single PR-style diff against `main`, no auto-deploy.

**Workstreams in this plan:**
- W1 polish (em-dash sweep, broken staleness display, tab nav overflow, 375px responsive)
- W2 data consolidation (collapse 4 pricing markdowns to 1 canonical, archive older drafts)
- W3 new Billing tab (inside `index.html`, hand-curated `data/billing.json`)

**Locked decisions from brainstorm:**
- Keep current dashboard palette (`--mm-deep-blue #457798` + `--mm-dark-blue #1E4366`), no cornflower migration
- Full retroactive em-dash sweep across visible copy
- Static JSON for billing data, no live Xero API
- Polish items included in this phase (not deferred)

**Out of scope:**
- `~/maplemoon-website` repo (separate Shopify build)
- Xero live API integration
- Photoshoot deliverables folder
- CLAUDE.md / memory file modifications
- Vercel deployment (Nate ships manually after review)
- Drafting or sending invoice C21_MM_07 (stays with parent session)
</phase_context>

<tasks>

<task id="T1" name="Data consolidation: archive old pricing markdowns">
<action>
1. Create directory `_archive/` at the repo root.
2. Move `PRICING_CALCULATIONS.md` to `_archive/PRICING_CALCULATIONS.md` using `git mv`.
3. Move `REVISED_PRICING.md` to `_archive/REVISED_PRICING.md` using `git mv`.
4. Prepend each archived file with this banner block on a new line at the very top:
   ```
   > **ARCHIVED 2026-05-28.** This document is no longer current. See `FINAL_PRICING_BREAKDOWN.md` for the canonical AFQA pricing.

   ---

   ```
5. Update `README.md` to reference `FINAL_PRICING_BREAKDOWN.md` as canonical pricing source. If README does not currently mention the pricing markdowns, add a short "Pricing" section: `## Pricing\n\nCanonical AFQA pricing: see [FINAL_PRICING_BREAKDOWN.md](FINAL_PRICING_BREAKDOWN.md).\n\nArchived earlier versions: `_archive/PRICING_CALCULATIONS.md`, `_archive/REVISED_PRICING.md`.`
6. Commit with message: `chore(data): consolidate pricing markdowns, archive older drafts`
</action>

<read_first>
- `~/maplemoon-dashboard/README.md`
- `~/maplemoon-dashboard/PRICING_CALCULATIONS.md` (head, to confirm before move)
- `~/maplemoon-dashboard/REVISED_PRICING.md` (head, to confirm before move)
- `~/maplemoon-dashboard/FINAL_PRICING_BREAKDOWN.md` (head, to confirm it's the canonical)
</read_first>

<acceptance_criteria>
- `test -f _archive/PRICING_CALCULATIONS.md` returns 0
- `test -f _archive/REVISED_PRICING.md` returns 0
- `test ! -f PRICING_CALCULATIONS.md` returns 0 (moved, not copied)
- `test ! -f REVISED_PRICING.md` returns 0
- `grep -c "ARCHIVED 2026-05-28" _archive/PRICING_CALCULATIONS.md` returns 1
- `grep -c "ARCHIVED 2026-05-28" _archive/REVISED_PRICING.md` returns 1
- `grep -c "FINAL_PRICING_BREAKDOWN.md" README.md` is at least 1
- `git log -1 --pretty=%s` contains the string "consolidate pricing markdowns"
</acceptance_criteria>
</task>

<task id="T2" name="Fix broken staleness display in initDynamicDate()">
<action>
1. In `index.html`, locate `function initDynamicDate()` (around line 5432). Read the current implementation.
2. Locate the `<span id="last-updated-text" data-updated="...">` element (search for `id="last-updated-text"`). Note the current hard-coded `data-updated` value.
3. Change `initDynamicDate()` to read the timestamp from `data/project_status.json`'s `lastUpdated` field instead of from the `data-updated` HTML attribute. The function should:
   a. Use the existing JSON fetch (or trigger it) to get `project_status.json`
   b. Parse `lastUpdated` (ISO 8601)
   c. Compute days-diff against `new Date()`
   d. Set textContent to the same "Updated N days ago" / "Updated today" / "Updated yesterday" pattern
   e. If JSON fetch fails or `lastUpdated` is missing, fall back to textContent "Recently updated" (no crash)
4. Remove the now-unused `data-updated="..."` attribute from the `<span id="last-updated-text">` element so there is only one truth source.
5. If `data/project_status.json` does not already have a current `lastUpdated` value, update it to today: `2026-05-28T17:00:00+10:00`.
6. Commit with message: `fix: staleness display reads from project_status.json, removes drifted hard-coded date`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` (specifically lines 5425-5450 and the `last-updated-text` element location)
- `~/maplemoon-dashboard/data/project_status.json` (to confirm `lastUpdated` field shape)
</read_first>

<acceptance_criteria>
- `grep -n "data-updated" index.html | wc -l` returns 0 (attribute removed)
- `grep -c "lastUpdated" index.html` returns at least 1 (function now references JSON field)
- `grep -c "Recently updated" index.html` returns at least 1 (fallback string present)
- Dashboard loads at `http://localhost:8765/` and the "Updated N days ago" text shows a small N (0, 1, or 2 days) matching today's data, NOT 106 days
- No JS console errors at page load
- `git log -1 --pretty=%s` contains the string "staleness display"
</acceptance_criteria>
</task>

<task id="T3" name="Fix tab nav overflow on desktop and small screens">
<action>
1. In `index.html`, locate the `.tab-navigation` CSS class definition.
2. Add the following CSS properties to `.tab-navigation`:
   - `overflow-x: auto`
   - `scroll-snap-type: x mandatory`
   - `-webkit-overflow-scrolling: touch`
   - `scrollbar-width: thin` (or use `::-webkit-scrollbar` styling consistent with the existing palette)
3. Add to `.tab-button`:
   - `scroll-snap-align: start`
   - `flex-shrink: 0`
4. Add a right-edge gradient cue via a pseudo-element or a sibling overlay div. Implementation: pseudo-element on `.tab-navigation::after` with `background: linear-gradient(to right, transparent, var(--mm-cream))`, positioned absolute at the right edge, `pointer-events: none`. The cream color matches the dashboard background so the gradient fades into the visible page.
5. Verify in Chrome at 1404px width: all 12 tabs accessible (visible or scrollable).
6. Commit with message: `fix(ui): tab nav scrolls horizontally with edge fade so all tabs reachable`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` (specifically the `.tab-navigation` and `.tab-button` CSS blocks, found around lines 1296-1340 and 1035-1100)
</read_first>

<acceptance_criteria>
- `grep -c "overflow-x: auto" index.html` returns at least 1 in `.tab-navigation` context
- `grep -c "scroll-snap-type" index.html` returns at least 1
- `grep -c "scroll-snap-align" index.html` returns at least 1
- At viewport 1404px, the tab nav scrolls horizontally (verified visually in Chrome via the running localhost:8765 instance)
- At viewport 375px, the tab nav scrolls horizontally without breaking the page layout
- `git log -1 --pretty=%s` contains the string "tab nav"
</acceptance_criteria>
</task>

<task id="T4" name="Author data/billing.json with the three-section structure">
<action>
1. Create file `data/billing.json` with the structure defined in the spec (see `docs/superpowers/specs/2026-05-28-dashboard-cleanup-billing-merge-design.md` section W3.2 for the canonical JSON). The file must contain:
   - `lastUpdated`: ISO 8601 timestamp for today, e.g. `"2026-05-28T17:00:00+10:00"`
   - `currency`: `"AUD"`
   - `afqa_retrospective`: scope_label, rate_context `"mates_rate"`, rate_explainer, invoices array of 5 paid entries (INV-0354/0355/0356/0359/0363) summing to $10,029.30
   - `website_progress`: scope_label, scope_total 13206.00, deposit_paid 3961.80, deposit_invoice INV-0369, consumed_percent 17, remaining 9244.20, rate_context `"standard_with_goodwill"`, line_items array of 10 entries (Store setup, Theme customisation, Content pages, Klaviyo, GA4, WooCommerce migration, Copywriting, Photo art direction, Reviews, Training) with status and weight fields summing to 100
   - `photoshoot`: scope_label, rate_context `"mates_rate_flat"`, rate_explainer, invoices array of 1 entry (number `"C21_MM_07"`, amount 500.00, status `"draft"`)
2. Validate the JSON parses: run `python3 -c "import json; json.load(open('data/billing.json'))"` and confirm exit code 0.
3. Commit with message: `data: add billing.json with AFQA retrospective, website progress, photoshoot scope`
</action>

<read_first>
- `~/maplemoon-dashboard/docs/superpowers/specs/2026-05-28-dashboard-cleanup-billing-merge-design.md` (section W3.2 has the canonical JSON)
- `~/maplemoon-dashboard/data/project_status.json` (to match formatting conventions: 2-space indent, double quotes)
</read_first>

<acceptance_criteria>
- `test -f data/billing.json` returns 0
- `python3 -c "import json; d=json.load(open('data/billing.json')); print(list(d.keys()))"` returns a list containing `lastUpdated`, `currency`, `afqa_retrospective`, `website_progress`, `photoshoot`
- `python3 -c "import json; d=json.load(open('data/billing.json')); print(sum(i['amount'] for i in d['afqa_retrospective']['invoices']))"` returns `10029.3`
- `python3 -c "import json; d=json.load(open('data/billing.json')); print(sum(li['weight'] for li in d['website_progress']['line_items']))"` returns `100`
- `python3 -c "import json; d=json.load(open('data/billing.json')); print(d['website_progress']['consumed_percent'])"` returns `17`
- `python3 -c "import json; d=json.load(open('data/billing.json')); print(d['photoshoot']['invoices'][0]['number'])"` returns `C21_MM_07`
- `git log -1 --pretty=%s` contains the string "billing.json"
</acceptance_criteria>
</task>

<task id="T5" name="Add Billing tab markup, renderer, and styling">
<action>
1. In `index.html`, add a new tab button to the `.tab-navigation` block. Insert it between the existing `Quote and Invoice` button and the `Project Tracker` button (so it appears as the 2nd tab):
   ```html
   <button class="tab-button" role="tab" aria-selected="false" aria-controls="billing-tab" tabindex="-1" onclick="switchTab('billing', event)"><i class="fas fa-receipt" style="margin-right:6px"></i>Billing</button>
   ```
2. Add a new tab content section after the existing `quote-tab` div and before `tracker-tab`:
   ```html
   <div id="billing-tab" class="tab-content" role="tabpanel" aria-labelledby="billing-tab-btn">
     <section id="billing-afqa" class="billing-section"></section>
     <section id="billing-website" class="billing-section"></section>
     <section id="billing-photoshoot" class="billing-section"></section>
   </div>
   ```
3. Add CSS rules inside the existing `<style>` block:
   - `.billing-section { background: var(--mm-white); border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }`
   - `.billing-section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }`
   - `.billing-section-header h2 { font-family: var(--font-primary); color: var(--mm-dark-blue); margin: 0; }`
   - `.mates-rate-pill { background: var(--mm-lilac); color: var(--mm-dark-blue); padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.5px; }`
   - `.status-pill { padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 500; display: inline-block; }`
   - `.status-pill.paid { background: var(--success-color); color: white; }`
   - `.status-pill.billed { background: var(--mm-deep-blue); color: white; }`
   - `.status-pill.in-progress { background: var(--warning-color); color: white; }`
   - `.status-pill.not-started { background: #B0B0B0; color: white; }`
   - `.billing-progress-bar { width: 100%; height: 14px; background: rgba(0,0,0,0.06); border-radius: 7px; overflow: hidden; margin: 12px 0; }`
   - `.billing-progress-fill { height: 100%; background: var(--mm-deep-blue); transition: width 300ms ease; }`
4. Add a JS renderer function `renderBilling()` called from `initDashboard()`. The function:
   a. `fetch('data/billing.json')` and parse JSON
   b. Render the AFQA section: section header with scope_label, total ($10,029.30), MATES RATE pill. Body is a table with columns Scope | Invoice | Date | Amount | Status. One row per invoice with PAID pill.
   c. Render the Website section: section header with scope_label, scope_total. Progress bar filled to consumed_percent. Quick row showing "Deposit paid: $3,961.80 | Remaining: $9,244.20". Line items as a list with status pill per item.
   d. Render the Photoshoot section: section header with scope_label, total ($500), MATES RATE pill. One row showing the C21_MM_07 entry with BILLED pill.
   e. Wrap in try/catch; on error, set each section innerHTML to a fallback "Billing data could not be loaded." message and log the error to console.
5. Add `'billing'` to the array of valid tab slugs for deep-link routing (if such an array exists in `initDeepLink()`; otherwise verify `initDeepLink()` already handles arbitrary slugs by checking `getElementById(hash + '-tab')`).
6. Verify in Chrome: clicking the Billing tab shows all three sections populated correctly.
7. Commit with message: `feat: add Billing tab with AFQA / Website / Photoshoot sections fed from billing.json`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` (tab nav block at line 3906-3920, tab content divs around line 3922+, `<style>` block for CSS conventions, `switchTab()` and `initDeepLink()` functions, `initDashboard()` for renderer registration)
- `~/maplemoon-dashboard/data/billing.json` (the source data, must exist from T4)
- `~/maplemoon-dashboard/docs/superpowers/specs/2026-05-28-dashboard-cleanup-billing-merge-design.md` (sections W3.3, W3.4, W3.5 for rendering rules)
- `~/UFC/tools/receipt_builder/index.html` (the bucket pattern reference, particularly the bucket-head and bucket-body structure for visual cues)
</read_first>

<acceptance_criteria>
- `grep -c 'id="billing-tab"' index.html` returns 1
- `grep -c "renderBilling" index.html` returns at least 2 (function definition + call)
- `grep -c "mates-rate-pill" index.html` returns at least 2 (CSS rule + at least one usage)
- `grep -c "billing-section" index.html` returns at least 4 (3 sections + 1 CSS rule)
- Dashboard at `http://localhost:8765/` shows a Billing tab in the nav between Quote and Invoice and Project Tracker
- Clicking Billing tab shows three sections populated with the data from billing.json
- AFQA section has MATES RATE pill, 5 invoice rows each with PAID pill, summing visibly to $10,029.30
- Website section has progress bar showing roughly 17% filled, deposit + remaining figures, 10 line items
- Photoshoot section has MATES RATE pill and one C21_MM_07 row with BILLED pill
- No JS console errors at page load
- Navigating to `http://localhost:8765/#billing` directly opens the Billing tab (deep-link works)
- `git log -1 --pretty=%s` contains the string "Billing tab"
</acceptance_criteria>
</task>

<task id="T6" name="Em-dash sweep across visible-copy lines">
<action>
1. Identify all em-dashes in visible copy: `grep -nE '—' index.html | grep -vE '<!--|^[[:space:]]*//' > /tmp/emdash_review.txt`
2. For each line in the review file, decide replacement:
   - If em-dash sits between two clauses, default to `, ` (comma-space)
   - If em-dash is bracketing a definition/explanation (e.g. `"Update — 18 Feb 2026"`), use `: ` (colon-space) or `(` and `)`
   - If em-dash is in a numeric range (`Weeks 1-4`), use `-` (hyphen)
   - If em-dash is just decorative (`<div class="week-amount">—</div>`), replace with the literal en-dash `–` (U+2013) or remove if it adds no info
3. Apply replacements line-by-line via the Edit tool, NEVER via bulk `sed -i` (CSS `--var` and HTML inline styles must not be touched).
4. Exclusions confirmed kept as-is:
   - HTML comments (`<!-- ... -->`)
   - JS inline comments (`// ...`)
   - CSS `--variable-name` patterns (these contain `--` not `—`, so grep already excludes them)
5. Also sweep `README.md`: replace 9 em-dashes with hyphens or sentence breaks per same rules.
6. Re-run grep: `grep -nE '—' index.html | grep -vE '<!--|//' | wc -l` must return 0.
7. Commit with message: `style(copy): replace em-dashes with hyphens / sentence breaks across visible copy`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` (all 88 visible-copy em-dash lines, identified via grep)
- `~/maplemoon-dashboard/README.md` (all 9 em-dash lines)
- `/Users/handtomouse/.claude/projects/-Users-handtomouse/memory/MEMORY.md` (the em-dash ban rule, for reference only - do not modify)
</read_first>

<acceptance_criteria>
- `grep -nE '—' index.html | grep -vE '<!--|//' | wc -l` returns 0
- `grep -nE '—' README.md | wc -l` returns 0
- `grep -c "Update.* 18 Feb 2026" index.html` returns at least 1 (the banner copy is preserved, just without em-dash; the regex matches both `: ` and `, ` replacements)
- Dashboard at `http://localhost:8765/` still loads with no JS errors
- The Update banner still reads coherently (manual visual check)
- `git diff HEAD~1 -- index.html | grep -c '^-.*—'` is approximately 88 (the 88 removed em-dash lines)
- `git log -1 --pretty=%s` contains the string "em-dashes"
</acceptance_criteria>
</task>

<task id="T7" name="Add 375px responsive breakpoint for any breaks found">
<action>
1. Open Chrome DevTools at the running localhost:8765 instance. Toggle device emulation to iPhone SE (375px wide).
2. Click through every tab and note any horizontal-scroll-on-body issues, clipped CTAs, overlapping text, or unreadable status pills.
3. Add a new `@media (max-width: 375px)` block in `index.html` addressing only the cases that broke. Common candidates:
   - `.tab-button { font-size: 0.85rem; padding: 8px 12px; }`
   - `.billing-section { padding: 16px; }`
   - `.financial-card` and similar grid items: stack vertically (`grid-template-columns: 1fr;`)
   - Hero header font-size scale-down
4. Re-test at 375px until no horizontal body scroll, all interactive elements reachable, all content readable without clipping.
5. Commit with message: `fix(responsive): add 375px breakpoint for iPhone SE layout`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` (existing `@media (max-width: 768px)` and `@media (max-width: 480px)` blocks for inheritance context)
</read_first>

<acceptance_criteria>
- `grep -c "@media (max-width: 375px)" index.html` returns at least 1
- At viewport 375px, `document.body.scrollWidth <= 375` evaluated via Chrome DevTools console (no horizontal body scroll)
- At viewport 375px, all 12 tabs are reachable (scrollable nav)
- At viewport 375px, the Billing tab's three sections render readably without overlap
- `git log -1 --pretty=%s` contains the string "375px"
</acceptance_criteria>
</task>

<task id="T8" name="Verification pass at all four viewport widths">
<action>
1. Confirm local server is running: `curl -sI http://localhost:8765/ | head -1` returns `HTTP/1.0 200 OK`. If not, start it: `cd ~/maplemoon-dashboard && python3 -m http.server 8765 &`
2. In Chrome, visit `http://localhost:8765/`.
3. For each viewport width in {1440, 768, 480, 375}, run the verification checklist from the spec:
   - Dashboard loads with no JS console errors
   - All 12 tabs accessible
   - `Quote and Invoice` tab renders correctly (no regression)
   - `Billing` tab present and clickable
   - `billing.json` data renders in all three sections
   - AFQA section: 5 paid invoices, total $10,029.30, MATES RATE pill
   - Website section: 17% progress bar, $13,206 scope, $3,961.80 deposit, $9,244.20 remaining, 10 line items
   - Photoshoot section: C21_MM_07 row, $500, BILLED pill, MATES RATE pill
   - Staleness display shows "Updated today" or "Updated 0 days ago"
   - No horizontal body scroll
   - No em-dashes visible in any client copy
4. Run final grep audits:
   - `grep -nE '—' index.html | grep -vE '<!--|//' | wc -l` returns 0
   - `grep -c "#7B9DBF" index.html` returns 0 (palette unchanged, no cornflower)
   - `git diff main --name-only | grep -E '(CLAUDE.md|/memory/)'` returns no results (no memory or CLAUDE.md touches)
   - `git diff main --name-only | grep maplemoon-website` returns no results (no website repo touches)
5. Compose a summary of what shipped: list of files changed, line count diff, key behavioral changes. Append this summary to the handoff file at `~/Library/CloudStorage/GoogleDrive-hello@handtomouse.org/My Drive/MrCC_PAI_Stage1_Files/UFC/ops/handoffs/handoff_20260528_171235_mm_dashboard_cleanup.md` as:
   ```
   ## Status: DONE | <one-line summary of what shipped>

   ### Files changed
   <git diff --stat>

   ### Behavioral changes
   <bullet list>
   ```
6. Final commit if anything was tweaked during verification: `chore: verification fixups`. Otherwise no commit.
</action>

<read_first>
- `~/.claude/worktrees/maplemoon-dashboard-cleanup-2026-05-28/docs/superpowers/specs/2026-05-28-dashboard-cleanup-billing-merge-design.md` (the Verification checklist section)
- `~/Library/CloudStorage/GoogleDrive-hello@handtomouse.org/My Drive/MrCC_PAI_Stage1_Files/UFC/ops/handoffs/handoff_20260528_171235_mm_dashboard_cleanup.md` (the handoff to append to)
</read_first>

<acceptance_criteria>
- All checklist items from the spec's "Verification checklist" section confirmed in chat
- Handoff file appended with `## Status: DONE | ...` block
- `grep -c "## Status: DONE" "<handoff path>"` returns 1
- `git log main..feature/dashboard-cleanup-billing-merge --oneline | wc -l` returns at least 7 (at least 7 commits on the branch from T1-T7)
- `git diff main feature/dashboard-cleanup-billing-merge --name-only | grep -c '^'` shows the file change list matches `files_modified` in this plan's frontmatter
</acceptance_criteria>
</task>

</tasks>

<execution_notes>
**Execution order:** T1 → T2 → T3 → T4 → T5 → T6 → T7 → T8. Sequential. Each task ends with a commit and the dashboard still loadable.

**Why sequential not parallel:** T2, T3, T5, T6, T7 all touch `index.html` in different sections. Parallel execution would require careful conflict resolution; sequential is safer and the time cost is small (each task is a focused diff).

**Checkpoint protocol:** If any task fails its acceptance criteria, stop and surface to Nate before continuing. Do NOT auto-skip to the next task.

**Commit discipline:** Each task is one commit. NEVER amend. NEVER squash. The PR review reads better with atomic commits.

**No deploy:** Nate ships this manually after reviewing the branch. The verification task (T8) does NOT trigger Vercel.
</execution_notes>

<verification_criteria>
The phase passes when:
1. All 8 tasks pass their acceptance_criteria
2. Branch `feature/dashboard-cleanup-billing-merge` has at least 7 atomic commits (T1-T7) plus optional T8 fixup
3. Handoff file appended with DONE status
4. No CLAUDE.md, memory, `~/maplemoon-website`, or Vercel touches
5. Dashboard at `localhost:8765` is fully functional at 1440 / 768 / 480 / 375px viewports
</verification_criteria>
</content>
