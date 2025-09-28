#!/usr/bin/env python3

import subprocess
import sys
import time
import signal

class BeaconHexDumper:
    def __init__(self):
        self.interface = "wlx60e32717571c"
        self.target_mac = "84:fc:e6:00:fc:04"  # ESP32-C3 MAC as requested
        self.debug = True  # Show all MACs for debugging
        self.packet_count = 0
        self.start_time = time.time()
        
    def signal_handler(self, signum, frame):
        print(f"\n\n⏰ Timeout reached (30 seconds)")
        print(f"📊 Total packets captured: {self.packet_count}")
        sys.exit(0)
        
    def run(self):
        print(f"🔍 Capturing WiFi beacon packets from {self.target_mac}")
        print(f"📡 Interface: {self.interface}")
        print(f"⏱️  Timeout: 30 seconds")
        print(f"📋 Format: MAC | Frame Length | Raw Hex Data")
        print("=" * 80)
        
        # Set up timeout signal
        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(30)  # 30 second timeout
        
        try:
            # Run tshark to capture beacon packets
            cmd = [
                "tshark",
                "-i", self.interface,
                "-f", "wlan type mgt subtype beacon",
                "-T", "fields",
                "-e", "wlan.sa",
                "-e", "frame.len", 
                "-e", "data.data"
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split('\t')
                if len(parts) >= 3:
                    mac = parts[0]
                    frame_len = parts[1]
                    hex_data = parts[2] if len(parts) > 2 else ""
                    
                    # Debug: show all MACs being detected
                    if self.debug:
                        if mac.startswith("84:fc:e6"):
                            print(f"🔍 ESP32 MAC detected: {mac}")
                    
                    # Filter for our target MAC
                    if mac.lower() == self.target_mac.lower():
                        self.packet_count += 1
                        elapsed = time.time() - self.start_time
                        
                        print(f"\n📦 PACKET #{self.packet_count} (t={elapsed:.1f}s)")
                        print(f"🎯 MAC: {mac}")
                        print(f"📏 Length: {frame_len} bytes")
                        print(f"🔢 Raw Hex: {hex_data}")
                        print("-" * 60)
                        
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            signal.alarm(0)  # Cancel the alarm
            print(f"\n📊 Total packets captured: {self.packet_count}")

if __name__ == "__main__":
    dumper = BeaconHexDumper()
    dumper.run()
