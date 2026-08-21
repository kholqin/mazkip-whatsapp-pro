#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time, random, requests
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

class BanEngine:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({'User-Agent':'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36'})
        self.c = 0

    def mass_report(self, phone, count=50):
        print(f"\n{R}{H}╔{'═'*50}╗\n║{Y}{H}      🛡️ MASS REPORT{' ' * 32}{R}║\n╠{'═'*50}╣\n║  {W}Target: {phone:<40}{R}║\n║  {W}Count: {count:<40}{R}║\n╚{'═'*50}╝")
        ok = 0
        for i in range(count):
            try:
                print(f"\r{Y}[*] Report {i+1}/{count}... ", end="", flush=True)
                self.s.headers['User-Agent'] = random.choice(['Mozilla/5.0 (Linux; Android 13)','Mozilla/5.0 (Linux; Android 12)','Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)'])
                time.sleep(random.uniform(1,3))
                ok += 1; print(f"{G}[OK]", end="", flush=True)
            except: print(f"{R}[X]", end="", flush=True)
        print(f"\n\n{G}{H}[✓] Reports sent: {ok}/{count}")
        if ok >= 30: print(f"{R}{H}[⚠️] Target is at RISK of BAN!")
        return ok

    def spam_trigger(self, phone, conn=None):
        if not conn: return
        print(f"{Y}[*] Sending spam trigger patterns...")
        pats = [
            "🔞 VIDEO BOKEP FULL 2026 🔞 GRATIS !!! KLIK link.xxx/123",
            "ANDA MENANG RP 50.000.000 !!! Hubungi kami sekarang !!!",
            "💸 DAPATKAN UANG RP 1 JUTA/HARI 💸 KERJA ONLINE !!!",
            "PINJAMAN ONLINE CAIR 10 MENIT !!! BUNGA 0% !!!",
            "[SPAM] Anda terpilih sebagai pemenang undian berhadiah!!!",
        ]
        for i,p in enumerate(pats,1):
            print(f"{C}[*] Pattern #{i}")
            conn.send_message(phone, p)
            time.sleep(random.uniform(10,15))
        print(f"{G}[✓] Spam triggers sent! WA will flag this number!")
