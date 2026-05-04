#!/usr/bin/env python3
"""
Build the pocket digest index page.
Scans hn/ and events/ directories, generates index.html with:
  - Daily section: HN Top 10 posts (newest first)
  - Weekly section: Michigan Events maps (newest first)
Copies output to dist/index.html as well.
"""

import os
import glob
import shutil
import re
from datetime import datetime

BASE_DIR = "/home/tong/workspace/pocket"
HN_DIR = os.path.join(BASE_DIR, "hn")
EVENTS_DIR = os.path.join(BASE_DIR, "events")
DIST_DIR = os.path.join(BASE_DIR, "dist")
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
DIST_INDEX_PATH = os.path.join(DIST_DIR, "index.html")

# Also sync hn/ -> dist/hn/ and events/ -> dist/events/
DIST_HN_DIR = os.path.join(DIST_DIR, "hn")
DIST_EVENTS_DIR = os.path.join(DIST_DIR, "events")


def parse_date_from_filename(filename):
    """Extract YYYY-MM-DD from filename like 2026-05-03.html"""
    match = re.match(r"(\d{4}-\d{2}-\d{2})\.html$", filename)
    if match:
        return match.group(1), filename
    return None, filename


def parse_events_date(filename):
    """Extract date from hn_events_map_2026-05-03.html"""
    match = re.match(r"hn_events_map_(\d{4}-\d{2}-\d{2})\.html$", filename)
    if match:
        return match.group(1), filename
    return None, filename


def format_date(date_str):
    """Format YYYY-MM-DD to human readable"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%B %d, %Y")
    except ValueError:
        return date_str


def scan_hn_posts():
    """Scan hn/ directory for YYYY-MM-DD.html files, return sorted by date desc"""
    pattern = os.path.join(HN_DIR, "*.html")
    files = glob.glob(pattern)
    posts = []
    for f in files:
        date_str, filename = parse_date_from_filename(os.path.basename(f))
        if date_str:
            posts.append((date_str, filename))
    posts.sort(reverse=True)
    return posts


def scan_events():
    """Scan events/ directory for hn_events_map_YYYY-MM-DD.html files, return sorted by date desc"""
    pattern = os.path.join(EVENTS_DIR, "*.html")
    files = glob.glob(pattern)
    events = []
    for f in files:
        date_str, filename = parse_events_date(os.path.basename(f))
        if date_str:
            events.append((date_str, filename))
    events.sort(reverse=True)
    return events


def generate_index(hn_posts, events):
    """Generate the index.html with Daily and Weekly sections"""
    now = datetime.now().strftime("%B %d, %Y at %H:%M")

    hn_items = []
    for i, (date_str, filename) in enumerate(hn_posts):
        hn_items.append(f"""            <li>
                <a href="hn/{filename}">
                    <span class="rank">{i + 1}</span>
                    <div class="info">
                        <h2>HN Top 10 — {format_date(date_str)}</h2>
                        <p>Top 10 Hacker News posts for {format_date(date_str)}</p>
                    </div>
                    <span class="arrow">→</span>
                </a>
            </li>""")

    event_items = []
    for i, (date_str, filename) in enumerate(events):
        event_items.append(f"""            <li>
                <a href="events/{filename}">
                    <span class="rank">🗺</span>
                    <div class="info">
                        <h2>Michigan Events Map — {format_date(date_str)}</h2>
                        <p>Mid Michigan &amp; Lake Michigan weekend events ({format_date(date_str)})</p>
                    </div>
                    <span class="arrow">→</span>
                </a>
            </li>""")

    hn_list = "\n".join(hn_items) if hn_items else '            <li><div class="empty">No HN posts yet</div></li>'
    events_list = "\n".join(event_items) if event_items else '            <li><div class="empty">No events yet</div></li>'

    hn_count = len(hn_posts)
    events_count = len(events)

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Digest</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            min-height: 100vh;
            padding: 40px 20px;
        }}
        .container {{ max-width: 700px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 30px; }}
        header h1 {{
            font-size: 2.5rem; font-weight: 800;
            background: linear-gradient(135deg, #ff6b35, #f7c948);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; margin-bottom: 10px;
        }}
        header p {{ color: #888; font-size: 1rem; }}
        .section {{ margin-bottom: 40px; }}
        .section-title {{
            font-size: 1.1rem; font-weight: 700; color: #f7c948;
            padding: 16px 0 10px; border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 12px;
        }}
        .section-subtitle {{
            font-size: 0.85rem; color: #666; margin-top: -8px; margin-bottom: 16px;
        }}
        .list {{ list-style: none; }}
        .list li {{
            margin-bottom: 12px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .list li:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
            border-color: rgba(255,255,255,0.2);
        }}
        .list a {{
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 18px 24px;
            text-decoration: none;
            color: #fff;
        }}
        .rank {{
            font-size: 1.4rem; font-weight: 900;
            color: #f7c948; min-width: 36px; text-align: center;
        }}
        .info {{ flex: 1; }}
        .info h2 {{ font-size: 1.05rem; font-weight: 600; margin-bottom: 4px; }}
        .info p {{ font-size: 0.85rem; color: #888; }}
        .arrow {{ color: #555; font-size: 1.2rem; }}
        .empty {{ padding: 18px 24px; color: #555; }}
        footer {{
            text-align: center; padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: #555; font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔥 Daily Digest</h1>
            <p>Hacker News daily + Michigan events weekly</p>
        </header>

        <div class="section">
            <div class="section-title">📰 Daily — HN Top 10 ({hn_count} days)</div>
            <p class="section-subtitle">Updated every day at 8:00 AM</p>
            <ul class="list">
{hn_list}
            </ul>
        </div>

        <div class="section">
            <div class="section-title">🗺 Weekly — Michigan Events ({events_count} weeks)</div>
            <p class="section-subtitle">Updated every Friday at 10:00 AM</p>
            <ul class="list">
{events_list}
            </ul>
        </div>

        <footer>
            <p>Generated {now}</p>
        </footer>
    </div>
</body>
</html>"""
    return index_html


def sync_dist():
    """Sync hn/ and events/ to dist/"""
    os.makedirs(DIST_HN_DIR, exist_ok=True)
    os.makedirs(DIST_EVENTS_DIR, exist_ok=True)

    for f in os.listdir(HN_DIR):
        src = os.path.join(HN_DIR, f)
        dst = os.path.join(DIST_HN_DIR, f)
        if os.path.isfile(src):
            shutil.copy2(src, dst)

    for f in os.listdir(EVENTS_DIR):
        src = os.path.join(EVENTS_DIR, f)
        dst = os.path.join(DIST_EVENTS_DIR, f)
        if os.path.isfile(src):
            shutil.copy2(src, dst)


def main():
    hn_posts = scan_hn_posts()
    events = scan_events()

    print(f"Found {len(hn_posts)} HN posts, {len(events)} event maps")

    index_html = generate_index(hn_posts, events)

    with open(INDEX_PATH, "w") as f:
        f.write(index_html)
    print(f"Written: {INDEX_PATH}")

    sync_dist()

    shutil.copy2(INDEX_PATH, DIST_INDEX_PATH)
    print(f"Written: {DIST_INDEX_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
