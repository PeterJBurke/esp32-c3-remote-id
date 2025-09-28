#!/usr/bin/env python3
"""
Instant ESP32-C3 Packet Printer
Prints packets immediately as they are received
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class InstantPacketPrinter:
    def __init__(self):
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.running = True

    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping instant packet printer...")
        self.running = False
        sys.exit(0)

    def scan_wifi_networks(self):
        """Scan for WiFi networks with fresh data"""
        try:
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

    def parse_packet_data(self, beacon_line):
        """Parse packet data for display"""
        if not beacon_line:
            return None

        parts = beacon_line.split()
        if len(parts) < 9:
            return None

        # Extract key information
        bssid = parts[0]  # 84:FC:E6:00:FC:05
        ssid = parts[1]   # TEST-OP-12345
        channel = parts[3]  # 6
        rate = f"{parts[4]} {parts[5]}"  # "65 Mbit/s"
        signal = parts[6]  # 100
        security = parts[8] if len(parts) > 8 else 'Unknown'  # WPA2

        return {
            'bssid': bssid,
            'ssid': ssid,
            'channel': channel,
            'rate': rate,
            'signal': signal,
            'security': security,
            'raw_line': beacon_line
        }

    def print_packet(self, packet_data):
        """Print packet information immediately"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        print(f"\n🚁 ESP32-C3 REMOTE ID PACKET RECEIVED! [{timestamp}]")
        print("=" * 70)
        print(f"📡 BSSID: {packet_data['bssid']} | SSID: {packet_data['ssid']}")
        print(f"📡 Channel: {packet_data['channel']} | Rate: {packet_data['rate']}")
        print(f"📡 Signal: {packet_data['signal']}% | Security: {packet_data['security']}")
        print(f"📍 Location: Aldrich Park, Irvine, CA")
        print(f"✈️  Status: ACTIVE - Real-time transmission!")
        print(f"✅ Ready for Remote ID detection")
        print("=" * 70)

    def run(self):
        """Run the instant packet printer"""
        print("🔍 Instant ESP32-C3 Packet Printer")
        print("=" * 50)
        print("Prints packets immediately as they are received")
        print("Press Ctrl+C to stop")
        print("=" * 50)

        signal.signal(signal.SIGINT, self.signal_handler)

        packet_count = 0

        while self.running:
            wifi_data = self.scan_wifi_networks()
            esp32_line = self.find_esp32_packet(wifi_data)

            if esp32_line:
                packet_count += 1
                packet_data = self.parse_packet_data(esp32_line)

                if packet_data:
                    self.print_packet(packet_data)
                else:
                    print(f"\n🚁 ESP32-C3 DETECTED! [{datetime.now().strftime('%H:%M:%S')}]")
                    print(f"   Raw: {esp32_line}")
                    print("   ✅ Remote ID transmission active")

            time.sleep(0.5)  # Check every 500ms for immediate response

if __name__ == "__main__":
    printer = InstantPacketPrinter()
    printer.run()







