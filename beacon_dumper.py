#!/usr/bin/env python3

import subprocess
import time
import sys

def capture_all_beacons():
    """Capture all WiFi beacon packets to see what's available"""
    
    interface = "wlx60e32717571c"
    timeout_seconds = 30
    
    print(f"Starting beacon capture on interface {interface}")
    print("Capturing ALL beacon packets")
    print(f"Will run for {timeout_seconds} seconds maximum")
    print("-" * 60)
    
    try:
        # Use tshark to capture all beacon packets
        cmd = [
            "sudo", "tshark", 
            "-i", interface,
            "-f", "wlan type mgt subtype beacon",
            "-T", "fields",
            "-e", "wlan.sa",  # Source MAC
            "-e", "wlan.ssid",  # SSID
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
        mac_addresses = set()
        
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
            if len(parts) >= 4:
                source_mac = parts[0]
                ssid = parts[1]
                frame_len = parts[2]
                hex_data = parts[3]
                
                mac_addresses.add(source_mac)
                packet_count += 1
                timestamp = time.strftime("%H:%M:%S.%f")[:-3]
                
                print(f"\n[{timestamp}] Beacon #{packet_count}")
                print(f"Source MAC: {source_mac}")
                print(f"SSID: {ssid}")
                print(f"Frame Length: {frame_len} bytes")
                print(f"Raw Hex Data: {hex_data[:100]}...")
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
    
    print(f"\nUnique MAC addresses seen: {len(mac_addresses)}")
    for mac in sorted(mac_addresses):
        print(f"  {mac}")

if __name__ == "__main__":
    capture_all_beacons()


