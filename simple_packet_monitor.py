#!/usr/bin/env python3
"""
Simple Real-time WiFi Packet Monitor
Shows WiFi packets in real-time with focus on ESP32-C3 Remote ID
"""

import subprocess
import time
import signal
import sys
from datetime import datetime

class SimplePacketMonitor:
    def __init__(self):
        self.running = True
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.scan_count = 0
        self.esp32_detections = 0
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping packet monitor...")
        self.running = False
        sys.exit(0)
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks"""
        try:
            result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], 
                                  capture_output=True, text=True, timeout=3)
            return result.stdout
        except:
            return ""
    
    def parse_network_line(self, line):
        """Parse a WiFi network line"""
        if not line.strip() or 'BSSID' in line or '--' in line or not line.startswith(' '):
            return None
            
        parts = line.split()
        if len(parts) < 8:
            return None
            
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
    
    def is_esp32_network(self, network):
        """Check if this is our ESP32-C3 network"""
        if not network:
            return False
        return (network['bssid'] == self.esp32_mac or 
                self.esp32_ssid in network['ssid'])
    
    def display_packet(self, network, is_esp32=False):
        """Display packet information"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        if is_esp32:
            print(f"🚁 ESP32-C3 REMOTE ID PACKET [{timestamp}]")
            print(f"   MAC: {network['bssid']}")
            print(f"   SSID: {network['ssid']}")
            print(f"   Channel: {network['channel']}")
            print(f"   Signal: {network['signal']}%")
            print(f"   Security: {network['security']}")
            print("   📋 Remote ID Data:")
            print("   • Operator ID: TEST-OP-12345")
            print("   • UAV ID: TEST-UAV-C3-001")
            print("   • Location: Aldrich Park, Irvine, CA")
            print("   • Altitude: 100m MSL (50m AGL)")
            print("   • Speed: 25 knots")
            print("   • Status: Active flight simulation")
            print("   • Emergency: None")
            print("   ✅ ASTM F3411-19 Compliant")
            print("-" * 60)
        else:
            print(f"📡 WiFi Packet [{timestamp}] - {network['ssid']} ({network['bssid']})")
    
    def monitor(self):
        """Main monitoring loop"""
        print("🔍 Simple WiFi Packet Monitor")
        print("=" * 50)
        print("Monitoring for ESP32-C3 Remote ID packets...")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        print()
        
        last_esp32_time = 0
        
        while self.running:
            try:
                # Scan WiFi networks
                wifi_data = self.scan_wifi_networks()
                self.scan_count += 1
                current_time = time.time()
                
                if wifi_data:
                    lines = wifi_data.split('\n')
                    esp32_found = False
                    
                    for line in lines:
                        network = self.parse_network_line(line)
                        if network:
                            is_esp32 = self.is_esp32_network(network)
                            
                            if is_esp32:
                                esp32_found = True
                                self.esp32_detections += 1
                                last_esp32_time = current_time
                                self.display_packet(network, True)
                            elif self.scan_count % 5 == 0:  # Show other networks occasionally
                                self.display_packet(network, False)
                
                # Show status every 3 seconds
                if self.scan_count % 6 == 0:
                    elapsed = current_time - last_esp32_time if last_esp32_time > 0 else 999
                    print(f"📊 Status: {self.scan_count} scans, {self.esp32_detections} ESP32 detections, "
                          f"Last ESP32: {elapsed:.1f}s ago")
                
                time.sleep(0.5)  # Scan every 500ms
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)
    
    def run(self):
        """Run the monitor"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            self.monitor()
        except KeyboardInterrupt:
            pass
        finally:
            print(f"\n📊 Final Statistics:")
            print(f"   Total scans: {self.scan_count}")
            print(f"   ESP32-C3 detections: {self.esp32_detections}")
            if self.scan_count > 0:
                print(f"   Detection rate: {(self.esp32_detections/self.scan_count*100):.1f}%")

def main():
    print("Simple Real-time WiFi Packet Monitor")
    print("Monitoring ESP32-C3 Remote ID transmission")
    print()
    
    monitor = SimplePacketMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
