# Battle Creek Visitor Bureau — Events Extraction

**URL:** https://www.battlecreekvisitors.org/events/
**CMS:** Custom category-based layout

## DOM Pattern

Each event `<article>`:
- **Date:** `time` children — month name + zero-padded day (e.g. MAY 07)
- **Title + URL:** `h3 a`
- **Location:** `li a` (optional)

## Extraction Script

```javascript
var evts=[];
document.querySelectorAll('article').forEach(function(art){
  var timeEl = art.querySelector('time');
  var titleEl = art.querySelector('h3 a');
  var locEl = art.querySelector('li a');
  if(titleEl && titleEl.textContent.trim()){
    var monthDay = '';
    if(timeEl){
      var texts = Array.from(timeEl.children).map(function(c){return c.textContent.trim();});
      monthDay = texts.filter(function(t){return t;}).join(' ');
    }
    var title = titleEl.textContent.trim();
    var url = titleEl.href || '';
    var location = locEl ? locEl.textContent.trim() : '';
    if(title &&
       title !== 'THIS WEEK ' &&
       title !== 'ANNUAL EVENTS & FESTIVALS ' &&
       title !== 'ALL EVENTS ' &&
       url.indexOf('/event/') >= 0){
      evts.push({date: monthDay, title: title, url: url, location: location || 'Battle Creek, MI'});
    }
  }
});
JSON.stringify(evts)
```

## Gotchas

1. **No time info** — only month + day. Detail page needed for time.
2. **Blog posts mixed in** — filter by `url.indexOf('/event/') >= 0`
3. **Navigation headers** — "THIS WEEK", "ANNUAL EVENTS & FESTIVALS", "ALL EVENTS" are also `<h3 a>`. Filter explicitly.
4. **~15 events per page** — "Load More" available
5. **Duplicates** — same event under multiple categories. Deduplicate by URL.
6. **Missing locations** — fall back to "Battle Creek, MI"

## Coordinates

Battle Creek city center: `42.3211, -85.1797`