#!/usr/bin/env python3
"""
Proxy Rotator - Rotate IP addresses using free proxies
"""

import requests
import time
import random
import threading
import sys
import signal

class ProxyRotator:
    def __init__(self):
        self.url = "https://api.ipify.org?format=json"
        self.stop_flag = False
        self.working_proxies = []
        
    def fetch_proxies_method1(self):
        """Method 1: Fetch from proxyscrape API"""
        try:
            response = requests.get(
                "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000&proxy_format=ipport&format=text",
                timeout=10
            )
            proxies = response.text.strip().split('\r\n')
            return [{"http": f"http://{p}", "https": f"http://{p}"} for p in proxies if p]
        except:
            return []

    def fetch_proxies_method2(self):
        """Method 2: Fetch from pubproxy API"""
        try:
            response = requests.get(
                "http://pubproxy.com/api/proxy?limit=20&format=json&type=http",
                timeout=10
            )
            data = response.json()
            proxies = []
            for item in data.get('data', []):
                proxy = f"{item['ip']}:{item['port']}"
                proxies.append({"http": f"http://{proxy}", "https": f"http://{proxy}"})
            return proxies
        except:
            return []

    def fetch_proxies_method3(self):
        """Method 3: Hardcoded backup proxies"""
        backup_list = [
            "165.227.104.122:3128",
            "47.88.58.222:80",
            "51.79.50.46:3128",
        ]
        return [{"http": f"http://{p}", "https": f"http://{p}"} for p in backup_list]

    def get_all_proxies(self):
        """Try all methods to get proxies"""
        all_proxies = []
        
        print("Trying method 1...")
        proxies = self.fetch_proxies_method1()
        all_proxies.extend(proxies)
        
        print("Trying method 2...")
        proxies = self.fetch_proxies_method2()
        all_proxies.extend(proxies)
        
        print("Using backup proxies...")
        proxies = self.fetch_proxies_method3()
        all_proxies.extend(proxies)
        
        return all_proxies

    def test_proxy(self, proxy):
        """Test if a proxy works"""
        try:
            start_time = time.time()
            r = requests.get(self.url, proxies=proxy, timeout=5)
            if r.status_code == 200:
                ip = r.json()['ip']
                response_time = time.time() - start_time
                print(f"  ✓ Proxy works: {ip} (Response time: {response_time:.2f}s)")
                return ip
        except:
            pass
        return None

    def get_ip(self, proxy):
        """Get IP using proxy"""
        try:
            r = requests.get(self.url, proxies=proxy, timeout=5)
            return r.json()["ip"]
        except:
            return None

    def rotate(self):
        """Main rotation loop"""
        while not self.stop_flag:
            if not self.working_proxies:
                print("\n" + "="*50)
                print("Fetching new proxies...")
                print("="*50)
                proxy_list = self.get_all_proxies()
                
                print(f"\nTesting {len(proxy_list)} proxies...")
                for i, proxy in enumerate(proxy_list, 1):
                    if self.stop_flag:
                        break
                    print(f"Testing proxy {i}/{len(proxy_list)}...", end=" ")
                    ip = self.test_proxy(proxy)
                    if ip:
                        self.working_proxies.append(proxy)
                    if len(self.working_proxies) >= 5:
                        break
                
                print(f"\nFound {len(self.working_proxies)} working proxies")
                
            if self.working_proxies:
                proxy = random.choice(self.working_proxies)
                ip = self.get_ip(proxy)
                if ip:
                    print(f"\n[✓] Current IP: {ip} (Using proxy)")
                    print(f"[i] Available proxies: {len(self.working_proxies)}")
                else:
                    print("[✗] Proxy failed, removing from list")
                    self.working_proxies.remove(proxy)
            else:
                print("\n[!] No working proxies found")
                print("[i] Waiting 30 seconds before retrying...")
                time.sleep(30)
                continue
                
            time.sleep(3)

    def start(self):
        """Start the proxy rotator"""
        print("="*50)
        print("Starting Proxy Rotator...")
        print("Press Ctrl+C to stop")
        print("="*50)
        
        # Handle Ctrl+C gracefully
        def signal_handler(sig, frame):
            self.stop_flag = True
            print("\n\n[!] Stopped by user")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        try:
            self.rotate()
        except KeyboardInterrupt:
            self.stop_flag = True
            print("\n\n[!] Stopped by user")

def main():
    rotator = ProxyRotator()
    rotator.start()

if __name__ == "__main__":
    main()