# MapleMoon Dashboard - Deployment Info

**Deployed**: 2025-11-27

---

## Production URLs

**Live Dashboard**: https://dashboarddeployment.vercel.app

**GitHub Repository**: https://github.com/Handtomouse/maplemoon-dashboard

**Vercel Project**: dashboard_deployment

**Latest Deployment**: https://dashboarddeployment-m5s4s2xkk-handtomouses-projects.vercel.app

---

## What's Deployed

Interactive client dashboard for MapleMoon AFQA Compliance Quote with:

- ✅ Embedded invoice PDF (INV-0341)
- ✅ Fixed Xero payment link (no more 500 error)
- ✅ Fixed approval email (mailto works now)
- ✅ All quote details and pricing
- ✅ Visual stage breakdown

---

## Deployment Details

**Platform**: Vercel
**Build**: Static HTML (no build process)
**Source**: GitHub auto-deploy (main branch)
**Size**: 157.6 KB (includes embedded PDF)

---

## Auto-Deploy Enabled

Any push to `main` branch will automatically redeploy:

```bash
cd /Users/handtomouse/Desktop/MrCC_PAI_Stage1_Files/UFC/clients/maplemoon/dashboard_deployment

# Make changes to index.html
git add .
git commit -m "Update dashboard"
git push

# Vercel auto-deploys in ~30 seconds
```

---

## Testing Checklist

- [ ] Visit: https://dashboarddeployment.vercel.app
- [ ] Click "Download Invoice" → Should download INV-0341.pdf
- [ ] Click "Make a Payment" → Should open Xero invoice page
- [ ] Click "Approve Quote" → Should open email with pre-filled message

---

## Client Sharing

Send this URL to MapleMoon (Dylan/Carli):

**https://dashboarddeployment.vercel.app**

Dashboard is live and ready for client review!

---

## Logs & Monitoring

**Deployment Logs**: https://vercel.com/handtomouses-projects/dashboard_deployment

**Inspect Latest**: `vercel inspect dashboarddeployment-ckk9l014m-handtomouses-projects.vercel.app --logs`

---

**Deployed by**: Claude Code
**Project**: MapleMoon AFQA Compliance Packaging
**Invoice**: INV-0341 ($811.24 for gap period Aug-Oct 2025)
