# ESP32-C3 Remote ID (OpenDroneID) Project

This project implements Remote ID (RID) broadcasting on an ESP32-C3 Mini 1 development board, compliant with ASTM F3411-19 standard for drone identification.

**Note**: This is a fork/extension of the [uav_electronic_ids](https://github.com/sxjack/uav_electronic_ids) project, with additional monitoring tools and ESP32-C3 specific implementations.

## 🎯 Project Overview

- **Hardware**: ESP32-C3 Mini 1 Dev Board
- **Protocol**: Remote ID via WiFi Beacon Frames
- **Standard**: ASTM F3411-19 (OpenDroneID)
- **Flight Simulation**: 4-waypoint pattern around Aldrich Park, UCI

## 📡 Key Features

- **Real-time RID Broadcasting**: Transmits drone identification data via WiFi beacons
- **Waypoint Navigation**: Simulates flight through predefined coordinates
- **Dual Packet Types**: Basic (184 bytes) and Extended (234 bytes) RID data
- **Monitor Mode Capture**: Python scripts for packet analysis and timing measurement

## 🛠️ Hardware Setup

### ESP32-C3 Configuration
- **Board**: ESP32-C3 Mini 1
- **USB Connection**: USB-C cable
- **Programming**: Arduino IDE or Arduino CLI
- **Libraries**: OpenDroneID, UTM conversion

### Upload Process
1. Hold BOOT button while connecting USB
2. Upload sketch via Arduino CLI
3. Monitor serial output at 115200 baud

## 🗺️ Flight Path

**Location**: Aldrich Park, UC Irvine, California

**Waypoints**:
1. **Center**: 33.6405°N, 117.8443°W (Aldrich Park center)
2. **North**: 33.6415°N, 117.8443°W 
3. **Northeast**: 33.6415°N, 117.8453°W
4. **East**: 33.6405°N, 117.8453°W

**Flight Pattern**: Square pattern, 10-second intervals between waypoints

## 📊 Transmission Analysis

### Packet Timing Results
- **Variable Intervals**: 0.5s to 9.0s between packets
- **Average Rate**: ~0.32 packets/second
- **Packet Sizes**: 184 bytes (basic) / 234 bytes (extended)

### RID Data Contents
- **Operator ID**: "TEST-OP-12345"
- **UAV ID**: "TEST-UAV-C3-001"
- **Operation Type**: Recreational
- **Real-time Position**: Updates based on waypoint navigation

## 🔍 Monitoring Tools

### Python Scripts
- `packet_timing_monitor.py`: Measures packet intervals
- `beacon_hex_dumper.py`: Captures raw hex packet data
- `timed_packet_dumper.py`: Human-readable packet display
- `rid_packet_decoder.py`: Decodes all RID fields

### WiFi Monitoring
- **Interface**: Monitor mode required (`wlx60e32717571c`)
- **Target MAC**: `84:fc:e6:00:fc:04`
- **Tools**: tshark, Python/Scapy, nmcli

## 🚀 Quick Start

### 1. Arduino Setup
```bash
# Install ESP32 board package
arduino-cli core install esp32:esp32@2.0.11

# Compile and upload
cd esp32c3_rid_broadcast
arduino-cli compile --fqbn esp32:esp32:esp32c3:CDCOnBoot=cdc .
arduino-cli upload --fqbn esp32:esp32:esp32c3:CDCOnBoot=cdc -p /dev/ttyACM0 .
```

### 2. Monitor Packets
```bash
# Real-time packet timing
python3 packet_timing_monitor.py

# Raw hex dump
python3 beacon_hex_dumper.py

# Human-readable display
python3 timed_packet_dumper.py
```

### 3. WiFi Analysis
```bash
# Scan for RID networks
nmcli dev wifi list | grep "TEST-OP"

# Capture with tshark
tshark -i wlx60e32717571c -f "wlan type mgt subtype beacon and ether src 84:fc:e6:00:fc:04"
```

## 📋 Requirements

### Hardware
- ESP32-C3 Mini 1 Development Board
- USB-C cable
- WiFi adapter with monitor mode support

### Software
- Arduino CLI or Arduino IDE
- Python 3.x
- tshark/Wireshark
- Libraries: OpenDroneID, UTM

### Python Dependencies
```bash
pip install scapy subprocess datetime
```

## 🔧 Troubleshooting

### Common Issues
- **Upload Failure**: Hold BOOT button during upload
- **Compilation Error**: Use ESP32 core version 2.0.11
- **No Packets**: Check WiFi interface in monitor mode
- **Permission Denied**: Add user to wireshark group

### Debugging
- Serial monitor: `arduino-cli monitor -p /dev/ttyACM0`
- Check USB device: `lsusb | grep ESP32`
- WiFi scan: `nmcli dev wifi list`

## 📈 Performance Metrics

- **Transmission Range**: ~100m typical
- **Update Rate**: Variable (0.5-9 second intervals)
- **Data Types**: Position, velocity, heading, operator info
- **Compliance**: ASTM F3411-19 Remote ID standard

## 🔬 Technical Details

### RID Implementation
- **Beacon Frames**: IEEE 802.11 management frames
- **Vendor IE**: OpenDroneID information elements
- **SSID Encoding**: Operator ID in network name
- **Payload**: Binary RID data in beacon body

### Coordinate System
- **Format**: WGS84 decimal degrees
- **Precision**: 6 decimal places (~0.1m accuracy)
- **Altitude**: MSL (Mean Sea Level) + AGL (Above Ground Level)

## 🔐 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
# ESP32-C3 MAC Addresses
ESP32_MAC_PRIMARY=84:fc:e6:00:fc:04
ESP32_MAC_SECONDARY=84:fc:e6:00:fc:05

# WiFi Monitor Interface  
WIFI_MONITOR_INTERFACE=wlx60e32717571c

# Geographic Coordinates (customize for your location)
WAYPOINT_1_LAT=33.6405
WAYPOINT_1_LON=-117.8443
```

**Note**: The `.env` file contains sensitive information like MAC addresses and coordinates. Never commit this file to version control.

## 📄 License

This project is a fork/extension of [uav_electronic_ids](https://github.com/sxjack/uav_electronic_ids) and uses the OpenDroneID library. It follows ASTM F3411-19 specifications for educational and testing purposes.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the Remote ID implementation or monitoring tools.
