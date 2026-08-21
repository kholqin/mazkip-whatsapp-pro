#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, re, time, json, random, subprocess, webbrowser
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

SESSIONS_DIR = Path.home() / "mazkip-whatsapp-pro" / "sessions"

class WhatsAppConnector:
    def __init__(self):
        self.mode = "clipboard"; self._detect_mode()

    def _detect_mode(self):
        try: import pywhatkit; self.pywhatkit_avail = True
        except: self.pywhatkit_avail = False
        try: from selenium import webdriver; self.selenium_avail = True
        except: self.selenium_avail = False
        try: subprocess.run(['which', 'termux-clipboard-set'], capture_output=True, timeout=2); self.tapi = True
        except: self.tapi = False
        if self.selenium_avail:
            try: subprocess.run(['which','chromedriver'], capture_output=True, check=True); self.mode="selenium"
            except: self.mode="pywhatkit" if self.pywhatkit_avail else "clipboard"
        elif self.pywhatkit_avail: self.mode="pywhatkit"

    def validate_phone(self, p):
        p = re.sub(r'[^\d+]','',p)
        if p.startswith('0'): p='62'+p[1:]
        elif p.startswith('+'): p=p[1:]
        elif not p.startswith('62'): p='62'+p
        return p if 10<=len(p)<=15 else None

    def send_message(self, phone, msg):
        phone = self.validate_phone(phone)
        if not phone: print(f"{R}[!] Invalid number!"); return False
        if self.mode=="selenium": return self._send_selenium(phone,msg)
        elif self.mode=="pywhatkit": return self._send_pywhatkit(phone,msg)
        else: return self._send_clipboard(phone,msg)

    def _send_clipboard(self, phone, msg):
        print(f"{Y}[*] Clipboard mode — buka wa.me/{phone}")
        webbrowser.open(f"https://wa.me/{phone}"); time.sleep(5)
        if self.tapi:
            try:
                for i in range(0,len(msg),10000):
                    subprocess.Popen(['termux-clipboard-set'],stdin=subprocess.PIPE).communicate(input=msg[i:i+10000].encode(),timeout=5)
            except: pass
        print(f"{G}[✓] Clipboard ready! Paste & send manually")
        return True

    def _send_pywhatkit(self, phone, msg):
        try:
            import pywhatkit; now=time.localtime(); h=now.tm_hour; m=now.tm_min+2
            if m>=60: m-=60; h+=1
            if h>=24: h-=24
            pywhatkit.sendwhatmsg(phone, msg[:50000], h, m, 15); time.sleep(5)
            print(f"{G}[✓] Sent!"); return True
        except Exception as e: print(f"{R}[!] {e}"); return self._send_clipboard(phone,msg)

    def _send_selenium(self, phone, msg):
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            opt=Options(); opt.add_argument("--no-sandbox"); opt.add_argument("--disable-dev-shm-usage")
            opt.add_argument("--user-data-dir="+str(SESSIONS_DIR/"chrome_data")); opt.add_argument("--disable-notifications")
            d=webdriver.Chrome(options=opt); d.get(f"https://web.whatsapp.com/send?phone={phone}"); time.sleep(3)
            box=WebDriverWait(d,30).until(EC.presence_of_element_located((By.XPATH,'//div[@contenteditable="true"]')))
            for i in range(0,len(msg),5000): box.send_keys(msg[i:i+5000]); time.sleep(0.5)
            box.send_keys(Keys.ENTER); time.sleep(2); d.quit()
            print(f"{G}[✓] Sent via Selenium!"); return True
        except Exception as e: print(f"{R}[!] {e}"); return self._send_clipboard(phone,msg)

    def send_multiple(self, phone, msg, count=100):
        print(f"\n{R}{H}[!] Sending {count} messages...")
        ok=0; deadline=time.time()+120
        for i in range(count):
            if time.time()>deadline: break
            if self.send_message(phone, f"[{i+1}/{count}] {msg[:200]}"): ok+=1
            time.sleep(random.uniform(0.5,1.5))
        print(f"{G}{H}[✓] Sent: {ok}/{count}"); return ok
