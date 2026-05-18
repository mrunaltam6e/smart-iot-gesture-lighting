const int ledPins[] = {9, 10, 11, 12, 13};  // LED pins
const int numLeds = 5;  // Total number of LEDs

void setup() {
  Serial.begin(9600);
  
  // Set all LED pins as outputs
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    int receivedNumber = Serial.parseInt();
    
    // Turn off all LEDs first
    for (int i = 0; i < numLeds; i++) {
      digitalWrite(ledPins[i], LOW);
    }
    
    // Light up LEDs based on received number
    for (int i = 0; i < receivedNumber && i < numLeds; i++) {
      digitalWrite(ledPins[i], HIGH);
    }
  }
}