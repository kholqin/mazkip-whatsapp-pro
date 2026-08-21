#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAZKIP WHATSAPP PRO — Webhook Module
Kirim notifikasi ke Discord/Telegram
(c) 2026 M4zk1Play Nusantara
"""

import os, sys, json, time, requests
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

WEBHOOK_FILE = Path.home() / "mazkip-whatsapp-pro" / "webhook_config.json"

class Webhook:
    """Kirim notifikasi hasil attack ke Discord/Telegram"""

    def __init__(self):
        self.config = self._load()

    def _load(self):
        default = {"discord": "", "telegram": {"bot_token": "", "chat_id": ""}}
        wf = Path.home() / "mazkip-whatsapp-pro" / "webhook_config.json"
        if wf.exists():
            try:
                return json.load(open(wf))
            except:
                return default
        json.dump(default, open(wf, 'w'), indent=4)
        return default

    def set_discord(self, url):
        """Set Discord webhook URL"""
        self.config['discord'] = url
        self._save()
        print(f"{G}[✓] Discord webhook set!")

    def set_telegram(self, bot_token, chat_id):
        """Set Telegram bot"""
        self.config['telegram']['bot_token'] = bot_token
        self.config['telegram']['chat_id'] = chat_id
        self._save()
        print(f"{G}[✓] Telegram bot set!")

    def _save(self):
        wf = Path.home() / "mazkip-whatsapp-pro" / "webhook_config.json"
        with open(wf, 'w') as f:
            json.dump(self.config, f, indent=4)

    def send_discord(self, message, title="MWP Alert"):
        """Kirim ke Discord"""
        url = self.config.get('discord', '')
        if not url:
            return False

        payload = {
            "embeds": [{
                "title": title,
                "description": message,
                "color": 13631488,  # Red
                "footer": {"text": "MAZKIP WHATSAPP PRO • M4zk1Play Nusantara"},
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
            }]
        }
        try:
            requests.post(url, json=payload, timeout=5)
            print(f"{G}[✓] Discord notification sent!")
            return True
        except:
            print(f"{R}[!] Gagal kirim ke Discord")
            return False

    def send_telegram(self, message):
        """Kirim ke Telegram"""
        bot_token = self.config.get('telegram', {}).get('bot_token', '')
        chat_id = self.config.get('telegram', {}).get('chat_id', '')
        if not bot_token or not chat_id:
            return False

        text = f"💀 *MWP ATTACK*\n{message}\n\n_— M4zk1Play Nusantara_"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=5)
            print(f"{G}[✓] Telegram notification sent!")
            return True
        except:
            print(f"{R}[!] Gagal kirim ke Telegram")
            return False

    def notify(self, message, title="MWP Alert"):
        """Kirim ke semua webhook yang terkonfigurasi"""
        self.send_discord(message, title)
        self.send_telegram(message)

    def send_attack_report(self, target, actions, status="completed"):
        """Kirim laporan attack"""
        msg = (
            f"🎯 *Target:* `{target}`\n"
            f"📋 *Actions:* {', '.join(actions)}\n"
            f"✅ *Status:* {status}\n"
            f"🕐 *Time:* {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.notify(msg, f"💀 Attack: {target}")
