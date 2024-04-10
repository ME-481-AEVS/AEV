#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_GPS.h>
#include <Adafruit_AHTX0.h>

#define GPS_SERIAL Serial3 // set GPS_SERIAL port to 3 (pins 14,15)

const int MOTOR_PIN_L = 5;
const int MOTOR_PIN_R = 6;
const int MOTOR_SPEED_STOP = 50;
const int MOTOR_SPEED_GO = 150; // between 0 (stopped) and 255 (full speed)
const int ULTRASONIC_THRESHOLD = 12; // cm that the ultrasonic sensors will alert
const int ULTRASONIC_TRIG_PIN_1 = 48;
const int ULTRASONIC_ECHO_PIN_1 = 50;
const bool GPS_ECHO = false; // turn off echoing the GPS data to the Serial console

const int T_RELAY_PIN = 35;
const int R_RELAY_PIN = 37;
const int E_RELAY_PIN = 39;

// TODO these should be different
const int TACTILE_BTN_FRONT = 4;
const int TACTILE_BTN_BACK = 4;
const int TACTILE_BTN_LEFT = 4;
const int TACTILE_BTN_RIGHT = 4;


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

    pinMode(MOTOR_PIN_R, OUTPUT); // motor pin is an output
    pinMode(MOTOR_PIN_L, OUTPUT); // motor pin is an output

    pinMode(T_RELAY_PIN, OUTPUT);
    pinMode(R_RELAY_PIN, OUTPUT);
    pinMode(E_RELAY_PIN, OUTPUT);

    // Set ultrasonic module pins mode
    pinMode(ULTRASONIC_TRIG_PIN_1, OUTPUT);
    pinMode(ULTRASONIC_ECHO_PIN_1, INPUT);

    // Check AHT20 is alive
    if (!tempSensor.begin()) {
        Serial.println("Could not find AHT? Check wiring");
        while (1) {
            delay(10);
        }
    }

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
    } else if (command == "<STOP>") {
        Serial.println("From dino: stopping");
        stop();
    } else if (command == "<TELEMETRY>") {
        Serial.println("From dino: getting telemetry");
        getTelemetry();
    } else {
        Serial.println("From dino: idk what to do! :(");
    }
}

void moveForward() {
    analogWrite(MOTOR_PIN_R, MOTOR_SPEED_GO);
    analogWrite(MOTOR_PIN_L, MOTOR_SPEED_GO);
}

void stop() {
    analogWrite(MOTOR_PIN_L, MOTOR_SPEED_STOP);
    analogWrite(MOTOR_PIN_R, MOTOR_SPEED_STOP);
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
                  "  'gps': {\n"
                  "    'quality': " + String(gpsFixQuality) + ",\n"
                  "    'fix': " + String(gpsFix) + ",\n"
                  "    'lat': " + String(gpsLat, 6) + ",\n"
                  "    'long': " + String(gpsLong, 6) + "\n"
                  "  },\n"
                  "  'accelerometer': '" + getAccel() + "',\n"
                  "  'temp_c': " + getTemp() + ",\n"
                  "  'ultrasonic_distances': {\n"
                  "     'front_l': " + String(ultraSonicDistance()) + "\n"
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

    //delay(200);
    //return temperature in degrees C
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
