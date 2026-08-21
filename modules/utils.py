#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, json, time, random
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)
R=Fore.RED; G=Fore.GREEN; Y=Fore.YELLOW; C=Fore.CYAN; W=Fore.WHITE; H=Style.BRIGHT

BD = Path.home()/"mazkip-whatsapp-pro"
CF = BD/"config.json"; TF = BD/"targets.txt"; OD = BD/"output"

def init_dirs():
    for d in [BD, BD/"modules", BD/"payloads", BD/"sessions", OD]: d.mkdir(parents=True, exist_ok=True)

def load_config():
    d = {"default_mode":"clipboard","delay_between_messages":2,"max_messages_per_session":500,"use_proxy":False,"proxy_list":[],"session_persistence":True,"auto_rotate_vectors":True}
    if CF.exists():
        try: return json.load(open(CF))
        except: pass
    json.dump(d, open(CF,'w'), indent=4); return d

def load_targets():
    if TF.exists(): return [l.strip() for l in open(TF) if l.strip() and not l.startswith('#')]
    return []

def save_targets(t):
    with open(TF,'w') as f: f.write('\n'.join(t)+'\n')

def add_target(p):
    t=load_targets()
    if p not in t: t.append(p); save_targets(t); print(f"{G}[✓] Added {p}!")
    else: print(f"{Y}[!] Already exists!")

def list_targets():
    t=load_targets()
    if not t: print(f"{Y}[!] No targets."); return
    print(f"\n{R}{H}╔{'═'*40}╗\n║{Y}{H}    🎯 TARGETS ({len(t)}){' ' * 21}{R}║\n╠{'═'*40}╣")
    for i,p in enumerate(t,1): print(f"║  {G}[{i:02d}]{W} {p:<34}{R}║")
    print(f"╚{'═'*40}╝")

def clear_targets(): save_targets([]); print(f"{G}[✓] All targets cleared!")

def countdown(sec, msg="Waiting"):
    for i in range(sec,0,-1):
        print(f"\r{Y}[*] {msg} {i}s...",end="",flush=True); time.sleep(1)
    print(f"\r{C}[*] Done!{' '*25}")
