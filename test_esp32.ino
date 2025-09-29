void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("ESP32-C3 Test Sketch");
  Serial.println("If you see this, the board is working!");
}

void loop() {
  Serial.println("Hello from ESP32-C3!");
  delay(1000);
}
