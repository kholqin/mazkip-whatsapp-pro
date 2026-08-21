#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAZKIP WHATSAPP PRO — C2 Persistence Module
Pantau status target + notifikasi
(c) 2026 M4zk1Play Nusantara
"""

import os, sys, time, json, threading, requests
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

MONITOR_FILE = Path.home() / "mazkip-whatsapp-pro" / "monitors.json"

class C2Client:
    """Pantau target secara real-time"""

    def __init__(self):
        self.monitors = []
        self.running = False
        self._load()

    def _load(self):
        if MONITOR_FILE.exists():
            try:
                with open(MONITOR_FILE) as f:
                    self.monitors = json.load(f)
            except:
                self.monitors = []

    def _save(self):
        with open(MONITOR_FILE, 'w') as f:
            json.dump(self.monitors, f, indent=4)

    def add_monitor(self, target, name=""):
        """Tambah target untuk dipantau"""
        mon = {
            "target": target,
            "name": name or target,
            "status": "unknown",
            "last_seen": None,
            "first_seen": time.strftime('%Y-%m-%d %H:%M:%S'),
            "alerts": 0,
        }
        self.monitors.append(mon)
        self._save()
        print(f"{G}[✓] Monitoring {target} dimulai!")
        return mon

    def check_status(self, target):
        """Cek status WhatsApp target"""
        try:
            url = f"https://wa.me/{target}"
            headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13) WhatsApp/2.24'}
            resp = requests.get(url, headers=headers, timeout=10)

            # Simulasi deteksi online/offline
            # WA: Typical response mengandung "WhatsApp" jika nomor terdaftar
            if resp.status_code == 200:
                if "WhatsApp" in resp.text:
                    return "registered"
                else:
                    return "unregistered"
            return "unknown"
        except:
            return "unknown"

    def start_monitoring(self, callback=None, interval=60):
        """Mulai monitoring di background"""
        self.running = True

        def _loop():
            while self.running:
                for mon in self.monitors:
                    if not self.running:
                        break
                    status = self.check_status(mon['target'])
                    prev = mon.get('status', 'unknown')
                    mon['status'] = status

                    if status == 'registered':
                        mon['last_seen'] = time.strftime('%Y-%m-%d %H:%M:%S')

                    # Alert kalo ada perubahan
                    if prev != status and prev != 'unknown':
                        if status == 'registered':
                            print(f"{G}[📶] {mon['name']} ONLINE!")
                            mon['alerts'] += 1
                        elif status == 'unregistered':
                            print(f"{R}[💀] {mon['name']} OFFLINE/UNREGISTERED!")
                            mon['alerts'] += 1

                        if callback:
                            callback(mon)

                    time.sleep(2)  # Delay antar cek

                self._save()
                time.sleep(max(interval, 30))  # Min 30 detik

        thread = threading.Thread(target=_loop, daemon=True)
        thread.start()
        print(f"{G}[✓] C2 monitoring started! Cek tiap {interval}s")
        return thread

    def stop(self):
        self.running = False
        print(f"{Y}[*] C2 dihentikan.")

    def list_monitors(self):
        if not self.monitors:
            print(f"{Y}[!] Tidak ada monitor.")
            return
        print(f"\n{R}{H}╔{'═'*55}╗")
        print(f"║{Y}{H}              🎯 C2 MONITOR LIST{' ' * 24}{R}║")
        print(f"╠{'═'*55}╣")
        for i, m in enumerate(self.monitors, 1):
            s = m.get('status', 'unknown')
            if s == 'registered': icon = f"{G}● ONLINE "
            elif s == 'unregistered': icon = f"{R}● OFFLINE"
            else: icon = f"{Y}● UNKNOWN"
            print(f"║  {icon}{W} {m['target']:<16} {m.get('name',''):<15} alerts:{m.get('alerts',0)}{R}║")
        print(f"╚{'═'*55}╝")
