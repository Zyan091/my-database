  import requests
import threading
import time
import sys
import hashlib
import subprocess
import os
import urllib3
from datetime import datetime

# Warning များ ပိတ်ထားခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# SERVER CONFIG
# ==========================================
GIST_RAW_URL = "https://raw.githubusercontent.com/Zyan091/my-database/refs/heads/main/key.txt"
KEY_FILE = ".alli_key.txt" 

# COLORS
R, G, Y, B, M, C, W = "\033[31m", "\033[32m", "\033[33m", "\033[34m", "\033[35m", "\033[36m", "\033[37m"
BOLD, RESET = "\033[1m", "\033[0m"

def get_hwid():
    try:
        model = subprocess.check_output("getprop ro.product.model", shell=True).decode().strip()
        serial = subprocess.check_output("getprop ro.serialno", shell=True).decode().strip()
        raw_id = f"{model}{serial}ALLI-AUTO-v4"
        return hashlib.sha256(raw_id.encode()).hexdigest()[:14].upper()
    except:
        return "ALLI-DEVICE-ERR"

def verify_license(user_key, current_hwid):
    try:
        response = requests.get(f"{GIST_RAW_URL}?nocache={time.time()}", timeout=20, verify=False)
        if response.status_code != 200: return {"v": False, "m": "DATABASE ERROR"}
        keys_data = response.text.splitlines()
        for line in keys_data:
            if not line.strip() or "|" not in line: continue
            k, stored_hwid, expiry_str, status = line.split('|')
            if user_key == k:
                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
                if datetime.now() > expiry_date: return {"v": False, "m": "LICENSE EXPIRED!"}
                if status.lower() != "active": return {"v": False, "m": "KEY INACTIVE!"}
                if stored_hwid == "None" or stored_hwid == current_hwid:
                    time_left = expiry_date - datetime.now()
                    return {"v": True, "m": f"{time_left.days}D LEFT", "p": (stored_hwid == "None")}
                else:
                    return {"v": False, "m": "HWID LOCKED!"}
    except:
        return {"v": False, "m": "CONNECTION ERROR"}
    return {"v": False, "m": "INVALID KEY"}

def get_portal_link():
    """မည်သည့် IP ဖြစ်စေ အလိုအလျောက် ရှာဖွေပေးသော စနစ်"""
    try:
        # လက်ရှိ ချိတ်ထားသော WiFi ၏ Gateway IP ကို ရှာခြင်း
        gw_cmd = "ip route show default | awk '{print $3}'"
        gw = subprocess.check_output(gw_cmd, shell=True).decode().strip()
        
        # IP ရှာမတွေ့ပါက Default 192.168.110.1 ကို သုံးမည်
        if not gw or "." not in gw:
            gw = "192.168.110.1"
            
        # Token နေရာတွင် Dynamic ID တစ်ခုကို ထည့်သွင်းပေးခြင်း
        return f"http://{gw}:2060/wifidog/auth?token=ALLI_AUTO_{int(time.time())}"
    except:
        return "http://192.168.110.1:2060/wifidog/auth?token=ALLI_AUTO_FIX"

def turbo_pulse(auth_link):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi 8)'}
    while True:
        try:
            requests.get(auth_link, headers=headers, timeout=5, verify=False)
        except: pass
        time.sleep(0.001)

def rainbow_alli():
    text = """
    █████╗ ██╗     ██╗     ██╗
    ██╔══██╗██║     ██║     ██║
    ███████║██║     ██║     ██║
    ██╔══██║██║     ██║     ██║
    ██║  ██║███████╗███████╗██║
    ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝"""
    colors = [R, G, Y, B, M, C]
    for line in text.splitlines():
        color = colors[int(time.time()*5) % len(colors)]
        print(f"{color}{BOLD}{line}{RESET}")
        time.sleep(0.01)

def banner():
    subprocess.run("clear", shell=True)
    rainbow_alli()
    print(f"{C}╔══════════════════════════════════════════════╗")
    print(f"║{W}   ALLI AUTO-BYPASS   |   STABLE v4.0        {C}║")
    print(f"║{W}   Status: {G}VIP PREMIUM{W}  |   Ping: {G}Anti-Lag      {C}║")
    print(f"╚══════════════════════════════════════════════╝{RESET}")

def start():
    banner()
    hwid = get_hwid()
    print(f"{M}[-] YOUR DEVICE ID: {W}{BOLD}{hwid}{RESET}")

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f: key = f.read().strip()
        print(f"{G}[*] Auto-loading saved license...{RESET}")
    else:
        key = input(f"{C}[>] ENTER LICENSE: {RESET}").strip()

    auth = verify_license(key, hwid)
    if not auth["v"]:
        if os.path.exists(KEY_FILE): os.remove(KEY_FILE)
        print(f"{R}[X] {auth['m']}{RESET}"); sys.exit()

    with open(KEY_FILE, "w") as f: f.write(key)
    if auth.get("p"):
        print(f"{R}[!] BIND THIS ID TO ALLI: {hwid}{RESET}"); sys.exit()

    # Link မတောင်းတော့ဘဲ IP ရှာပြီး တန်းမောင်းပါမည်
    final_link = get_portal_link()
    
    subprocess.run("clear", shell=True)
    banner()
    print(f"\n{G}  [✓] ENGINE STARTED: {Y}{final_link}")
    print(f"  [✓] ALL WARNINGS SUPPRESSED.")
    print(f"  [✓] AUTO-GATEWAY DETECTION ACTIVE.{RESET}\n")

    for _ in range(60):
        threading.Thread(target=turbo_pulse, args=(final_link,), daemon=True).start()
    
    colors = [R, G, Y, B, M, C]
    i = 0
    while True:
        print(f"\r{colors[i%6]}{BOLD} [⚡] ALLI PRO RUNNING... SPEED: MAX | PING: STABLE {RESET}", end="")
        i += 1
        time.sleep(0.2)

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        sys.exit()     
