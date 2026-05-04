# SimpleView CMS Event Extraction

## Platform
SimpleView Inc. — powers Destination Marketing Organization (DMO) / tourism sites:
- traversecity.com
- visitdestin.com
- travelgrandrapids.com
- visitflamingovilles.com
- And ~200+ other tourism boards (assets.simpleviewinc.com)

## Recognizing SimpleView Sites
- Page source / network requests reference `assets.simpleviewinc.com`
- URL patterns: `/event-detail/<slug>/<recid>/`
- Templates use `{{~}}` Mustache-like syntax in `<script type="text/template">` blocks
- Events rendered server-side into `.shared-items-container`

## DOM Tree

```
.listings-wrapper
└── .flex-wrapper
    └── .map-list-cont
        └── .shared-items-container
            └── ul
                └── li (one per event)
                    └── .shared-item item              ← data-eventid, data-recid, data-type
                        ├── .image-container
                        │   ├── .feat-listing          ← "featured" badge (optional)
                        │   ├── a > picture > img.thumb ← event image
                        │   └── .date-cont
                        │       └── .date
                        │           ├── .month          ← "May"
                        │           └── .day            ← "03"
                        └── .contents
                            ├── h2 > a                  ← title + href to detail page
                            ├── .date-range             ← "May 3, 2026" or "Recurring daily until..."
                            ├── .address                ← location ⚠️ see pitfall below
                            └── .quickview-wrapper > a  ← data-qv-url mirrors detail page
```

## CSS Selector Reference

| Selector | Field | Notes |
|---|---|---|
| `.shared-items-container li` | Event container | Count = total visible events |
| `.shared-item` | Item wrapper | `data-eventid`, `data-recid` attrs |
| `.contents h2 a` | Title | `textContent` = title |
| `.contents h2 a` | URL | `href` = relative path |
| `.date-range` | Date (full) | "May 3, 2026", "Dates vary between...", "Recurring daily until..." |
| `.month` | Display month | "May" |
| `.day` | Display day | "03" |
| `.address` | Location | ⚠️ needs text cleanup |
| `.image-container img.thumb` | Image | `src` attribute |

## ⚠️ Pitfall: Address Text Contamination

The `.address` element contains a hidden `<span class="ae-compliance-indent">` with the event title + ": Map Marker" text for screen readers. When you read `.address.textContent`, it bleeds into the result:

```
Bad: "Indoor Sidewalk Sales: Map Marker  The Village at Grand Traverse Commons"
Good: "The Village at Grand Traverse Commons"
```

**Fix:** Strip the title + `": Map Marker"` prefix:
```javascript
var location = addressEl.textContent.trim();
var titleText = titleEl.textContent.trim();
var escaped = titleText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
location = location.replace(new RegExp('^' + escaped + ':\\s*Map\\s*Marker\\s*'), '').trim();
```

## Time Field

Time is NOT present in the listing view at all. No `.time` element exists in `<li>` items. To get time, you must navigate to the detail page.

## Pagination

SimpleView uses `skip` query parameter for pagination. The initial load shows a limited set (typically 10–15). Check for `.map-list-pager` or a "Load More" button. Some sites load all events on the initial render.

## Working Extraction Script

```javascript
(function() {
  var events = document.querySelectorAll('.shared-items-container li');
  var results = [];
  for (var i = 0; i < events.length; i++) {
    var item = events[i];
    var sharedItem = item.querySelector('.shared-item');
    var titleEl = item.querySelector('.contents h2 a');
    var dateRangeEl = item.querySelector('.date-range');
    var addressEl = item.querySelector('.address');
    var imgEl = item.querySelector('.image-container img.thumb');
    var location = addressEl ? addressEl.textContent.trim() : '';
    if (titleEl && location) {
      var escaped = titleEl.textContent.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      location = location.replace(new RegExp('^' + escaped + ':\\s*Map\\s*Marker\\s*'), '').trim();
    }
    results.push({
      title: titleEl ? titleEl.textContent.trim() : '',
      date: dateRangeEl ? dateRangeEl.textContent.trim() : '',
      location: location,
      url: titleEl ? 'https://www.traversecity.com' + titleEl.getAttribute('href') : '',
      image: imgEl ? imgEl.getAttribute('src') : '',
      eventId: sharedItem ? sharedItem.getAttribute('data-eventid') : ''
    });
  }
  return { totalCount: events.length, events: results };
})();
```

## Session Source

Discovered 2026-05-03 via traverse-city-events-extraction task. Tested against traversecity.com/events/ with 15 visible events on default date range.
