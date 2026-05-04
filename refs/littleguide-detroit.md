# Mid Michigan & Lake Michigan Events — Working Extraction Examples

## Site 1: LittleGuide Detroit (Detroit Metro)

Site: https://littleguidedetroit.com/events/
Plugin: WordPress The Events Calendar (Ed TEC)

## DOM Structure

Each event is an `<article>` with these child selectors:

| Field     | Selector            | Notes                                  |
|-----------|---------------------|----------------------------------------|
| Date      | `.edtec-badge`      | e.g. "May 3"                           |
| Title     | `.edtec-title a`    | Link text (not the `<h3>` wrapper)     |
| Time      | `.edtec-time`       | e.g. "12:00 PM - 4:00 PM"             |
| Location  | `.edtec-venue`      | Venue name                             |
| URL       | `.edtec-more` href  | Full event page URL                    |

## Extraction JavaScript

```javascript
var evts = [];
var arts = document.querySelectorAll('article');
arts.forEach(function(art) {
  var date = art.querySelector('.edtec-badge');
  var title = art.querySelector('.edtec-title a');
  var time = art.querySelector('.edtec-time');
  var venue = art.querySelector('.edtec-venue');
  var moreLink = art.querySelector('.edtec-more');
  var d = date ? date.textContent.trim() : '';
  var t = title ? title.textContent.trim() : '';
  var tm = time ? time.textContent.trim() : '';
  var v = venue ? venue.textContent.trim() : '';
  var url = moreLink ? moreLink.getAttribute('href') : '';
  if (t) evts.push({date: d, title: t, time: tm, location: v, url: url});
});
JSON.stringify(evts)
```

## Cron Extraction (for weekly reminders)

Use the JS above, then format as Discord markdown:

```
📅 **SATURDAY, May 10**
• [Event Name](url) — Time @ Location
```

## Known Venues & Coordinates

These recur frequently — use as a lookup table before geocoding:

```json
{
  "KENSINGTON METRO PARK FARM CENTER, MI": [42.4914, -83.0936],
  "PLYMOUTH HISTORICAL MUSEUM, MI": [42.4207, -83.4976],
  "Starr-Jaycee Park, Detroit, MI": [42.3766, -83.0586],
  "FARMINGTON COMMUNITY LIBRARY, MI": [42.4783, -83.3965],
  "BELLE ISLE NATURE CENTER, Detroit, MI": [42.3421, -82.9717],
  "Greektown, Detroit, MI": [42.3386, -83.0476],
  "Longway Planetarium, Detroit Zoo, MI": [42.4753, -83.3901],
  "John Ball Zoo, Grand Rapids, MI": [42.9626, -85.6669],
  "Theut's Flower Barn, MI": [42.5157, -83.1529],
  "Blake Farms and Apple Orchard, MI": [42.4480, -83.1265],
  "CRANBROOK SCIENCE MUSEUM, Bloomfield Hills, MI": [42.5023, -83.2668],
  "MSU Tollgate Farm, East Lansing, MI": [42.7165, -84.4987]
}
```

## Pitfalls

- The `.edtec-title` is an `<h3>` wrapper — extract text from the `<a>` inside it to also get the URL
- `.edtec-more` is the "Learn More" link — use `getAttribute('href')` for the full event URL
- Page loads 75+ events but only ~44 unique after dedup (recurring events share coords)
- Always scroll to bottom before extracting: `window.scrollTo(0, document.body.scrollHeight)`

---

## Site 2: South Haven Area Chamber

Site: https://www.southhavenmi.com/events/
Events: 928 total, 10 per page

### DOM Structure

| Field | Selector | Notes |
|-------|----------|-------|
| Card container | `.row.gz-cards.gz-events-cards .gz-events-card` | 10 cards/page |
| Title + URL | `h5.gz-card-title a` | `.textContent` and `.href` |
| Date start | `li.gz-card-date a.card-link span[content]` | Text + ISO in `content` attr |
| Date end | `span.gz-card-end-date, meta[content]` | Optional |
| DateTime (ISO) | `span[content]` → `.getAttribute('content')` | e.g. `2026-05-03T07:00` |
| Categories | `.gz-events-cat .gz-cat` | Multiple per card |
| **Time** | ⚠️ Not in list view | Extract from ISO datetime |
| **Location** | ⚠️ Requires detail page | Visit event URL to get |

### Extraction JavaScript

```javascript
var evts=[];
document.querySelectorAll('.row.gz-cards.gz-events-cards .gz-events-card').forEach(function(c){
  var tl=c.querySelector('h5.gz-card-title a');
  var ds=c.querySelector('li.gz-card-date a.card-link span[content]');
  var es=c.querySelector('span.gz-card-end-date,meta[content]');
  var cats=[];
  c.querySelectorAll('.gz-events-cat .gz-cat').forEach(function(x){cats.push(x.textContent.trim());});
  var dt=ds?ds.getAttribute('content')||'':'';
  var time='All day';
  if(dt&&dt.split('T')[1]&&dt.split('T')[1]!=='00:00') time=dt.split('T')[1].substring(0,5);
  if(tl&&tl.textContent.trim())
    evts.push({title:tl.textContent.trim(),url:tl.href||'',dateStart:ds?ds.textContent.trim():'',dateEnd:es?es.textContent.trim():'',time:time,categories:cats});
});
JSON.stringify(evts)
```

### Pitfalls
- Only 10 cards per page, no pagination buttons (use URL params `?Lookahead=30` for more)
- Time and location NOT in listing view — time comes from ISO datetime attr, location requires visiting detail page
- Weekend filtering: check if date text contains "Saturday" or "Sunday"

---

## Site 3: Traverse City

Site: https://www.traversecity.com/events/
Events: ~15 visible per date range

### DOM Structure

| Field | Selector | Notes |
|-------|----------|-------|
| Container | `.shared-items-container li` | Each event |
| Wrapper | `.shared-item` | Has `data-eventid` attr |
| Title + URL | `.contents h2 a` | `.textContent` and `.getAttribute('href')` |
| Date | `.date-range` | e.g. "May 3, 2026" or "Recurring daily until May 10" |
| Location | `.address` | **Must cleanup** — contains map marker accessibility text |
| Image | `.image-container img.thumb` | `.src` |
| **Time** | ⚠️ Requires detail page | Not in listing view |

### Extraction JavaScript

```javascript
var evts=[];
document.querySelectorAll('.shared-items-container li').forEach(function(li){
  var tl=li.querySelector('.contents h2 a');
  var dr=li.querySelector('.date-range');
  var ad=li.querySelector('.address');
  if(tl&&tl.textContent.trim()){
    var loc=ad?ad.textContent.trim():'';
    loc=loc.replace(/\s*map-marker\s*/g,'').trim();
    evts.push({title:tl.textContent.trim(),url:tl.getAttribute('href')||'',date:dr?dr.textContent.trim():'',location:loc});
  }
});
JSON.stringify(evts)
```

### Pitfalls
- `.address` text includes "map-marker" accessibility text — strip it with regex
- Time NOT in listing — must visit detail page
- Date text includes recurring event language like "Recurring daily until..."

---

## Site 4: Grand Haven

Site: https://www.visitgrandhaven.com/events/
Events: ~16 cards visible

### DOM Structure

| Field | Selector | Notes |
|-------|----------|-------|
| Container | `.event-thumbnail` | 2 layouts: featured + standard |
| Title + URL | `h3 a` | `.textContent` and `.getAttribute('href')` |
| Date | `p.strong` containing `\w+ \d{1,2}, \d{4}` | Must regex-match |
| Time | `time` element | e.g. "10:00 am - 11:00 am" |
| Description | `.flex-1 p` | Optional, not on all cards |
| **Location** | ⚠️ Requires detail page | Only on `/events/{slug}/` |

### Extraction JavaScript

```javascript
var evts=[];
document.querySelectorAll('.event-thumbnail').forEach(function(el){
  var tl=el.querySelector('h3 a');
  var d='';
  var ps=el.querySelectorAll('p');
  for(var j=0;j<ps.length;j++){
    if(ps[j].classList.contains('strong')&&ps[j].textContent.trim().match(/\w+ \d{1,2}, \d{4}/)){
      d=ps[j].textContent.trim();break;
    }
  }
  var te=el.querySelector('time');
  if(tl&&tl.textContent.trim())
    evts.push({title:tl.textContent.trim(),url:tl.getAttribute('href')||'',date:d,time:te?te.textContent.trim():''});
});
JSON.stringify(evts)
```

### Pitfalls
- Two card layouts (featured vs standard) — same selectors work for both
- Date is in `p.strong` but must be regex-matched (not all `.strong` paragraphs are dates)
- Location NOT in listing view — requires visiting detail page
- Calendar grid at top is cosmetic; same listing renders regardless of date filter
