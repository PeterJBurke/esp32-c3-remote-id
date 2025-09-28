#!/usr/bin/env python3
"""
Real-time ESP32-C3 Packet Dumper
Properly detects when ESP32 goes online/offline
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class RealtimePacketDumper:
    def __init__(self):
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.start_time = time.time()
        self.esp32_online = False
        self.last_seen_time = 0
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping real-time packet dumper...")
        sys.exit(0)
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks with fresh data and LAST-SEEN field."""
        try:
            subprocess.run(['nmcli', 'dev', 'wifi', 'rescan'],
                           capture_output=True, text=True, check=True, timeout=3)
            # Use terse output with explicit fields to get LAST-SEEN consistently
            result = subprocess.run([
                'nmcli', '-t', '-f',
                'BSSID,SSID,CHAN,RATE,SIGNAL,BARS,SECURITY,LAST-SEEN',
                'dev', 'wifi', 'list'
            ], capture_output=True, text=True, check=True, timeout=5)
            return result.stdout
        except Exception as e:
            return f"Error: {e}"

    def _parse_last_seen_seconds(self, last_seen_str: str) -> float:
        """Convert nmcli LAST-SEEN string to seconds. Returns large number on failure."""
        if not last_seen_str:
            return 1e9
        s = last_seen_str.strip().lower()
        if s == 'now':
            return 0.0
        # Examples: '1 second ago', '5 seconds ago', '2 minutes ago', '1 hour ago'
        parts = s.split()
        if not parts:
            return 1e9
        try:
            value = float(parts[0])
        except Exception:
            return 1e9
        unit = parts[1] if len(parts) > 1 else 'seconds'
        if unit.startswith('sec'):
            return value
        if unit.startswith('min'):
            return value * 60.0
        if unit.startswith('hour'):
            return value * 3600.0
        return 1e9
    
    def is_esp32_present(self, wifi_data):
        """Check if ESP32-C3 is present and seen recently (<3s) in current scan."""
        if "Error" in wifi_data:
            return False, "Scan error"
        lines = [ln for ln in wifi_data.strip().split('\n') if ln.strip()]
        # nmcli -t uses ':' as delimiter: BSSID:SSID:CHAN:RATE:SIGNAL:BARS:SECURITY:LAST-SEEN
        for line in lines:
            parts = line.split(':')
            if len(parts) < 8:
                continue
            bssid, ssid = parts[0].strip(), parts[1].strip()
            last_seen = parts[-1].strip()
            if bssid.upper() == self.esp32_mac.upper() and ssid == self.esp32_ssid:
                seconds = self._parse_last_seen_seconds(last_seen)
                # Treat as live only if seen within last 3 seconds
                if seconds <= 3.0:
                    return True, line
                else:
                    return False, f"Stale entry (LAST-SEEN {last_seen})"
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
        """Run the real-time packet dumper"""
        print("🔍 Real-time ESP32-C3 Packet Dumper")
        print("=" * 50)
        print("Properly detects when ESP32 goes online/offline")
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
    dumper = RealtimePacketDumper()
    dumper.run()
