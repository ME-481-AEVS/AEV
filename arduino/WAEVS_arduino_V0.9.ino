#include <Wire.h>
#include <Adafruit_Sensor.h> 
#include <Adafruit_ADXL345_U.h>
#include <Adafruit_GPS.h>
#include <Adafruit_AHTX0.h>
#include <Servo.h>


Adafruit_AHTX0 aht;
Adafruit_ADXL345_Unified accel = Adafruit_ADXL345_Unified();
Adafruit_Sensor *aht_temp;

// define the distance in cm that the ultrasonic sensors will alert 
#define ultrasonicThreshold 12;

// Define the PWM pins for motor control
const int motorLpin = 9; // PWM pin for motorL
const int motorRpin = 10; // PWM pin for motorR

// Create Servo objects for motor control
Servo motorL;
Servo motorR;


// set GPSSerial port to 3 (pins 14,15)
#define GPSSerial Serial3

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);

// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

//decalre GPS pointers
int GPS_sat;
float GPS_lon;
int GPS_fix;
int GPS_fixq;
int GPS_speed;
int GPS_ant;

// define relay pins
#define BRAKE_RELAY_PIN 25 //brake -> relay 1
#define LinearActuator_UP1 27
#define LinearActuator_DOWN1 29
#define LinearActuator_UP2 31
#define LinearActuator_DOWN2 33
#define T_RELAY_PIN 35
#define R_RELAY_PIN 37
#define E_RELAY_PIN 39

// define ultrasonic pins
#define TrigPin_1 48
#define EchoPin_1 50

void setup()
{
  Serial.begin(115200);
  while (!Serial); // wait for serial to connect

  initializeMotors(); // Initialize motors

  // set relay pin as an output
  pinMode(BRAKE_RELAY_PIN, OUTPUT);
  pinMode(LinearActuator_UP1, OUTPUT);
  pinMode(LinearActuator_DOWN1, OUTPUT);
  pinMode(LinearActuator_UP2, OUTPUT);
  pinMode(LinearActuator_DOWN2, OUTPUT);
  pinMode(T_RELAY_PIN, OUTPUT);
  pinMode(R_RELAY_PIN, OUTPUT);
  pinMode(E_RELAY_PIN, OUTPUT);

  // set ultrasonic module pins 
  pinMode(TrigPin_1, OUTPUT);
  pinMode(EchoPin_1, INPUT);

  //check AHT20 is alive
  if (! aht.begin()) {
    Serial.println("Could not find AHT? Check wiring");
    while (1) delay(10);
  }
  Serial.println("AHT10 or AHT20 found");
  aht_temp = aht.getTemperatureSensor();
  aht_temp->printSensorDetails();

  //check ADXL345 is alive 
  if(!accel.begin())
   {
      Serial.println("No ADXL345 sensor detected.");
      while(1);
   }

  //Ultimate GPS Setup
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_BAUD_9600 "$PMTK251,9600*17");
  // uncomment this line to turn on RMC (recommended minimum) and GGA (fix data) including altitude
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
  GPSSerial.println(PMTK_Q_RELEASE);
}

void getGPS(int *satellites, float *longitude, int *fix, int *fix_quality);

// recive GPS coordinates **need to test and set return data**
void getGPS(int *satellites, float *longitude, int *fix, int *fix_quality) 
{
  // read data from the GPS in the 'main loop'
  char c = GPS.read();
  // if you want to debug, this is a good time to do it!
  if (GPSECHO)
    if (c) Serial.print(c);
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trying to print out data
    Serial.print(GPS.lastNMEA()); // this also sets the newNMEAreceived() flag to false
    if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
      return; // we can fail to parse a sentence in which case we should just wait for another
  }

  // approximately every 2 seconds or so, print out the current stats
  // delay(2000);
  *fix_quality = ((int)GPS.fixquality);
  *fix = ((int)GPS.fix);
  if (GPS.fix) {
    // GPS_lat = GPS.lat;
    *longitude = GPS.lon;
    // GPS_speed = ((int)GPS.speed);
    // Serial.print("Angle: "); Serial.println(GPS.angle);
    // Serial.print("Altitude: "); Serial.println(GPS.altitude);
    *satellites = ((int)GPS.satellites);
    // GPS_ant = ((int)GPS.antenna);
  }

}

String getAccel() 
{
   sensors_event_t event; 
   accel.getEvent(&event);

   //delay(200);
   //return acceleration data X,Y,Z
   return String(event.acceleration.x)+","+String(event.acceleration.y)+","+String(event.acceleration.z);
}

float getTemp() {
  sensors_event_t temp;
  aht_temp->getEvent(&temp);

  //delay(200);
  //return temperature in degrees C
  return temp.temperature;
}


int brake() { // int brake(int type)
  // if (type == 1){
  //   // turn brakes on
  //   digitalWrite(BRAKE_RELAY_PIN, HIGH);
  // } else if (type == 0) {
  //   digitalWrite(BRAKE_RELAY_PIN, LOW);
  // }
  
  digitalWrite(O_RELAY_PIN, HIGH);
  delay(100);
  digitalWrite(O_RELAY_PIN, LOW);
  digitalWrite(I_RELAY_PIN, HIGH);
  delay(100);
  digitalWrite(I_RELAY_PIN, LOW);
  digitalWrite(U_RELAY_PIN, HIGH);
  delay(100);
  digitalWrite(U_RELAY_PIN, LOW);
  digitalWrite(Y_RELAY_PIN, HIGH);
  delay(100);
  digitalWrite(Y_RELAY_PIN, LOW);
  digitalWrite(T_RELAY_PIN, HIGH);
  delay(100);
  digitalWrite(T_RELAY_PIN, LOW);
  digitalWrite(R_RELAY_PIN, HIGH);
  delay(100);
  digitalWrite(R_RELAY_PIN, LOW);
  digitalWrite(E_RELAY_PIN, HIGH);
  delay(100);
  digitalWrite(E_RELAY_PIN, LOW);
}

// fucntion to fetch ultrasonic sensor distances 
// returns an array of integers with a length of 4. 0 = no concern 1 = proximity alert utilizing the predefined 'ultrasonicThreshold' definition
int ultraSonicDistance() {
  digitalWrite(TrigPin_1, LOW);
  delayMicroseconds(5);

  digitalWrite(TrigPin_1, HIGH);
  delayMicroseconds(10);
  digitalWrite(TrigPin_1, LOW);

  long duration = pulseIn(EchoPin_1, HIGH);
  long distance = duration * 0.034 / 2; //distance in cm
  Serial.print("Distance:");
  Serial.println(distance);

  if (distance < 0.01) 
    return 1;
  return 0;
}

// Function to control motor speed
// Parameters: motorNum (1 or 2), speed (-100 to 100)
void setMotorSpeed(int motor, int speed) {
  int pwmValue = map(abs(speed), 0, 100, 0, 255); // Map speed to PWM range

  if (motor == 'L') {
    if (speed >= 0) {
      motorL.writeMicroseconds(1500 + pwmValue * 8); // Forward
    } else {
      motorL.writeMicroseconds(1500 - pwmValue * 8); // Reverse
    }
  } else if (motor == 'R') {
    if (speed >= 0) {
      motorR.writeMicroseconds(1500 + pwmValue * 8); // Forward
    } else {
      motorR.writeMicroseconds(1500 - pwmValue * 8); // Reverse
    }
  }
}

// Function to initialize the motors
void initializeMotors() {
  motorL.attach(motorLpin); // Attach motorL to its PWM pin
  motorR.attach(motorRpin); // Attach motorR to its PWM pin
}

void loop() {
  getGPS(&GPS_sat, &GPS_lon, &GPS_fix, &GPS_fixq);
  if (GPS_fix == 0){
    Serial.print("no GPS fix");
  } else {
   Serial.println(GPS_fix);
   Serial.print("fixq: ");
   Serial.println(GPS_fixq);
  }
  Serial.println();
  Serial.println(getAccel());
  Serial.println(getTemp());
  brake();
  ultraSonicDistance();
}

//Function to move Linear Actuators up and down
const int LinearActuator_UP1 = 27;
const int LinearActuator_DOWN1 = 29;
const int LinearActuator_UP2 = 31;
const int LinearActuator_DOWN2 = 33;

void setup(){
    pinMode(LinearActuator_UP1, OUTPUT);
    pinMode(LinearActuator_DOWN1, OUTPUT);
    pinMode(LinearActuator_UP2, OUTPUT);
    pinMode(LinearActuator_DOWN2, OUTPUT);
}

void loop(){
    delay(10000);
    //Extend
    digitalWrite(LinearActuator_UP1, LOW);
    digitalWrite(LinearActuator_DOWN1, HIGH);
    digitalWrite(LinearActuator_UP2, LOW);
    digitalWrite(LinearActuator_DOWN2, HIGH);
    delay(20000);
    //Retract
    digitalWrite(LinearActuator_UP1, HIGH);
    digitalWrite(LinearActuator_DOWN1, LOW);
    digitalWrite(LinearActuator_UP2, HIGH);
    digitalWrite(LinearActuator_DOWN2, LOW);
    delay(10000);
}


// KOMO WORK FROM HERE:

// String InBytes; 
// void loop (){
//   // check if serial communication if live
//   if (Serial.available() > 0) {
//     InBytes = Serial.readStringUntil('\n'); // read data until python adds its end of command \n
//     // format InBytes to parse data 

//       // seperate type and its data
//       // add all ^ to an array of integers
//   // run a loop until the command has been executed // loop this and remove data st its postion
//   // once ^ loop is done return a confirmation of commands executed // additionally, if only some of the InBytes commands were executed, send back what was not executedf
  
//   if (InBytes== "on")
//   {
//     brake(1);
//   }
//   if (InBytes == "off")
//   {
//     brake(0);
//   }
//   else
//   {
//     Serial.write("invalid input");
//   }
//   }
// }

// https://forum.arduino.cc/t/serial-input-basics-updated/382007/3 example 6 modified
const byte numBytes = 32;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;
void loop() {
    recvBytesWithStartEndMarkers();
    showNewData();
}

void recvBytesWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    byte startMarker = 0x3C; // <
    byte endMarker = 0x3E; // >
    byte rb;
   

    while (Serial.available() > 0 && newData == false) {
        rb = Serial.read();

        if (recvInProgress == true) {
            if (rb != endMarker) {
                receivedBytes[ndx] = rb;
                ndx++;
                if (ndx >= numBytes) {
                    ndx = numBytes - 1;
                }
            }
            else {
                receivedBytes[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                numReceived = ndx;  // save the number for use when printing
                ndx = 0;
                newData = true;
            }
        }

        else if (rb == startMarker) {
            recvInProgress = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        Serial.print("This just in (HEX values)... ");
        for (byte n = 0; n < numReceived; n++) {
            Serial.print(receivedBytes[n], HEX);
            Serial.print(' ');
            char fN = (char)receivedBytes[n];
            
            // run the function with name corrisponding char value of the recived hex
            if (n == 1) {
              if (fN == 'T') {
                getTemp();
              } else if (fN == 'M') {
                  brake(0);
              } else {
                Serial.print("Invalid function name");
              }
            }
        }
        Serial.println();
        newData = false;
    }
}

//Example: Set motor 1 to 50% speed forward and motor 2 to 75% speed reverse
  // setMotorSpeed('L', 50);
  // setMotorSpeed('R', -75);
  
  // delay(1000); // Delay for demonstration
  
  // stopMotors(); // Stop motors
  // delay(1000); // Delay for demonstration

