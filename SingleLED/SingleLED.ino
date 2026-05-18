// Arduino Uno LED Control Code

// Define the LED pins
const int redPin = 9;
const int greenPin = 10;
const int bluePin = 11;
const int yellowPin = 12;
const int whitePin = 13;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Set LED pins as output
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(yellowPin, OUTPUT);
  pinMode(whitePin, OUTPUT);
  
  // Ensure all LEDs are initially off
  digitalWrite(redPin, LOW);
  digitalWrite(greenPin, LOW);
  digitalWrite(bluePin, LOW);
  digitalWrite(yellowPin, LOW);
  digitalWrite(whitePin, LOW);
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming number
    int receivedNumber = Serial.parseInt();
    
    // Turn off all LEDs first
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, LOW);
    digitalWrite(bluePin, LOW);
    digitalWrite(yellowPin, LOW);
    digitalWrite(whitePin, LOW);
    
    // Turn on the corresponding LED based on the received number
    switch(receivedNumber) {
      case 1:
        digitalWrite(redPin, HIGH);
        break;
      case 2:
        digitalWrite(greenPin, HIGH);
        break;
      case 3:
        digitalWrite(bluePin, HIGH);
        break;
      case 4:
        digitalWrite(yellowPin, HIGH);
        break;
      case 5:
        digitalWrite(whitePin, HIGH);
        break;
      default:
        // If number is not 1-5, all LEDs remain off
        break;
    }
  }
}