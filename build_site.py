#!/usr/bin/env python3
"""
build_site.py
Converts all .md writeup files to full HTML pages for the GitHub Pages site.
- Converts Obsidian ![[image]] syntax to <img> tags
- Copies referenced images to github-pages-site/images/
- Wraps content in site template
"""

import os
import re
import shutil
import markdown

# ── Paths ────────────────────────────────────────────────────────────────────
WRITEUP_DIR  = r"c:\Users\999lu\OneDrive\Desktop\WriteupTHM\WRITEUP 1"
IMAGES_SRC   = r"c:\Users\999lu\OneDrive\Desktop\WriteupTHM"
SITE_DIR     = r"c:\Users\999lu\OneDrive\Desktop\github-pages-site"
IMAGES_DST   = os.path.join(SITE_DIR, "images")
WRITEUPS_DST = os.path.join(SITE_DIR, "writeups")

os.makedirs(IMAGES_DST,   exist_ok=True)
os.makedirs(WRITEUPS_DST, exist_ok=True)

# ── Slug map (md filename → html slug) ───────────────────────────────────────
SLUG_MAP = {
    "Brainpan1.md":      "brainpan1",
    "Daily Bugle.md":    "daily-bugle",
    "Deaddrop.md":       "deaddrop",
    "Domino.md":         "domino",
    "Forward.md":        "forward",
    "Internal.md":       "internal",
    "MrRobotCTF.md":     "mrrobotctf",
    "Relevant.md":       "relevant",
    "Retro.md":          "retro",
    "Silent Monitor.md": "silent-monitor",
    "Skynet.md":         "skynet",
}

TITLE_MAP = {
    "brainpan1":      "Brainpan 1",
    "daily-bugle":    "Daily Bugle",
    "deaddrop":       "Deaddrop",
    "domino":         "Domino",
    "forward":        "Forward",
    "internal":       "Internal",
    "mrrobotctf":     "Mr. Robot CTF",
    "relevant":       "Relevant",
    "retro":          "Retro",
    "silent-monitor": "Silent Monitor",
    "skynet":         "Skynet",
}

DIFFICULTY_MAP = {
    "brainpan1":      ("Hard", "Linux"),
    "daily-bugle":    ("Hard", "Linux"),
    "deaddrop":       ("Medium", "Linux"),
    "domino":         ("Medium", "Windows"),
    "forward":        ("Medium", "Linux"),
    "internal":       ("Hard", "Linux"),
    "mrrobotctf":     ("Medium", "Linux"),
    "relevant":       ("Medium", "Windows"),
    "retro":          ("Hard", "Windows"),
    "silent-monitor": ("Hard", "Linux"),
    "skynet":         ("Easy", "Linux"),
}

# ── HTML template ─────────────────────────────────────────────────────────────
def html_template(slug, content_html, images_used):
    title      = TITLE_MAP.get(slug, slug)
    difficulty, os_name = DIFFICULTY_MAP.get(slug, ("Medium", "Linux"))

    diff_class = {"Easy": "diff-easy", "Medium": "diff-medium",
                  "Hard": "diff-hard", "Insane": "diff-insane"}.get(difficulty, "diff-medium")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} — Writeup | OfflineDevc</title>
  <link rel="stylesheet" href="../style.css"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet"/>
</head>
<body>
  <!-- NAV -->
  <nav class="navbar">
    <a href="../index.html" class="nav-logo">&lt;OfflineDevc/&gt;</a>
    <div class="nav-links">
      <a href="../index.html">Home</a>
      <a href="../index.html#writeups">Writeups</a>
    </div>
  </nav>

  <!-- WRITEUP HEADER -->
  <section class="writeup-hero">
    <div class="container">
      <div class="writeup-meta-top">
        <a href="../index.html#writeups" class="back-link">← All Writeups</a>
        <span class="platform-badge thm">TryHackMe</span>
      </div>
      <h1 class="writeup-title">{title}</h1>
      <div class="writeup-badges">
        <span class="badge {diff_class}">{difficulty}</span>
        <span class="badge badge-os">{os_name}</span>
      </div>
    </div>
  </section>

  <!-- WRITEUP CONTENT -->
  <main class="writeup-body">
    <div class="container writeup-content">
{content_html}
    </div>
  </main>

  <!-- FOOTER -->
  <footer class="footer">
    <p>Built by <a href="https://github.com/OfflineDevc" target="_blank">OfflineDevc</a> · 
       <a href="https://tryhackme.com/p/Distowel" target="_blank">TryHackMe</a> · 
       <a href="https://www.linkedin.com/in/kun-poonkasetvatana-4b6317326/" target="_blank">LinkedIn</a></p>
  </footer>
  <script src="../script.js"></script>
</body>
</html>
"""

# ── Preprocess markdown text ──────────────────────────────────────────────────
IMG_RE  = re.compile(r'!\[\[([^\]]+\.png)\]\]', re.IGNORECASE)

def preprocess(text, images_used):
    """Replace Obsidian ![[X.png]] with standard markdown ![](../images/X.png)"""
    def replace_img(m):
        fname = m.group(1)
        images_used.add(fname)
        # URL-encode spaces for safety
        encoded = fname.replace(' ', '%20')
        return f'![screenshot](../images/{encoded})'
    return IMG_RE.sub(replace_img, text)

# ── Build each writeup ────────────────────────────────────────────────────────
md_ext = ['fenced_code', 'tables', 'nl2br', 'sane_lists', 'toc']

copied = 0
errors = []

for md_file, slug in SLUG_MAP.items():
    md_path = os.path.join(WRITEUP_DIR, md_file)
    if not os.path.exists(md_path):
        print(f"  [SKIP] {md_file} not found")
        continue

    with open(md_path, 'r', encoding='utf-8') as f:
        raw = f.read()

    images_used = set()
    processed   = preprocess(raw, images_used)

    # Convert markdown → HTML
    content_html = markdown.markdown(processed, extensions=md_ext)

    # Wrap in full page template
    page_html = html_template(slug, content_html, images_used)

    out_path = os.path.join(WRITEUPS_DST, f"{slug}.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page_html)
    print(f"  [OK]   {slug}.html  ({len(images_used)} images)")

    # Copy referenced images
    for img_name in images_used:
        src = os.path.join(IMAGES_SRC, img_name)
        dst = os.path.join(IMAGES_DST, img_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied += 1
        else:
            errors.append(f"Missing image: {img_name}")

print(f"\nDone. {copied} images copied.")
if errors:
    print(f"{len(errors)} missing images:")
    for e in errors:
        print(f"  {e}")
