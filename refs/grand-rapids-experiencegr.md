# Grand Rapids CVB — experiencegr.com

## Site Info
- **URL:** https://www.experiencegr.com/events/
- **CMS:** Custom event directory (WordPress-based)
- **Organization:** Experience Grand Rapids (CVB)
- **Events per page:** ~148 total, no pagination, no lazy loading

## DOM Structure

Each event is an `<article>` element containing:
- **Title + URL:** `h3 a` — text is title, `href` is detail page URL
- **Date:** Multiple overlapping `<span>` elements in the article text:
  - Month abbreviation (e.g. "Jul")
  - Day number (e.g. "17")
  - Full date range (e.g. "July 17, 2026 - July 18, 2026")
- **Location:** Optional — may appear as venue name in the article text (e.g. "Belknap Park", "John Ball Zoo")
- **Time:** NOT present in list view — requires detail page navigation
- **~50% of articles are listings/tours** without event dates (brewery tours, restaurant tours) — these have `/listing/` URLs and no date

## Extraction JS

```javascript
var evts=[];
document.querySelectorAll('article').forEach(function(el){
  var titleEl = el.querySelector('h2 a, h3 a');
  if(!titleEl || !titleEl.textContent.trim()) return;
  var title = titleEl.textContent.trim();
  var url = titleEl.href || '';
  // Skip non-event pages
  if(!url.includes('/event/')) return;
  // Extract clean date from full article text
  var fullText = el.textContent;
  var dateMatch = fullText.match(/((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})/);
  if(!dateMatch) return; // Skip articles without dates (listings/tours)
  var dateStr = dateMatch[1];
  // Extract known venue names from text
  var locMatch = fullText.match(/(?:John Ball Zoo|Belknap Park|Heritage Landing Park|Acrisure Amphitheater|Tulip Time Festival|DeVos Place|Van Andel Arena|The Intersection|GLC Live at 20 Monroe|Midtown Park|Ferry Beach Park)/);
  var locText = locMatch ? locMatch[0].trim() : 'Grand Rapids, MI';
  evts.push({title: title, url: url, date: dateStr, location: locText});
});
JSON.stringify(evts)
```

## Notes
- Returns ~15 actual dated events out of ~73 articles (rest are listings/tours)
- No scroll needed — all events render on initial page load
- URL pattern for filtering: only keep articles with `/event/` in the URL, skip `/listing/`
- Known venues to look for: Belknap Park, John Ball Zoo, Acrisure Amphitheater, DeVos Place, Heritage Landing Park, Tulip Time Festival
- Coordinates for map: **42.9634, -85.6681** (Grand Rapids city center)
