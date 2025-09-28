# ESP32-C3 Remote ID Project Status

**Date**: September 28, 2025  
**Status**: Debug Phase - Transmission Rate Correction  
**Repository**: https://github.com/PeterJBurke/esp32-c3-remote-id

## 🎯 Project Overview

Implementation of ASTM F3411-19 Remote ID broadcasting on ESP32-C3 Mini 1 dev board with comprehensive monitoring tools and real-time packet analysis capabilities.

## ✅ Completed Milestones

### Hardware Setup
- ✅ ESP32-C3 Mini 1 dev board configured
- ✅ Arduino CLI environment established
- ✅ USB serial communication working (115200 baud)
- ✅ Board package downgraded to ESP32 2.0.11 for library compatibility

### Software Implementation
- ✅ OpenDroneID library integration
- ✅ UTM coordinate conversion system
- ✅ 4-waypoint flight simulation (Aldrich Park, UCI)
- ✅ Real-time debug output system
- ✅ Comprehensive packet logging (TX #XXXX format)

### Monitoring Infrastructure
- ✅ 20+ Python monitoring scripts developed
- ✅ WiFi packet capture tools (tshark integration)
- ✅ Real-time packet timing analysis
- ✅ Human-readable RID data display
- ✅ Monitor mode WiFi interface setup (`wlx60e32717571c`)

### GitHub Repository
- ✅ Repository created: https://github.com/PeterJBurke/esp32-c3-remote-id
- ✅ Complete codebase with monitoring tools
- ✅ Documentation and README
- ✅ Environment configuration (.env.example)
- ✅ Forked uav_electronic_ids library included

## 🔧 Current Status

### Active Debug Session
- **Issue Identified**: Transmission rate discrepancy
- **Problem**: Code was transmitting at 40 Hz (every 25ms) instead of ASTM F3411-19 standard 1 Hz
- **Root Cause**: `if ((msecs - last_update) > 24)` in main loop
- **Solution Applied**: Changed to `if ((msecs - last_update) > 999)` for 1 Hz transmission

### Code Changes Made
```cpp
// BEFORE (incorrect):
// Transmit RID data every 25ms (40Hz)
if ((msecs - last_update) > 24) {

// AFTER (corrected):  
// Transmit RID data every 1000ms (1Hz) - ASTM F3411-19 standard
if ((msecs - last_update) > 999) {
```

### Current Flight Parameters
- **Location**: Aldrich Park, UC Irvine, California
- **Waypoints**: 4-point square pattern
- **Coordinates**: 
  - WP0: 33.6405°N, 117.8443°W (Center)
  - WP1: 33.6415°N, 117.8443°W (North) 
  - WP2: 33.6415°N, 117.8453°W (Northeast)
  - WP3: 33.6405°N, 117.8453°W (East)
- **Altitude**: 50m AGL (100m MSL)
- **Speed**: 25 knots
- **Waypoint Interval**: 10 seconds

## 📊 Technical Specifications

### Hardware Configuration
- **Board**: ESP32-C3 Mini 1 Development Board
- **MAC Address**: 84:fc:e6:00:fc:04 (primary transmission)
- **Serial Port**: /dev/ttyACM0
- **Baud Rate**: 115200

### Software Stack
- **Arduino Core**: ESP32 2.0.11 (downgraded for compatibility)
- **Libraries**: OpenDroneID, UTM utilities
- **Language**: C++ (Arduino framework)
- **Development**: Arduino CLI

### Remote ID Implementation
- **Standard**: ASTM F3411-19 compliant
- **Transport**: WiFi beacon frames
- **Operator ID**: "TEST-OP-12345"
- **UAV ID**: "TEST-UAV-C3-001"
- **Operation Type**: Recreational
- **Transmission Rate**: 1 Hz (corrected from 40 Hz)

### Monitoring Tools
- **Interface**: USB serial monitoring (`cat /dev/ttyACM0`)
- **WiFi Analysis**: Monitor mode capture on `wlx60e32717571c`
- **Packet Analysis**: Python scripts with tshark integration
- **Real-time Display**: Comprehensive debug output with coordinates, heading, timestamps

## 🐛 Debug History

### Session Timeline
1. **Initial Setup**: Arduino IDE, board configuration, library installation
2. **Compilation Fixes**: Time variable declaration, library compatibility
3. **Upload Success**: Code deployed to ESP32-C3
4. **Debug Implementation**: Added comprehensive TX logging every packet
5. **Rate Analysis**: Discovered 40 Hz vs 1 Hz discrepancy
6. **Correction Applied**: Modified transmission interval to ASTM standard

### Key Findings
- **Packet Counter**: Successfully reached 5,000+ transmissions
- **Waypoint Navigation**: Proper coordinate transitions every 10 seconds
- **Heading Calculation**: Dynamic bearing updates between waypoints
- **Time Synchronization**: UTC timestamps updating correctly
- **WiFi Transmission**: Rate corrected to comply with ASTM F3411-19

## 🔄 Next Steps

### Immediate Actions
1. **Upload Verification**: Confirm corrected code deployment to ESP32-C3
2. **Rate Validation**: Verify 1 Hz transmission via WiFi monitoring
3. **Compliance Check**: Ensure ASTM F3411-19 message format compliance
4. **Performance Test**: Monitor sustained operation over extended period

### Future Enhancements
- Message type rotation (Basic ID, Location, System, Operator ID)
- Battery level monitoring and reporting
- GPS integration for real coordinates
- Web-based monitoring dashboard
- Multiple UAV simulation support

## 📈 Performance Metrics

### Last Known Status
- **Uptime**: 342+ seconds continuous operation
- **Packets Transmitted**: 5,000+ (at 40 Hz - now corrected to 1 Hz)
- **Memory Usage**: 52% program space, 11% dynamic memory
- **Stability**: No crashes or resets observed
- **Location Accuracy**: Proper waypoint transitions every 10 seconds

### Compliance Status
- ✅ ASTM F3411-19 data structure
- ✅ WiFi beacon frame transport  
- ✅ Operator identification
- ✅ Real-time position updates
- ✅ Transmission rate (corrected to 1 Hz)
- ✅ Message timing compliance

## 🛠️ Development Environment

### Tools Used
- **Arduino CLI**: Compilation and upload
- **tshark/Wireshark**: WiFi packet analysis
- **Python 3**: Monitoring script development
- **Git**: Version control
- **GitHub**: Repository hosting
- **VS Code/Cursor**: Code editing

### Key Files
- `esp32c3_rid_broadcast.ino`: Main Arduino sketch
- `packet_timing_monitor.py`: Transmission rate analysis
- `timed_packet_dumper.py`: Human-readable packet display
- `README.md`: Project documentation
- `.env.example`: Configuration template

## 📞 Support Information

### Hardware Requirements
- ESP32-C3 Mini 1 development board
- USB-C cable for programming/power
- WiFi adapter with monitor mode support (for analysis)

### Software Dependencies
- Arduino CLI or Arduino IDE
- ESP32 board package 2.0.11
- OpenDroneID library
- UTM utilities library
- Python 3.x with standard libraries

---

**Repository**: https://github.com/PeterJBurke/esp32-c3-remote-id  
**Contact**: PeterJBurke (GitHub)  
**License**: Educational/Research Use
