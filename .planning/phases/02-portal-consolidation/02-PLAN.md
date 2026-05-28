---
phase: 02
phase_name: Portal Consolidation
plan_number: 02
plan_name: Five-Tab Lifecycle + Visible Archive
wave: 1
depends_on: ["01-dashboard-cleanup-billing-merge"]
autonomous: false
files_modified:
  - index.html
  - data/archive_index.json
  - data/milestones.json
requirements_addressed:
  - W1-data-scaffolding
  - W2-archive-tab
  - W3-nav-restructure
  - W4-status-enhancements
  - W5-specs-dimensions
  - W6-billing-cross-link
  - W7-breadcrumbs
  - W8-visual-refresh
must_haves:
  - Branch feature/portal-consolidation contains all changes
  - No CLAUDE.md or memory file modifications
  - No ~/maplemoon-website touches
  - No Vercel deploy triggered from CLI
  - No invoices drafted or sent
  - Dashboard loads at localhost:8765 with no JS console errors after each task
  - Tab nav contains exactly 5 buttons after T3 (Status, Billing, Specs, Final Files, Archive)
spec_reference: docs/superpowers/specs/2026-05-28-portal-consolidation-design.md
---

<phase_context>
**Phase:** 02 - Portal Consolidation
**Spec:** `docs/superpowers/specs/2026-05-28-portal-consolidation-design.md`
**Goal:** Reshape the dashboard's 12-tab nav into a 5-tab client portal for Carli and Dylan, with a visible Archive surface for historical artifacts. Ship as 4 PRs against `main`, no auto-deploy.

**Workstreams in this plan:**
- W1 data scaffolding (`data/archive_index.json` + `data/milestones.json`)
- W2 Archive tab content and rendering
- W3 nav restructure (remove 7 buttons, rename 2, add 1)
- W4 Status tab enhancements ("This week" hook + Assets fold-in)
- W5 Specs SKU and barcode reference table
- W6 Billing footer cross-link to Archive#quote
- W7 back-to-source breadcrumbs
- W8 small visual refresh on the 5 surviving tabs (typography, spacing, hero H1 cleanup) - added post-plan via T9

**Locked decisions from brainstorm:**
- Proposal B: 5-tab lifecycle + visible Archive (Status, Billing, Specs, Final Files, Archive)
- Retired tab HTML is retained, only hidden from nav (lowest risk, reversible)
- Quote tab archived AND cross-linked from Billing
- Timeline condensed to 10 milestones in Status's "This week" hook; full 1834-line version reachable via Archive. **10 milestones curated and inlined in T1 below (locked 2026-05-28); items 8-10 dates marked "(target)".**
- Design Review kept linkable from Archive with "last current as of" date
- Client Form retired to Archive with "if already submitted, this is historical" footnote
- Palette stays locked (mm-deep-blue #457798 + mm-dark-blue #1E4366); no cornflower migration
- **W5 scope pivoted from artwork dimensions to SKU and barcode reference (artwork specs live outside dashboard data; this delivers data anchored in `project_status.json`).** 16-row table inlined in T5 below.

**PR grouping (4 PRs, per execute-phase handoff 2026-05-28):**
- PR-1 = T0 + T1 + T2 (foundation commit + data scaffolding + Archive tab content; no nav change yet)
- PR-2 = T3 + T7 (nav restructure + breadcrumbs - the visible-change cluster)
- PR-3 = T4 + T5 + T6 (Status enhancements + Specs table + Billing cross-link)
- PR-4 = T9 + T8 (W8 visual refresh + 4-viewport verification)

**Out of scope:**
- `~/maplemoon-website` repo (read-only)
- Vercel deployment
- Cornflower palette migration
- Hard-deletion of any retired tab content
- Refreshing `review/` screenshots
- Comms to Carli and Dylan announcing the restructure
- INV-0406 or any invoice work
- `CLAUDE.md` / memory file modifications
</phase_context>

<tasks>

<task id="T1" name="W1 data scaffolding: create archive_index.json and milestones.json">
<action>
1. Create branch `feature/portal-consolidation` from current `main` (`git checkout main && git pull && git checkout -b feature/portal-consolidation`).
2. Create `data/archive_index.json` with 8 cards. Schema:
   ```json
   {
     "lastUpdated": "2026-05-28T17:00:00+10:00",
     "cards": [
       { "id": "quote", "title": "...", "subtitle": "...", "context": "...",
         "last_current": "YYYY-MM-DD", "anchor": "quote-tab" },
       ...
     ]
   }
   ```
   8 cards total, ids: `quote`, `ecommerce`, `research`, `preview`, `clientform`, `photoshoot`, `review`, `timeline`. Copy per spec section "Archive cards (8)". Pre-flight em-dash sweep before saving (replace any "—" with " - " or sentence break).
3. Create `data/milestones.json` with the 10 curated milestones below (locked during spec review 2026-05-28):
   ```json
   {
     "lastUpdated": "2026-05-28T17:00:00+10:00",
     "milestones": [
       { "date": "2026-01-15", "title": "AFQA Bars, Icons, Bar CDUs paid", "status": "done",
         "context": "INV-0354 (icons), INV-0355 (6 bars), INV-0356 (6 bar CDUs) all paid same day. Phase 1 AFQA core complete." },
       { "date": "2026-01-25", "title": "INV-0359 paid: AFQA Moons (6)", "status": "done",
         "context": "Pure Carob Moon master + 5 flavour clones. New packaging dimensions received and applied." },
       { "date": "2026-02-06", "title": "INV-0363 paid: Moon CDUs + Bananas", "status": "done",
         "context": "6 Moon CDUs + Banana 4-pack + Banana CDU. All barcodes and SKUs confirmed." },
       { "date": "2026-02-17", "title": "New SKUs added at 25% rate", "status": "done",
         "context": "Lavender + Orange Bars and Moons added to the AFQA scope." },
       { "date": "2026-02-18", "title": "Shopify website project approved", "status": "done",
         "context": "Shopify e-commerce build green-lit; staging in flight at maplemoon-website." },
       { "date": "2026-05-24", "title": "Shopify photoshoot completed", "status": "done",
         "context": "Mitch and Melly captured 122 Shopify-mapped shots across the product range." },
       { "date": "2026-05-28", "title": "Photoshoot art direction underway", "status": "in_progress",
         "context": "INV-0406 ($1,750) authorised for shot selection, retouching, and curation pass." },
       { "date": "2026-06-15", "title": "Staging review with Carli and Dylan (target)", "status": "upcoming",
         "context": "Review live staging URL; feedback drives website direction finalisation." },
       { "date": "2026-06-30", "title": "Photo deliverables to MapleMoon (target)", "status": "upcoming",
         "context": "Final selects from photoshoot delivered for Shopify build and ongoing marketing." },
       { "date": "2026-07-31", "title": "Shopify website launch (target)", "status": "upcoming",
         "context": "Website direction finalised, products live, AFQA assets integrated." }
     ]
   }
   ```
   Dates marked "(target)" on items 8-10 are estimates. Nate can firm up before commit if desired.
4. Commit: `data: add archive_index.json + milestones.json scaffolding for portal consolidation`
</action>

<read_first>
- `~/maplemoon-dashboard/data/billing.json` (schema reference for `lastUpdated` format)
- `~/maplemoon-dashboard/data/project_status.json` (reference for tone of `context` fields)
- `~/maplemoon-dashboard/docs/superpowers/specs/2026-05-28-portal-consolidation-design.md` (sections "Archive cards (8)" and "milestones.json structure")
</read_first>

<acceptance_criteria>
- `test -f data/archive_index.json` returns 0
- `test -f data/milestones.json` returns 0
- `jq '.cards | length' data/archive_index.json` returns 8
- `jq '.milestones | length' data/milestones.json` returns 10
- `jq -r '.milestones[].status' data/milestones.json | sort -u | tr '\n' ' '` returns `done in_progress upcoming` (or a subset of those values; no "tbd" or "todo")
- `grep -c "—" data/archive_index.json data/milestones.json` returns 0 (no em-dashes)
- `git log -1 --pretty=%s` contains "archive_index.json"
- No changes to `index.html` in this commit
</acceptance_criteria>
</task>

<task id="T2" name="W2 add Archive tab content and renderer (no nav changes yet)">
<action>
1. In `index.html`, locate the last tab content div (currently `#clientform-tab` around line 8518) and find its closing `</div>` boundary.
2. Insert a new tab content div after the last existing tab div, before the closing `</div>` of the `.container`:
   ```html
   <!-- Archive Tab (Phase 02) -->
   <div id="archive-tab" class="tab-content" role="tabpanel" aria-labelledby="archive-tab-btn">
       <header class="brand-header fade-in">
           ... title + subtitle ...
       </header>
       <div id="archive-grid" class="archive-grid">
           <!-- populated by renderArchiveCards() -->
       </div>
   </div>
   ```
3. Add CSS in the existing `<style>` block (use the Billing card aesthetic as template):
   - `.archive-grid` - 2-column responsive grid, 1 column at <600px
   - `.archive-card` - bg white, border-radius 8px, padding 24px, box-shadow consistent with `.billing-section`
   - `.archive-card-title` - mm-dark-blue, var(--font-primary), 1.4rem
   - `.archive-card-subtitle` - mm-deep-blue, 0.95rem, italic
   - `.archive-card-context` - color #66584D, 0.9rem, line-height 1.4
   - `.archive-card-meta` - color #888, 0.75rem (for "Last current as of")
   - `.archive-card-view-btn` - button styled like Billing's primary action; calls `archiveOpen(id)`
4. Add a small `escapeHtml` helper near the top of the existing inline JS block (if not already present in the repo):
   ```js
   function escapeHtml(s) {
       return String(s ?? '').replace(/[&<>"']/g, ch =>
           ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch])
       );
   }
   ```
   Then add inline JS `renderArchiveCards()` function:
   ```js
   async function renderArchiveCards() {
       try {
           const res = await fetch('data/archive_index.json');
           if (!res.ok) throw new Error('archive_index fetch failed');
           const data = await res.json();
           const grid = document.getElementById('archive-grid');
           grid.innerHTML = data.cards.map(card => `
               <article class="archive-card">
                   <h3 class="archive-card-title">${escapeHtml(card.title)}</h3>
                   <p class="archive-card-subtitle">${escapeHtml(card.subtitle)}</p>
                   <p class="archive-card-context">${escapeHtml(card.context)}</p>
                   <p class="archive-card-meta">Last current as of: ${escapeHtml(card.last_current)}</p>
                   <button class="archive-card-view-btn" data-anchor="${escapeHtml(card.anchor)}">View</button>
               </article>
           `).join('');
           grid.querySelectorAll('.archive-card-view-btn').forEach(btn => {
               btn.addEventListener('click', () => archiveOpen(btn.dataset.anchor));
           });
       } catch (err) {
           console.warn('Archive render failed:', err);
           document.getElementById('archive-grid').innerHTML =
               '<p class="archive-empty">Reference data not loaded. Refresh the page or contact Nate.</p>';
       }
   }
   ```
   Note: button click is wired via `addEventListener` post-render rather than inline `onclick="archiveOpen('${...}')"` to keep the `anchor` value out of an HTML-attribute string interpolation path. Card text fields are HTML-escaped via `escapeHtml` so future hand-edits containing `<`, `>`, or `&` in `data/archive_index.json` render literally rather than as markup. Matches Phase 01 same-origin-JSON convention with a defensive cleanup.
5. Add `archiveOpen(anchor)` helper:
   ```js
   function archiveOpen(anchor) {
       sessionStorage.setItem('mm:returnTo', 'archive');
       // synthesize an event-like object for switchTab signature
       const btn = document.querySelector(`[aria-controls="${anchor}"]`);
       if (btn) {
           switchTab(anchor.replace('-tab', ''), { target: btn });
       } else {
           // No nav button exists for retired tabs; manually toggle classes
           document.querySelectorAll('.tab-content.active').forEach(el => el.classList.remove('active'));
           const target = document.getElementById(anchor);
           if (target) {
               target.classList.add('active');
               target.scrollIntoView({ behavior: 'smooth', block: 'start' });
           } else {
               console.warn('Archive target not found:', anchor);
           }
       }
   }
   ```
6. Wire `renderArchiveCards()` into existing init code (search for the existing tab init or DOMContentLoaded handler; add the call there alongside other render calls).
7. **Do NOT yet add an Archive nav button** (deferred to T3 so the nav restructure ships in one atomic commit).
8. Verify dashboard loads at `localhost:8765` and `archiveOpen('quote-tab')` from the JS console brings the Quote tab into view. Existing nav buttons still work (all 13 tabs still present in nav).
9. Commit: `feat(archive): add Archive tab content and renderArchiveCards (nav add deferred to T3)`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` (locate the existing tab init function and switchTab, lines 4100-4115 nav block, and the .billing-section CSS for visual reference)
- `~/maplemoon-dashboard/data/archive_index.json` (from T1, confirm the 8 cards present)
</read_first>

<acceptance_criteria>
- `grep -c 'id="archive-tab"' index.html` returns 1
- `grep -c "renderArchiveCards" index.html` returns at least 2 (definition + call)
- `grep -c "archiveOpen" index.html` returns at least 2 (definition + 8 inline references via card render template, so closer to 9 if the template literal is inline)
- Dashboard loads at `localhost:8765/` with no JS console errors
- In browser console, `document.getElementById('archive-tab')` returns the element
- In browser console, `archiveOpen('quote-tab')` brings the Quote tab into view (`#quote-tab.active`)
- Existing 13 nav buttons all still present and functional
- `git log -1 --pretty=%s` contains "archive"
</acceptance_criteria>
</task>

<task id="T3" name="W3 nav restructure: retire 7 buttons, rename 2, add Archive">
<action>
1. In `index.html`, locate `<div class="tab-navigation">` (around line 4101). Read the current 13 buttons (Quote, Billing, Project Tracker, Spec Tracker, Timeline, Assets, Final Files, E-Commerce, Photoshoot, Research, Preview, Client Form, Design Review).
2. Replace the nav block with the new 5-button structure (preserve all role/aria attributes patterns from existing buttons):
   ```html
   <div class="tab-navigation" role="tablist" aria-label="Project sections">
       <button class="tab-button active" role="tab" aria-selected="true" aria-controls="tracker-tab" tabindex="0" onclick="switchTab('tracker', event)"><i class="fas fa-tasks" style="margin-right:6px"></i>Status</button>
       <button class="tab-button" role="tab" aria-selected="false" aria-controls="billing-tab" tabindex="-1" onclick="switchTab('billing', event)"><i class="fas fa-receipt" style="margin-right:6px"></i>Billing</button>
       <button class="tab-button" role="tab" aria-selected="false" aria-controls="specs-tab" tabindex="-1" onclick="switchTab('specs', event)"><i class="fas fa-clipboard-list" style="margin-right:6px"></i>Specs</button>
       <button class="tab-button" role="tab" aria-selected="false" aria-controls="files-tab" tabindex="-1" onclick="switchTab('files', event)"><i class="fas fa-folder-open" style="margin-right:6px"></i>Final Files</button>
       <button class="tab-button" role="tab" aria-selected="false" aria-controls="archive-tab" tabindex="-1" onclick="switchTab('archive', event)"><i class="fas fa-archive" style="margin-right:6px"></i>Archive</button>
   </div>
   ```
3. Default-active tab is now Status (was Quote). Update any init JS that hard-codes `switchTab('quote', ...)` on page load to use `switchTab('tracker', ...)` instead. Search: `grep -n "switchTab('quote'" index.html`.
4. Update `<title>` and any open-graph or meta tags that reference "Quote" as default landing tab, if present.
5. **Do NOT delete the tab content divs for retired tabs.** They stay in HTML, only hidden from nav. The CSS class `.tab-content` already defaults to `display: none`; only `.tab-content.active` is shown. So the retired divs are auto-hidden.
6. Verify in browser:
   - Nav shows exactly 5 buttons
   - Default tab is Status
   - Each of the 5 buttons switches correctly
   - Archive button shows 8 cards
   - Clicking an Archive card's "View" button brings the retired tab into view
   - Nav fits without horizontal overflow at 1440px (use a wider window or DevTools responsive mode)
   - Nav still scroll-snaps cleanly at 375px (Phase 01 behavior preserved)
7. Commit: `refactor(nav): retire 7 historical tabs from nav, rename Tracker to Status and Spec Tracker to Specs, add Archive`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` lines 4090-4120 (full nav block)
- `~/maplemoon-dashboard/index.html` (search for `switchTab\('quote'` to find init hard-codes)
</read_first>

<acceptance_criteria>
- `grep -c 'class="tab-button' index.html` for the visible nav (between `<div class="tab-navigation">` and its closing `</div>`) returns 5
- `grep -c 'aria-controls="quote-tab"' index.html` returns 0 (Quote button removed from nav; tab content div still present)
- `grep -c 'aria-controls="archive-tab"' index.html` returns 1
- `grep -c 'aria-controls="ecommerce-tab"' index.html` returns 0
- `grep -c '>Status<' index.html` returns at least 1 (button text)
- `grep -c '>Specs<' index.html` returns at least 1
- `grep -c 'id="quote-tab"' index.html` returns 1 (content div retained)
- `grep -c 'id="ecommerce-tab"' index.html` returns 1 (content div retained)
- Dashboard loads at `localhost:8765/`, default tab is Status, all 5 nav buttons work, all 8 Archive cards open their target
- `git log -1 --pretty=%s` contains "retire 7 historical tabs"
</acceptance_criteria>
</task>

<task id="T7" name="W7 back-to-source breadcrumbs">
<action>
1. In `index.html`, modify `switchTab(tabName, event)` to read `sessionStorage.getItem('mm:returnTo')` after switching, and if set:
   - Inject a breadcrumb element `<div class="back-link">← Back to <Archive|Billing></div>` at the top of the now-active tab content (if not already present)
   - Clear the sessionStorage flag
   - Click handler on the breadcrumb: `switchTab('<returnTo>', event); breadcrumbCleanup();`
2. Add `breadcrumbCleanup()` that removes any existing `.back-link` elements from all tab content divs (called by any direct nav button click).
3. Wire all 5 nav buttons' onclick to also call `breadcrumbCleanup()` before `switchTab(...)` (or inside switchTab when called via event, not via archiveOpen).
4. Add CSS for `.back-link`:
   ```css
   .back-link {
       display: inline-flex;
       align-items: center;
       gap: 8px;
       padding: 8px 16px;
       margin: 0 0 20px 0;
       background: var(--mm-cream);
       color: var(--mm-dark-blue);
       border-radius: 6px;
       font-size: 0.9rem;
       cursor: pointer;
       text-decoration: none;
       transition: background 0.2s;
   }
   .back-link:hover { background: rgba(69,119,152,0.1); }
   ```
5. Update `archiveOpen(anchor)` from T2 to set `sessionStorage.setItem('mm:returnTo', 'archive')` before switching, and to inject the breadcrumb consistently regardless of whether the target has a nav button.
6. Verify:
   - Click Archive → click any card's "View" → breadcrumb "← Back to Archive" appears at top of the retired tab
   - Click the breadcrumb → returns to Archive
   - Click any other top-nav button → breadcrumb removed cleanly
7. Commit: `feat(nav): add back-to-source breadcrumbs for Archive and Billing cross-links`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` (locate `switchTab` definition and the T2-added `archiveOpen`)
</read_first>

<acceptance_criteria>
- `grep -c "back-link" index.html` returns at least 2 (CSS + injected element)
- `grep -c "mm:returnTo" index.html` returns at least 2 (set + read)
- `grep -c "breadcrumbCleanup" index.html` returns at least 2 (definition + at least one call)
- In browser: Archive → "View Quote" → Quote tab shows breadcrumb. Click breadcrumb → back to Archive
- In browser: direct nav button click → no stray breadcrumbs from prior navigation
- No JS console errors
- `git log -1 --pretty=%s` contains "breadcrumb"
</acceptance_criteria>
</task>

<task id="T4" name="W4 Status enhancements: This week hook + Assets fold-in">
<action>
1. In `index.html`, locate `#tracker-tab` (around line 4957). Read the current structure to find the top of the tab content (just after the opening `<div id="tracker-tab">`).
2. Insert a new section at the top of `#tracker-tab`:
   ```html
   <section id="status-this-week" class="status-section">
       <h2 class="status-section-title">This week</h2>
       <div id="status-this-week-cards" class="status-cards-grid">
           <!-- populated by renderThisWeek() -->
       </div>
   </section>
   ```
3. Locate `#assets-tab` (around line 6826). Identify the JS function that renders the asset grid (search for the render call hooked off the `#assets-tab` selector).
4. Insert a new section at the BOTTOM of `#tracker-tab` (before its closing `</div>`):
   ```html
   <section id="status-assets" class="status-section">
       <h2 class="status-section-title">Assets and specs</h2>
       <div id="status-assets-grid">
           <!-- populated by renderStatusAssets() -->
       </div>
   </section>
   ```
5. Add `renderThisWeek()`:
   ```js
   async function renderThisWeek() {
       try {
           const res = await fetch('data/milestones.json');
           if (!res.ok) throw new Error();
           const data = await res.json();
           // Pick up to 3: most recent done + next 2 upcoming, fallback to next 3
           const sorted = data.milestones.slice().sort((a,b) => a.date.localeCompare(b.date));
           const today = new Date().toISOString().slice(0,10);
           const done = sorted.filter(m => m.status === 'done' && m.date <= today).slice(-1);
           const upcoming = sorted.filter(m => m.status !== 'done' || m.date > today).slice(0, 3 - done.length);
           const picks = [...done, ...upcoming].slice(0, 3);
           const safeStatus = s => (['done','in_progress','upcoming'].includes(s) ? s : 'upcoming');
           document.getElementById('status-this-week-cards').innerHTML = picks.map(m => {
               const st = safeStatus(m.status);
               return `
               <article class="status-card status-${st}">
                   <span class="status-pill status-pill-${st}">${escapeHtml(st.replace('_',' '))}</span>
                   <h3 class="status-card-title">${escapeHtml(m.title)}</h3>
                   <p class="status-card-date">${escapeHtml(m.date)}</p>
                   <p class="status-card-context">${escapeHtml(m.context)}</p>
               </article>`;
           }).join('') || '<p>No upcoming milestones.</p>';
       } catch (err) {
           document.getElementById('status-this-week').style.display = 'none';
       }
   }
   ```
6. Add `renderStatusAssets()`: either parameterize the existing assets renderer to accept a target selector and call it with `#status-assets-grid`, OR if the existing renderer is tightly coupled, duplicate its DOM-build logic into a small local function pointed at `#status-assets-grid`. Decision made during execute based on existing code shape.
7. Add CSS for `.status-section`, `.status-section-title`, `.status-cards-grid`, `.status-card`, `.status-pill-done`, `.status-pill-in_progress`, `.status-pill-upcoming`. Visual style consistent with Billing tab cards.
8. Wire `renderThisWeek()` and `renderStatusAssets()` into the existing init code so they fire on page load (alongside the existing kanban render).
9. Verify in browser:
   - Status tab shows: "This week" cards at top → existing kanban in middle → "Assets and specs" at bottom
   - Up to 3 milestone cards render, with correct status pills
   - Assets section renders the same items as the old Assets tab
   - No JS console errors
10. Commit: `feat(status): add This week milestones hook and fold Assets section inline`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` `#tracker-tab` block (around lines 4957-4970)
- `~/maplemoon-dashboard/index.html` `#assets-tab` block (around line 6826) and any related JS render function
- `~/maplemoon-dashboard/data/milestones.json` (from T1, confirm milestone shape)
- `~/maplemoon-dashboard/data/project_status.json` (if assets data lives here, confirm structure)
</read_first>

<acceptance_criteria>
- `grep -c 'id="status-this-week"' index.html` returns 1
- `grep -c 'id="status-assets"' index.html` returns 1
- `grep -c "renderThisWeek" index.html` returns at least 2 (definition + call)
- `grep -c "renderStatusAssets" index.html` returns at least 2 (definition + call)
- In browser, Status tab shows This week section at top with up to 3 milestone cards; existing kanban below; Assets section at bottom with item grid
- The retired `#assets-tab` div still exists (not deleted; just no longer in nav)
- No JS console errors at page load or on Status tab switch
- `git log -1 --pretty=%s` contains "This week" or "Status"
</acceptance_criteria>
</task>

<task id="T5" name="W5 Specs SKU and barcode reference table">
<action>
1. In `index.html`, locate `#specs-tab` (around line 4970). Identify the top of the tab content.
2. Insert a new section at the TOP of `#specs-tab` with the curated 16-row table (data anchored in `data/project_status.json` `products[].checklist` entries):
   ```html
   <section id="specs-codes" class="specs-section">
       <h2 class="specs-section-title">SKU and barcode reference</h2>
       <p class="specs-section-explainer">For manufacturer-share comms. Confirm with print partner before run.</p>
       <div class="specs-codes-table-wrap">
       <table class="specs-codes-table">
           <thead>
               <tr><th>Product</th><th>SKU</th><th>Barcode</th><th>Status</th><th>Notes</th></tr>
           </thead>
           <tbody>
               <tr><td>Pure Carob Bar CDU</td><td>-</td><td>0743966644696</td><td>Paid</td><td>50% master template</td></tr>
               <tr><td>Goji and Coconut Bar CDU</td><td>-</td><td>0743966127625</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Cayenne Chilli Bar CDU</td><td>-</td><td>0743966644719</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Salted Almond Bar CDU</td><td>-</td><td>0743966644733</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Peppermint Buckwheat Bar CDU</td><td>-</td><td>0743966644757</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Roasted Hazelnut Bar CDU</td><td>-</td><td>0743966644771</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Pure Carob Moon CDU</td><td>-</td><td>0743966644641</td><td>Paid</td><td>100% master design</td></tr>
               <tr><td>Coconut and Goji Moon CDU</td><td>-</td><td>0743966644542</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Almond Celtic Salt Moon CDU</td><td>-</td><td>0743966644566</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Cayenne Chilli Moon CDU</td><td>-</td><td>0743966644580</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Roasted Hazelnut Moon CDU</td><td>-</td><td>0743966644603</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Peppermint Buckwheat Moon CDU</td><td>-</td><td>0743966644627</td><td>Paid</td><td>15% clone</td></tr>
               <tr><td>Banana 4-pack</td><td>MM_MUL_BANN_4PK</td><td>0743966127632</td><td>Paid</td><td>80g, NIP 320kJ/1600kJ</td></tr>
               <tr><td>Banana CDU</td><td>MM_CDU_BANN</td><td>0743966644665</td><td>Paid</td><td>-</td></tr>
               <tr><td>Pure Carob Elixir 250ml</td><td>MM_ELX_PCAR_250ML</td><td>pending</td><td>In progress</td><td>AFQA color and copy in flight</td></tr>
               <tr><td>Spicy Elixir 250ml</td><td>MM_ELX_SPIC_250ML</td><td>pending</td><td>In progress</td><td>AFQA color and copy in flight</td></tr>
           </tbody>
       </table>
       </div>
   </section>
   ```
3. Add CSS for `.specs-section`, `.specs-section-title`, `.specs-section-explainer`, `.specs-codes-table-wrap` (horizontal scroll wrapper for narrow viewports), and `.specs-codes-table`. Match the Billing-section aesthetic (white background, 8px radius, subtle shadow, mm-dark-blue header text).
4. Verify in browser:
   - Specs tab shows the table at top with all 16 rows visible
   - Existing Spec Tracker content below, unchanged
   - Table scrolls horizontally on mobile rather than wrapping awkwardly
5. Commit: `feat(specs): add SKU and barcode reference table for manufacturer share`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` `#specs-tab` block (around lines 4970-4992)
- `~/maplemoon-dashboard/data/project_status.json` (source of truth for barcodes and SKUs; verify the curated values above match before commit)
</read_first>

<acceptance_criteria>
- `grep -c 'id="specs-codes"' index.html` returns 1
- `grep -c "specs-codes-table" index.html` returns at least 2 (CSS + element)
- `grep -c '0743966' index.html` returns at least 14 (12 CDUs + 2 Banana entries)
- `grep -c 'MM_MUL_BANN_4PK\|MM_CDU_BANN\|MM_ELX_PCAR\|MM_ELX_SPIC' index.html` returns at least 4
- In browser, Specs tab shows the 16-row reference table at top
- Existing Spec Tracker content still renders below the new table
- No JS console errors
- `git log -1 --pretty=%s` contains "SKU" or "barcode"
</acceptance_criteria>
</task>

<task id="T6" name="W6 Billing footer cross-link to Archive#quote">
<action>
1. In `index.html`, locate the AFQA section render code (search for `billing-afqa` or the section that renders AFQA invoices from `billing.json`). Find the bottom of the AFQA section render template.
2. Add a footer paragraph after the AFQA invoices list, inside the section render template:
   ```html
   <p class="billing-cross-link">
       See the original quote and invoice rationale -
       <button class="billing-cross-link-btn" onclick="archiveOpen('quote-tab')">View in Archive</button>
   </p>
   ```
   Note: uses the existing `archiveOpen` helper from T2 so breadcrumb behavior is consistent.
3. Add CSS for `.billing-cross-link` and `.billing-cross-link-btn`. Style as inline-link, not a primary button (subtle, not competing with main billing UI).
4. Verify in browser:
   - Billing tab AFQA section shows the cross-link at the bottom
   - Clicking the link opens the Quote tab via Archive flow
   - Breadcrumb "← Back to Archive" appears (from T7's sessionStorage flag, OR set `mm:returnTo` to `billing` here for a "Back to Billing" breadcrumb instead - decision: use `billing` so the back link is contextually accurate)
5. Update `archiveOpen` (or call directly) to accept an optional `returnTo` argument: `archiveOpen('quote-tab', 'billing')`. Default if omitted: `'archive'`.
6. Pre-flight em-dash sweep on the new copy.
7. Commit: `feat(billing): cross-link to Archive quote for original invoice rationale`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` Billing tab render code (search `billing-afqa` and the JS that builds the section)
- `~/maplemoon-dashboard/index.html` `archiveOpen` definition (from T2)
- `~/maplemoon-dashboard/data/billing.json` (confirm AFQA section shape)
</read_first>

<acceptance_criteria>
- `grep -c "billing-cross-link" index.html` returns at least 2 (CSS + element)
- `grep -c "View in Archive" index.html` returns 1
- `grep -c "—" index.html` returns 0 (no em-dashes in new copy)
- In browser, Billing tab AFQA section shows cross-link at bottom
- Click cross-link → Quote tab opens with breadcrumb "← Back to Billing" (or "← Back to Archive", per T7 wiring decision)
- No JS console errors
- `git log -1 --pretty=%s` contains "Archive quote" or "invoice rationale"
</acceptance_criteria>
</task>

<task id="T9" name="W8 visual refresh: typography + spacing + hero H1 cleanup on 5 surviving tabs">
<action>
1. **Hero H1 cleanup.** In `index.html` around line 4128, replace `<h1>Project Portal - Updated Feb 2026</h1>` with `<h1>MapleMoon Project Portal</h1>`. The staleness pill below the H1 already carries the freshness signal. Also update the document `<title>` element (line 6) and any meta `og:title` from "MapleMoon Project Portal - Updated Feb 2026" to "MapleMoon Project Portal".
2. **Surface tab nav active-state colour pick to Nate BEFORE applying.** Two options:
   - (a) Keep `#D4A574` coral as-is (intentional brand spice)
   - (b) Swap to `var(--mm-deep-blue)` for palette consistency
   STOP and ask Nate; do not unilaterally pick. The default is `#D4A574` per existing CSS; only change if Nate picks (b).
3. **Typography scale.** Add explicit CSS rules in the existing `<style>` block:
   - `.tab-content h1`: 2rem / 700, Crimson Text serif, `var(--mm-dark-blue)`
   - `.tab-content h2`: 1.5rem / 600, Inter sans, `var(--mm-deep-blue)`
   - `.tab-content h3`: 1.15rem / 600, Inter sans, `var(--mm-dark-blue)`
   - `.tab-content p`: 1rem / 400 (bumped from 0.95rem to hit WCAG 16px ideal)
   - Labels / pills: 0.78rem / 600, uppercase
4. **Spacing rationalisation.** Add CSS for surviving tabs (`#tracker-tab`, `#billing-tab`, `#specs-tab`, `#files-tab`, `#archive-tab`):
   - Section gap (between major blocks within a tab): 32px
   - Card padding (inside `.financial-card`, `.billing-section`, equivalent): 24px desktop, 16px mobile
   - Inline element gap (between header items, money rows): 16px
5. **Inline-style cleanup.** Find and remove ad-hoc inline `style="font-size:..."` and `style="margin:..."` overrides on h1/h2/h3/p elements WITHIN the 5 surviving tab divs only (do NOT touch retired tab content). Class rules from steps 3 and 4 supersede.
6. **Apply Nate's tab nav active-state colour pick from step 2** to the `.tab-button.active` CSS rule.
7. Verify in browser at 1440 / 768 / 480 / 375px:
   - H1 reads "MapleMoon Project Portal" (no date)
   - 5 surviving tabs render with the new type rhythm
   - No JS console errors
   - Tab nav active state matches Nate's pick
8. Commit: `style(w8): typography scale, spacing rationalisation, hero H1 cleanup`
</action>

<read_first>
- `~/maplemoon-dashboard/index.html` lines 1-1290 (global CSS, includes existing `.tab-button.active` rule and tab-nav styles)
- `~/maplemoon-dashboard/index.html` line 6 (document `<title>` element) and line 4128 (hero H1)
- Spec section "W8. Small visual refresh on the 5 surviving tabs" in `docs/superpowers/specs/2026-05-28-portal-consolidation-design.md` lines 211-246
- The 5 surviving tab divs after T3 lands: `#tracker-tab` (4957), `#billing-tab` (4947), `#specs-tab` (4970), `#files-tab` (6842), `#archive-tab` (T2-added)
</read_first>

<acceptance_criteria>
- `grep -c 'MapleMoon Project Portal' index.html` returns at least 2 (H1 + title meta)
- `grep -c 'Updated Feb 2026' index.html` returns 0 (stale date removed from H1 and title)
- `grep -cE '\.tab-content h1' index.html` returns at least 1
- `grep -cE '\.tab-content h2' index.html` returns at least 1
- `grep -cE '\.tab-content h3' index.html` returns at least 1
- `grep -cE '\.tab-content p\b' index.html` returns at least 1
- Tab nav active-state colour matches Nate's pick (coral `#D4A574` OR `var(--mm-deep-blue)`)
- 5 surviving tabs render at 1440 / 768 / 480 / 375px with no horizontal overflow, no JS console errors
- `git log -1 --pretty=%s` contains "w8" or "typography"
</acceptance_criteria>
</task>

<task id="T8" name="Verification pass at four viewport widths">
<action>
1. Start dev server: `cd ~/maplemoon-dashboard && python3 -m http.server 8765` (or equivalent).
2. Open `http://localhost:8765/` in browser. Open DevTools, switch to Responsive Design Mode.
3. For each viewport (1440px desktop, 768px tablet, 480px mobile, 375px iPhone SE):
   a. Tab nav fits without horizontal clipping (or scrolls correctly at <600px)
   b. All 5 nav buttons visible / reachable
   c. Status tab: This week cards render correctly; Assets section renders below kanban
   d. Billing tab: 3 sections render; cross-link visible and functional
   e. Specs tab: dimensions table renders; existing tracker below
   f. Final Files tab: links render
   g. Archive tab: 8 cards render in 2-col grid at desktop, 1-col at <600px
   h. Click each Archive card "View" → target tab opens with breadcrumb
   i. Breadcrumb click → returns to Archive
   j. Click any direct nav button → breadcrumb cleared
   k. No JS console errors at any step
4. Em-dash sweep on the full diff: `git diff main feature/portal-consolidation -- index.html data/archive_index.json data/milestones.json | grep "^+" | grep "—" | head` should return empty.
5. Kill dev server (`lsof -i :8765` + kill PID if needed).
6. If any task above tweaked anything during verification, final commit: `chore: verification fixups`. Otherwise no commit.
</action>

<read_first>
- All task acceptance criteria above
</read_first>

<acceptance_criteria>
- All 7 task acceptance criteria pass
- Visual verification at all 4 viewports shows no layout breaks
- `git diff main feature/portal-consolidation | grep "^+" | grep "—" | wc -l` returns 0
- Dev server stopped cleanly after verification
- Branch has 7 atomic commits (T1-T7), optional T8 fixup
</acceptance_criteria>
</task>

</tasks>

<execution_notes>
**PR grouping for the parent session to ship after this phase executes:**
- PR-1 = T1 (data scaffolding, isolated, mergeable first)
- PR-2 = T2 + T3 + T7 (Archive content + nav restructure + breadcrumbs; the visible cluster)
- PR-3 = T4 (Status enhancements)
- PR-4 = T5 + T6 (Specs + Billing finishing)

Nate can collapse these PRs further if review bandwidth permits; the atomic commit history allows any 1-2-3-4 ordering.

**Why sequential not parallel:** T2 through T7 all touch `index.html` in different sections. Parallel execution would require careful conflict resolution; sequential is safer and the time cost is small (each task is a focused diff).

**Checkpoint protocol:** If any task fails its acceptance criteria, stop and surface to Nate before continuing. Do NOT auto-skip to the next task.

**Commit discipline:** Each task is one commit. NEVER amend. NEVER squash. Atomic history makes review and revert easier.

**No deploy:** Nate ships this manually after reviewing the branch. T8 verification does NOT trigger Vercel.

**No CLAUDE.md / memory touches:** read-only.

**Backup:** Working on a feature branch; git is the safety net. No `cp -r` backup needed for these additive changes.

**XSS hardening:** The repo's established renderer pattern uses `innerHTML` with template literals against same-origin hand-curated JSON (Phase 01 set this precedent). Phase 02 follows the convention but adds an `escapeHtml` helper applied to every interpolated text field, plus a `safeStatus` allowlist on any field that maps to a CSS class. Click handlers are wired post-render via `addEventListener` and `data-` attributes rather than inline `onclick="fn('${...}')"` to keep dynamic values out of HTML-attribute string interpolation paths. This is a defensive convention against future hand-edits in `archive_index.json` / `milestones.json` containing `<`, `>`, `&`, `"`, or `'`. No DOMPurify dependency added: data sources remain hand-curated and same-origin.

**Per-task Time Estimate:**
- T1: 30-45 min (curate 8 cards + 10 milestones)
- T2: 60-90 min (new tab content, JS renderer, CSS)
- T3: 30 min (nav restructure; small high-leverage diff)
- T7: 30-45 min (breadcrumb logic)
- T4: 60-90 min (This week + Assets fold-in; coupling to existing assets renderer is the unknown)
- T5: 30-60 min (dimensions table; depends on whether values are pre-curated)
- T6: 20-30 min (single cross-link + helper update)
- T8: 30 min (4-viewport visual sweep)
- Total: 4.5-6.5 hours of focused work
</execution_notes>

<verification_criteria>
The phase passes when:
1. All 7 tasks (T1-T7) pass their acceptance_criteria
2. T8 verification pass completes with no layout breaks at 4 viewports
3. Branch `feature/portal-consolidation` has 7 atomic commits (T1-T7), optionally plus a T8 fixup
4. Handoff file appended with DONE status (after PRs are shipped, not after plan completion)
5. No CLAUDE.md, memory, `~/maplemoon-website`, or Vercel touches
6. Tab nav has exactly 5 buttons in order: Status, Billing, Specs, Final Files, Archive
7. All 8 retired tabs are reachable in one click from Archive
8. Billing tab has working cross-link to Quote via Archive flow
9. No em-dashes in any new client-visible copy
10. Dashboard at `localhost:8765` is fully functional at 1440 / 768 / 480 / 375px viewports
</verification_criteria>
