#!/usr/bin/env python3
"""
build_site.py
Converts all .md writeup files to full HTML pages for OfflineDevc.github.io.
Features:
- Two-column layout with sticky writeup sidebar
- Mobile drawer navigation
- Dark theme typography and tables
- Image lightbox zoom
- Skynet marked as Easy
- Automatic image copying from WriteupTHM/ to github-pages-site/images/
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

# ── Writeups Registry (Difficulty, Platform, OS) ──────────────────────────────
# Skynet is explicitly marked as Easy!
WRITEUPS = [
    # (slug, filename, display_title, difficulty, os_name, platform)
    ("skynet",         "Skynet.md",         "Skynet",         "Easy",   "Linux",   "TryHackMe"),
    ("deaddrop",       "Deaddrop.md",       "Deaddrop",       "Medium", "Linux",   "TryHackMe"),
    ("domino",         "Domino.md",         "Domino",         "Medium", "Windows", "TryHackMe"),
    ("mrrobotctf",     "MrRobotCTF.md",     "Mr. Robot CTF",  "Medium", "Linux",   "TryHackMe"),
    ("relevant",       "Relevant.md",       "Relevant",       "Medium", "Windows", "TryHackMe"),
    ("brainpan1",      "Brainpan1.md",      "Brainpan 1",     "Hard",   "Linux",   "TryHackMe"),
    ("daily-bugle",    "Daily Bugle.md",    "Daily Bugle",    "Hard",   "Linux",   "TryHackMe"),
    ("forward",        "Forward.md",        "Forward",        "Hard",   "Linux",   "TryHackMe"),
    ("internal",       "Internal.md",       "Internal",       "Hard",   "Linux",   "TryHackMe"),
    ("retro",          "Retro.md",          "Retro",          "Hard",   "Windows", "TryHackMe"),
    ("silent-monitor", "Silent Monitor.md", "Silent Monitor", "Hard",   "Linux",   "TryHackMe"),
]

# ── Sidebar Generator ─────────────────────────────────────────────────────────
def generate_sidebar_html(current_slug):
    groups = {"Easy": [], "Medium": [], "Hard": []}
    for slug, _, title, diff, os_name, _ in WRITEUPS:
        groups[diff].append((slug, title, os_name, diff))

    html = []
    html.append('<aside class="writeup-sidebar" id="sidebar">')
    html.append('  <div class="sidebar-header">')
    html.append('    <span class="sidebar-label">WRITEUPS</span>')
    html.append('    <span class="sidebar-count">11 ROOMS</span>')
    html.append('  </div>')
    html.append('  <nav class="sidebar-menu">')

    for diff in ["Easy", "Medium", "Hard"]:
        items = groups[diff]
        pill_cls = f"pill-{diff.lower()}"
        html.append('    <div class="sidebar-group">')
        html.append('      <div class="sidebar-group-header">')
        html.append(f'        <span class="sidebar-group-name">{diff.upper()}</span>')
        html.append(f'        <span class="sidebar-group-badge {pill_cls}">{len(items)}</span>')
        html.append('      </div>')
        html.append('      <ul class="sidebar-list">')
        for slug, title, os_name, d in items:
            is_active = (slug == current_slug)
            active_cls = " active" if is_active else ""
            html.append(f'        <li class="sidebar-item{active_cls}">')
            html.append(f'          <a href="{slug}.html" class="sidebar-link" title="{title}">')
            html.append('            <span class="sidebar-item-bullet"></span>')
            html.append(f'            <span class="sidebar-item-title">{title}</span>')
            html.append(f'            <span class="sidebar-os-tag">{os_name[:3]}</span>')
            html.append('          </a>')
            html.append('        </li>')
        html.append('      </ul>')
        html.append('    </div>')

    html.append('  </nav>')
    html.append('  <div class="sidebar-footer">')
    html.append('    <a href="../index.html#writeups" class="sidebar-home-link">')
    html.append('      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>')
    html.append('      <span>All Writeups Grid</span>')
    html.append('    </a>')
    html.append('  </div>')
    html.append('</aside>')
    return '\n'.join(html)

# ── Preprocess Markdown ───────────────────────────────────────────────────────
IMG_RE = re.compile(r'!\[\[([^\]]+\.png)\]\]', re.IGNORECASE)

def preprocess_markdown(text, images_used):
    # 1. Remove duplicate leading H1 header (e.g. "# Brainpan 1 - TryHackMe Writeup") and following HR
    text = re.sub(r'^\s*#\s+.*?(?:Writeup|CTF).*?\n+(?:---\s*\n+)?', '', text, flags=re.IGNORECASE)

    # 2. Convert Obsidian ![[Pasted image ...]] -> standard markdown ![](../images/...)
    def replace_img(m):
        fname = m.group(1).strip()
        images_used.add(fname)
        encoded = urllib.parse.quote(fname)
        return f'![screenshot](../images/{encoded})'

    text = IMG_RE.sub(replace_img, text)
    return text

# ── Page HTML Template ────────────────────────────────────────────────────────
def render_page(slug, title, difficulty, os_name, platform, content_html):
    sidebar_html = generate_sidebar_html(slug)
    diff_class = f"diff-{difficulty.lower()}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} — Writeup | OfflineDevc</title>
  <link rel="stylesheet" href="../style.css"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
</head>
<body class="writeup-page">

  <!-- TOP NAVBAR -->
  <nav class="navbar">
    <div class="nav-inner">
      <a href="../index.html" class="nav-logo">&gt; OfflineDevc<span class="cursor">_</span></a>
      <div class="nav-links">
        <a href="../index.html">Home</a>
        <a href="../index.html#writeups">Writeups</a>
        <a href="https://github.com/OfflineDevc" target="_blank" rel="noopener" class="nav-github-link">GitHub</a>
      </div>
    </div>
  </nav>

  <!-- WRITEUP HERO HEADER -->
  <header class="writeup-hero">
    <div class="writeup-hero-inner">
      <div class="writeup-breadcrumb">
        <a href="../index.html#writeups" class="back-link">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          All Writeups
        </a>
        <span class="breadcrumb-slash">/</span>
        <span class="breadcrumb-current">{title}</span>
      </div>
      <div class="writeup-header-content">
        <h1 class="writeup-title">{title}</h1>
        <div class="writeup-badges">
          <span class="badge {diff_class}">{difficulty}</span>
          <span class="badge badge-os">{os_name}</span>
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
    <span class="mobile-current-title">{title}</span>
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
    </main>
  </div>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="footer-inner">
      <p class="footer-copy">Built by <a href="https://github.com/OfflineDevc" target="_blank">OfflineDevc</a> · 
         <a href="https://tryhackme.com/p/Distowel" target="_blank">TryHackMe</a> · 
         <a href="https://profile.hackthebox.com/profile/01a11ceb-de8c-7382-a00c-8fab28836ef1" target="_blank">HackTheBox</a> · 
         <a href="https://www.linkedin.com/in/kun-poonkasetvatana-4b6317326/" target="_blank">LinkedIn</a></p>
    </div>
  </footer>

  <script src="../script.js"></script>
</body>
</html>
"""

# ── Build All Writeups ────────────────────────────────────────────────────────
md_ext = ['fenced_code', 'tables', 'nl2br', 'sane_lists']

total_images = 0
for slug, md_file, title, difficulty, os_name, platform in WRITEUPS:
    md_path = os.path.join(WRITEUP_DIR, md_file)
    if not os.path.exists(md_path):
        print(f"  [MISSING FILE] {md_file}")
        continue

    with open(md_path, 'r', encoding='utf-8') as f:
        raw_md = f.read()

    images_used = set()
    cleaned_md = preprocess_markdown(raw_md, images_used)

    content_html = markdown.markdown(cleaned_md, extensions=md_ext)
    full_html = render_page(slug, title, difficulty, os_name, platform, content_html)

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

    print(f"  [BUILT] {slug}.html ({len(images_used)} images, {difficulty})")

print(f"\nDone! All writeup pages built successfully. Total images copied/verified: {total_images}")
