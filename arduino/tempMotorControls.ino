const int MOTOR_PIN = 5;
const int MOTOR_SPEED_STOP = 1;
const int MOTOR_SPEED_GO = 150; // between 0 (stopped) and 255 (full speed)

void setup() {
  Serial.begin(115200);
  pinMode(MOTOR_PIN, OUTPUT); // motor pin is an output
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read data until newline character
    parseCommand(command);
  }
}

void parseCommand(String command) {
  if (command == "<FORWARD>") {
    Serial.println("Moving forward");
    moveForward();
  } else if (command == "<STOP>") {
    Serial.println("Stopping");
    stop();
  }
}

void moveForward() {
  analogWrite(MOTOR_PIN, MOTOR_SPEED_GO);
}

void stop() {
  analogWrite(MOTOR_PIN, MOTOR_SPEED_STOP);
}
