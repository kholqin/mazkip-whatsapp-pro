#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAZKIP WHATSAPP PRO — Proxy Rotator
Auto rotate IP untuk bypass rate-limit mass report
(c) 2026 M4zk1Play Nusantara
"""

import os, sys, json, time, random, threading
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

PROXY_FILE = Path.home() / "mazkip-whatsapp-pro" / "proxies.txt"

class ProxyRotator:
    """Rotasi proxy otomatis untuk menghindari rate-limiting"""

    def __init__(self):
        self.proxies = []
        self.current = 0
        self._load_proxies()

    def _load_proxies(self):
        """Load proxy dari file"""
        proxies = []

        # Proxy publik default (rotate sendiri nantinya)
        default_proxies = [
            "socks5://127.0.0.1:9050",  # Tor
            "http://128.199.0.1:8080",
            "http://167.99.0.1:3128",
            "http://68.183.0.1:80",
            "http://165.22.0.1:8080",
        ]

        if PROXY_FILE.exists():
            with open(PROXY_FILE) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        proxies.append(line)

        self.proxies = proxies if proxies else default_proxies
        print(f"{C}[*] Loaded {len(self.proxies)} proxies")

    def get_proxy(self):
        """Dapatkan proxy berikutnya (round-robin)"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current % len(self.proxies)]
        self.current += 1
        return proxy

    def get_random_proxy(self):
        """Dapatkan proxy acak"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def add_proxy(self, proxy):
        """Tambah proxy baru"""
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            self._save()

    def remove_proxy(self, proxy):
        """Hapus proxy"""
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            self._save()

    def _save(self):
        """Simpan daftar proxy ke file"""
        with open(PROXY_FILE, 'w') as f:
            for p in self.proxies:
                f.write(p + '\n')

    def test_proxy(self, proxy):
        """Test apakah proxy hidup"""
        import requests
        try:
            resp = requests.get('https://api.ipify.org', proxies={'http': proxy, 'https': proxy}, timeout=5)
            if resp.status_code == 200:
                print(f"{G}[✓] Proxy {proxy} — IP: {resp.text}")
                return True
        except:
            print(f"{R}[✗] Proxy {proxy} — MATI")
        return False

    def test_all(self):
        """Test semua proxy"""
        print(f"\n{Y}[*] Testing {len(self.proxies)} proxies...")
        alive = []
        for p in self.proxies:
            if self.test_proxy(p):
                alive.append(p)
            time.sleep(1)
        print(f"{G}[✓] {len(alive)}/{len(self.proxies)} proxy hidup")
        return alive
