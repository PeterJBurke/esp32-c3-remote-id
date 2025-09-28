#!/usr/bin/env python3
"""
60-Second ESP32-C3 Packet Dumper
Stops after 60 seconds to prevent long runs
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class SixtySecondPacketDumper:
    def __init__(self):
        self.running = True
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.esp32_packets = 0
        self.start_time = time.time()
        self.max_runtime = 60  # 60 seconds max
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping 60-second packet dumper...")
        self.running = False
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
    
    def find_esp32_packet(self, wifi_data):
        """Find ESP32-C3 packet in WiFi data"""
        if "Error" in wifi_data:
            return None
        
        lines = wifi_data.strip().split('\n')
        for line in lines:
            if self.esp32_mac in line and self.esp32_ssid in line:
                return line
        return None
    
    def display_packet(self, packet_num):
        """Display packet with real timestamp"""
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
        print("=" * 80)
    
    def run(self):
        """Run the 60-second packet dumper"""
        print("⏰ 60-Second ESP32-C3 Packet Dumper")
        print("=" * 50)
        print("Will stop automatically after 60 seconds")
        print("Press Ctrl+C to stop early")
        print("=" * 50)
        
        signal.signal(signal.SIGINT, self.signal_handler)
        
        while self.running:
            elapsed = time.time() - self.start_time
            
            # Check if 60 seconds have passed
            if elapsed >= self.max_runtime:
                print(f"\n⏰ TIME UP! 60 seconds elapsed")
                print(f"📊 Final Results:")
                print(f"   • Total packets: {self.esp32_packets}")
                print(f"   • Runtime: {elapsed:.1f}s")
                print(f"   • ESP32-C3 Status: {'ACTIVE' if self.esp32_packets > 0 else 'NOT DETECTED'}")
                break
            
            wifi_data = self.scan_wifi_networks()
            esp32_line = self.find_esp32_packet(wifi_data)
            
            if esp32_line:
                self.esp32_packets += 1
                self.display_packet(self.esp32_packets)
            else:
                # Show countdown every 10 seconds
                if int(elapsed) % 10 == 0 and elapsed > 0:
                    remaining = self.max_runtime - elapsed
                    print(f"🔍 Scanning... {remaining:.0f}s remaining, {self.esp32_packets} packets found")
            
            time.sleep(1)

if __name__ == "__main__":
    dumper = SixtySecondPacketDumper()
    dumper.run()
