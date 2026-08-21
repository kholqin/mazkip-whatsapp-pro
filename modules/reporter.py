#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAZKIP WHATSAPP PRO — Report Generator
Generate laporan attack dalam format HTML profesional
(c) 2026 M4zk1Play Nusantara
"""

import os, sys, json, time, base64
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

OUTPUT_DIR = Path.home() / "mazkip-whatsapp-pro" / "output"

class ReportGenerator:
    """Generate laporan attack"""

    def generate_html(self, target, actions, status="completed"):
        """Generate laporan HTML keren"""
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        filename = f"report_{target}_{int(time.time())}.html"
        filepath = OUTPUT_DIR / filename

        # Action icons
        action_icons = {
            "crash": "💀",
            "ban": "🛡️",
            "spam": "💣",
            "osint": "📡",
            "media": "📎",
            "trigger": "⚠️",
            "report": "📋",
        }

        actions_html = ""
        for a in actions:
            icon = action_icons.get(a, "🔹")
            actions_html += f"""
            <div class="action-item">
                <span class="action-icon">{icon}</span>
                <span class="action-name">{a.upper()}</span>
                <span class="action-status success">✓</span>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MWP Attack Report — {target}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #fff; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{ text-align: center; padding: 30px; border: 1px solid #ff0000; margin-bottom: 20px; }}
        .header h1 {{ color: #ff0000; font-size: 24px; }}
        .header .sub {{ color: #888; font-size: 14px; }}
        .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px; }}
        .info-item {{ background: #111; padding: 15px; border: 1px solid #333; }}
        .info-item .label {{ color: #888; font-size: 12px; }}
        .info-item .value {{ color: #0f0; font-size: 16px; font-weight: bold; }}
        .actions {{ background: #111; padding: 20px; border: 1px solid #333; margin-bottom: 20px; }}
        .actions h2 {{ color: #ff0000; margin-bottom: 15px; }}
        .action-item {{ display: flex; align-items: center; padding: 10px; border-bottom: 1px solid #222; }}
        .action-icon {{ font-size: 20px; margin-right: 15px; }}
        .action-name {{ flex: 1; color: #fff; }}
        .action-status {{ color: #0f0; font-weight: bold; }}
        .footer {{ text-align: center; color: #444; font-size: 12px; margin-top: 30px; }}
        .danger {{ color: #ff0000; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💀 MAZKIP WHATSAPP PRO</h1>
            <div class="sub">Attack Report — Generated {now}</div>
        </div>

        <div class="info-grid">
            <div class="info-item">
                <div class="label">TARGET</div>
                <div class="value">{target}</div>
            </div>
            <div class="info-item">
                <div class="label">STATUS</div>
                <div class="value">{status.upper()}</div>
            </div>
            <div class="info-item">
                <div class="label">DATE</div>
                <div class="value">{now}</div>
            </div>
            <div class="info-item">
                <div class="label">ACTIONS</div>
                <div class="value">{len(actions)}</div>
            </div>
        </div>

        <div class="actions">
            <h2>🔥 EXECUTED ACTIONS</h2>
            {actions_html}
        </div>

        <div class="footer">
            MAZKIP WHATSAPP PRO v2.0 — M4zk1Play Nusantara<br>
            ANONIMUS CYBER NUSANTARA
            <p class="danger">⚠️ For authorized testing only</p>
        </div>
    </div>
</body>
</html>
"""

        with open(filepath, 'w') as f:
            f.write(html)

        print(f"{G}[✓] Report: {filepath}")
        return filepath

    def generate_summary(self, targets):
        """Generate summary semua attack"""
        pass
