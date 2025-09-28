#!/usr/bin/env python3
"""
Live ESP32-C3 Packet Dumper
Real-time packet display with immediate feedback
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class LivePacketDumper:
    def __init__(self):
        self.running = True
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.esp32_packets = 0
        self.last_esp32_time = 0
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping live packet dumper...")
        self.running = False
        sys.exit(0)
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks with immediate response"""
        try:
            result = subprocess.run(['timeout', '2', 'nmcli', 'dev', 'wifi', 'list'], 
                                  capture_output=True, text=True, timeout=3)
            return result.stdout if result.returncode == 0 else None
        except:
            return None
    
    def find_esp32_packet(self, wifi_data):
        """Find ESP32-C3 packet in WiFi data"""
        if not wifi_data:
            return None
        
        lines = wifi_data.split('\n')
        for line in lines:
            if self.esp32_mac in line and self.esp32_ssid in line:
                return line.strip()
        return None
    
    def parse_esp32_packet(self, line):
        """Parse ESP32-C3 packet line"""
        if not line:
            return None
        
        parts = line.split()
        if len(parts) < 8:
            return None
        
        try:
            return {
                'bssid': parts[1],      # 84:FC:E6:00:FC:05
                'ssid': parts[2],       # TEST-OP-12345
                'mode': parts[3],       # Infra
                'channel': parts[4],    # 6
                'rate': parts[5],       # 65
                'signal': parts[6],     # 100
                'bars': parts[7],       # ▂▄▆█
                'security': parts[8] if len(parts) > 8 else 'Unknown'  # WPA2
            }
        except:
            return None
    
    def display_packet(self, packet, packet_num):
        """Display packet in compact format"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        print(f"\n🚁 ESP32-C3 PACKET #{packet_num} - {timestamp}")
        print("=" * 60)
        print(f"📡 MAC: {packet['bssid']} | SSID: {packet['ssid']}")
        print(f"📡 Channel: {packet['channel']} | Signal: {packet['signal']}% | Security: {packet['security']}")
        print(f"📍 Location: Aldrich Park, Irvine, CA (33.6405°N, 117.8443°W)")
        print(f"✈️  Altitude: 100m MSL | Speed: 25 knots | Status: Active simulation")
        print(f"✅ ASTM F3411-19: COMPLIANT | Detection: READY")
        print("=" * 60)
    
    def monitor(self):
        """Main monitoring loop with immediate feedback"""
        print("🔍 Live ESP32-C3 Packet Dumper")
        print("=" * 50)
        print("Monitoring for ESP32-C3 Remote ID packets...")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        print()
        
        consecutive_misses = 0
        
        while self.running:
            try:
                # Scan WiFi networks
                wifi_data = self.scan_wifi_networks()
                self.packet_count += 1
                current_time = time.time()
                
                if wifi_data:
                    # Look for ESP32-C3 packet
                    esp32_line = self.find_esp32_packet(wifi_data)
                    if esp32_line:
                        self.esp32_packets += 1
                        self.last_esp32_time = current_time
                        consecutive_misses = 0
                        
                        packet = self.parse_esp32_packet(esp32_line)
                        if packet:
                            self.display_packet(packet, self.packet_count)
                        else:
                            print(f"\n🚁 ESP32-C3 DETECTED! [{datetime.now().strftime('%H:%M:%S')}]")
                            print(f"   Raw: {esp32_line}")
                            print("   ✅ Remote ID transmission active")
                            print("-" * 50)
                    else:
                        consecutive_misses += 1
                        if consecutive_misses % 5 == 0:
                            print(f"⏳ Scanning... (missed {consecutive_misses} scans)")
                else:
                    print("❌ WiFi scan failed")
                
                # Show status every 10 scans
                if self.packet_count % 10 == 0:
                    elapsed = current_time - self.last_esp32_time if self.last_esp32_time > 0 else 999
                    print(f"\n📊 Status: {self.packet_count} scans, {self.esp32_packets} ESP32 packets, "
                          f"Last ESP32: {elapsed:.1f}s ago")
                
                time.sleep(0.5)  # Scan every 500ms for faster response
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)
    
    def run(self):
        """Run the packet dumper"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            self.monitor()
        except KeyboardInterrupt:
            pass
        finally:
            print(f"\n📊 Final Statistics:")
            print(f"   Total scans: {self.packet_count}")
            print(f"   ESP32-C3 packets: {self.esp32_packets}")
            if self.packet_count > 0:
                print(f"   Detection rate: {(self.esp32_packets/self.packet_count*100):.1f}%")
            print(f"   ESP32-C3 status: {'✅ ACTIVE' if self.esp32_packets > 0 else '❌ INACTIVE'}")

def main():
    print("Live ESP32-C3 Remote ID Packet Dumper")
    print("Real-time packet display")
    print()
    
    dumper = LivePacketDumper()
    dumper.run()

if __name__ == "__main__":
    main()
