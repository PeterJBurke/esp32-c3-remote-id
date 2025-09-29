// Simple ESP32-C3 blink sketch to test basic functionality
#define LED_PIN 2  // Built-in LED on ESP32-C3

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("ESP32-C3 Blink Test Starting...");
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED ON");
  delay(1000);

  digitalWrite(LED_PIN, LOW);
  Serial.println("LED OFF");
  delay(1000);
}
