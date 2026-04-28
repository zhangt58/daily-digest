#!/usr/bin/env python3
"""Generate index.html from hn/ folder HTML reports."""

import os, re, datetime

hn_dir = "hn"
files = sorted(
    [f for f in os.listdir(hn_dir) if f.endswith(".html")],
    reverse=True
)

items = []
for f in files:
    m = re.search(r"(\d{4}-\d{2}-\d{2})\.html", f)
    if m:
        date_str = m.group(1)
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        display = date_obj.strftime("%B %d, %Y")
        num = date_obj.day
        items.append((display, num, date_str, f))

links_html = ""
for display, num, date_str, filename in items:
    links_html += (
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
        header { text-align: center; margin-bottom: 40px; }
        header h1 {
            font-size: 2.5rem; font-weight: 800;
            background: linear-gradient(135deg, #ff6b35, #f7c948);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text; margin-bottom: 10px;
        }
        header p { color: #888; font-size: 1rem; }
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
    <title>HN Top 10 Archive</title>
    <style>{css.strip()}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>\U0001f525 HN Top 10 Archive</h1>
            <p>Curated Hacker News daily reports</p>
        </header>
        <ul class="list">
{links_html}        </ul>
    </div>
</body>
</html>'''

with open("index.html", "w") as f:
    f.write(html)

print(f"Generated index.html with {len(files)} entries")
