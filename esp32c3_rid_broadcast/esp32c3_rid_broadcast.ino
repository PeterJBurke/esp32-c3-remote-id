/* -*- tab-width: 2; mode: c; -*-
 * 
 * ESP32-C3 Remote ID Broadcast Example
 * 
 * This sketch broadcasts Remote ID signals using WiFi beacon mode
 * on an ESP32-C3 Mini. It simulates a drone flying in a pattern around
 * Aldrich Park, Irvine, California.
 * 
 * Based on the uav_electronic_ids library by Steve Jack
 * 
 * Note: ESP32-C3 does not have Bluetooth, only WiFi is used.
 */

#include <Arduino.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <WiFi.h>

#include "id_open.h"

// Flight pattern waypoints - Aldrich Park, Irvine, California
#define WAYPOINTS 4
static double latitude[WAYPOINTS] = {
  33.6405,  // Waypoint 1 - Aldrich Park center
  33.6415,  // Waypoint 2 - North
  33.6415,  // Waypoint 3 - Northeast
  33.6405   // Waypoint 4 - East
};
static double longitude[WAYPOINTS] = {
  -117.8443,  // Waypoint 1 - Aldrich Park center
  -117.8443,  // Waypoint 2 - North
  -117.8453,  // Waypoint 3 - Northeast
  -117.8453   // Waypoint 4 - East
};

// RID objects
static ID_OpenDrone squitter;
static UTM_Utilities utm_utils;

// UTM data structures
static struct UTM_parameters utm_parameters;
static struct UTM_data utm_data;

// Flight simulation variables
static int waypoint = 0;
static int speed_kn = 25;  // Speed in knots
static float altitude_m = 50.0;  // Altitude in meters
static double deg2rad = 0.0;
static double m_deg_lat = 0.0, m_deg_long = 0.0;

// Debug variables
static uint32_t packet_count = 0;
static uint32_t last_debug_print = 0;

void setup() {
  char text[128];
  time_t time_2;
  struct tm clock_tm;
  struct timeval tv = {0,0};
  struct timezone utc = {0,0};
  
  // Print WiFi MAC address for debugging
  uint8_t mac[6];
  WiFi.macAddress(mac);
  Serial.printf("WiFi MAC: %02X:%02X:%02X:%02X:%02X:%02X\n", 
               mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
  
  // Scan WiFi networks to find the best channel
  Serial.println("Scanning WiFi networks...");
  int n = WiFi.scanNetworks();
  if (n == 0) {
    Serial.println("No networks found");
  } else {
    Serial.printf("Found %d networks:\n", n);
    for (int i = 0; i < n; ++i) {
      Serial.printf("%2d: %s (%d) %s\n", 
                   i + 1, 
                   WiFi.SSID(i).c_str(), 
                   WiFi.channel(i), 
                   (WiFi.encryptionType(i) == WIFI_AUTH_OPEN) ? "open" : "encrypted");
    }
  }
  
  Serial.begin(115200);
  delay(2000);  // Give more time for ESP32-C3 to initialize
  Serial.println("\n=== ESP32-C3 Remote ID Broadcast ===");
  Serial.println("Initializing...\n");
  
  // Calculate degrees to radians conversion
  deg2rad = (4.0 * atan(1.0)) / 180.0;
  
  // Set system time (you can modify this to current time)
  memset(&clock_tm, 0, sizeof(struct tm));
  clock_tm.tm_hour = 10;
  clock_tm.tm_mday = 27;
  clock_tm.tm_mon = 11;  // December (0-based)
  clock_tm.tm_year = 122; // 2022 (years since 1900)
  
  time_2 = mktime(&clock_tm);
  tv.tv_sec = time_2;
  settimeofday(&tv, &utc);
  
  Serial.print("Time set to: ");
  Serial.println(ctime(&time_2));
  
  // Configure UTM parameters
  memset(&utm_parameters, 0, sizeof(utm_parameters));
  
  // Set your operator ID (modify this!)
  strcpy(utm_parameters.UAS_operator, "TEST-OP-12345");
  
  // Set UAV ID
  strcpy(utm_parameters.UAV_id, "TEST-UAV-C3-001");
  
  // Set flight description
  strcpy(utm_parameters.flight_desc, "C3 Test Flight");
  
  // Region and classification
  utm_parameters.region = 1;        // 1 = Europe
  utm_parameters.EU_category = 1;   // Open category
  utm_parameters.EU_class = 5;      // Class 5 (under 25kg)
  utm_parameters.UA_type = 1;       // Aeroplane
  utm_parameters.ID_type = 1;       // Serial number
  
  // Initialize the RID transmitter
  squitter.init(&utm_parameters);
  Serial.println("RID transmitter initialized");
  
  // Set up flight data
  memset(&utm_data, 0, sizeof(utm_data));
  
  // Set base location (first waypoint) - Aldrich Park, Irvine, CA
  utm_data.base_latitude = latitude[0];
  utm_data.base_longitude = longitude[0];
  utm_data.base_alt_m = 50.0;  // Base altitude (Irvine is ~50m above sea level)
  utm_data.base_valid = 1;
  
  // Set initial position
  utm_data.latitude_d = latitude[0];
  utm_data.longitude_d = longitude[0];
  utm_data.alt_msl_m = utm_data.base_alt_m + altitude_m;
  utm_data.alt_agl_m = altitude_m;
  
  // Set flight parameters
  utm_data.speed_kn = speed_kn;
  utm_data.satellites = 12;  // Simulated GPS satellites
  utm_data.heading = 0;
  
  // Calculate meters per degree for this latitude
  utm_utils.calc_m_per_deg(utm_data.latitude_d, &m_deg_lat, &m_deg_long);
  
  // Print configuration
  Serial.println("\nConfiguration:");
  Serial.print("Board: ESP32-C3 Mini\n");
  Serial.print("WiFi Channel: ");
  Serial.println(WIFI_CHANNEL);
  Serial.print("Operator ID: ");
  Serial.println(utm_parameters.UAS_operator);
  Serial.print("UAV ID: ");
  Serial.println(utm_parameters.UAV_id);
  Serial.print("Base location: ");
  Serial.print(utm_data.base_latitude, 6);
  Serial.print(", ");
  Serial.println(utm_data.base_longitude, 6);
  Serial.print("Altitude: ");
  Serial.print(utm_data.alt_msl_m);
  Serial.println(" m MSL");
  Serial.print("Speed: ");
  Serial.print(utm_data.speed_kn);
  Serial.println(" knots");
  Serial.print("Meters per degree lat: ");
  Serial.println(m_deg_lat, 2);
  Serial.print("Meters per degree long: ");
  Serial.println(m_deg_long, 2);
  
  // Print WiFi status
  Serial.println("\nWiFi Status:");
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  Serial.print("Channel: ");
  Serial.println(WiFi.channel());
  Serial.print("Status: ");
  Serial.println(WiFi.status() == WL_CONNECTED ? "Connected" : "Disconnected");
  
  Serial.println("\nStarting RID broadcast...");
  Serial.println("Look for WiFi network: 'OpenDroneID_XXXXXX'");
  Serial.println("Use a Remote ID scanner app to detect the signal");
  Serial.println("Note: ESP32-C3 only supports WiFi, no Bluetooth");
  Serial.println("\n=== DEBUG MODE: Printing every RID packet transmission ===\n");
  
  // Seed random number generator
  srand(micros());
}

void loop() {
  static uint32_t last_update = 0, last_waypoint = 0, last_status = 0;
  static int waypoint_counter = 0;
  uint32_t msecs = millis();
  char text[64];
  
  // Change waypoint every 10 seconds
  if ((msecs - last_waypoint) > 10000) {
    last_waypoint = msecs;
    
    // Move to next waypoint
    waypoint_counter = (waypoint_counter + 1) % WAYPOINTS;
    waypoint = waypoint_counter;
    
    utm_data.latitude_d = latitude[waypoint];
    utm_data.longitude_d = longitude[waypoint];
    
    // Calculate heading to next waypoint
    int next_waypoint = (waypoint + 1) % WAYPOINTS;
    double lat1 = latitude[waypoint] * deg2rad;
    double lon1 = longitude[waypoint] * deg2rad;
    double lat2 = latitude[next_waypoint] * deg2rad;
    double lon2 = longitude[next_waypoint] * deg2rad;
    
    double dlon = lon2 - lon1;
    double y = sin(dlon) * cos(lat2);
    double x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon);
    utm_data.heading = (int)(atan2(y, x) * 180.0 / M_PI + 360.0) % 360;
    
    // Print waypoint info
    Serial.print("\nWaypoint ");
    Serial.print(waypoint);
    Serial.print(": ");
    Serial.print(utm_data.latitude_d, 6);
    Serial.print(", ");
    Serial.print(utm_data.longitude_d, 6);
    Serial.print(" (heading: ");
    Serial.print(utm_data.heading);
    Serial.println("°)");
  }
  
  // Transmit RID data every 1000ms (1Hz) - ASTM F3411-19 standard
  if ((msecs - last_update) >= 1000) {
    last_update = msecs - (msecs % 1000);  // Align to 1-second boundary
    
    // Update time
    time_t time_2;
    time(&time_2);
    struct tm* gmt = gmtime(&time_2);
    utm_data.seconds = gmt->tm_sec;
    utm_data.minutes = gmt->tm_min;
    utm_data.hours = gmt->tm_hour;
    
    // Print status every 5 seconds
    if ((msecs - last_status) >= 5000) {
      last_status = msecs;
      Serial.print("\nWiFi Status: ");
      Serial.print(WiFi.status() == WL_CONNECTED ? "Connected" : "Disconnected");
      Serial.print(", Channel: ");
      Serial.print(WiFi.channel());
      Serial.print(", RSSI: ");
      Serial.print(WiFi.RSSI());
      Serial.print(" dBm, Packets: ");
      Serial.println(packet_count);
    }
    
    // Transmit RID data
    squitter.transmit(&utm_data);
    packet_count++;
    
    // Debug: Print every packet transmission (every 1000ms)
    Serial.print("📡 TX #");
    Serial.print(packet_count);
    Serial.print(" | Time: ");
    if (utm_data.hours < 10) Serial.print("0");
    Serial.print(utm_data.hours);
    Serial.print(":");
    if (utm_data.minutes < 10) Serial.print("0");
    Serial.print(utm_data.minutes);
    Serial.print(":");
    if (utm_data.seconds < 10) Serial.print("0");
    Serial.print(utm_data.seconds);
    Serial.print(" | Pos: ");
    Serial.print(utm_data.latitude_d, 4);
    Serial.print(",");
    Serial.print(utm_data.longitude_d, 4);
    Serial.print(" | Alt: ");
    Serial.print(utm_data.alt_agl_m, 0);
    Serial.print("m | Hdg: ");
    Serial.print(utm_data.heading);
    Serial.print("° | Speed: ");
    Serial.print(utm_data.speed_kn);
    Serial.println("kn");
    
    // Print summary every 5 seconds
    static uint32_t last_status = 0;
    if ((msecs - last_status) > 5000) {
      last_status = msecs;
      Serial.print("\n📊 SUMMARY: ");
      Serial.print(packet_count);
      Serial.print(" packets transmitted | Rate: ");
        Serial.print(1.0, 1);  // 1000ms = 1Hz
      Serial.print(" Hz | Uptime: ");
      Serial.print(msecs / 1000);
      Serial.println(" seconds\n");
    }
  }
}
