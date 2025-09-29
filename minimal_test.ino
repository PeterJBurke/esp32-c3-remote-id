// Minimal ESP32-C3 test sketch to isolate the issue
void setup() {
  Serial.begin(115200);
  delay(1000);  // Give serial time to initialize
  Serial.println("=== ESP32-C3 Minimal Test ===");

  // Test basic functionality without WiFi
  Serial.println("Testing basic functions...");

  // Just test Serial output
  for(int i = 0; i < 5; i++) {
    Serial.print("Test message ");
    Serial.println(i);
    delay(500);
  }

  Serial.println("Basic test complete");
}

void loop() {
  Serial.println("Loop running...");
  delay(2000);
}
