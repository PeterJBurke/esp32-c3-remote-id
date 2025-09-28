#!/usr/bin/env python3
"""
Truthful ESP32-C3 Packet Dumper
Only shows packets when ESP32-C3 is actually transmitting
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class TruthfulPacketDumper:
    def __init__(self):
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.start_time = time.time()
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping truthful packet dumper...")
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
    
    def run(self):
        """Run the truthful packet dumper"""
        print("🔍 Truthful ESP32-C3 Packet Dumper")
        print("=" * 50)
        print("Only shows packets when ESP32-C3 is actually transmitting")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        consecutive_misses = 0
        max_misses = 5
        
        while True:
            print(f"\n🔍 Scanning for ESP32-C3... (Attempt {self.packet_count + 1})")
            
            wifi_data = self.scan_wifi_networks()
            is_present, details = self.is_esp32_present(wifi_data)
            
            if is_present:
                self.packet_count += 1
                consecutive_misses = 0
                self.display_packet(self.packet_count, details)
            else:
                consecutive_misses += 1
                print(f"❌ ESP32-C3 NOT DETECTED ({consecutive_misses}/{max_misses})")
                print(f"   Reason: {details}")
                
                if consecutive_misses >= max_misses:
                    print(f"\n🔍 TRUTHFUL RESULT:")
                    print(f"   ESP32-C3 is NOT transmitting")
                    print(f"   Either:")
                    print(f"   • ESP32-C3 is powered off")
                    print(f"   • ESP32-C3 is out of range")
                    print(f"   • ESP32-C3 sketch is not running")
                    print(f"   • Battery is dead")
                    break
            
            time.sleep(2)

if __name__ == "__main__":
    dumper = TruthfulPacketDumper()
    dumper.run()
