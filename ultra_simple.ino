// Ultra-simple ESP32-C3 test - no WiFi, no complex features
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=== ESP32-C3 ULTRA SIMPLE TEST ===");
  Serial.println("This should work without event loop issues");
}

void loop() {
  Serial.println("Hello from ESP32-C3!");
  delay(1000);
}
