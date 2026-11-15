#!/usr/bin/env python3
"""
build_site.py
Converts all .md writeup files to full HTML pages for OfflineDevc.github.io.
Author: Kun Poonkasetvatana (@OfflineDevc)
Design: Senior UI/UX & Technical Blog Standard (Dual Theme: Light & Dark Mode)
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

# ── Ordered Writeups Registry ────────────────────────────────────────────────
WRITEUPS = [
    # (slug, filename, display_title, difficulty, os_name, os_class, platform, date, tags)
    # EASY (1)
    ("skynet",         "Skynet.md",         "Skynet",         "Easy",   "Linux",      "os-linux",   "TryHackMe", "13 Nov 2026", "SMB, Web, Hydra, RFI, Cron, Tar Wildcard"),

    # MEDIUM (6)
    ("deaddrop",       "Deaddrop.md",       "Deaddrop",       "Medium", "Linux / AD", "os-ad",      "TryHackMe", "11 Nov 2026", "Active Directory, Kerberoasting, BloodHound"),
    ("domino",         "Domino.md",         "Domino",         "Medium", "Linux",      "os-linux",   "TryHackMe", "10 Nov 2026", "Web Enumeration, Privilege Escalation"),
    ("forward",        "Forward.md",        "Forward",        "Medium", "Windows",    "os-windows", "TryHackMe", "09 Nov 2026", "Port Forwarding, Chisel, Internal Pivot"),
    ("mrrobotctf",     "MrRobotCTF.md",     "Mr. Robot CTF",  "Medium", "Linux",      "os-linux",   "TryHackMe", "08 Nov 2026", "WordPress, Wpscan, Hydra, SUID nmap"),
    ("relevant",       "Relevant.md",       "Relevant",       "Medium", "Windows",    "os-windows", "TryHackMe", "07 Nov 2026", "SMB Share, WebDAV, PrintSpoofer, JuicyPotato"),
    ("silent-monitor", "Silent Monitor.md", "Silent Monitor", "Medium", "Linux",      "os-linux",   "TryHackMe", "06 Nov 2026", "Monitoring, SNMP, Log Poisoning"),

    # HARD (4)
    ("brainpan1",      "Brainpan1.md",      "Brainpan 1",     "Hard",   "Linux",      "os-linux",   "TryHackMe", "05 Nov 2026", "Buffer Overflow x86, Immunity Debugger, SUID"),
    ("daily-bugle",    "Daily Bugle.md",    "Daily Bugle",    "Hard",   "Linux",      "os-linux",   "TryHackMe", "04 Nov 2026", "Joomla SQLi, John the Ripper, Yum Sudo"),
    ("internal",       "Internal.md",       "Internal",       "Hard",   "Linux",      "os-linux",   "TryHackMe", "03 Nov 2026", "Jenkins, SSH Tunneling, Docker Breakout"),
    ("retro",          "Retro.md",          "Retro",          "Hard",   "Windows",    "os-windows", "TryHackMe", "02 Nov 2026", "CVE-2019-1388, UAC Bypass, WordPress"),
]

# ── TryHackMe Authentic Room Descriptions ─────────────────────────────────────
ROOM_DESCRIPTIONS = {
    "skynet": "A vulnerable machine inspired by the Terminator franchise. Features anonymous SMB shares, SquirrelMail credential harvesting, Cuppa CMS Remote File Inclusion (RFI), and root cron job wildcard injection.",
    "deaddrop": "An enterprise Active Directory simulation focusing on anonymous LDAP recon, Kerberoasting service tickets, BloodHound privilege path mapping, and domain trust escalation to achieve Enterprise Admin.",
    "domino": "A multi-stage Linux security audit focusing on multi-tiered web services, credential harvesting, lateral movement via internal SSH keys, and sudo privilege escalation.",
    "forward": "A realistic network pivoting challenge navigating dual-homed subnets with Chisel reverse SOCKS proxies, internal service pivoting, and Windows unquoted service paths.",
    "mrrobotctf": "Based on the Mr. Robot series. Features robots.txt clues, dictionary optimization, WordPress user brute-forcing, and SUID nmap interactive shell breakout to root.",
    "relevant": "A penetration testing assessment involving high-port WebDAV anonymous file uploads, ASPX reverse webshells, and SeImpersonatePrivilege abuse via PrintSpoofer to NT AUTHORITY\\SYSTEM.",
    "silent-monitor": "A Linux auditing challenge exploring SNMP public community strings, process tree snooping, monitoring agent log poisoning, and kernel-level root escalation.",
    "brainpan1": "Classic binary exploitation room designed to teach x86 buffer overflows, Immunity Debugger memory inspection, finding EIP offsets, bad character elimination, and SUID root exploitation.",
    "daily-bugle": "Joomla CMS exploitation room featuring CVE-2017-8917 SQL injection, bcrypt password hash cracking with John The Ripper, administrative PHP template uploads, and Yum sudo GTFOBins.",
    "internal": "An enterprise penetration test scenario covering WordPress admin brute-forcing, SSH local port forwarding, internal Jenkins Groovy console RCE, and Docker container breakout.",
    "retro": "A Windows security challenge involving web author comment credential leakage, RDP access, and Windows Certificate Dialog UAC bypass (CVE-2019-1388) to obtain NT AUTHORITY\\SYSTEM.",
}

# ── Sidebar Generator (Left Drawer / Desktop Sidebar) ─────────────────────────
def generate_sidebar_html(current_slug):
    groups = {"Easy": [], "Medium": [], "Hard": []}
    for item in WRITEUPS:
        slug, _, title, diff, os_name, os_cls, _, _, _ = item
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
    html.append('    <span>WRITEUPS ARCHIVE</span>')
    html.append('    <span>11 ROOMS</span>')
    html.append('  </div>')
    html.append('  <nav class="sidebar-menu">')

    diff_config = [
        ("Easy",   "EASY",   "dot-easy",   "diff-easy"),
        ("Medium", "MEDIUM", "dot-medium", "diff-medium"),
        ("Hard",   "HARD",   "dot-hard",   "diff-hard"),
    ]

    for diff_key, label, dot_cls, badge_cls in diff_config:
        items = groups[diff_key]
        room_label = "ROOM" if len(items) == 1 else "ROOMS"
        html.append('    <div class="sidebar-group">')
        html.append('      <div class="sidebar-group-header">')
        html.append(f'        <div class="group-left"><span class="diff-indicator {dot_cls}"></span><span>{label}</span></div>')
        html.append(f'        <span class="badge {badge_cls}">{len(items)} {room_label}</span>')
        html.append('      </div>')
        html.append('      <ul class="sidebar-list">')
        for slug, title, os_name, os_cls, _ in items:
            is_active = (slug == current_slug)
            active_cls = " active" if is_active else ""
            html.append(f'        <li class="sidebar-item{active_cls}">')
            html.append(f'          <a href="{slug}.html" class="sidebar-link" title="{title}">')
            html.append('            <span class="sidebar-item-bullet"></span>')
            html.append(f'            <span class="sidebar-item-title">{title}</span>')
            html.append(f'            <span class="sidebar-os-badge">{os_name}</span>')
            html.append('          </a>')
            html.append('        </li>')
        html.append('      </ul>')
        html.append('    </div>')

    html.append('  </nav>')
    html.append('  <div style="margin-top: 24px; padding-top: 14px; border-top: 1px solid var(--border-light);">')
    html.append('    <a href="../index.html#writeups" class="back-link">')
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

    prev_slug, _, prev_title, prev_diff, prev_os, _, _, _, _ = WRITEUPS[prev_idx]
    next_slug, _, next_title, next_diff, next_os, _, _, _, _ = WRITEUPS[next_idx]

    return f"""
    <nav class="writeup-pagination">
      <a href="{prev_slug}.html" class="pagination-card">
        <span class="pagination-sub">← PREVIOUS WRITEUP</span>
        <span class="pagination-title">{prev_title}</span>
        <div class="pagination-badges-row">
          <span class="pagination-badge">{prev_diff}</span>
          <span class="pagination-badge">{prev_os}</span>
        </div>
      </a>
      <a href="{next_slug}.html" class="pagination-card" style="text-align: right;">
        <span class="pagination-sub">NEXT WRITEUP →</span>
        <span class="pagination-title">{next_title}</span>
        <div class="pagination-badges-row" style="justify-content: flex-end;">
          <span class="pagination-badge">{next_diff}</span>
          <span class="pagination-badge">{next_os}</span>
        </div>
      </a>
    </nav>
    """

# ── Preprocess Markdown ───────────────────────────────────────────────────────
IMG_RE = re.compile(r'!\[\[([^\]]+\.png)\]\]', re.IGNORECASE)

def preprocess_markdown(text, images_used):
    text = re.sub(r'^\s*#\s+.*?(?:Writeup|CTF).*?\n+(?:---\s*\n+)?', '', text, flags=re.IGNORECASE)

    def replace_img(m):
        fname = m.group(1).strip()
        images_used.add(fname)
        encoded = urllib.parse.quote(fname)
        return f'![screenshot](../images/{encoded})'

    text = IMG_RE.sub(replace_img, text)
    return text

# ── Headings & Table of Contents Generator ────────────────────────────────────
def process_headings_and_generate_toc(html_content):
    headings = []
    used_ids = set()

    def make_id(title_text):
        cleaned = re.sub(r'<[^>]+>', '', title_text).strip()
        slug = re.sub(r'[^a-zA-Z0-9\s_-]', '', cleaned).strip().lower()
        slug = re.sub(r'[\s_]+', '-', slug)
        if not slug:
            slug = "section"
        orig_slug = slug
        counter = 1
        while slug in used_ids:
            slug = f"{orig_slug}-{counter}"
            counter += 1
        used_ids.add(slug)
        return slug

    def replace_h2_h3(match):
        tag = match.group(1).lower()
        attrs = match.group(2)
        inner = match.group(3)

        id_match = re.search(r'id=["\']([^"\']+)["\']', attrs)
        if id_match:
            heading_id = id_match.group(1)
        else:
            heading_id = make_id(inner)

        clean_title = re.sub(r'<[^>]+>', '', inner).strip()
        headings.append((tag, heading_id, clean_title))

        return f'<{tag} id="{heading_id}"{attrs}>{inner}</{tag}>'

    pattern = re.compile(r'<(h[23])(\s*[^>]*)>(.*?)</\1>', re.IGNORECASE | re.DOTALL)
    modified_html = pattern.sub(replace_h2_h3, html_content)

    toc_html_list = []
    toc_html_list.append('<aside class="toc-sidebar">')
    toc_html_list.append('  <div class="toc-title">ON THIS PAGE</div>')
    toc_html_list.append('  <ul class="toc-menu">')

    for tag, heading_id, title in headings:
        indent = ' style="padding-left: 12px; font-size: 12.5px;"' if tag == 'h3' else ''
        toc_html_list.append(f'    <li{indent}><a href="#{heading_id}" class="toc-link">{title}</a></li>')

    if not headings:
        toc_html_list.append('    <li><a href="#overview" class="toc-link">Top of Article</a></li>')

    toc_html_list.append('  </ul>')
    toc_html_list.append('</aside>')

    return modified_html, '\n'.join(toc_html_list)

# ── Page HTML Template ────────────────────────────────────────────────────────
def render_page(index, slug, title, difficulty, os_name, os_cls, platform, date, tags, content_html):
    sidebar_html = generate_sidebar_html(slug)
    pagination_html = generate_pagination_html(index)
    modified_content, toc_html = process_headings_and_generate_toc(content_html)
    room_desc = ROOM_DESCRIPTIONS.get(slug, "A comprehensive TryHackMe security assessment and technical walkthrough.")

    diff_class = f"diff-{difficulty.lower()}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} — TryHackMe Writeup | Kun Poonkasetvatana</title>
  <!-- Immediate Theme Application (Prevents FOUT) -->
  <script>
    (function() {{
      try {{
        var theme = localStorage.getItem('theme');
        if (theme) {{
          document.documentElement.setAttribute('data-theme', theme);
        }} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
          document.documentElement.setAttribute('data-theme', 'dark');
        }}
      }} catch (e) {{}}
    }})();
  </script>
  <link rel="stylesheet" href="../style.css?v=5.3"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700;800&family=Sarabun:wght@300;400;500;600&display=swap" rel="stylesheet"/>
</head>
<body class="writeup-page">

  <!-- TOP NAVBAR -->
  <nav class="navbar">
    <div class="nav-inner">
      <a href="../index.html" class="nav-logo">
        <span class="logo-badge">&gt;</span> Kun Poonkasetvatana
        <span class="logo-handle">(@OfflineDevc)</span>
      </a>
      <div class="nav-links">
        <a href="../index.html" class="nav-link-item">Home</a>
        <a href="../index.html#writeups" class="nav-link-item active">Writeups</a>
        <a href="../index.html#about" class="nav-link-item">About</a>

        <!-- Theme Toggle Button -->
        <button class="theme-toggle-btn" id="themeToggle" type="button" aria-label="Toggle Dark/Light Mode" title="Toggle Dark/Light Mode">
          <svg class="sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
          <svg class="moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
        </button>

        <div class="nav-social-pills">
          <a href="https://tryhackme.com/p/Distowel" target="_blank" rel="noopener" class="pill-social" title="TryHackMe Profile">THM</a>
          <a href="https://profile.hackthebox.com/profile/01a11ceb-de8c-7382-a00c-8fab28836ef1" target="_blank" rel="noopener" class="pill-social" title="HackTheBox Profile">HTB</a>
          <a href="https://www.linkedin.com/in/kun-poonkasetvatana-4b6317326/" target="_blank" rel="noopener" class="pill-social" title="LinkedIn Profile">IN</a>
          <a href="https://github.com/OfflineDevc" target="_blank" rel="noopener" class="pill-social" title="GitHub Profile">GH</a>
        </div>
      </div>
    </div>
  </nav>

  <!-- WRITEUP HERO HEADER -->
  <header class="writeup-hero">
    <div class="writeup-hero-inner">
      <div class="hero-top-meta">
        <a href="../index.html#writeups" class="back-link">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          All Writeups Archive
        </a>
        <div class="author-hero-pill">
          <span class="author-live-dot"></span>
          <span>Author: <strong>Kun Poonkasetvatana</strong> (@OfflineDevc) · Published: {date}</span>
        </div>
      </div>

      <div class="hero-main-row">
        <div class="hero-title-group">
          <span class="room-platform-badge">{platform.upper()} ROOM WALKTHROUGH</span>
          <h1 class="writeup-title">{title}</h1>
          <p class="writeup-room-desc">{room_desc}</p>
        </div>

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
    <span style="font-size: 13px; font-weight: 500; color: var(--text-secondary);">{title} ({os_name})</span>
  </div>

  <!-- BACKDROP OVERLAY FOR MOBILE SIDEBAR -->
  <div class="sidebar-overlay" id="sidebarOverlay"></div>

  <!-- MAIN THREE-COLUMN LAYOUT -->
  <div class="writeup-layout">
    {sidebar_html}

    <main class="writeup-main">
      <article class="writeup-content">
{modified_content}
      </article>

      <!-- PREV / NEXT NAVIGATION -->
      {pagination_html}
    </main>

    {toc_html}
  </div>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="footer-inner">
      <p style="font-weight: 600; color: var(--text-main); margin-bottom: 6px;">Security Research &amp; Writeups Archive</p>
      <p class="footer-copy">Built with classic minimalist design by <a href="https://github.com/OfflineDevc" target="_blank">OfflineDevc</a> · 
         <a href="https://tryhackme.com/p/Distowel" target="_blank">TryHackMe</a> · 
         <a href="https://profile.hackthebox.com/profile/01a11ceb-de8c-7382-a00c-8fab28836ef1" target="_blank">HackTheBox</a> · 
         <a href="https://www.linkedin.com/in/kun-poonkasetvatana-4b6317326/" target="_blank">LinkedIn</a></p>
    </div>
  </footer>

  <script src="../script.js?v=5.3"></script>
</body>
</html>
"""

# ── Build All Writeups ────────────────────────────────────────────────────────
md_ext = ['fenced_code', 'tables', 'nl2br', 'sane_lists']

total_images = 0
for idx, (slug, md_file, title, difficulty, os_name, os_cls, platform, date, tags) in enumerate(WRITEUPS):
    md_path = os.path.join(WRITEUP_DIR, md_file)
    if not os.path.exists(md_path):
        print(f"  [MISSING FILE] {md_file}")
        continue

    with open(md_path, 'r', encoding='utf-8') as f:
        raw_md = f.read()

    images_used = set()
    cleaned_md = preprocess_markdown(raw_md, images_used)

    content_html = markdown.markdown(cleaned_md, extensions=md_ext)
    full_html = render_page(idx, slug, title, difficulty, os_name, os_cls, platform, date, tags, content_html)

    out_path = os.path.join(WRITEUPS_DST, f"{slug}.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    for img_name in images_used:
        src = os.path.join(IMAGES_SRC, img_name)
        dst = os.path.join(IMAGES_DST, img_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            total_images += 1

    print(f"  [{idx+1:02d}/11] {title:15} | OS: {os_name:10} | Diff: {difficulty:6} -> {slug}.html")

print(f"\nDone! All 11 writeups regenerated with enhanced room title and authentic TryHackMe descriptions.")
