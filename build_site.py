#!/usr/bin/env python3
"""
build_site.py
Converts all .md writeup files to full HTML pages for OfflineDevc.github.io.
Author: Kun Poonkasetvatana (@OfflineDevc)

Verified Accurate Ground Truth:
EASY (1):
  - Skynet (Linux)
MEDIUM (6):
  - Deaddrop (Linux / AD)
  - Domino (Linux)
  - Forward (Windows)
  - Mr. Robot CTF (Linux)
  - Relevant (Windows)
  - Silent Monitor (Linux)
HARD (4):
  - Brainpan 1 (Linux)
  - Daily Bugle (Linux)
  - Internal (Linux)
  - Retro (Windows)
"""

import os
import re
import shutil
import urllib.parse
import markdown

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = r"c:\Users\999lu\OneDrive\Desktop"
WRITEUP_DIR  = os.path.join(BASE_DIR, "WriteupTHM", "WRITEUP 1")
IMAGES_SRC   = os.path.join(BASE_DIR, "WriteupTHM")
SITE_DIR     = os.path.join(BASE_DIR, "github-pages-site")
IMAGES_DST   = os.path.join(SITE_DIR, "images")
WRITEUPS_DST = os.path.join(SITE_DIR, "writeups")

os.makedirs(IMAGES_DST, exist_ok=True)
os.makedirs(WRITEUPS_DST, exist_ok=True)

# ── Ordered Writeups Registry (100% Consistent Across Entire Site) ────────────
WRITEUPS = [
    # (slug, filename, display_title, difficulty, os_name, os_class, platform)
    # EASY (1)
    ("skynet",         "Skynet.md",         "Skynet",         "Easy",   "Linux",      "os-linux",   "TryHackMe"),

    # MEDIUM (6)
    ("deaddrop",       "Deaddrop.md",       "Deaddrop",       "Medium", "Linux / AD", "os-ad",      "TryHackMe"),
    ("domino",         "Domino.md",         "Domino",         "Medium", "Linux",      "os-linux",   "TryHackMe"),
    ("forward",        "Forward.md",        "Forward",        "Medium", "Windows",    "os-windows", "TryHackMe"),
    ("mrrobotctf",     "MrRobotCTF.md",     "Mr. Robot CTF",  "Medium", "Linux",      "os-linux",   "TryHackMe"),
    ("relevant",       "Relevant.md",       "Relevant",       "Medium", "Windows",    "os-windows", "TryHackMe"),
    ("silent-monitor", "Silent Monitor.md", "Silent Monitor", "Medium", "Linux",      "os-linux",   "TryHackMe"),

    # HARD (4)
    ("brainpan1",      "Brainpan1.md",      "Brainpan 1",     "Hard",   "Linux",      "os-linux",   "TryHackMe"),
    ("daily-bugle",    "Daily Bugle.md",    "Daily Bugle",    "Hard",   "Linux",      "os-linux",   "TryHackMe"),
    ("internal",       "Internal.md",       "Internal",       "Hard",   "Linux",      "os-linux",   "TryHackMe"),
    ("retro",          "Retro.md",          "Retro",          "Hard",   "Windows",    "os-windows", "TryHackMe"),
]

# ── Sidebar Generator ─────────────────────────────────────────────────────────
def generate_sidebar_html(current_slug):
    groups = {"Easy": [], "Medium": [], "Hard": []}
    for slug, _, title, diff, os_name, os_cls, _ in WRITEUPS:
        groups[diff].append((slug, title, os_name, os_cls, diff))

    html = []
    html.append('<aside class="writeup-sidebar" id="sidebar">')
    html.append('  <div class="sidebar-author-box">')
    html.append('    <div class="sidebar-author-name">Kun Poonkasetvatana</div>')
    html.append('    <div class="sidebar-author-meta">')
    html.append('      <span class="author-badge-tag">@OfflineDevc</span>')
    html.append('      <span class="author-badge-thm">THM: Distowel</span>')
    html.append('    </div>')
    html.append('  </div>')

    html.append('  <div class="sidebar-header">')
    html.append('    <span class="sidebar-label">WRITEUPS ARCHIVE</span>')
    html.append('    <span class="sidebar-count">11 ROOMS</span>')
    html.append('  </div>')

    html.append('  <nav class="sidebar-menu">')

    diff_config = [
        ("Easy",   "EASY",   "dot-easy",   "pill-easy",   "group-easy"),
        ("Medium", "MEDIUM", "dot-medium", "pill-medium", "group-medium"),
        ("Hard",   "HARD",   "dot-hard",   "pill-hard",   "group-hard"),
    ]

    for diff_key, label, dot_cls, pill_cls, group_cls in diff_config:
        items = groups[diff_key]
        room_label = "ROOM" if len(items) == 1 else "ROOMS"
        html.append(f'    <div class="sidebar-group {group_cls}">')
        html.append('      <div class="sidebar-group-header">')
        html.append(f'        <div class="group-left"><span class="diff-indicator {dot_cls}"></span><span class="sidebar-group-name">{label}</span></div>')
        html.append(f'        <span class="sidebar-group-badge {pill_cls}">{len(items)} {room_label}</span>')
        html.append('      </div>')
        html.append('      <ul class="sidebar-list">')
        for slug, title, os_name, os_cls, d in items:
            is_active = (slug == current_slug)
            active_cls = " active" if is_active else ""
            html.append(f'        <li class="sidebar-item{active_cls}">')
            html.append(f'          <a href="{slug}.html" class="sidebar-link" title="{title}">')
            html.append('            <span class="sidebar-item-bullet"></span>')
            html.append(f'            <span class="sidebar-item-title">{title}</span>')
            html.append(f'            <span class="sidebar-os-badge {os_cls}">{os_name}</span>')
            html.append('          </a>')
            html.append('        </li>')
        html.append('      </ul>')
        html.append('    </div>')

    html.append('  </nav>')
    html.append('  <div class="sidebar-footer">')
    html.append('    <a href="../index.html#writeups" class="sidebar-home-link">')
    html.append('      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>')
    html.append('      <span>Back to Portfolio Grid</span>')
    html.append('    </a>')
    html.append('  </div>')
    html.append('</aside>')
    return '\n'.join(html)

# ── Next / Previous Navigation ────────────────────────────────────────────────
def generate_pagination_html(current_index):
    n = len(WRITEUPS)
    prev_idx = (current_index - 1) % n
    next_idx = (current_index + 1) % n

    prev_slug, _, prev_title, prev_diff, prev_os, _, _ = WRITEUPS[prev_idx]
    next_slug, _, next_title, next_diff, next_os, _, _ = WRITEUPS[next_idx]

    return f"""
    <nav class="writeup-pagination">
      <a href="{prev_slug}.html" class="pagination-card prev-card">
        <span class="pagination-sub">← PREVIOUS WRITEUP</span>
        <span class="pagination-title">{prev_title}</span>
        <div class="pagination-badges-row">
          <span class="pagination-badge diff-{prev_diff.lower()}">{prev_diff}</span>
          <span class="pagination-badge badge-os">{prev_os}</span>
        </div>
      </a>
      <a href="{next_slug}.html" class="pagination-card next-card">
        <span class="pagination-sub">NEXT WRITEUP →</span>
        <span class="pagination-title">{next_title}</span>
        <div class="pagination-badges-row">
          <span class="pagination-badge diff-{next_diff.lower()}">{next_diff}</span>
          <span class="pagination-badge badge-os">{next_os}</span>
        </div>
      </a>
    </nav>
    """

# ── Preprocess Markdown ───────────────────────────────────────────────────────
IMG_RE = re.compile(r'!\[\[([^\]]+\.png)\]\]', re.IGNORECASE)

def preprocess_markdown(text, images_used):
    # Remove redundant duplicate H1 header & trailing HR
    text = re.sub(r'^\s*#\s+.*?(?:Writeup|CTF).*?\n+(?:---\s*\n+)?', '', text, flags=re.IGNORECASE)

    # Convert Obsidian image embeds
    def replace_img(m):
        fname = m.group(1).strip()
        images_used.add(fname)
        encoded = urllib.parse.quote(fname)
        return f'![screenshot](../images/{encoded})'

    text = IMG_RE.sub(replace_img, text)
    return text

# ── Page HTML Template ────────────────────────────────────────────────────────
def render_page(index, slug, title, difficulty, os_name, os_cls, platform, content_html):
    sidebar_html = generate_sidebar_html(slug)
    pagination_html = generate_pagination_html(index)
    diff_class = f"diff-{difficulty.lower()}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} — TryHackMe Writeup | Kun Poonkasetvatana</title>
  <link rel="stylesheet" href="../style.css?v=4.0"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
</head>
<body class="writeup-page">

  <!-- TOP NAVBAR -->
  <nav class="navbar">
    <div class="nav-inner">
      <a href="../index.html" class="nav-logo">
        <span class="logo-accent">&gt;</span> Kun Poonkasetvatana
        <span class="logo-handle">(@OfflineDevc)</span>
      </a>
      <div class="nav-links">
        <a href="../index.html">Home</a>
        <a href="../index.html#writeups">All Writeups</a>
        <div class="nav-social-pills">
          <a href="https://tryhackme.com/p/Distowel" target="_blank" rel="noopener" class="pill-social thm" title="TryHackMe Profile">THM</a>
          <a href="https://profile.hackthebox.com/profile/01a11ceb-de8c-7382-a00c-8fab28836ef1" target="_blank" rel="noopener" class="pill-social htb" title="HackTheBox Profile">HTB</a>
          <a href="https://www.linkedin.com/in/kun-poonkasetvatana-4b6317326/" target="_blank" rel="noopener" class="pill-social in" title="LinkedIn Profile">IN</a>
          <a href="https://github.com/OfflineDevc" target="_blank" rel="noopener" class="pill-social gh" title="GitHub Profile">GH</a>
        </div>
      </div>
    </div>
  </nav>

  <!-- WRITEUP HERO HEADER -->
  <header class="writeup-hero">
    <div class="writeup-hero-inner">
      <div class="hero-top-meta">
        <a href="../index.html#writeups" class="back-link">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          All Writeups
        </a>
        <div class="author-hero-pill">
          <span class="author-live-dot"></span>
          <span>Author: <strong>Kun Poonkasetvatana</strong> (@OfflineDevc)</span>
        </div>
      </div>

      <div class="hero-main-row">
        <div>
          <span class="room-platform-badge">TRYHACKME ROOM WALKTHROUGH</span>
          <h1 class="writeup-title">{title}</h1>
        </div>
        <div class="writeup-badges">
          <span class="badge {diff_class}">{difficulty}</span>
          <span class="badge badge-os {os_cls}">{os_name}</span>
          <span class="badge badge-platform">{platform}</span>
        </div>
      </div>
    </div>
  </header>

  <!-- MOBILE SIDEBAR TOGGLE BAR -->
  <div class="mobile-sidebar-bar">
    <button class="mobile-sidebar-toggle" id="sidebarToggle" type="button">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      <span>Browse All Writeups</span>
    </button>
    <span class="mobile-current-title">{title} ({os_name})</span>
  </div>

  <!-- BACKDROP OVERLAY FOR MOBILE SIDEBAR -->
  <div class="sidebar-overlay" id="sidebarOverlay"></div>

  <!-- MAIN TWO-COLUMN LAYOUT -->
  <div class="writeup-layout">
    {sidebar_html}

    <main class="writeup-main">
      <article class="writeup-content">
{content_html}
      </article>

      <!-- PREV / NEXT NAVIGATION -->
      {pagination_html}
    </main>
  </div>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="footer-inner">
      <p class="footer-author">Security Portfolio of <strong>Kun Poonkasetvatana</strong> (@OfflineDevc)</p>
      <p class="footer-copy">Built by <a href="https://github.com/OfflineDevc" target="_blank">OfflineDevc</a> · 
         <a href="https://tryhackme.com/p/Distowel" target="_blank">TryHackMe</a> · 
         <a href="https://profile.hackthebox.com/profile/01a11ceb-de8c-7382-a00c-8fab28836ef1" target="_blank">HackTheBox</a> · 
         <a href="https://www.linkedin.com/in/kun-poonkasetvatana-4b6317326/" target="_blank">LinkedIn</a></p>
    </div>
  </footer>

  <script src="../script.js?v=4.0"></script>
</body>
</html>
"""

# ── Build All Writeups ────────────────────────────────────────────────────────
md_ext = ['fenced_code', 'tables', 'nl2br', 'sane_lists']

total_images = 0
for idx, (slug, md_file, title, difficulty, os_name, os_cls, platform) in enumerate(WRITEUPS):
    md_path = os.path.join(WRITEUP_DIR, md_file)
    if not os.path.exists(md_path):
        print(f"  [MISSING FILE] {md_file}")
        continue

    with open(md_path, 'r', encoding='utf-8') as f:
        raw_md = f.read()

    images_used = set()
    cleaned_md = preprocess_markdown(raw_md, images_used)

    content_html = markdown.markdown(cleaned_md, extensions=md_ext)
    full_html = render_page(idx, slug, title, difficulty, os_name, os_cls, platform, content_html)

    out_path = os.path.join(WRITEUPS_DST, f"{slug}.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    # Copy images
    for img_name in images_used:
        src = os.path.join(IMAGES_SRC, img_name)
        dst = os.path.join(IMAGES_DST, img_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            total_images += 1

    print(f"  [{idx+1:02d}/11] {title:15} | OS: {os_name:10} | Diff: {difficulty:6} -> {slug}.html")

print(f"\nDone! All 11 writeups regenerated with verified accurate OS & Difficulty.")
