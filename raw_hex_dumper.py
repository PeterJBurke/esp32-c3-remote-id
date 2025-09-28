#!/usr/bin/env python3

import subprocess
import re
import time
import sys

def capture_raw_packets():
    """Capture raw hex packets from ESP32-C3 in monitor mode"""
    
    target_mac = "84:FC:E6:00:FC:04"
    interface = "wlx60e32717571c"
    timeout_seconds = 30
    
    print(f"Starting raw packet capture on interface {interface}")
    print(f"Looking for packets from MAC: {target_mac}")
    print(f"Will run for {timeout_seconds} seconds maximum")
    print("-" * 60)
    
    try:
        # Use tshark to capture WiFi beacon packets in monitor mode
        cmd = [
            "sudo", "tshark", 
            "-i", interface,
            "-f", "wlan type mgt subtype beacon",  # Filter for beacon packets only
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
                
                # Check if this is from our target MAC
                if source_mac.lower() == target_mac.lower():
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
    capture_raw_packets()
