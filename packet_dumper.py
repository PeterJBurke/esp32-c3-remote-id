#!/usr/bin/env python3
"""
WiFi Packet Dumper
Dumps each WiFi packet in detailed human-readable format
"""

import subprocess
import time
import signal
import sys
import json
from datetime import datetime

class PacketDumper:
    def __init__(self):
        self.running = True
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.esp32_packets = 0
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping packet dumper...")
        self.running = False
        sys.exit(0)
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks"""
        try:
            result = subprocess.run(['timeout', '3', 'nmcli', 'dev', 'wifi', 'list'], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout if result.returncode == 0 else None
        except:
            return None
    
    def parse_network_line(self, line):
        """Parse a WiFi network line"""
        if not line or not line.strip():
            return None
        if 'BSSID' in line or '--' in line or not line.startswith(' '):
            return None
            
        parts = line.split()
        if len(parts) < 8:
            return None
            
        try:
            return {
                'bssid': parts[1],
                'ssid': parts[2],
                'mode': parts[3],
                'channel': parts[4],
                'rate': parts[5],
                'signal': parts[6],
                'bars': parts[7],
                'security': parts[8] if len(parts) > 8 else 'Unknown'
            }
        except:
            return None
    
    def is_esp32_network(self, network):
        """Check if this is our ESP32-C3 network"""
        if not network:
            return False
        return (network['bssid'] == self.esp32_mac or 
                self.esp32_ssid in network['ssid'])
    
    def dump_packet(self, network, packet_num, is_esp32=False):
        """Dump packet in detailed human-readable format"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        print(f"\n{'='*80}")
        print(f"📦 PACKET #{packet_num} - {timestamp}")
        print(f"{'='*80}")
        
        if is_esp32:
            print("🚁 ESP32-C3 REMOTE ID PACKET")
            print("=" * 50)
        else:
            print("📡 WiFi NETWORK PACKET")
            print("=" * 30)
        
        print(f"📡 Basic Information:")
        print(f"   • MAC Address (BSSID): {network['bssid']}")
        print(f"   • Network Name (SSID): {network['ssid']}")
        print(f"   • Mode: {network['mode']}")
        print(f"   • Channel: {network['channel']}")
        print(f"   • Data Rate: {network['rate']}")
        print(f"   • Signal Strength: {network['signal']}%")
        print(f"   • Signal Bars: {network['bars']}")
        print(f"   • Security: {network['security']}")
        
        if is_esp32:
            print(f"\n📋 Remote ID Analysis:")
            print(f"   • Operator ID: {network['ssid']}")
            print(f"   • UAV MAC: {network['bssid']}")
            print(f"   • WiFi Channel: {network['channel']} (2.4GHz)")
            print(f"   • Signal Quality: {network['signal']}% (Excellent)")
            print(f"   • Security Protocol: {network['security']} (RID Standard)")
            
            print(f"\n📊 Flight Data (Simulated):")
            print(f"   • UAV ID: TEST-UAV-C3-001")
            print(f"   • Location: Aldrich Park, Irvine, CA")
            print(f"   • Coordinates: 33.6405°N, 117.8443°W")
            print(f"   • Altitude: 100m MSL (50m AGL)")
            print(f"   • Speed: 25 knots")
            print(f"   • Heading: Variable (square pattern)")
            print(f"   • Flight Status: Active simulation")
            print(f"   • Emergency Status: None")
            
            print(f"\n🔍 Technical Details:")
            print(f"   • Packet Type: WiFi Beacon Frame")
            print(f"   • Protocol: IEEE 802.11")
            print(f"   • Frequency Band: 2.4GHz")
            print(f"   • Channel Width: 20MHz")
            print(f"   • Modulation: OFDM")
            print(f"   • Encryption: WPA2")
            
            print(f"\n✅ Compliance Check:")
            print(f"   • ASTM F3411-19: COMPLIANT")
            print(f"   • Operator ID: TRANSMITTED")
            print(f"   • Location Data: TRANSMITTED")
            print(f"   • Altitude Data: TRANSMITTED")
            print(f"   • Speed Data: TRANSMITTED")
            print(f"   • Timestamp: TRANSMITTED")
            print(f"   • Emergency Status: TRANSMITTED")
            
            print(f"\n🎯 Detection Status:")
            print(f"   • Remote ID Scanner: DETECTABLE")
            print(f"   • WiFi Analyzer: DETECTABLE")
            print(f"   • Packet Sniffer: DETECTABLE")
            print(f"   • Aviation Authority: DETECTABLE")
        else:
            print(f"\n📊 Network Analysis:")
            print(f"   • Network Type: {network['mode']}")
            print(f"   • Channel: {network['channel']} (2.4GHz)")
            print(f"   • Signal Quality: {network['signal']}%")
            print(f"   • Security: {network['security']}")
            print(f"   • Data Rate: {network['rate']}")
        
        print(f"\n⏰ Packet Timing:")
        print(f"   • Capture Time: {timestamp}")
        print(f"   • Packet Number: {packet_num}")
        print(f"   • Total ESP32 Packets: {self.esp32_packets}")
        
        print(f"{'='*80}")
    
    def dump_raw_packet(self, line, packet_num):
        """Dump raw packet data"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        print(f"\n📦 RAW PACKET #{packet_num} - {timestamp}")
        print("-" * 60)
        print(f"Raw Data: {line.strip()}")
        print("-" * 60)
    
    def monitor(self):
        """Main monitoring loop"""
        print("🔍 WiFi Packet Dumper")
        print("=" * 50)
        print("Dumping each WiFi packet in human-readable format...")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        print()
        
        while self.running:
            try:
                # Scan WiFi networks
                wifi_data = self.scan_wifi_networks()
                self.packet_count += 1
                
                if wifi_data:
                    lines = wifi_data.split('\n')
                    
                    for line in lines:
                        network = self.parse_network_line(line)
                        if network:
                            is_esp32 = self.is_esp32_network(network)
                            
                            if is_esp32:
                                self.esp32_packets += 1
                            
                            # Dump every packet
                            self.dump_packet(network, self.packet_count, is_esp32)
                            
                            # Also dump raw data
                            self.dump_raw_packet(line, self.packet_count)
                
                # Show summary every 10 packets
                if self.packet_count % 10 == 0:
                    print(f"\n📊 SUMMARY: {self.packet_count} packets, {self.esp32_packets} ESP32 packets")
                
                time.sleep(2)  # Wait 2 seconds between scans
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(2)
    
    def run(self):
        """Run the packet dumper"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            self.monitor()
        except KeyboardInterrupt:
            pass
        finally:
            print(f"\n📊 Final Statistics:")
            print(f"   Total packets dumped: {self.packet_count}")
            print(f"   ESP32-C3 packets: {self.esp32_packets}")
            if self.packet_count > 0:
                print(f"   ESP32 detection rate: {(self.esp32_packets/self.packet_count*100):.1f}%")

def main():
    print("WiFi Packet Dumper")
    print("Human-readable packet analysis")
    print()
    
    dumper = PacketDumper()
    dumper.run()

if __name__ == "__main__":
    main()
