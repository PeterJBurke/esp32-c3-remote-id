#!/usr/bin/env python3
"""
Final ESP32-C3 Packet Test
Only shows packets when ESP32 is actually transmitting
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class FinalPacketTest:
    def __init__(self):
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.start_time = time.time()
        self.esp32_online = False
        self.last_seen_time = 0
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping final packet test...")
        sys.exit(0)
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks with fresh data"""
        try:
            # Force a fresh scan each time
            subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'], 
                          capture_output=True, text=True, check=True, timeout=2)
            
            result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], 
                                  capture_output=True, text=True, check=True, timeout=3)
            return result.stdout
        except Exception as e:
            return f"Error: {e}"
    
    def is_esp32_present(self, wifi_data):
        """Check if ESP32-C3 is actually present in current scan"""
        if "Error" in wifi_data:
            return False, "Scan error"
        
        lines = wifi_data.strip().split('\n')
        for line in lines:
            if self.esp32_mac in line and self.esp32_ssid in line:
                return True, line
        return False, "ESP32-C3 not found in current scan"
    
    def display_packet(self, packet_num, raw_line):
        """Display packet information"""
        current_time = datetime.now()
        rid_timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        elapsed = time.time() - self.start_time
        
        print(f"\n🚁 ESP32-C3 PACKET #{packet_num} - {rid_timestamp}")
        print("=" * 80)
        print(f"📡 MAC: {self.esp32_mac} | SSID: {self.esp32_ssid}")
        print(f"⏰ RID Timestamp: {rid_timestamp}")
        print(f"⏱️  Runtime: {elapsed:.1f}s | Packets: {packet_num}")
        print(f"📍 Location: Aldrich Park, Irvine, CA")
        print(f"✅ Status: ACTIVE - Real-time transmission!")
        print(f"🔍 Raw data: {raw_line}")
        print("=" * 80)
    
    def display_offline(self):
        """Display offline status"""
        current_time = datetime.now()
        elapsed = time.time() - self.start_time
        time_since_last_seen = time.time() - self.last_seen_time if self.last_seen_time > 0 else 0
        
        print(f"\n❌ ESP32-C3 OFFLINE - {current_time.strftime('%H:%M:%S')}")
        print("=" * 80)
        print(f"📡 MAC: {self.esp32_mac} | SSID: {self.esp32_ssid}")
        print(f"⏱️  Runtime: {elapsed:.1f}s | Packets: {self.packet_count}")
        print(f"📍 Location: Aldrich Park, Irvine, CA")
        print(f"❌ Status: OFFLINE - No transmission detected!")
        print(f"⏰ Time since last seen: {time_since_last_seen:.1f}s")
        print("=" * 80)
    
    def run(self):
        """Run the final packet test"""
        print("🔍 Final ESP32-C3 Packet Test")
        print("=" * 50)
        print("Only shows packets when ESP32 is actually transmitting")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        while True:
            wifi_data = self.scan_wifi_networks()
            is_present, details = self.is_esp32_present(wifi_data)
            
            if is_present:
                # ESP32 is online
                if not self.esp32_online:
                    print(f"\n🟢 ESP32-C3 CAME ONLINE at {datetime.now().strftime('%H:%M:%S')}")
                    self.esp32_online = True
                
                self.packet_count += 1
                self.last_seen_time = time.time()
                self.display_packet(self.packet_count, details)
            else:
                # ESP32 is offline
                if self.esp32_online:
                    print(f"\n🔴 ESP32-C3 WENT OFFLINE at {datetime.now().strftime('%H:%M:%S')}")
                    self.esp32_online = False
                
                # Show offline status every 5 seconds
                if int(time.time() - self.start_time) % 5 == 0:
                    self.display_offline()
            
            time.sleep(1)

if __name__ == "__main__":
    test = FinalPacketTest()
    test.run()







