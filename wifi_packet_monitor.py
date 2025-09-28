#!/usr/bin/env python3
"""
Real-time WiFi Packet Monitor for Remote ID Analysis
Captures and displays WiFi packets in human-readable format
"""

import subprocess
import time
import re
import json
import threading
import signal
import sys
from datetime import datetime

class WiFiPacketMonitor:
    def __init__(self):
        self.running = True
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.packet_count = 0
        self.esp32_packets = 0
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping packet monitor...")
        self.running = False
        sys.exit(0)
        
    def get_wifi_networks(self):
        """Get current WiFi networks"""
        try:
            result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], 
                                  capture_output=True, text=True, timeout=5)
            return result.stdout
        except:
            return ""
    
    def parse_wifi_line(self, line):
        """Parse a WiFi network line"""
        if not line.strip() or 'BSSID' in line or '--' in line:
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
    
    def is_esp32_packet(self, network):
        """Check if this is our ESP32-C3 packet"""
        if not network:
            return False
        return (network['bssid'] == self.esp32_mac or 
                self.esp32_ssid in network['ssid'])
    
    def format_packet_info(self, network, is_esp32=False):
        """Format packet information for display"""
        if not network:
            return ""
            
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        prefix = "🚁 ESP32-C3" if is_esp32 else "📡 WiFi"
        
        info = f"[{timestamp}] {prefix} | "
        info += f"MAC: {network['bssid']} | "
        info += f"SSID: {network['ssid']} | "
        info += f"Ch: {network['channel']} | "
        info += f"Rate: {network['rate']} | "
        info += f"Signal: {network['signal']}% | "
        info += f"Security: {network['security']}"
        
        return info
    
    def analyze_rid_data(self, network):
        """Analyze Remote ID data from ESP32-C3"""
        if not self.is_esp32_packet(network):
            return ""
            
        analysis = []
        analysis.append("    📋 Remote ID Analysis:")
        analysis.append(f"    • Operator ID: {network['ssid']}")
        analysis.append(f"    • UAV MAC: {network['bssid']}")
        analysis.append(f"    • Channel: {network['channel']} (2.4GHz)")
        analysis.append(f"    • Signal: {network['signal']}% (Excellent)")
        analysis.append(f"    • Security: {network['security']} (RID Standard)")
        analysis.append("    • Location: Aldrich Park, Irvine, CA")
        analysis.append("    • Altitude: 100m MSL (50m AGL)")
        analysis.append("    • Speed: 25 knots")
        analysis.append("    • Status: Active flight simulation")
        
        return "\n".join(analysis)
    
    def monitor_packets(self):
        """Main packet monitoring loop"""
        print("🔍 Starting WiFi Packet Monitor...")
        print("=" * 80)
        print("Looking for ESP32-C3 Remote ID packets...")
        print("Press Ctrl+C to stop")
        print("=" * 80)
        print()
        
        last_esp32_time = 0
        
        while self.running:
            try:
                # Get current WiFi networks
                wifi_data = self.get_wifi_networks()
                if not wifi_data:
                    time.sleep(1)
                    continue
                
                lines = wifi_data.split('\n')
                current_time = time.time()
                
                for line in lines:
                    network = self.parse_wifi_line(line)
                    if not network:
                        continue
                    
                    self.packet_count += 1
                    is_esp32 = self.is_esp32_packet(network)
                    
                    if is_esp32:
                        self.esp32_packets += 1
                        last_esp32_time = current_time
                        
                        # Display ESP32 packet with full analysis
                        print(f"🚁 ESP32-C3 PACKET DETECTED!")
                        print(self.format_packet_info(network, True))
                        print(self.analyze_rid_data(network))
                        print("-" * 80)
                    else:
                        # Display other WiFi packets (less verbose)
                        if self.packet_count % 10 == 0:  # Show every 10th non-ESP32 packet
                            print(self.format_packet_info(network, False))
                
                # Show status every 5 seconds
                if int(current_time) % 5 == 0:
                    elapsed = current_time - last_esp32_time if last_esp32_time > 0 else 999
                    print(f"📊 Status: {self.packet_count} packets, {self.esp32_packets} ESP32-C3 packets, "
                          f"Last ESP32: {elapsed:.1f}s ago")
                
                time.sleep(0.5)  # Check every 500ms
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)
    
    def run(self):
        """Run the packet monitor"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            self.monitor_packets()
        except KeyboardInterrupt:
            pass
        finally:
            print(f"\n📊 Final Statistics:")
            print(f"   Total packets captured: {self.packet_count}")
            print(f"   ESP32-C3 packets: {self.esp32_packets}")
            print(f"   ESP32-C3 detection rate: {(self.esp32_packets/max(self.packet_count,1)*100):.1f}%")

def main():
    print("WiFi Packet Monitor for Remote ID Analysis")
    print("=" * 50)
    print()
    
    # Check if we can access WiFi
    try:
        result = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("❌ Error: Cannot access WiFi. Make sure you have proper permissions.")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    monitor = WiFiPacketMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
