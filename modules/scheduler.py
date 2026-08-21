#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAZKIP WHATSAPP PRO — Scheduler Module
Jadwalkan attack otomatis pada waktu tertentu
(c) 2026 M4zk1Play Nusantara
"""

import os, sys, time, json, threading
from pathlib import Path
from datetime import datetime, timedelta
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

SCHEDULE_FILE = Path.home() / "mazkip-whatsapp-pro" / "schedule.json"

class Scheduler:
    """Penjadwalan attack otomatis"""

    def __init__(self):
        self.jobs = []
        self.running = False
        self._load()

    def _load(self):
        """Load jadwal dari file"""
        if SCHEDULE_FILE.exists():
            try:
                with open(SCHEDULE_FILE) as f:
                    self.jobs = json.load(f)
            except:
                self.jobs = []

    def _save(self):
        """Simpan jadwal ke file"""
        with open(SCHEDULE_FILE, 'w') as f:
            json.dump(self.jobs, f, indent=4)

    def add_job(self, name, target, action="crash", hour=0, minute=0, repeat=False):
        """Tambah jadwal baru"""
        job = {
            "id": len(self.jobs) + 1,
            "name": name,
            "target": target,
            "action": action,
            "hour": hour,
            "minute": minute,
            "repeat": repeat,
            "enabled": True,
            "created": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.jobs.append(job)
        self._save()
        print(f"{G}[✓] Job '{name}' dijadwalkan setiap {hour:02d}:{minute:02d}")
        return job

    def list_jobs(self):
        """Tampilkan semua jadwal"""
        if not self.jobs:
            print(f"{Y}[!] Belum ada jadwal.")
            return

        print(f"\n{R}{H}╔{'═'*55}╗")
        print(f"║{Y}{H}                 ⏰ SCHEDULED JOBS{' ' * 18}{R}║")
        print(f"╠{'═'*55}╣")
        for j in self.jobs:
            status = f"{G}ON{R}" if j.get('enabled', True) else f"{R}OFF{R}"
            repeat = "🔄" if j.get('repeat') else "🔴"
            print(f"║  {status} [{j['id']:02d}] {j['name']:<15} {j['target']:<18} {j['action']:<8} {j['hour']:02d}:{j['minute']:02d} {repeat}  ║")
        print(f"╚{'═'*55}╝")

    def remove_job(self, job_id):
        """Hapus jadwal"""
        self.jobs = [j for j in self.jobs if j['id'] != job_id]
        self._save()
        print(f"{G}[✓] Job #{job_id} dihapus!")

    def check_jobs(self, callback=None):
        """Cek jadwal yang harus dijalankan sekarang"""
        now = datetime.now()
        for job in self.jobs:
            if not job.get('enabled', True):
                continue

            if job['hour'] == now.hour and job['minute'] == now.minute:
                print(f"\n{R}{H}[!] MENJALANKAN JOB: {job['name']}!{W}")
                print(f"{Y}[*] Target: {job['target']} | Action: {job['action']}")

                if callback:
                    callback(job)

                if not job.get('repeat', False):
                    job['enabled'] = False
                    self._save()
                else:
                    print(f"{C}[*] Job akan diulang besok...")

    def start(self, callback=None):
        """Mulai scheduler di background"""
        self.running = True
        def _loop():
            while self.running:
                self.check_jobs(callback)
                time.sleep(30)  # Cek setiap 30 detik

        thread = threading.Thread(target=_loop, daemon=True)
        thread.start()
        print(f"{G}[✓] Scheduler started di background!")
        return thread

    def stop(self):
        """Hentikan scheduler"""
        self.running = False
        print(f"{Y}[*] Scheduler stopped.")
