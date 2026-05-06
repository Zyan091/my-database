#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import urllib3
import time
import threading
import hashlib
import subprocess
import os
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs

urllib3.disable_warnings()
os.environ['PYTHONWARNINGS'] = 'ignore'

# ==========================================
# CONFIG & DATABASE
# ==========================================
GIST_RAW_URL = "https://raw.githubusercontent.com/Zyan091/my-database/refs/heads/main/key.txt"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".alli_key.txt")
HWID_FILE = os.path.join(os.path.expanduser("~"), ".alli_hwid.txt") # HWID အသေသိမ်းရန်ဖိုင်
THREADS = 50 # Gaming အတွက် အကောင်းဆုံး thread

# COLORS
W = "\033[97m"   # White
P = "\033[95m"   # Pink
O = "\033[38;5;214m" # Orange
G = "\033[92m"   # Green
R = "\033[91m"   # Red
C = "\033[96m"   # Cyan
YELLOW = "\033[93m"
BOLD, RESET = "\033[1m", "\033[0m"

def get_hwid():
    """Redmi 8 HWID - ထွက်ပြီးပြန်ဝင်လည်း ID လုံးဝမပြောင်းလဲစေရန် Local ဖိုင်ဖြင့် ထိန်းသိမ်းခြင်း"""
    if os.path.exists(HWID_FILE):
        with open(HWID_FILE, "r") as f:
            saved_hwid = f.read().strip()
            if saved_hwid: return saved_hwid

    try:
        model = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
        serial = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
        new_hwid = hashlib.sha256(f"{model}{serial}ZYAN-PRO".encode()).hexdigest()[:14].upper()
        
        with open(HWID_FILE, "w") as f:
            f.write(new_hwid)
        return new_hwid
    except: 
        return "ALLI-DEV-ERR"

def verify_license(user_key, current_hwid):
    """Key & Expiry (နေ့ရက်/အချိန်) များကို Database တွင် အသေးစိတ်စစ်ဆေးခြင်း"""
    try:
        response = requests.get(f"{GIST_RAW_URL}?nocache={time.time()}", timeout=10, verify=False)
        for line in response.text.splitlines():
            if "|" not in line: continue
            k, stored_hwid, expiry_str, status = line.split('|')
            if user_key == k:
                exp_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
                diff = exp_date - datetime.now()
                if diff.total_seconds() <= 0: return {"v": False, "m": "EXPIRED"}
                if stored_hwid == "None" or stored_hwid == current_hwid:
                    time_left = f"{diff.days} ရက်၊ {diff.seconds // 3600} နာရီ၊ {(diff.seconds // 60) % 60} မိနစ်"
                    return {"v": True, "m": time_left, "key": k, "exp": expiry_str}
        return {"v": False, "m": "INVALID KEY"}
    except: return {"v": False, "m": "OFFLINE"}

def auto_capture_portal():
    """ဝိုင်ဖိုင်လင့်ခ်ကို Background တွင် အလိုအလျောက် လှမ်းဖတ်သည့်စနစ်"""
    test_url = "http://connectivitycheck.gstatic.com/generate_204"
    try:
        r = requests.get(test_url, allow_redirects=True, timeout=5, verify=False)
        if r.url != test_url:
            return r.url
    except:
        pass
    return None

def turbo_ping(auth_link):
    """မူရင်း Engine Logic (MLBB ငြိမ်စေရန်)"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi 8)',
        'X-Requested-With': 'com.android.settings',
        'Connection': 'keep-alive'
    }
    with requests.Session() as s:
        while True:
            try: s.get(auth_link, headers=headers, timeout=5, verify=False)
            except: pass
            time.sleep(0.001)

def banner():
    subprocess.run("clear", shell=True)
    # Alli အလိုရှိသော အဖြူနှင့် ပန်းရောင်စပ် Premium Banner
    print(f"{P}{BOLD}    █████╗ ██╗     ██╗     ██╗")
    print(f"   ██╔══██╗██║     ██║     ██║")
    print(f"{W}   ███████║██║     ██║     ██║")
    print(f"   ██╔══██║██║     ██║     ██║")
    print(f"{P}   ██║  ██║███████╗███████╗██║")
    print(f"   ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝{RESET}")
    print(f"{O}      ALLI PREMIUM | RUIJIE CLOUD VIP{RESET}")
    print(f"{W}  ------------------------------------------{RESET}")

def start():
    banner()
    hwid = get_hwid()
    print(f"{P}[-] DEVICE ID : {W}{hwid}{RESET}")
    
    key = None
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f: key = f.read().strip()
        auth = verify_license(key, hwid)
        if not auth["v"]: key = None

    if not key:
        key = input(f"{O}[>] ENTER KEY : {W}").strip()
        auth = verify_license(key, hwid)
        if not auth["v"]: print(f"{R}[X] {auth['m']}{RESET}"); sys.exit()

    with open(KEY_FILE, "w") as f: f.write(key)
    
    # ----------------------------------------------------
    # NEW HYBRID SYSTEM - AUTO DETECT WITH MANUAL FALLBACK
    # ----------------------------------------------------
    print(f"\n{O}[*] Scanning WiFi Portal Automatically...{RESET}")
    portal_url = auto_capture_portal()
    
    if portal_url:
        print(f"{G}[✓] WiFi Portal Detected Automatically!{RESET}")
        time.sleep(1)
    else:
        # Auto ဖတ်မရပါက အရင်အတိုင်း လက်နဲ့ထည့်ခိုင်းမည်ဖြစ်၍ လိုင်းဆွဲအားကို စိတ်ချရပါသည်
        print(f"{YELLOW}[!] Auto-Scan missed. Please paste your URL manually below:{RESET}")
        portal_url = input(f"{O}[>] URL: {W}").strip()
    # ----------------------------------------------------
    
    try:
        parsed = urlparse(portal_url)
        params = parse_qs(parsed.query)
        sid = params.get('sessionId', [None])[0] or params.get('token', [None])[0]
        gw_addr = params.get('gw_address', ["192.168.110.1"])[0]
        gw_port = params.get('gw_port', ['2060'])[0]

        if not sid:
            print(f"{R}[!] Session ID not found in Link!{RESET}"); return

        auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
        
        banner()
        # ဝယ်သူတွေ ယုံကြည်မှုတက်စေမည့် အသေးစိတ် အချက်အလက်မျက်နှာပြင်
        print(f"{G}[✓] BYPASS ACTIVE! (PREMIUM LICENSE){RESET}")
        print(f"{W}  ------------------------------------------")
        print(f"{P}[+] YOUR KEY : {W}{auth['key']}")
        print(f"{P}[+] EXP DATE : {W}{auth['exp']}")
        print(f"{P}[+] TIME LEFT: {O}{BOLD}{auth['m']}{RESET}")
        print(f"{W}  ------------------------------------------")

        for _ in range(THREADS):
            threading.Thread(target=turbo_ping, args=(auth_link,), daemon=True).start()

        # အောက်ခြေ ရောင်စုံ Status Animation (Syntax Error Fix ပြီး)
        colors = [P, W, O, G, C]
        i = 0
        while True:
            color = colors[i % len(colors)]
            sys.stdout.write(f"\r{color}{BOLD} [⚡] ALLI PRO INJECTING SPEED... STATUS: ULTRA STABLE {RESET}")
            sys.stdout.flush()
            i += 1
            time.sleep(0.3)

    except Exception as e:
        print(f"{R}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    try: start()
    except KeyboardInterrupt: sys.exit()            
