# VisitWizard / MeetMTP CMS Event Extraction

## Platform
VisitWizard powers tourism/Chamber of Commerce event calendars. Look for "Meet Here" branding or VisitWizard footer.

**Known sites:** meetmtp.com (Mt. Pleasant MI), visitlansing.org, and ~50+ other tourism boards.

## Recognizing VisitWizard Sites
- URL patterns: `/events/?view=list`, `/events/?view=calendar`
- "Meet Here" / "Plan Your Visit" navigation
- Tab filters: "Visitor Events", "Local Events", "All", "Calendar View"
- Events load dynamically via JavaScript — **server HTML returns empty event containers**

## DOM Structure (after JS renders)

```
main
└── .view-list-view (or similar container)
    └── p
        └── a[href="/event/..."]  ← each event link
            └── textContent: "DDmonthHH:mm am/pmHH:mm am/pmTitle..."
```

**Text format (concatenated, no spaces):**
```
04may6:00 pm8:00 pmColored Pencil Drawing: Advanced6:00 pm - 8:00 pm(GMT-04:00) 
Event Organized ByArt Reach of Mid MichiganArt Reach of Mid Michigan, 111 E Broadway St, Mt Pleasant, MI 48858Event Type Arts & Crafts, Class & Workshop
```

Components:
1. `DD` - Day of month (no leading zero always)
2. `month` - 3-letter lowercase month (jan, feb, mar...)
3. `HH:mm am/pm` - Start time (no space from month)
4. `HH:mm am/pm` - End time (no space from start)
5. `Title` - Event title (no space from end time)
6. `HH:mm am/pm - HH:mm am/pm` - Full time range
7. `(GMT-04:00)` - Timezone
8. `Event Organized By` - Organizer label (no space before)
9. `Organizer Name` - Organization
10. `Address` - Venue address
11. `Event Type` - Category tags

## ⚠️ Critical Pitfalls

1. **Events are JS-rendered** — curl/urllib will return empty containers. Must use browser automation.
2. **Text is concatenated** — No spaces between date, time, and title fields. Parse with regex, not string splitting.
3. **Duplicate events** — Same event appears multiple times across recurring instances. Deduplicate by URL.
4. **`/var/ri-X.l-L1` suffixes** — Recurring instances have unique URL suffixes but same title. Keep unique URLs.
5. **Show More button** — Only first ~12 events render initially. Click "Show More" to load all.
6. **ICS download available** — Link with text "Download all events as ICS file" exists on page. Alternative extraction path.

## Working Extraction Script

```javascript
var evts = [];
document.querySelectorAll('main p>a[href*="/event/"]').forEach(function(a) {
  var t = a.textContent.trim();
  var m = t.match(/^(\d{2})(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(\d{1,2}:\d{2}\s*(?:am|pm))(\d{1,2}:\d{2}\s*(?:am|pm))(.*)$/is);
  if (m) {
    var day = m[1];
    var month = m[2].toUpperCase();
    var startTime = m[3];
    var endTime = m[4];
    var rest = m[5];
    var fullTime = startTime + ' - ' + endTime;
    // Title ends at the space before the full time range followed by (GMT
    var titleMatch = rest.match(/^(.*?)\s*\d{1,2}:\d{2}\s*(?:am|pm)\s*-\s*\d{1,2}:\d{2}\s*(?:am|pm)\s*\(/);
    var title = titleMatch ? titleMatch[1].trim() : rest.substring(0, 80);
    if (title.length > 3) {
      evts.push({date: day + ' ' + month, title: title, time: fullTime, url: a.href});
    }
  }
});
// Deduplicate by URL
var seen = {};
var unique = evts.filter(function(e) { return seen[e.url] ? false : (seen[e.url] = true); });
JSON.stringify(unique)
```

## URL Parameters

- `?view=list` — List view (events render here)
- `?view=calendar` — Calendar grid view
- `?event_type_2=visitor&event_type_2_id=657` — Visitor events filter
- `?event_type_2=local&event_type_2_id=656` — Local events filter

## Alternative Extraction: ICS Feed

If direct DOM extraction fails, use the ICS download link:
1. Find `<a>` with text "Download all events as ICS file"
2. Navigate to the URL — it triggers an `.ics` file download
3. Parse ICS format for structured event data
