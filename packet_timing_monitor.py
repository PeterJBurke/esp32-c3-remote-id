#!/usr/bin/env python3

import subprocess
import sys
import time
import signal
from datetime import datetime

class PacketTimingMonitor:
    def __init__(self):
        self.interface = "wlx60e32717571c"
        self.target_mac = "84:fc:e6:00:fc:04"
        self.packet_count = 0
        self.start_time = time.time()
        self.last_packet_time = None
        
    def signal_handler(self, signum, frame):
        print(f"\n\n⏰ Timeout reached (30 seconds)")
        print(f"📊 Total packets captured: {self.packet_count}")
        if self.packet_count > 1:
            avg_interval = 30.0 / (self.packet_count - 1) if self.packet_count > 1 else 0
            print(f"📈 Average packet interval: {avg_interval:.2f} seconds")
        sys.exit(0)
        
    def run(self):
        print(f"⏱️  Monitoring packet timing from ESP32-C3")
        print(f"🎯 MAC: {self.target_mac}")
        print(f"📡 Interface: {self.interface}")
        print(f"⏲️  Timeout: 30 seconds")
        print("=" * 80)
        
        # Set up timeout signal
        signal.signal(signal.SIGALRM, self.signal_handler)
        signal.alarm(30)  # 30 second timeout
        
        try:
            # Run tshark to capture beacon packets with timestamps
            cmd = [
                "tshark",
                "-i", self.interface,
                "-f", "wlan type mgt subtype beacon",
                "-T", "fields",
                "-e", "frame.time_epoch",
                "-e", "wlan.sa",
                "-e", "frame.len"
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split('\t')
                if len(parts) >= 3:
                    timestamp_str = parts[0]
                    mac = parts[1]
                    frame_len = parts[2]
                    
                    # Filter for our target MAC
                    if mac.lower() != self.target_mac.lower():
                        continue
                    
                    try:
                        current_time = float(timestamp_str)
                        current_datetime = datetime.fromtimestamp(current_time)
                        
                        self.packet_count += 1
                        elapsed = current_time - self.start_time
                        
                        # Calculate time since last packet
                        if self.last_packet_time is not None:
                            interval = current_time - self.last_packet_time
                            interval_str = f"{interval:.3f}s"
                        else:
                            interval_str = "---"
                        
                        print(f"📦 Packet #{self.packet_count:2d} | "
                              f"Time: {current_datetime.strftime('%H:%M:%S.%f')[:-3]} | "
                              f"Interval: {interval_str:>8} | "
                              f"Length: {frame_len:>3} bytes | "
                              f"Elapsed: {elapsed:6.1f}s")
                        
                        self.last_packet_time = current_time
                        
                    except ValueError as e:
                        print(f"❌ Error parsing timestamp: {e}")
                        
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            signal.alarm(0)  # Cancel the alarm
            print(f"\n📊 Final Statistics:")
            print(f"   • Total packets: {self.packet_count}")
            if self.packet_count > 1:
                total_time = self.last_packet_time - (self.start_time + (time.time() - self.start_time - 30))
                avg_interval = 30.0 / (self.packet_count - 1) if self.packet_count > 1 else 0
                print(f"   • Average interval: {avg_interval:.3f} seconds")
                estimated_rate = 1.0 / avg_interval if avg_interval > 0 else 0
                print(f"   • Estimated rate: {estimated_rate:.2f} packets/second")

if __name__ == "__main__":
    monitor = PacketTimingMonitor()
    monitor.run()
