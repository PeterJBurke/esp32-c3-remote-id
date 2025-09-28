#!/usr/bin/env python3
"""
Real Battery Test - Actually checks if ESP32-C3 is transmitting
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class RealBatteryTest:
    def __init__(self):
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.start_time = time.time()
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping real battery test...")
        sys.exit(0)
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks with fresh data"""
        try:
            # Use a fresh scan each time
            result = subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'], 
                                  capture_output=True, text=True, check=True, timeout=3)
            
            result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], 
                                  capture_output=True, text=True, check=True, timeout=3)
            return result.stdout
        except Exception as e:
            return f"Error: {e}"
    
    def check_esp32_presence(self, wifi_data):
        """Check if ESP32-C3 is actually present in current scan"""
        if "Error" in wifi_data:
            return False, "Scan error"
        
        lines = wifi_data.strip().split('\n')
        for line in lines:
            if self.esp32_mac in line and self.esp32_ssid in line:
                return True, line
        return False, "Not found in current scan"
    
    def run_test(self):
        """Run the real battery test"""
        print("🔋 REAL ESP32-C3 Battery Test")
        print("=" * 50)
        print("This will actually check if ESP32-C3 is transmitting")
        print("when powered by battery/external source")
        print("=" * 50)
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        consecutive_misses = 0
        max_misses = 5
        
        while True:
            print(f"\n🔍 Scanning for ESP32-C3... (Attempt {self.packet_count + 1})")
            
            wifi_data = self.scan_wifi_networks()
            is_present, details = self.check_esp32_presence(wifi_data)
            
            if is_present:
                self.packet_count += 1
                consecutive_misses = 0
                elapsed = time.time() - self.start_time
                
                print(f"✅ ESP32-C3 DETECTED! (Packet #{self.packet_count})")
                print(f"   Time: {datetime.now().strftime('%H:%M:%S')}")
                print(f"   Runtime: {elapsed:.1f}s")
                print(f"   MAC: {self.esp32_mac}")
                print(f"   SSID: {self.esp32_ssid}")
                print(f"   Status: ACTIVE - Battery powered!")
                print(f"   Raw data: {details}")
            else:
                consecutive_misses += 1
                print(f"❌ ESP32-C3 NOT DETECTED ({consecutive_misses}/{max_misses})")
                print(f"   Reason: {details}")
                
                if consecutive_misses >= max_misses:
                    print(f"\n🔋 BATTERY TEST RESULT:")
                    print(f"   ESP32-C3 is NOT transmitting")
                    print(f"   Either:")
                    print(f"   • ESP32-C3 is powered off")
                    print(f"   • ESP32-C3 is out of range")
                    print(f"   • ESP32-C3 sketch is not running")
                    print(f"   • Battery is dead")
                    break
            
            time.sleep(2)  # Wait 2 seconds between scans

if __name__ == "__main__":
    test = RealBatteryTest()
    test.run_test()
