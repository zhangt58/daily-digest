# Midland, MI — Domain Discovery Failures

## Goal
Find a working visitor bureau / CVB event calendar for Midland, Michigan.

## Candidate Domains Tested

| Domain | Status | Notes |
|--------|--------|-------|
| `midlandmichigan.org` | ❌ DNS doesn't resolve | `dig +short` returns nothing. |
| `midlandmichigan.com` | ❌ Domain for sale | Redirects to Afternic/GoDaddy. |
| `visitmidlandmi.com` | ❌ DNS resolves but no site | Cloudflare IP `162.159.134.42`, browser fails `ERR_NAME_NOT_RESOLVED` — parked domain with no active origin. |
| `visitmidland.com` | ❌ Texas | Midland, Texas visitor bureau. |
| `midlandchamber.org` | ❌ Texas | Redirects to `midlandtxchamber.com`. |
| `www.cityofmidland.org` | ⚠️ Empty page | Loads blank `/lander`. |
| `midlandmuseum.org` | ❌ DNS doesn't resolve | |

## Eventbrite (Alternative)
- **URL:** `eventbrite.com/d/mi--midland/`
- Has real events for Midland, MI but **Angular-rendered SPA** — `document.querySelectorAll()` returns 0. Not scrapable for cron.

## Verdict
**Midland, MI has no active visitor bureau event calendar.** Skip from automated monitoring.
