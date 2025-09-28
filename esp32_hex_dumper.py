#!/usr/bin/env python3

import subprocess
import time
import sys

def capture_esp32_packets():
    """Capture raw hex packets from any ESP32-like device in monitor mode"""
    
    interface = "wlx60e32717571c"
    timeout_seconds = 30
    
    print(f"Starting raw packet capture on interface {interface}")
    print("Looking for any WiFi packets (will show all)")
    print(f"Will run for {timeout_seconds} seconds maximum")
    print("-" * 60)
    
    try:
        # Use tshark to capture raw packets in monitor mode
        cmd = [
            "sudo", "tshark", 
            "-i", interface,
            "-T", "fields",
            "-e", "wlan.sa",  # Source MAC
            "-e", "frame.len",  # Frame length
            "-e", "data.data"  # Raw hex data
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        packet_count = 0
        start_time = time.time()
        
        while True:
            # Check if we've exceeded the timeout
            if time.time() - start_time > timeout_seconds:
                print(f"\nTimeout reached ({timeout_seconds} seconds). Stopping capture.")
                break
                
            line = process.stdout.readline()
            if not line:
                break
                
            line = line.strip()
            if not line:
                continue
                
            # Parse tshark output
            parts = line.split('\t')
            if len(parts) >= 3:
                source_mac = parts[0]
                frame_len = parts[1]
                hex_data = parts[2]
                
                packet_count += 1
                timestamp = time.strftime("%H:%M:%S.%f")[:-3]
                
                print(f"\n[{timestamp}] Packet #{packet_count}")
                print(f"Source MAC: {source_mac}")
                print(f"Frame Length: {frame_len} bytes")
                print(f"Raw Hex Data:")
                print(hex_data)
                print("-" * 40)
                
                # Flush output immediately
                sys.stdout.flush()
    
    except KeyboardInterrupt:
        print(f"\n\nCapture stopped. Total packets received: {packet_count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'process' in locals():
            process.terminate()

if __name__ == "__main__":
    capture_esp32_packets()


