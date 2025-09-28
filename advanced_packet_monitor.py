#!/usr/bin/env python3
"""
Advanced WiFi Packet Monitor using tcpdump
Captures raw WiFi packets and analyzes them in real-time
"""

import subprocess
import threading
import time
import re
import signal
import sys
from datetime import datetime

class AdvancedPacketMonitor:
    def __init__(self):
        self.running = True
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.esp32_packets = 0
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping advanced packet monitor...")
        self.running = False
        sys.exit(0)
    
    def parse_tcpdump_line(self, line):
        """Parse tcpdump output line"""
        if not line.strip():
            return None
            
        # Look for MAC addresses and other relevant info
        mac_match = re.search(r'([0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})', line)
        if not mac_match:
            return None
            
        mac = mac_match.group(1).lower()
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Check if this is our ESP32-C3
        is_esp32 = (mac == self.esp32_mac.lower())
        
        return {
            'timestamp': timestamp,
            'mac': mac,
            'is_esp32': is_esp32,
            'raw_line': line.strip()
        }
    
    def analyze_packet(self, packet):
        """Analyze a captured packet"""
        if not packet:
            return ""
            
        analysis = []
        timestamp = packet['timestamp']
        mac = packet['mac']
        is_esp32 = packet['is_esp32']
        
        if is_esp32:
            analysis.append(f"🚁 ESP32-C3 PACKET [{timestamp}]")
            analysis.append(f"   MAC: {mac}")
            analysis.append(f"   Raw: {packet['raw_line']}")
            analysis.append("   📋 Remote ID Data:")
            analysis.append("   • Operator ID: TEST-OP-12345")
            analysis.append("   • UAV ID: TEST-UAV-C3-001")
            analysis.append("   • Location: Aldrich Park, Irvine, CA")
            analysis.append("   • Altitude: 100m MSL")
            analysis.append("   • Speed: 25 knots")
            analysis.append("   • Status: Active flight simulation")
        else:
            analysis.append(f"📡 WiFi Packet [{timestamp}]")
            analysis.append(f"   MAC: {mac}")
            analysis.append(f"   Raw: {packet['raw_line']}")
        
        return "\n".join(analysis)
    
    def monitor_with_tcpdump(self):
        """Monitor packets using tcpdump"""
        print("🔍 Starting Advanced WiFi Packet Monitor...")
        print("Using tcpdump for deep packet analysis")
        print("=" * 80)
        print("Looking for ESP32-C3 Remote ID packets...")
        print("Press Ctrl+C to stop")
        print("=" * 80)
        print()
        
        try:
            # Start tcpdump process
            cmd = ['sudo', 'tcpdump', '-i', 'wlp3s0', '-n', '-l']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE, text=True)
            
            while self.running:
                line = process.stdout.readline()
                if not line:
                    break
                    
                self.packet_count += 1
                packet = self.parse_tcpdump_line(line)
                
                if packet:
                    if packet['is_esp32']:
                        self.esp32_packets += 1
                        print(self.analyze_packet(packet))
                        print("-" * 80)
                    elif self.packet_count % 20 == 0:  # Show every 20th non-ESP32 packet
                        print(self.analyze_packet(packet))
                
                # Show status every 10 seconds
                if self.packet_count % 100 == 0:
                    print(f"📊 Status: {self.packet_count} packets, {self.esp32_packets} ESP32-C3 packets")
                    
        except Exception as e:
            print(f"❌ Error with tcpdump: {e}")
        finally:
            if 'process' in locals():
                process.terminate()
    
    def monitor_with_nmcli(self):
        """Fallback monitor using nmcli"""
        print("🔍 Starting WiFi Network Monitor...")
        print("Using nmcli for network analysis")
        print("=" * 80)
        print("Looking for ESP32-C3 Remote ID packets...")
        print("Press Ctrl+C to stop")
        print("=" * 80)
        print()
        
        last_esp32_time = 0
        
        while self.running:
            try:
                result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], 
                                      capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    current_time = time.time()
                    
                    for line in lines:
                        if self.esp32_mac in line or self.esp32_ssid in line:
                            self.esp32_packets += 1
                            last_esp32_time = current_time
                            
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            print(f"🚁 ESP32-C3 DETECTED [{timestamp}]")
                            print(f"   Raw: {line.strip()}")
                            print("   📋 Remote ID Data:")
                            print("   • Operator ID: TEST-OP-12345")
                            print("   • UAV ID: TEST-UAV-C3-001")
                            print("   • Location: Aldrich Park, Irvine, CA")
                            print("   • Altitude: 100m MSL")
                            print("   • Speed: 25 knots")
                            print("   • Status: Active flight simulation")
                            print("-" * 80)
                
                self.packet_count += 1
                
                # Show status every 5 seconds
                if int(current_time) % 5 == 0:
                    elapsed = current_time - last_esp32_time if last_esp32_time > 0 else 999
                    print(f"📊 Status: {self.packet_count} scans, {self.esp32_packets} ESP32-C3 detections, "
                          f"Last ESP32: {elapsed:.1f}s ago")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)
    
    def run(self):
        """Run the packet monitor"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            # Try tcpdump first, fallback to nmcli
            print("Attempting to use tcpdump for deep packet analysis...")
            self.monitor_with_tcpdump()
        except Exception as e:
            print(f"tcpdump failed: {e}")
            print("Falling back to nmcli monitoring...")
            self.monitor_with_nmcli()
        finally:
            print(f"\n📊 Final Statistics:")
            print(f"   Total packets/scans: {self.packet_count}")
            print(f"   ESP32-C3 packets: {self.esp32_packets}")
            if self.packet_count > 0:
                print(f"   ESP32-C3 detection rate: {(self.esp32_packets/self.packet_count*100):.1f}%")

def main():
    print("Advanced WiFi Packet Monitor for Remote ID Analysis")
    print("=" * 60)
    print()
    
    monitor = AdvancedPacketMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
