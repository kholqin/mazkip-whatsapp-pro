#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAZKIP WHATSAPP PRO — Logger Module
Logging system dengan rotasi file
(c) 2026 M4zk1Play Nusantara
"""

import os, sys, time, logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init
init(autoreset=True)

LOG_DIR = Path.home() / "mazkip-whatsapp-pro" / "logs"

class MWLogger:
    """Sistem logging untuk MWP"""

    def __init__(self):
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger('MWP')
        self.logger.setLevel(logging.DEBUG)

        # Format
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File handler dengan rotasi (max 5MB, 3 backup)
        fh = RotatingFileHandler(
            LOG_DIR / 'mwp.log',
            maxBytes=5*1024*1024,
            backupCount=3
        )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # Error handler
        eh = RotatingFileHandler(
            LOG_DIR / 'mwp_error.log',
            maxBytes=5*1024*1024,
            backupCount=3
        )
        eh.setLevel(logging.ERROR)
        eh.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(eh)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def attack(self, target, action, status):
        """Catat aktivitas attack"""
        msg = f"ATTACK | Target: {target} | Action: {action} | Status: {status}"
        self.logger.info(msg)

        # Simpan juga di attack log terpisah
        log_file = LOG_DIR / "attacks.log"
        with open(log_file, 'a') as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

    def get_recent(self, lines=20):
        """Ambil log terbaru"""
        log_file = LOG_DIR / "mwp.log"
        if not log_file.exists():
            return ["No logs yet."]
        with open(log_file) as f:
            all_lines = f.readlines()
        return all_lines[-lines:]

logger = MWLogger()
