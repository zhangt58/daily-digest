---
name: web-monitoring-automation
description: Create automated recurring browser tasks — website monitoring, event tracking, price checking, content summaries. Includes scraping techniques, WordPress/The Events Calendar patterns, and cron job setup.
---

# Automated Web Monitoring

**Trigger:** User wants to monitor a website, track events/news/prices, receive periodic summaries, or create recurring browser-based tasks.

## Workflow

1. **Scrape the site manually first** to understand structure and validate approach
2. **Create extraction code** that works reliably in browser console
3. **Set up cron job** with comprehensive prompt including all steps
4. **Test manually** before scheduling

## Browser Scraping Best Practices

### Extracting Structured Data

When a page has consistent structure, use CSS selectors to extract data programmatically:

```javascript
var items = [];
document.querySelectorAll('container-selector').forEach(function(el) {
  items.push({
    field1: el.querySelector('.selector1')?.textContent?.trim() || '',
    field2: el.querySelector('.selector2')?.textContent?.trim() || '',
    // ...
  });
});
JSON.stringify(items)
```

### Key Principles

- **Test incrementally** — Start with one element, verify it works, then expand
- **Use `.textContent.trim()`** — Cleaner than innerHTML for text extraction
- **Handle missing elements** — Use `?.` optional chaining and fallback values
- **Scroll to load dynamic content** — Some pages load content lazily:
  ```javascript
  window.scrollTo(0, document.body.scrollHeight);
  // Then extract
  ```
- **Inspect DOM structure first** — Use `document.querySelector('first-item')?.innerHTML` to see the actual HTML structure before writing extraction code

## Finding New Sites to Monitor

When user asks for similar event sites or new monitoring targets, `web_search` is NOT available in this environment. Use browser-based discovery with DuckDuckGo or direct URL testing.

See `references/site-discovery.md` for proven browser search techniques and known site landscapes.

### DuckDuckGo Lite Search (programmatic)

For bulk site discovery, use DDG Lite via `urllib` — faster than browser automation:

```python
import urllib.request, urllib.parse, re
query = urllib.parse.quote(f"{city} MI events calendar tourism")
url = f"https://lite.duckduckgo.com/lite/?q={query}"
resp = urllib.request.urlopen(url, headers={'User-Agent': 'Mozilla/5.0'})
html = resp.read().decode('utf-8')
redirects = re.findall(r'uddg=([^&"]+)', html)
for r in redirects:
    decoded = urllib.parse.unquote(r)  # actual URL
```

See `scripts/ddg-search.py` for a reusable bulk search + verify script.

See `references/michigan-event-sites.md` for verified Michigan event sites discovered this way.

## Common Plugin Patterns

### WordPress The Events Calendar

Common structure for Event Calendar plugin:
- Container: `<article>` elements
- Date: `.edtec-badge`
- Title: `.edtec-title` (text from `<h3>` or `<a>`)
- Time: `.edtec-time`
- Location: `.edtec-venue`

See `references/littleguide-detroit.md` for full working extraction example.

### SimpleView CMS (e.g. traversecity.com, visitdestin.com)

SimpleView powers many Destination Marketing Organization (DMO) sites. Key patterns:

- **Container:** `.shared-items-container li` (each `<li>` = one event)
- **Item wrapper:** `.shared-item` with `data-eventid` and `data-recid` attributes
- **Title + URL:** `.contents h2 a` — text is title, `href` is relative URL
- **Date (full):** `.date-range` — text like "May 3, 2026", "Recurring daily until May 10", or "Dates vary between Apr 30 - May 3"
- **Date (display):** `.month` + `.day` — individual month name and zero-padded day
- **Location:** `.address` — ⚠️ **pitfall:** the map marker accessibility text bleeds into this element's `textContent`, producing artifacts like `"Event Title: Map Marker  Actual Venue Name"`. Clean by stripping the event title + `: Map Marker` prefix.
- **Image:** `.image-container img.thumb` — `src` attribute
- **Time:** NOT present in listing view — requires detail page navigation
- **Detail page pattern:** `/event-detail/<slug>/<recid>/`

See `references/simpleview-cms-events.md` for full working extraction script and DOM tree.

### VisitWizard / MeetMTP CMS (e.g. meetmtp.com, ~50+ tourism boards)

VisitWizard powers many tourism/Chamber event calendars. Recognizable by "Meet Here" / "Plan Your Visit" navigation and tab filters ("Visitor Events", "Local Events", "All"). **Critical: events are JS-rendered — server HTML returns empty containers. Must use browser automation.**

Key patterns:

- **Events are `main p>a[href*="/event/"]`** — each link's `textContent` is concatenated date+time+title+organizer (no spaces between fields)
- **Text format:** `DDmonthHH:mm am/pmHH:mm am/pmTitle...` — parse with regex, not string splitting
- **Deduplicate by URL** — recurring events appear multiple times with `/var/ri-X.l-L1` suffixes
- **"Show More" button** — only first ~12 events render initially
- **ICS download link** available as alternative extraction path
- **URL params:** `?view=list` for list view, `?event_type_2=visitor` for visitor filter

See `references/visitwizard-meetmtp.md` for full extraction script and DOM tree.

### Battle Creek Visitor Bureau (e.g. battlecreekvisitors.org)

Custom category-based layout. Events organized under `<h2>` category headings with `<article>` cards:

- **Date:** `time` element with month/day children (no year, no time)
- **Title + URL:** `h3 a`
- **Location:** `li a` (optional — about 50% of events have no venue link)
- **Filter out:** blog posts (`/blog/` URLs), navigation headers ("THIS WEEK", "ANNUAL EVENTS", "ALL EVENTS")
- **Duplicates** across categories — deduplicate by URL
- **~15 events per page** with "Load More" button

See `references/battle-creek-visitor-bureau.md` for full extraction script and DOM details.

### GrowthZone / ChamberMaster CMS (e.g. southhavenmi.com, many .com chambers)

GrowthZone powers many Chamber of Commerce event calendars (look for "GrowthZone - Membership Management Software" link in footer, or `ChamberMaster` branding). Consistent structure across all GrowthZone-powered sites:

- **Card wrapper:** `.row.gz-cards.gz-events-cards` (contains all visible event cards)
- **Event card:** `.gz-events-card` (each card = one event)
- **Title + URL:** `h5.gz-card-title a` — text is title, `href` is detail page URL
- **Date (text):** `li.gz-card-date a.card-link span[content]` — e.g. "Thursday Apr 16, 2026"
- **Date end (text):** `li.gz-card-date a.card-link span.gz-card-end-date` — multi-day events only; single-day events use `<meta content="...">` instead
- **DateTime (ISO 8601):** `span[content].getAttribute('content')` — e.g. `"2026-05-03T07:00"` (time encoded here!)
- **Categories:** `.gz-events-cat .gz-cat` — one `<span>` per category
- **Image:** `.card-header img` or text fallback `.gz-img-placeholder`
- **⚠️ Location NOT in list view** — must navigate to detail page at URL from title link
- **⚠️ Time NOT visible in list view text** — only in `content` attribute on date span. Parse: split on `T`, if second part != `"00:00"` then it has a start time
- **Detail page structure:**
  - Date/time: `.gz-event-date span[itemprop="startDate"]` / `[itemprop="endDate"]`
  - Location: `.gz-event-location span[itemprop="name"]`
  - Fees: `.gz-event-fees .gz-event-fees`
  - Website: `.gz-event-website a[itemprop="url"]`

- **GrowthZone pagination** — Only 10 cards per page, no reliable `per_page` param. Extract first page + use client-side date filtering for weekend events.

See `references/events-watcher-all-sites.md` for full GrowthZone extraction script (South Haven section).

### Grand Rapids CVB (e.g. experiencegr.com)

Custom event directory powered by Experience Grand Rapids. Recognizable by date-range pickers + category/venue dropdowns at top of page. **All events load on initial render — no scroll needed, no JS lazy loading.**

Key patterns:

- **Articles:** Each event is an `<article>` with `h3 a` (title + URL)
- **Date:** Multiple `<span>` elements with overlapping date text — month abbreviation, day number, and full date range. Join matching spans for clean date
- **Location:** Optional — look for `[class*="venue"], [class*="location"], [class*="address"]` — ~50% of events have no venue in list view
- **Time:** NOT in list view — must navigate to detail page
- **~148 events** total on one page with no pagination
- **Detail page:** `/event/<slug>/<id>/`
- **GrowthZone pagination** — Only 10 cards per page, no reliable `per_page` param. Extract first page + use client-side date filtering for weekend events.

See `references/events-watcher-all-sites.md` for full GrowthZone extraction script (South Haven section).

## Geocoding & Map Visualization

When scraped data includes venue names/addresses, you can create an interactive map:

### Geocoding Approach

1. **Use a known-coordinates lookup table** for recurring venues (faster, more reliable)
2. **Fall back to Nominatim API** for unknown locations:
   ```python
   import urllib.request, urllib.parse, json, time
   query = urllib.parse.quote("Venue Name, City, State")
   url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}&limit=1"
   req = urllib.request.Request(url, headers={'User-Agent': 'EventsMap/1.0'})
   resp = urllib.request.urlopen(req, timeout=10)
   data = json.loads(resp.read())
   # data[0]['lat'], data[0]['lon']
   ```
   - **Rate limit:** 0.5s between requests (`time.sleep(0.5)`)
   - **Always send a User-Agent header** — Nominatim rejects requests without one
   - **⚠️ HTTP 403 Forbidden:** After ~20+ requests in a session window, Nominatim returns 403 and blocks ALL further requests from your IP for the remainder of the session. When this happens, **switch to known-coordinates lookup** for all remaining venues. Pre-build a coordinate table for the target region before scraping.
   - **City-center fallback:** For events without specific addresses, use city center coordinates. E.g. South Haven [42.4059, -86.3163], Traverse City [44.7631, -85.6206], Grand Haven [43.0650, -86.2270].

### Interactive Leaflet Map Template

Build single-file HTML maps with:
- Leaflet via CDN (`unpkg.com/leaflet@1.9.4`)
- Category-colored markers (custom `L.divIcon` with CSS circles)
- Sidebar event cards linked to map markers
- Category filter buttons

See `templates/leaflet-events-map.html` for a full working template with:
- Dark/light theme toggle using CSS custom properties (`[data-theme="light"]`)
- Map tile layer swapping (CartoDB Dark ↔ OpenStreetMap)
- `localStorage` persistence + `prefers-color-scheme` system detection
- Category filtering with animated map bounds adjustment

### Theme Toggle Pattern (CSS Variables)

For any single-file HTML output that needs light/dark mode:

```css
:root { --bg: #0f172a; --text: #e2e8f0; /* dark defaults */ }
[data-theme="light"] { --bg: #f1f5f9; --text: #1e293b; }
body { background: var(--bg); color: var(--text); }
```

```js
function setTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  localStorage.setItem('theme', t);
}
// Init: localStorage > system pref > default
const saved = localStorage.getItem('theme');
setTheme(saved || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'));
```

For map tiles, keep a reusable `L.tileLayer` reference and call `tileLayer.setUrl()` on toggle — don't create/destroy layers.

## Cron Job Setup

Create recurring browser tasks with comprehensive prompts:

```python
cronjob(
    action="create",
    name="Descriptive Name",
    schedule="0 10 * * 5",  # Cron format: min hour day month weekday
    deliver="origin",
    enabled_toolsets=["browser", "discord"],  # List ALL needed toolsets
    prompt="Step-by-step instructions that include:\n" +
           "1. Navigate to URL\n" +
           "2. Exact JavaScript extraction code\n" +
           "3. Processing/formatting rules\n" +
           "4. Delivery format"
)
```

### Schedule Format (CRITICAL)

Use standard cron format `min hour day month weekday`:
- `0 10 * * 5` = Every Friday at 10am
- `0 9 * * *` = Daily at 9am
- `*/30 * * * *` = Every 30 minutes

**Never use** natural language like "every Friday at 10am" — it will FAIL with "Invalid duration" error.

### Prompt Design for Cron Jobs

The prompt must be completely self-contained since cron jobs run independently:
- Include exact URLs to visit
- Include complete JavaScript extraction code
- Include formatting instructions
- Include error handling guidance
- Reference specific CSS selectors (not generic descriptions)

### Multi-Site Cron Jobs

When monitoring multiple sites from a single cron job, include all extraction scripts in one prompt with clear delimiters. Structure the prompt with `## Site N: Name` sections, each with its own URL and JS. Add error handling: if one site fails, continue with remaining sites and note failures at the end of the output.

## Merging Data From Multiple Sites

When combining events from multiple scraped sources into one output (HTML map, consolidated JSON, etc.):

1. **Normalize all sites to a common schema** — each event must have `title`, `date`, `time`, `location`, `lat`, `lon`, `category`, `url` at minimum
2. **Add a `site` field** to distinguish origin (e.g. "Detroit Metro", "South Haven")
3. **Deduplicate** by `(title.lower(), site)` — recurring events appear multiple times across date ranges
4. **Geocode unknown venues** before merging — if Nominatim hits 403, use city-center fallback coordinates
5. **Update map center** to cover all regions (wider zoom, centered on geographic middle)

### Injecting Large JSON Into HTML

When embedding a large JSON array into an existing HTML file:

- **DO NOT use `re.sub()`** — JSON contains Unicode escapes (`\u2013`, `\u2019`) that cause `re.error: bad escape` in Python's regex engine
- **Use `str.find()` + string slicing** instead:
  ```python
  start = html.find('const events = [')
  end = html.find('];', start + 200)  # skip ahead past start
  new_json = json.dumps(events)
  html = html[:start] + f'const events = {new_json};' + html[end+2:]
  ```
- **Validate after write** — parse the embedded JSON back out and verify event count

See `references/events-watcher-all-sites.md` for consolidated extraction patterns for all 7 Michigan sites (Detroit, South Haven, Traverse City, Grand Haven, Mt. Pleasant, Battle Creek, Grand Rapids).

## Deploying to GitHub Pages (pocket pattern)

The `pocket` repo (`/home/tong/workspace/pocket/`) uses a build workflow: `.github/workflows/scripts/generate_index.py` creates `dist/` with:
- `dist/index.html` — unified index page linking all reports
- `dist/hn/` — HN daily reports
- `dist/events/` — Michigan events maps + data

Workflow (`.github/workflows/deploy.yml`):
1. `python3 .github/workflows/scripts/generate_index.py` — generates `dist/` from source folders (run from repo root)
2. `actions/upload-pages-artifact@v3` with `path: "dist"`
3. `actions/deploy-pages@v4`

When adding a new section type (e.g. `events/`), update `generate_index.py` to:
1. Add `events_dir` and `dist_events_dir` paths
2. Scan `events_dir` for `.html` files, generate links
3. Copy files to `dist_events_dir` via `shutil.copy2()`
4. Add a new `<ul class="list">` section in the index HTML template

**Note:** The HN cron job and `hackernews-api` skill both reference `/home/tong/workspace/pocket/` as the output path. The events cron job (`6826679aaa01`) now also commits to the repo automatically — it copies updated map/JSON to `pocket/events/`, runs `git add/commit/push`, then delivers to Discord.

## Common Pitfalls

- **Missing toolsets** — If job needs browser + discord, list both in `enabled_toolsets`
- **Vague prompts** — Future agent won't know exact selectors to use
- **Assuming current state** — Don't assume page is already loaded or scrolled
- **Over-extraction** — Extract what's needed, not everything (avoid hitting rate limits)
- **Natural language schedules** — The cron system ONLY accepts standard cron format
- **Nominatim 403 wall** — After ~20 requests, ALL further geocoding fails for the session. Use known coords or city-center fallback immediately.
- **Missing terminal toolset** — If your cron job needs to commit to git or run shell commands, include `"terminal"` in `enabled_toolsets`. Without it, `git add/commit/push` will fail silently.
- **SimpleView map-marker artifact** — `.address` textContent includes "Map Marker" accessibility text. Strip with `.replace(/\s*Map Marker\s*/g, '')`.
- **GrowthZone pagination** — Only 10 cards per page, no reliable `per_page` param. Extract first page + use client-side date filtering for weekend events.
- **VisitWizard JS rendering** — Server returns empty containers. Must use browser automation, then parse concatenated text format (`DDmonthHH:mm...`) from `a[href*="/event/"]` elements. Deduplicate by URL.
- **ITI Digital / imgoingcalendar iframe** — Sites like `experiencejackson.com` load events via `imgoingcalendar.com` scripts with 2 iframes. Events render in shadow DOM inside the iframe — parent page has zero access. No public API/RSS. **Mark as unscrapable, move on.**
- **Blog-style event pages** — Sites like `thingstodoinannarbor.com` are blog articles about annual events with vague dates ("Dates vary yearly", "Memorial Day weekend"). Not proper calendars — no extractable data.
- **CivicPlus broken calendars** — Many cities have `/events` or `/calendar.aspx` that return 404. CivicPlus calendar URLs are unstable — navigate from homepage menu to find working links, or use alternative tourism sites for the same region.
- **Angular/SPA event aggregators (e.g. Eventbrite)** — Sites like Eventbrite render all event cards via Angular (`ng-` directives, shadow DOM). Browser console JS extraction returns empty arrays because the DOM structure the selector targets doesn't exist in the rendered output. Mark as unscrapable via console.
- **Domain discovery failures** — `web_search` doesn't exist. Use `browser_navigate` to DuckDuckGo or `curl` lite.duckduckgo.com for search. Many tourism sites have parked/for-sale domains — verify each URL before investing time. Some cities (e.g. Midland, MI) have no active visitor bureau website — all candidate domains either fail DNS or resolve to Texas. See `references/midland-mi-domain-failures.md` for examples.
- **Subagent URL hallucination** — Delegated agents will invent plausible-looking URLs that don't exist (e.g. `visitmuskegon.com` → 0KB, `marquettetourism.com` → 404). **Always verify every URL with `urllib`/`curl` before trusting subagent output.** Decode DDG redirect URLs from `uddg=` params — never use subagent-guessed domains directly.

## Leaflet Map Pitfalls (single-file HTML maps)

- **Legend clipped at map edge** — Leaflet's `L.control({ position: 'bottomleft' })` places the legend flush against the edge. Fix: add `margin: 12px` and `z-index: 1000` to the `.legend` CSS class so it has padding and renders above map tiles.
- **Stray `</div>` breaking responsive layout** — When building multi-filter-bar headers, an extra closing `</div>` can prematurely close the parent container, hiding subsequent filter rows on larger screens while appearing fine on mobile (because the mobile CSS forces different flow). Always verify the HTML nesting by printing the full header region after string manipulation.
- **Injecting large JSON arrays into HTML** — Never use `re.sub()` on embedded JSON — Unicode escapes (`\u2013`) cause `re.error: bad escape`. Use `str.find()` + slicing instead:
  ```python
  start = html.find('const events = [')
  end = html.find('];', start + 200)
  html = html[:start] + f'const events = {json.dumps(events)};' + html[end+2:]
  ```