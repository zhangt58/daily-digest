# Lake Michigan Events Watcher — All Site Extraction Patterns

## Overview
Consolidated extraction patterns for all 7 monitored Michigan event sites. Used by the "Lake Michigan Weekend Events Watcher" cron job (Friday 10am).

## Site List & Coordinates

| Site | URL | City Center Coords |
|------|-----|-------------------|
| Detroit Metro | https://littleguidedetroit.com/events/ | 42.3314, -83.0458 |
| South Haven | https://www.southhavenmi.com/events/ | 42.4059, -86.3163 |
| Traverse City | https://www.traversecity.com/events/ | 44.7631, -85.6206 |
| Grand Haven | https://www.visitgrandhaven.com/events/ | 43.0650, -86.2270 |
| Mt. Pleasant | https://meetmtp.com/events/ | 43.5975, -84.7423 |
| Battle Creek | https://www.battlecreekvisitors.org/events/ | 42.3211, -85.1797 |
| Grand Rapids | https://www.experiencegr.com/events/ | 42.9634, -85.6681 |

---

## Site 1: LittleGuide Detroit (Detroit Metro)
**Plugin:** WordPress The Events Calendar (Ed TEC)
**URL:** https://littleguidedetroit.com/events/

### Extraction Script
```javascript
var evts=[];
var arts=document.querySelectorAll('article');
arts.forEach(function(art){
  var date=art.querySelector('.edtec-badge');
  var title=art.querySelector('.edtec-title a');
  var time=art.querySelector('.edtec-time');
  var venue=art.querySelector('.edtec-venue');
  var more=art.querySelector('.edtec-more');
  var d=date?date.textContent.trim():'';
  var t=title?title.textContent.trim():'';
  var tm=time?time.textContent.trim():'';
  var v=venue?venue.textContent.trim():'';
  var url=more?more.getAttribute('href'):'';
  if(t) evts.push({date:d,title:t,time:tm,location:v,url:url});
});
JSON.stringify(evts)
```

### Known Venues & Coordinates
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

### Pitfalls
- `.edtec-title` is an `<h3>` wrapper — extract text from the `<a>` inside it
- `.edtec-more` is the "Learn More" link — use `getAttribute('href')`
- Scroll to bottom before extracting: `window.scrollTo(0, document.body.scrollHeight)`
- ~44 unique events after dedup (recurring events share coords)

---

## Site 2: South Haven Area Chamber (GrowthZone)
**Plugin:** GrowthZone / ChamberMaster
**URL:** https://www.southhavenmi.com/events/

### Extraction Script
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
- Only 10 cards per page, no reliable `per_page` param
- Time and location NOT in listing view — time from ISO datetime attr, location requires detail page
- Weekend filtering: check if date text contains "Saturday" or "Sunday"

---

## Site 3: Traverse City (SimpleView CMS)
**Plugin:** SimpleView CMS
**URL:** https://www.traversecity.com/events/

### Extraction Script
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
**Plugin:** Custom CMS
**URL:** https://www.visitgrandhaven.com/events/

### Extraction Script
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
- Date is in `p.strong` but must be regex-matched
- Location NOT in listing view — requires visiting detail page

---

## Site 5: Mt. Pleasant (VisitWizard/MeetMTP)
**Plugin:** VisitWizard CMS
**URL:** https://meetmtp.com/events/

### Extraction Script
```javascript
var evts=[];
document.querySelectorAll('main p>a[href*="/event/"]').forEach(function(a){
  var t=a.textContent.trim();
  var m=t.match(/^(\d{2})(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(\d{1,2}:\d{2}\s*(?:am|pm)|)(\d{1,2}:\d{2}\s*(?:am|pm)|)(.*)$/is);
  if(m){
    var day=m[1];
    var month=m[2].toUpperCase();
    var startTime=m[3]?m[3].trim():'';
    var endTime=m[4]?m[4].trim():'';
    var rest=m[5];
    var fullTime=startTime&&endTime?startTime+' - '+endTime:'All day';
    var titleMatch=rest.match(/^(.*?)\s*\d{1,2}:\d{2}\s*(?:am|pm)\s*-\s*\d{1,2}:\d{2}\s*(?:am|pm)\s*\(/);
    var title=titleMatch?titleMatch[1].trim():rest.substring(0,80);
    if(title.length>3) evts.push({date:day+' '+month,title:title,time:fullTime,url:a.href});
  }
});
var seen={};
var unique=evts.filter(function(e){return seen[e.url]?false:(seen[e.url]=true);});
JSON.stringify(unique)
```

### Pitfalls
- **Events are JS-rendered** — server HTML returns empty containers. Must use browser automation
- **Text is concatenated** — no spaces between date, time, and title fields
- **Duplicate events** — recurring instances have unique URL suffixes. Deduplicate by URL
- **Show More button** — only first ~12 events render initially
- ICS download available as alternative extraction path

---

## Site 6: Battle Creek Visitor Bureau
**Plugin:** Custom category-based layout
**URL:** https://www.battlecreekvisitors.org/events/

### Extraction Script
```javascript
var evts=[];
document.querySelectorAll('article').forEach(function(art){
  var timeEl=art.querySelector('time');
  var titleEl=art.querySelector('h3 a');
  var locEl=art.querySelector('li a');
  if(titleEl&&titleEl.textContent.trim()){
    var monthDay='';
    if(timeEl){
      var texts=Array.from(timeEl.children).map(function(c){return c.textContent.trim();});
      monthDay=texts.filter(function(t){return t;}).join(' ');
    }
    var title=titleEl.textContent.trim();
    var url=titleEl.href||'';
    var location=locEl?locEl.textContent.trim():'';
    if(title&&title!=='THIS WEEK '&&title!=='ANNUAL EVENTS & FESTIVALS '&&title!=='ALL EVENTS '&&url.indexOf('/event/')>=0){
      evts.push({date:monthDay,title:title,url:url,location:location||'Battle Creek, MI'});
    }
  }
});
JSON.stringify(evts)
```

### Pitfalls
- No time info — only month + day. Detail page needed for time
- Blog posts mixed in — filter by `url.indexOf('/event/') >= 0`
- Navigation headers — "THIS WEEK", "ANNUAL EVENTS & FESTIVALS", "ALL EVENTS" are also `<h3 a>`
- ~15 events per page — "Load More" available
- Duplicates across categories — deduplicate by URL
- Missing locations — fall back to "Battle Creek, MI"

---

## Site 7: Grand Rapids (ExperienceGR)
**Plugin:** Custom WordPress event directory
**URL:** https://www.experiencegr.com/events/

### Extraction Script
```javascript
var evts=[];
document.querySelectorAll('article').forEach(function(el){
  var titleEl=el.querySelector('h3 a');
  if(!titleEl||!titleEl.textContent.trim()) return;
  var title=titleEl.textContent.trim();
  var url=titleEl.href||'';
  if(!url.includes('/event/')) return;
  var fullText=el.textContent;
  var dateMatch=fullText.match(/((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})/);
  if(!dateMatch) return;
  var dateStr=dateMatch[1];
  var locMatch=fullText.match(/(?:John Ball Zoo|Belknap Park|Heritage Landing Park|Acrisure Amphitheater|Tulip Time Festival|DeVos Place|Van Andel Arena|The Intersection|GLC Live at 20 Monroe|Midtown Park|Ferry Beach Park)/);
  var locText=locMatch?locMatch[0].trim():'Grand Rapids, MI';
  evts.push({title:title,url:url,date:dateStr,location:locText});
});
JSON.stringify(evts)
```

### Pitfalls
- ~15 actual dated events out of ~148 articles (rest are listings/tours)
- No scroll needed — all events render on initial page load
- Filter by `/event/` in URL, skip `/listing/`
- Known venues: Belknap Park, John Ball Zoo, Acrisure Amphitheater, DeVos Place, Heritage Landing Park, Tulip Time Festival

---

## Git Commit/Push Steps

After scraping and updating the map/JSON, commit to the `pocket` repo:

```bash
cd /home/tong/workspace/pocket && \
  git add -A && \
  git commit -m "Update events map - $(date +%Y-%m-%d)" && \
  git push
```
