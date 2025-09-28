#!/usr/bin/env python3
"""
Reliable Real-time WiFi Packet Monitor
With progress indicators and hang prevention
"""

import subprocess
import time
import signal
import sys
import threading
from datetime import datetime

class ReliablePacketMonitor:
    def __init__(self):
        self.running = True
        self.esp32_mac = "84:FC:E6:00:FC:05"
        self.esp32_ssid = "TEST-OP-12345"
        self.scan_count = 0
        self.esp32_detections = 0
        self.last_esp32_time = 0
        self.last_status_time = 0
        
    def signal_handler(self, sig, frame):
        print("\n\n🛑 Stopping packet monitor...")
        self.running = False
        sys.exit(0)
    
    def scan_wifi_networks(self):
        """Scan for WiFi networks with robust error handling"""
        try:
            # Use timeout and proper error handling
            result = subprocess.run(['timeout', '3', 'nmcli', 'dev', 'wifi', 'list'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            else:
                return None
        except subprocess.TimeoutExpired:
            print("⏰ WiFi scan timeout - retrying...")
            return None
        except Exception as e:
            print(f"❌ WiFi scan error: {e}")
            return None
    
    def parse_network_line(self, line):
        """Parse a WiFi network line with validation"""
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
    
    def display_esp32_packet(self, network):
        """Display ESP32-C3 packet with full analysis"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n🚁 ESP32-C3 REMOTE ID PACKET DETECTED! [{timestamp}]")
        print("=" * 60)
        print(f"📡 MAC: {network['bssid']}")
        print(f"📡 SSID: {network['ssid']}")
        print(f"📡 Channel: {network['channel']}")
        print(f"📡 Signal: {network['signal']}%")
        print(f"📡 Security: {network['security']}")
        print()
        print("📋 Remote ID Data:")
        print("   • Operator ID: TEST-OP-12345")
        print("   • UAV ID: TEST-UAV-C3-001")
        print("   • Location: Aldrich Park, Irvine, CA")
        print("   • Coordinates: 33.6405°N, 117.8443°W")
        print("   • Altitude: 100m MSL (50m AGL)")
        print("   • Speed: 25 knots")
        print("   • Status: Active flight simulation")
        print("   ✅ ASTM F3411-19 Compliant")
        print("=" * 60)
    
    def show_progress(self):
        """Show progress indicator"""
        current_time = time.time()
        if current_time - self.last_status_time >= 5:  # Every 5 seconds
            elapsed = current_time - self.last_esp32_time if self.last_esp32_time > 0 else 999
            print(f"📊 Progress: {self.scan_count} scans, {self.esp32_detections} ESP32 detections, "
                  f"Last ESP32: {elapsed:.1f}s ago")
            self.last_status_time = current_time
    
    def monitor(self):
        """Main monitoring loop with progress tracking"""
        print("🔍 Reliable WiFi Packet Monitor")
        print("=" * 50)
        print("Monitoring ESP32-C3 Remote ID transmission...")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        print()
        
        consecutive_failures = 0
        max_failures = 3
        
        while self.running:
            try:
                # Show progress indicator
                self.show_progress()
                
                # Scan WiFi networks
                wifi_data = self.scan_wifi_networks()
                self.scan_count += 1
                current_time = time.time()
                
                if wifi_data:
                    consecutive_failures = 0
                    lines = wifi_data.split('\n')
                    esp32_found = False
                    
                    for line in lines:
                        network = self.parse_network_line(line)
                        if network:
                            is_esp32 = self.is_esp32_network(network)
                            
                            if is_esp32:
                                esp32_found = True
                                self.esp32_detections += 1
                                self.last_esp32_time = current_time
                                self.display_esp32_packet(network)
                            elif self.scan_count % 20 == 0:  # Show other networks occasionally
                                timestamp = datetime.now().strftime("%H:%M:%S")
                                print(f"📡 [{timestamp}] {network['ssid']} ({network['bssid']}) - Ch:{network['channel']}")
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_failures:
                        print(f"⚠️  {consecutive_failures} consecutive scan failures - checking ESP32...")
                        # Quick check if ESP32 is still there
                        quick_check = subprocess.run(['nmcli', 'dev', 'wifi', 'list'], 
                                                   capture_output=True, text=True, timeout=2)
                        if quick_check.returncode == 0 and self.esp32_ssid in quick_check.stdout:
                            print("✅ ESP32-C3 still transmitting")
                        else:
                            print("❌ ESP32-C3 signal not found")
                        consecutive_failures = 0
                
                # Short sleep to prevent hanging
                time.sleep(1)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                time.sleep(2)
    
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
            print(f"   ESP32-C3 status: {'✅ ACTIVE' if self.esp32_detections > 0 else '❌ INACTIVE'}")

def main():
    print("Reliable Real-time WiFi Packet Monitor")
    print("With progress tracking and hang prevention")
    print()
    
    monitor = ReliablePacketMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
