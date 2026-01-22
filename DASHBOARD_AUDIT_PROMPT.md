# MapleMoon Dashboard Comprehensive Audit

Run this audit to check the dashboard at:
https://dashboarddeployment.vercel.app/

---

## 1. PRICING VERIFICATION
Search index.html and project_status.json for all prices and verify:

| Category | Expected | Check |
|----------|----------|-------|
| Bars Total | $1,567.09 | [ ] |
| Pure Carob Bar (Master 50%) | $626.84 | [ ] |
| Other 5 Bars (Clone 15% each) | $188.05 x 5 = $940.25 | [ ] |
| Moons Total | $1,567.09 | [ ] |
| Pure Carob Moon (Master 50%) | $626.84 | [ ] |
| Other 5 Moons (Clone 15% each) | $188.05 x 5 = $940.25 | [ ] |
| Bar CDUs Total | $2,350.61 | [ ] |
| Pure Carob Bar CDU (Master 50%) | $940.26 | [ ] |
| Other 5 Bar CDUs (Clone 15% each) | $282.07 x 5 = $1,410.35 | [ ] |
| Moon CDUs Total | $3,290.86 | [ ] |
| Pure Carob Moon CDU (NEW 100%) | $1,880.51 | [ ] |
| Other 5 Moon CDUs (Clone 15% each) | $282.07 x 5 = $1,410.35 | [ ] |
| Bananas | $162.12 | [ ] |
| Banana CDU (50% mates) | $940.26 | [ ] |
| Icons Total | $151.25 | [ ] |
| 4 Updated Icons (25%) | $30.25 | [ ] |
| 4 New Icons (100%) | $121.00 | [ ] |
| **PROJECT TOTAL** | **$10,029.28** | [ ] |

---

## 2. PAYMENT STATUS VERIFICATION

| Item | Expected Status | Check |
|------|-----------------|-------|
| Original Project ($10,980.21) | PAID | [ ] |
| Gap Period INV-0341 ($811.24) | PAID | [ ] |
| Total Paid | $11,791.45 | [ ] |
| Phase 1 Due (Bars/Moons/Bar CDUs/Icons) | $5,636.04 | [ ] |
| Phase 2 Pending (Bananas/Banana CDU/Moon CDUs) | $4,393.24 | [ ] |
| Total Relationship Value | $21,820.73 | [ ] |

---

## 3. DEADLINE CONSISTENCY
Search for ALL date references and verify they match current deadline:

**Expected values:**
- Primary deadline: **February 13, 2026**
- No Christmas references remaining
- No CNY/Jan 13 references remaining
- Week timelines are generic (Week 1, Week 2, etc.)

**Search commands:**
```bash
# Check for old date references
grep -n "Dec\|December\|Christmas\|CNY\|Jan 13\|2025-12" index.html
grep -n "Dec\|December\|Christmas\|CNY\|Jan 13\|2025-12" data/project_status.json
```

---

## 4. CALCULATION VERIFICATION
Verify these totals add up correctly:

```
Phase 1: $1,567.09 + $1,567.09 + $2,350.61 + $151.25 = $5,636.04
Phase 2: $162.12 + $940.26 + $3,290.86 = $4,393.24
Project Total: $5,636.04 + $4,393.24 = $10,029.28
Relationship: $10,980.21 + $811.24 + $10,029.28 = $21,820.73
```

---

## 5. UI/CONTENT CHECKS

- [ ] All finance cards show correct amounts
- [ ] Gap Period shows "PAID" with green styling
- [ ] AFQA shows "IN PROGRESS" status
- [ ] Primary Actions show Phase 1 as current invoice
- [ ] Phase 2 button is disabled/pending
- [ ] Downloadable summary text is accurate
- [ ] Contact section has current date

---

## 6. DATA CONSISTENCY
Compare index.html hardcoded values with project_status.json:

- [ ] Product prices match in both files
- [ ] Status values match (in_progress, ready, blocked)
- [ ] Aggregate values (inProgressValue, blockedValue, readyValue) are correct
- [ ] targetDate is "2026-02-13" in project_status.json

---

## 7. FUNCTIONAL CHECKS

- [ ] All tabs load correctly (Finance, Tracker, Specs, Assets)
- [ ] Kanban board populates from JSON
- [ ] Download buttons work
- [ ] Copy to clipboard works
- [ ] Tooltips display correct info
- [ ] Countdown timer targets Feb 13, 2026

---

## 8. COMMON ISSUES TO CHECK

- [ ] Inconsistent decimal places ($2,350.61 vs $2,350.63)
- [ ] Old prices in tooltips or JavaScript comments
- [ ] Stale dates in "Updated:" timestamps
- [ ] Orphaned references to old statuses
- [ ] JavaScript errors in console

---

## Quick Verification Commands

```bash
# Verify no old dates remain
grep -rn "Christmas\|Dec 22\|Dec 23\|Jan 13\|CNY" .

# Check targetDate in JSON
grep "targetDate" data/project_status.json

# Check all "Updated" references
grep -n "Updated" index.html

# Verify countdown target in JS
grep -n "blockerDeadline\|targetDate" index.html
```

---

## Last Audit
- Date: _____________
- By: _____________
- Issues Found: _____________
- Status: [ ] PASS / [ ] FAIL
