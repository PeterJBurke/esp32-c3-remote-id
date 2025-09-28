#!/usr/bin/env python3
"""
Battery-Powered ESP32-C3 Test Monitor
Tests if ESP32-C3 packets can be detected when powered from external source
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class BatteryTestMonitor:
    def __init__(self):
        self.running = True
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.esp32_packets = 0
        self.start_time = time.time()
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping battery test monitor...")
        self.running = False
        sys.exit(0)
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks"""
        try:
            result = subprocess.run(['timeout', '3', 'nmcli', 'dev', 'wifi', 'list'], 
                                  capture_output=True, text=True, check=True, timeout=5)
            return result.stdout
        except subprocess.TimeoutExpired:
            return "Error: Command timed out"
        except subprocess.CalledProcessError as e:
            return f"Error running nmcli: {e.stderr}"
        except FileNotFoundError:
            return "Error: 'nmcli' command not found"
    
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
        """Display packet information"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        elapsed = time.time() - self.start_time
        
        print(f"\n🔋 BATTERY-POWERED ESP32-C3 PACKET #{packet_num} - {timestamp}")
        print("=" * 80)
        print(f"📡 MAC: {self.esp32_mac} | SSID: {self.esp32_ssid}")
        print(f"⏱️  Runtime: {elapsed:.1f}s | Packets: {packet_num}")
        print(f"🔋 Power Source: External (Battery/External Supply)")
        print(f"📡 Transmission: WiFi Beacon Mode")
        print(f"📍 Location: Aldrich Park, Irvine, CA")
        print(f"✅ Status: ACTIVE - No USB connection required!")
        print("=" * 80)
    
    def run(self):
        """Run the battery test monitor"""
        print("🔋 ESP32-C3 Battery Power Test Monitor")
        print("=" * 50)
        print("Testing if ESP32-C3 packets can be detected when")
        print("powered from external source (battery/external supply)")
        print("=" * 50)
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        # Set up signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        while self.running:
            wifi_data = self.scan_wifi_networks()
            
            if "Error" in wifi_data:
                print(f"❌ {wifi_data}")
                time.sleep(2)
                continue
            
            # Look for ESP32-C3 packet
            esp32_line = self.find_esp32_packet(wifi_data)
            if esp32_line:
                self.esp32_packets += 1
                self.display_packet(self.esp32_packets)
            else:
                # Show scanning status every 5 seconds
                if int(time.time() - self.start_time) % 5 == 0:
                    elapsed = time.time() - self.start_time
                    print(f"🔍 Scanning... {elapsed:.0f}s elapsed, {self.esp32_packets} packets found")
            
            time.sleep(1)  # Scan every second

if __name__ == "__main__":
    monitor = BatteryTestMonitor()
    monitor.run()
