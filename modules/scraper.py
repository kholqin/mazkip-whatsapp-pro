#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAZKIP WHATSAPP PRO — Phone Scraper
Scrape nomor telepon dari berbagai sumber
(c) 2026 M4zk1Play Nusantara
"""

import os, sys, re, json, time, random
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

PHONE_REGEX = re.compile(r'(?:\+?62|0)[0-9]{9,13}')
OUTPUT_DIR = Path.home() / "mazkip-whatsapp-pro" / "output"

class PhoneScraper:
    """Scrape nomor telepon dari berbagai sumber"""

    def scrape_from_text(self, text):
        """Ekstrak nomor dari teks"""
        phones = PHONE_REGEX.findall(text)
        # Format ke 62xx
        formatted = []
        for p in phones:
            if p.startswith('0'):
                p = '62' + p[1:]
            elif p.startswith('+'):
                p = p[1:]
            if len(p) >= 10 and len(p) <= 15:
                formatted.append(p)
        return list(set(formatted))

    def scrape_from_file(self, filepath):
        """Scrape nomor dari file teks"""
        fp = Path(filepath)
        if not fp.exists():
            print(f"{R}[!] File tidak ditemukan: {filepath}")
            return []
        with open(fp, 'r', errors='ignore') as f:
            text = f.read()
        return self.scrape_from_text(text)

    def scrape_from_group_file(self, filepath):
        """Scrape dari file export group chat WhatsApp (.txt)"""
        phones = []
        fp = Path(filepath)
        if not fp.exists():
            return phones

        with open(fp, 'r', errors='ignore') as f:
            for line in f:
                # Format WA: "12/08/26, 10:00 - +62xxx: Pesan"
                # Cari nomor setelah strip
                match = re.search(r'-\s*(\+?62\d{9,13})', line)
                if match:
                    p = match.group(1)
                    if p.startswith('+'):
                        p = p[1:]
                    phones.append(p)
        return list(set(phones))

    def scrape_save(self, phones, filename="scraped_phones.txt"):
        """Simpan nomor yang ditemukan"""
        if not phones:
            print(f"{Y}[!] Tidak ada nomor ditemukan.")
            return

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        fp = OUTPUT_DIR / filename
        with open(fp, 'w') as f:
            for p in phones:
                f.write(p + '\n')

        print(f"{G}[✓] {len(phones)} nomor tersimpan di {fp}")
        return fp

    def show_results(self, phones):
        """Tampilkan hasil scrape"""
        if not phones:
            print(f"{Y}[!] Tidak ada nomor.")
            return

        print(f"\n{R}{H}╔{'═'*50}╗")
        print(f"║{Y}{H}        📱 PHONE NUMBERS FOUND: {len(phones)}{' ' * 18}{R}║")
        print(f"╠{'═'*50}╣")
        for i, p in enumerate(phones[:20], 1):
            print(f"║  {G}[{i:02d}]{W} {p:<44}{R}║")
        if len(phones) > 20:
            print(f"║  {Y}... dan {len(phones)-20} nomor lainnya{' ' * 18}{R}║")
        print(f"╚{'═'*50}╝")
