#!/usr/bin/env python3
"""Generate index.html from hn/ and events/ folders."""

import os, re, datetime, shutil

repo_wdir = "../../../"
hn_dir = os.path.join(repo_wdir, "hn")
events_dir = os.path.join(repo_wdir, "events")
dist_dir = os.path.join(repo_wdir, "dist")
dist_hn_dir = os.path.join(dist_dir, "hn")
dist_events_dir = os.path.join(dist_dir, "events")
out_index_path = os.path.join(dist_dir, "index.html")
os.makedirs(dist_hn_dir, exist_ok=True)
os.makedirs(dist_events_dir, exist_ok=True)

# --- HN files ---
hn_files = sorted(
    [f for f in os.listdir(hn_dir) if f.endswith(".html")],
    reverse=True
)

hn_items = []
for f in hn_files:
    m = re.search(r"(\d{4}-\d{2}-\d{2})\.html", f)
    if m:
        date_str = m.group(1)
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        display = date_obj.strftime("%B %d, %Y")
        num = date_obj.day
        hn_items.append((display, num, date_str, f))

hn_links_html = ""
for display, num, date_str, filename in hn_items:
    hn_links_html += (
        f'            <li>\n'
        f'                <a href="hn/{filename}">\n'
        f'                    <span class="rank">#{num}</span>\n'
        f'                    <div class="info">\n'
        f'                        <h2>{display}</h2>\n'
        f'                        <p>hn_top10_{date_str}.html</p>\n'
        f'                    </div>\n'
        f'                    <span class="arrow">\u2192</span>\n'
        f'                </a>\n'
        f'            </li>\n'
    )

# --- Events files ---
events_files = sorted(
    [f for f in os.listdir(events_dir) if f.endswith(".html")],
    reverse=True
)

events_links_html = ""
for ef in events_files:
    m = re.search(r"(\d{4}-\d{2}-\d{2})\.html", ef)
    if m:
        date_str = m.group(1)
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        display = date_obj.strftime("%B %d, %Y")
        events_links_html += (
            f'            <li>\n'
            f'                <a href="events/{ef}">\n'
            f'                    <span class="rank">\U0001f5fa</span>\n'
            f'                    <div class="info">\n'
            f'                        <h2>Events Map — {display}</h2>\n'
            f'                        <p>Mid Michigan &amp; Lake Michigan events</p>\n'
            f'                    </div>\n'
            f'                    <span class="arrow">\u2192</span>\n'
            f'                </a>\n'
            f'            </li>\n'
        )

css = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container { max-width: 700px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 30px; }
        header h1 {
            font-size: 2.5rem; font-weight: 800;
            background: linear-gradient(135deg, #ff6b35, #f7c948);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; margin-bottom: 10px;
        }
        header p { color: #888; font-size: 1rem; }
        .section-title {
            font-size: 1.1rem; font-weight: 700; color: #f7c948;
            padding: 16px 0 10px; border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 12px;
        }
        .list { list-style: none; }
        .list li {
            margin-bottom: 12px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .list li:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            border-color: rgba(255,255,255,0.2);
        }
        .list a {
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 18px 24px;
            text-decoration: none;
            color: #fff;
        }
        .rank {
            font-size: 1.4rem; font-weight: 900;
            color: #f7c948; min-width: 36px;
        }
        .info { flex: 1; }
        .info h2 { font-size: 1.05rem; font-weight: 600; margin-bottom: 4px; }
        .info p { font-size: 0.85rem; color: #888; }
        .arrow { color: #555; font-size: 1.2rem; }
"""

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Digest</title>
    <style>{css.strip()}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>\U0001f525 Daily Digest</h1>
            <p>Hacker News reports &amp; Michigan events</p>
        </header>
'''

if events_links_html:
    html += f'''        <div class="section-title">\U0001f5fa Michigan Events</div>
        <ul class="list">
{events_links_html}        </ul>
'''

html += f'''        <div class="section-title">\U0001f4c4 HN Top 10</div>
        <ul class="list">
{hn_links_html}        </ul>
    </div>
</body>
</html>'''

with open(out_index_path, "w") as f:
    f.write(html)

# Copy hn HTML files into dist/hn
for f in hn_files:
    src = os.path.join(hn_dir, f)
    dst = os.path.join(dist_hn_dir, f)
    shutil.copy2(src, dst)

# Copy events files into dist/events
for f in events_files:
    src = os.path.join(events_dir, f)
    dst = os.path.join(dist_events_dir, f)
    shutil.copy2(src, dst)

print(f"Generated {out_index_path} with {len(hn_files)} HN entries and {len(events_files)} events entries")
