#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time
from colorama import Fore, Style, init
init(autoreset=True)

R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE
H=Style.BRIGHT; N=Style.NORMAL

BANNER = f"""
{R}{H}
╔══════════════════════════════════════════════════════════╗
║    __  __    _    ____   _  _______ ____   ____   ___   ║
║   |  \\/  |  / \\  |  _ \\ | |/ / ____|  _ \\ / ___| / _ \\  ║
║   | |\\/| | / _ \\ | |_) | ' /|  _| | |_) | |    | | | | ║
║   | |  | |/ ___ \\|  _ < | . \\| |___|  _ <| |___ | |_| | ║
║   |_|  |_/_/   \\_\\_| \\_\\|_|\\_\\_____|_| \\_\\\\____| \\___/  ║
║                                                          ║
║  {W}{H}██╗  ██╗██╗   ██╗███████╗ █████╗ ██████╗  █████╗ {R}██╗  ██╗{W}
║  {W}{H}██║  ██║╚██╗ ██╔╝██╔════╝██╔══██╗██╔══██╗██╔══██╗{R}██║ ██╔╝{W}
║  {W}{H}███████║ ╚████╔╝ █████╗  ███████║██████╔╝███████║{R}█████╔╝ {W}
║  {W}{H}██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██║██╔══██╗██╔══██║{R}██╔═██╗ {W}
║  {W}{H}██║  ██║   ██║   ███████╗██║  ██║██║  ██║██║  ██║{R}██║  ██╗{W}
║  {W}{H}╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{R}╚═╝  ╚═╝{W}
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  {Y}{H}MAZKIP WHATSAPP PRO v2.0 — Fullstack Assault Suite{Y}   ║
║  {R}{H}CODED BY : M4zk1Play Nusantara{Y}                      ║
║  {R}{H}TEAM     : ANONIMUS CYBER NUSANTARA{Y}                 ║
╚══════════════════════════════════════════════════════════╝
{R}{H}
"""

DISCLAIMER = f"""
{R}{H}╔{'═'*54}╗
║{Y}{H}⚠️  DISCLAIMER HUKUM — BACA DULU ! ⚠️{R}           ║
║{W}Tools ini untuk EDUKASI & PENTEST yg DIIZINKAN.        ║
║{W}Segala penyalahgunaan TANGGUNG JAWAB PRIBADI USER.     ║
║{R}{H}[!] M4zk1Play TIDAK BERTANGGUNG JAWAB !             ║
║{Y}{H}[+] Dengan menggunakan, Anda setuju:                ║
║{W}  1. Hanya untuk test keamanan punya sendiri            ║
║{W}  2. Tidak merugikan orang lain                         ║
║{W}  3. Siap konsekuensi hukum                              ║
║{C}{H}[*] Authorized Pentester Only — GASKEN !{R}         ║
╚{'═'*54}╝
{N}
"""

def clear_screen(): os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    clear_screen(); print(BANNER)

def print_disclaimer():
    print(DISCLAIMER)
    choice = input(f"\n{Y}{H}[?] Ketik {G}'gasken'{Y} untuk lanjut: {W}").strip().lower()
    if choice != 'gasken':
        print(f"{R}[!] Keluar..."); sys.exit(0)
    clear_screen()

def loading_anim(text="Loading...", delay=0.1):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    for _ in range(3):
        for f2 in frames:
            sys.stdout.write(f"\r{R}{H}[ {f2} ] {Y}{text}{N}"); sys.stdout.flush(); time.sleep(delay)
    print()

def print_menu():
    print(f"""
{R}{H}╔{'═'*50}╗
║{Y}{H}  [01] 💀  CRASH ENGINE     — 7x Crash Vector        {R}║
║{Y}{H}  [02] 🛡️   BAN ENGINE       — Auto Report + Ban     {R}║
║{Y}{H}  [03] 📡  OSINT GATHERING   — Profil + Pattern      {R}║
║{Y}{H}  [04] 💣  SPAM TSUNAMI      — 10K Msg Auto Send     {R}║
║{Y}{H}  [05] 📎  MEDIA BOMBER      — File Corrupt + Virus   {R}║
║{Y}{H}  [06] 🎯  MULTI TARGET      — Batch Attack.txt      {R}║
║{Y}{H}  [07] 🔄  SESSION TOOL      — Save/Load Session     {R}║
║{Y}{H}  [08] 🚀  AUTO PWN          — Full Auto Attack      {R}║
║{Y}{H}  [09] ℹ️   ABOUT            — Info Tools            {R}║
║{Y}{H}  [00] 🚪  EXIT              — Keluar                {R}║
╚{'═'*50}╝""")
