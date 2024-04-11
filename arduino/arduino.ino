/*
 * TODOS:
 *  - Add the rest of the ultrasonic sensors - update fn to take in a pin (?) and return distance
 *  - Add tactile sensor fn
 *  - Add brake fn (confirm pin 25? other pin?)
 *  - Add linear actuators fn (implement stop?)
 *  - Confirm motor pins (L/R, forward/back should match)
 *  - Double check turn logic..
 */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_GPS.h>
#include <Adafruit_AHTX0.h>

// define pins
#define GPS_SERIAL Serial3 // set GPS_SERIAL port to 3 (pins 14,15)
const int MOTOR_L_FORWARD_PIN = 5;
const int MOTOR_R_FORWARD_PIN = 6;
const int MOTOR_L_REVERSE_PIN = 35;
const int MOTOR_R_REVERSE_PIN = 37;
const int ULTRASONIC_TRIG_PIN_1 = 48;
const int ULTRASONIC_ECHO_PIN_1 = 50;
const int HEADLIGHTS_PIN = 31;
const int LINEAR_ACUTATOR_PIN_1 = 27;
const int LINEAR_ACUTATOR_PIN_2 = 29;
const int T_RELAY_PIN = 35;
const int R_RELAY_PIN = 37;
const int E_RELAY_PIN = 39;

// TODO update
const int TACTILE_BTN_FRONT = 4;
const int TACTILE_BTN_BACK = 4;
const int TACTILE_BTN_LEFT = 4;
const int TACTILE_BTN_RIGHT = 4;

// settings
const int ULTRASONIC_THRESHOLD = 12; // cm that the ultrasonic sensors will alert
const int MOTOR_SPEED_STOP = 50;
const int MOTOR_SPEED_GO = 200; // between 0 (stopped) and 255 (full speed)
const int MOTOR_SPEED_TURN = 150;
const bool GPS_ECHO = false; // turn off echoing the GPS data to the Serial console


// Initialize the AHT20 sensor
Adafruit_AHTX0 tempSensor;
// Initialize the ADXL345 sensor
Adafruit_ADXL345_Unified accelerometerSensor = Adafruit_ADXL345_Unified();
// Pointer for the temperature sensor
Adafruit_Sensor *tempSensorPointer;
// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPS_SERIAL);

void setup() {
    Serial.begin(115200);

    // relays
    pinMode(T_RELAY_PIN, OUTPUT);
    pinMode(R_RELAY_PIN, OUTPUT);
    pinMode(E_RELAY_PIN, OUTPUT);

    // motor pins
    pinMode(MOTOR_R_FORWARD_PIN, OUTPUT);
    pinMode(MOTOR_L_FORWARD_PIN, OUTPUT);

    // headlights
    pinMode(HEADLIGHTS_PIN, OUTPUT);

    // linear actuators
    pinMode(LINEAR_ACUTATOR_PIN_1, OUTPUT);
    pinMode(LINEAR_ACUTATOR_PIN_2, OUTPUT);

    // ultrasonics
    pinMode(ULTRASONIC_TRIG_PIN_1, OUTPUT);
    pinMode(ULTRASONIC_ECHO_PIN_1, INPUT);

    // Check AHT20 is alive
    if (!tempSensor.begin()) {
        Serial.println("Could not find AHT :(");
        while (1) {
            delay(10);
        }
    }

    tempSensorPointer = tempSensor.getTemperatureSensor();
    tempSensorPointer->printSensorDetails();

    // Check ADXL345 is alive
    if (!accelerometerSensor.begin()) {
        Serial.println("No ADXL345 sensor detected :(");
        while (1);
    }

    // GPS setup
    GPS.begin(9600);
    GPS.sendCommand(PMTK_SET_BAUD_9600 "$PMTK251,9600*17");
    // Uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
    GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
    // uncomment this line to turn on only the "minimum recommended" data
    //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
    // For parsing data, we don't suggest using anything but either RMC only or RMC+GGA since
    // the parser doesn't care about other sentences at this time
    // Set the update rate
    GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate

    // Request updates on antenna status, comment out to keep quiet
    GPS.sendCommand(PGCMD_ANTENNA);
    delay(1000);

    // Ask for firmware version
    GPS_SERIAL.println(PMTK_Q_RELEASE);
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n'); // Read data until newline character
        parseCommand(command);
    }
}

void parseCommand(String command) {
    Serial.println(command);
    if (command == "<FORWARD>") {
        Serial.println("From dino: moving forward");
        moveForward();
    } else if (command == "<REVERSE>") {
        Serial.println("From dino: reversing");
        reverse();
    } else if (command == "<RIGHT>") {
        Serial.println("From dino: turning right");
        turnRight();
    } else if (command == "<LEFT>") {
        Serial.println("From dino: turning left");
        turnLeft();
    } else if (command == "<FORWARD_RIGHT>") {
        Serial.println("From dino: moving forward right");
        forwardRight();
    } else if (command == "<FORWARD_LEFT>") {
        Serial.println("From dino: moving forward left");
        forwardLeft();
    } else if (command == "<REVERSE_RIGHT>") {
        Serial.println("From dino: moving reverse right");
        reverseRight();
    } else if (command == "<REVERSE_LEFT>") {
        Serial.println("From dino: moving reverse left");
        reverseLeft();
    } else if (command == "<STOP>") {
        Serial.println("From dino: stopping");
        stop();
    } else if (command == "<TELEMETRY>") {
        Serial.println("From dino: getting telemetry");
        getTelemetry();
    } else if (command == "<HEADLIGHTS_ON>") {
        Serial.println("From dino: turning headlights on");
        turnOnHeadlights();
    } else if (command == "<HEADLIGHTS_OFF>") {
        Serial.println("From dino: turning headlights off");
        turnOffHeadlights();
    } else if (command == "<OPEN>") {
        Serial.println("From dino: opening door");
        openDoor();
    } else if (command == "<CLOSE>") {
        Serial.println("From dino: closing door");
        closeDoor();
    } else {
        Serial.println("From dino: idk what to do! :(");
    }
}

void moveForward() {
    analogWrite(MOTOR_R_FORWARD_PIN, MOTOR_SPEED_GO);
    analogWrite(MOTOR_L_FORWARD_PIN, MOTOR_SPEED_GO);
}

void reverse() {
    analogWrite(MOTOR_R_REVERSE_PIN, MOTOR_SPEED_TURN);
    analogWrite(MOTOR_L_REVERSE_PIN, MOTOR_SPEED_TURN);
}

void turnRight() {
    analogWrite(MOTOR_R_REVERSE_PIN, MOTOR_SPEED_TURN);
    analogWrite(MOTOR_L_FORWARD_PIN, MOTOR_SPEED_TURN);
}

void turnLeft() {
    analogWrite(MOTOR_R_FORWARD_PIN, MOTOR_SPEED_TURN);
    analogWrite(MOTOR_L_REVERSE_PIN, MOTOR_SPEED_TURN);
}

void forwardRight() {
    analogWrite(MOTOR_R_FORWARD_PIN, MOTOR_SPEED_TURN);
    analogWrite(MOTOR_L_FORWARD_PIN, MOTOR_SPEED_GO);
}

void forwardLeft() {
    analogWrite(MOTOR_R_FORWARD_PIN, MOTOR_SPEED_GO);
    analogWrite(MOTOR_L_FORWARD_PIN, MOTOR_SPEED_TURN);
}

void reverseRight() {
    analogWrite(MOTOR_R_REVERSE_PIN, MOTOR_SPEED_GO);
    analogWrite(MOTOR_L_REVERSE_PIN, MOTOR_SPEED_TURN);
}

void reverseLeft() {
    analogWrite(MOTOR_R_REVERSE_PIN, MOTOR_SPEED_TURN);
    analogWrite(MOTOR_L_REVERSE_PIN, MOTOR_SPEED_GO);
}

void stop() {
    analogWrite(MOTOR_R_FORWARD_PIN, MOTOR_SPEED_STOP);
    analogWrite(MOTOR_L_FORWARD_PIN, MOTOR_SPEED_STOP);
    analogWrite(MOTOR_R_REVERSE_PIN, MOTOR_SPEED_STOP);
    analogWrite(MOTOR_L_REVERSE_PIN, MOTOR_SPEED_STOP);
}

// turn on headlights
void turnOnHeadlights() {
    digitalWrite(HEADLIGHTS_PIN, HIGH);
}

// turn off headlights
void turnOffHeadlights() {
    digitalWrite(HEADLIGHTS_PIN, LOW);
}

// Get all telemetry data
String getTelemetry() {
    int gpsSat;
    float gpsLat = 0;
    float gpsLong = 0;
    int gpsFix = -1;
    int gpsFixQuality = -1;

    getGPS(&gpsSat, &gpsLat, &gpsLong, &gpsFix, &gpsFixQuality);

    String json = "{\n"
                  "  \"gps\": {\n"
                  "    \"quality\": " + String(gpsFixQuality) + ",\n"
                  "    \"fix\": " + String(gpsFix) + ",\n"
                  "    \"lat\": " + String(gpsLat, 6) + ",\n"
                  "    \"long\": " + String(gpsLong, 6) + "\n"
                  "  },\n"
                  "  \"accelerometer\": \"" + getAccel() + "\",\n"
                  "  \"temp_c\": " + getTemp() + ",\n"
                  "  \"ultrasonic_distances\": {\n"
                  "     \"front_l\": " + String(ultraSonicDistance()) + "\n"
                  "   }\n"
                  "}";
    Serial.println(json);
    return json;
}

// Receive GPS coordinates
// TODO need to test and set return data
void getGPS(int *satellites, float *latitude, float *longitude, int *fix, int *fixQuality) {
    if (GPS_ECHO) {
        char c = GPS.read();
        if (c) {
            Serial.print(c);
        }
    }
    // if a sentence is received, we can check the checksum, parse it...
    if (GPS.newNMEAreceived()) {
        // a tricky thing here is if we print the NMEA sentence, or data
        // we end up not listening and catching other sentences!
        // so be very wary if using OUTPUT_ALLDATA and trying to print out data
        Serial.print(GPS.lastNMEA()); // this also sets the newNMEAreceived() flag to false
        if (!GPS.parse(GPS.lastNMEA()))  {// this also sets the newNMEAreceived() flag to false
            return; // we can fail to parse a sentence in which case we should just wait for another
        }
    }

    // approximately every 2 seconds or so, print out the current stats
    // delay(2000);
    *fixQuality = ((int)GPS.fixquality);
    *fix = ((int)GPS.fix);
    if (GPS.fix) {
        *latitude = GPS.lat;
        *longitude = GPS.lon;
        // GPS_speed = ((int)GPS.speed);
        // Serial.print("Angle: "); Serial.println(GPS.angle);
        // Serial.print("Altitude: "); Serial.println(GPS.altitude);
        *satellites = ((int)GPS.satellites);
        // GPS_ant = ((int)GPS.antenna);
    }
}


// Read the tactile sensors and return area of concern
int readTactileSensor() {
    byte front = digitalRead(TACTILE_BTN_FRONT); // 1 = front
    byte back = digitalRead(TACTILE_BTN_BACK);   // 2 = back
    byte left = digitalRead(TACTILE_BTN_LEFT);   // 3 = left
    byte right = digitalRead(TACTILE_BTN_RIGHT); // 4 = right

    if (front == LOW) {
        return 1;
    }
    if (back == LOW) {
        return 2;
    }
    if (left == LOW) {
        return 3;
    }
    if (right == LOW) {
        return 4;
    }
    return 0;
}


// Get accelerometer data
String getAccel() {
    sensors_event_t event;
    accelerometerSensor.getEvent(&event);
    delay(200);
    return String("") + event.acceleration.x + ", " + event.acceleration.y + ", " + event.acceleration.z;
}


// Get temperature data
float getTemp() {
    sensors_event_t temp;
    tempSensorPointer->getEvent(&temp);
    delay(200);
    return temp.temperature;
}

// Get ultrasonic sensor distances
// Just one for now, need to add more later
int ultraSonicDistance() {
    digitalWrite(ULTRASONIC_TRIG_PIN_1, LOW);
    delayMicroseconds(5);

    digitalWrite(ULTRASONIC_TRIG_PIN_1, HIGH);
    delayMicroseconds(10);
    digitalWrite(ULTRASONIC_TRIG_PIN_1, LOW);

    long duration = pulseIn(ULTRASONIC_ECHO_PIN_1, HIGH);
    long distance = duration * 0.034 / 2; // distance in cm
    return distance;
}

// extend linear actuators
void openDoor() {
    digitalWrite(LINEAR_ACUTATOR_PIN_1, LOW);
    digitalWrite(LINEAR_ACUTATOR_PIN_2, HIGH);
    delay(12500);
    digitalWrite(LINEAR_ACUTATOR_PIN_1, LOW);
    digitalWrite(LINEAR_ACUTATOR_PIN_2, LOW);
}

// retract linear actuators
void closeDoor() {
    digitalWrite(LINEAR_ACUTATOR_PIN_1, HIGH);
    digitalWrite(LINEAR_ACUTATOR_PIN_2, LOW);
    delay(12500);
    digitalWrite(LINEAR_ACUTATOR_PIN_1, LOW);
    digitalWrite(LINEAR_ACUTATOR_PIN_2, LOW);
}
