// Authors: Anna Kiraly, Owen Bramley, Christian Komo, Rob Godfrey

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_GPS.h>
#include <Adafruit_AHTX0.h>
#include <Servo.h>

// Define pins
#define BRAKE_RELAY_PIN 25  // brake -> relay 1
#define LINEAR_ACTUATOR_UP_1 27
#define LINEAR_ACTUATOR_UP_2 31
#define LINEAR_ACTUATOR_DOWN_1 29
#define LINEAR_ACTUATOR_DOWN_2 33
#define T_RELAY_PIN 35
#define R_RELAY_PIN 37
#define E_RELAY_PIN 39
#define LEFT_MOTOR_PIN 9 // PWM pin for left motor
#define RIGHT_MOTOR_PIN 10 // PWM pin for right motor
#define GPS_SERIAL Serial3 // set GPS_SERIAL port to 3 (pins 14,15)
#define GPS_ECHO false // turn off echoing the GPS data to the Serial console
#define ULTRASONIC_THRESHOLD 12 // cm that the ultrasonic sensors will alert
#define ULTRASONIC_TRIG_PIN_1 48
#define ULTRASONIC_ECHO_PIN_1 50


// TODO shouldn't these be different?
#define TACTILE_BTN_FRONT 4
#define TACTILE_BTN_BACK 4
#define TACTILE_BTN_LEFT 4
#define TACTILE_BTN_RIGHT 4

// Initialize the AHT20 sensor
Adafruit_AHTX0 tempSensor;
// Initialize the ADXL345 sensor
Adafruit_ADXL345_Unified accelerometerSensor = Adafruit_ADXL345_Unified();
// Pointer for the temperature sensor
Adafruit_Sensor *tempSensorPointer;

// Create Servo objects for motor control
Servo leftServoMotor;
Servo rightServoMotor;

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPS_SERIAL);


// Initial setup
void setup() {
    Serial.begin(115200);
    while (!Serial); // wait for serial to connect

    initializeMotors(); // init motors

    // Set relay pins mode
    pinMode(BRAKE_RELAY_PIN, OUTPUT);
    pinMode(LINEAR_ACTUATOR_UP_1, OUTPUT);
    pinMode(LINEAR_ACTUATOR_DOWN_1, OUTPUT);
    pinMode(LINEAR_ACTUATOR_UP_2, OUTPUT);
    pinMode(LINEAR_ACTUATOR_DOWN_2, OUTPUT);
    pinMode(T_RELAY_PIN, OUTPUT);
    pinMode(R_RELAY_PIN, OUTPUT);
    pinMode(E_RELAY_PIN, OUTPUT);

    // Set ultrasonic module pins mode
    pinMode(ULTRASONIC_TRIG_PIN_1, OUTPUT);
    pinMode(ULTRASONIC_ECHO_PIN_1, INPUT);

    // Set tactile sensor pins mode
    pinMode(TACTILE_BTN_FRONT, INPUT_PULLUP);
    pinMode(TACTILE_BTN_BACK, INPUT_PULLUP);
    pinMode(TACTILE_BTN_LEFT, INPUT_PULLUP);
    pinMode(TACTILE_BTN_RIGHT, INPUT_PULLUP);

    // Check AHT20 is alive
    if (!tempSensor.begin()) {
        Serial.println("Could not find AHT? Check wiring");
        while (1) {
            delay(10);
        }
    }
    Serial.println("AHT10 or AHT20 found");
    tempSensorPointer = tempSensor.getTemperatureSensor();
    tempSensorPointer->printSensorDetails();

    // Check ADXL345 is alive
    if (!accelerometerSensor.begin()) {
        Serial.println("No ADXL345 sensor detected.");
        while (1);
    }

    // Ultimate GPS Setup
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


// Main loop
void loop() {
    recvBytesWithStartEndMarkers();
    if (newData) {
        processReceivedData();
    }
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


// Initialize the motors
void initializeMotors() {
    leftServoMotor.attach(LEFT_MOTOR_PIN); // Attach motorL to its PWM pin
    rightServoMotor.attach(RIGHT_MOTOR_PIN); // Attach motorR to its PWM pin
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

    //delay(200);
    //return acceleration data X,Y,Z
    return String(event.acceleration.x)+","+String(event.acceleration.y)+","+String(event.acceleration.z);
}

// Get temperature data
float getTemp() {
    sensors_event_t temp;
    tempSensorPointer->getEvent(&temp);

    //delay(200);
    //return temperature in degrees C
    return temp.temperature;
}

// Turn brakes on/off
int brake(int type) {
    if (type == 1) {
        digitalWrite(BRAKE_RELAY_PIN, HIGH); // turn brakes on
    } else if (type == 0) {
        digitalWrite(BRAKE_RELAY_PIN, LOW); // turn brakes off
    }
}

// Get ultrasonic sensor distances
// returns an array of integers with a length of 4. 0 = no concern 1 = proximity alert utilizing the predefined 'ULTRASONIC_THRESHOLD' definition
int ultraSonicDistance() {
    digitalWrite(ULTRASONIC_TRIG_PIN_1, LOW);
    delayMicroseconds(5);

    digitalWrite(ULTRASONIC_TRIG_PIN_1, HIGH);
    delayMicroseconds(10);
    digitalWrite(ULTRASONIC_TRIG_PIN_1, LOW);

    long duration = pulseIn(ULTRASONIC_ECHO_PIN_1, HIGH);
    long distance = duration * 0.034 / 2; //distance in cm
    Serial.print("Distance:");
    Serial.println(distance);

    if (distance < 0.01) {
        return 1;
    }
    return 0;
}

// Control motor speed
// Parameters: motorNum (1 or 2), speed (-100 to 100)
void setMotorSpeed(int motor, int speed) {
    int pwmValue = map(abs(speed), 0, 100, 0, 255); // Map speed to PWM range

    if (motor == 'L') {
        if (speed >= 0) {
            leftServoMotor.writeMicroseconds(1500 + pwmValue * 8); // Forward
        } else {
            leftServoMotor.writeMicroseconds(1500 - pwmValue * 8); // Reverse
        }
    } else if (motor == 'R') {
        if (speed >= 0) {
            rightServoMotor.writeMicroseconds(1500 + pwmValue * 8); // Forward
        } else {
            rightServoMotor.writeMicroseconds(1500 - pwmValue * 8); // Reverse
        }
    }
}

// Get all telemetry data
void getTelemetry() {
    int gpsSat;
    float gpsLat;
    float gpsLong;
    int gpsFix;
    int gpsFixQuality;

    getGPS(&gpsSat, &gpsLat, &gpsLong, &gpsFix, &gpsFixQuality);
    if (gpsFix == 0){
        Serial.print("No GPS fix");
    } else {
        Serial.println(gpsFix);
        Serial.print("GPS fix quality: ");
        Serial.println(gpsFixQuality);
    }
    Serial.println();
    Serial.println(getAccel());
    Serial.println(getTemp());
    ultraSonicDistance();
}


/*
TODO check this logic

// Extend linear actuators
void extendLinearActuators() {
    digitalWrite(LINEAR_ACTUATOR_UP_1, LOW);
    digitalWrite(LINEAR_ACTUATOR_DOWN_1, HIGH);
    digitalWrite(LINEAR_ACTUATOR_UP_2, LOW);
    digitalWrite(LINEAR_ACTUATOR_DOWN_2, HIGH);
    delay(20000);
}

// Retract linear actuators
void retractLinearActuators() {
    digitalWrite(LINEAR_ACTUATOR_UP_1, HIGH);
    digitalWrite(LINEAR_ACTUATOR_DOWN_1, LOW);
    digitalWrite(LINEAR_ACTUATOR_UP_2, HIGH);
    digitalWrite(LINEAR_ACTUATOR_DOWN_2, LOW);
    delay(10000);
}
*/

// Jetson <-> Arduino communication FROM: https://forum.arduino.cc/t/serial-input-basics-updated/382007/3 (example 6 modified)

const byte numBytes = 32;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;

void recvBytesWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    byte startMarker = 0x3C;
    byte endMarker = 0x3E;
    byte rb;

    while (Serial.available() > 0 && newData == false) {
        rb = Serial.read();

        if (recvInProgress) {
            if (rb != endMarker) {
                receivedBytes[ndx] = rb;
                ndx++;
                if (ndx >= numBytes) {
                    ndx = numBytes - 1;
                }
            } else {
                receivedBytes[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                numReceived = ndx;  // save the number for use when printing
                ndx = 0;
                newData = true;
            }
            // Check if rb is the byte 0x4C (L)
            if (rb == 0x4C) {
                brake(1); // Call the function brake if byte 0x4C is received
            }
        } else if (rb == startMarker) {
            recvInProgress = true;
        }
    }
}

void processReceivedData() {
    // Check is the received data is at least 3 bytes
    if (numReceived >= 3) {
         // Check if the received data has the correct start and end markers
        if (receivedBytes[0] == '<' && receivedBytes[numReceived] == '>') {
            // If the received data is contains b (brake)
            if (receivedBytes[1] == 'b') {
                // Check value attached to the start marker
                if (receivedBytes[2] == '1') {
                    Serial.println("Received <b1>. Performing specific action...");
                }
            } else {
                Serial.println(receivedBytes);
            }
        } else {
            Serial.println("<ERROR>");
        }
        newData = false;
    } else {
        Serial.println("<ERROR>"); // Print error message if the received data has less than 3 bytes
    }
}
