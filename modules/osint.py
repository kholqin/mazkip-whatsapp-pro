#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, time, re, requests
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

class OSINTEngine:
    def __init__(self):
        self.s = requests.Session(); self.r = {}

    def check_phone(self, phone):
        prov = self._provider(phone)
        v = "Valid ✓" if re.match(r'^62[0-9]{8,12}$', phone) else "Invalid ✗"
        n = "Indonesia" if phone.startswith("62") else "Unknown"
        print(f"\n{R}{H}╔{'═'*50}╗\n║{Y}{H}      📡 OSINT INFO{' ' * 36}{R}║\n╠{'═'*50}╣\n║  {W}Number : {phone:<40}{R}║\n║  {W}Country: {n:<40}{R}║\n║  {W}Provider:{prov:<40}{R}║\n║  {W}Valid  : {v:<40}{R}║\n╚{'═'*50}╝")
        self.r = {"phone":phone,"country":n,"provider":prov,"valid":v}

    def _provider(self, p):
        prov = {"11":"Telkomsel","12":"Telkomsel","13":"Telkomsel","21":"Telkomsel","22":"Telkomsel","23":"Telkomsel","52":"Hutchinson","53":"Hutchinson","55":"Hutchinson","56":"Hutchinson","57":"Hutchinson","58":"Hutchinson","59":"Hutchinson","81":"Indosat","82":"Indosat","83":"Indosat","84":"Indosat","85":"Indosat","86":"Indosat","87":"Indosat","88":"Indosat","89":"Indosat","96":"Three","97":"Three","98":"Three","99":"Three","31":"XL Axiata","32":"XL Axiata","33":"XL Axiata","77":"XL Axiata","78":"XL Axiata","79":"XL Axiata","91":"Smartfren","92":"Smartfren","93":"Smartfren","94":"Smartfren"}
        return prov.get(p[2:4] if len(p)>=4 else "","Unknown")

    def save(self, phone):
        out = Path.home()/"mazkip-whatsapp-pro"/"output"; out.mkdir(parents=True,exist_ok=True)
        fp = out/f"osint_{phone}.json"
        with open(fp,'w') as f: json.dump(self.r, f, indent=4)
        print(f"{G}[✓] Saved: {fp}")
