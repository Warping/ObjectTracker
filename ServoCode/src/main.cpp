#include <Arduino.h>
#include <DynamixelShield.h>
#include <math.h>

#if defined(ARDUINO_AVR_UNO) || defined(ARDUINO_AVR_MEGA2560)
  #include <SoftwareSerial.h>
  SoftwareSerial soft_serial(7, 8); // DYNAMIXELShield UART RX/TX
  #define DEBUG_SERIAL soft_serial
#elif defined(ARDUINO_SAM_DUE) || defined(ARDUINO_SAM_ZERO)
  #define DEBUG_SERIAL SerialUSB    
#else
  #define DEBUG_SERIAL Serial
#endif

#define MAX_INPUT 20

const uint8_t DXL_ID = 1;
const float DXL_PROTOCOL_VERSION = 2.0;

DynamixelShield dxl;

//This namespace is required to use Control table item names
using namespace ControlTableItem;

void printPos(int id);
int degreesToRaw(float degrees);
float rawToDegrees(int raw);
void setPosDegrees(int id, float newPosDegrees);
void setPosRaw(int id, float newPosRaw);
float getPosDegrees(int id);
void lerpToPos(int id, int newPosRaw);
void process_data (const char * data);
void processIncomingByte (const byte inByte);

int servoPos[] = {0, 0};
int targetPos[] = {0, 0};

void setup() {
  // put your setup code here, to run once:
  
  // For Uno, Nano, Mini, and Mega, use UART port of DYNAMIXEL Shield to debug.
  DEBUG_SERIAL.begin(115200);
  // Set Port baudrate to 57600bps. This has to match with DYNAMIXEL baudrate.
  dxl.begin(57600);
  // Set Port Protocol Version. This has to match with DYNAMIXEL protocol version.
  dxl.setPortProtocolVersion(DXL_PROTOCOL_VERSION);
  for (int i = 1; i <= 2; i++) {
    // Get DYNAMIXEL information
    dxl.ping(i);
    // Turn off torque when configuring items in EEPROM area
    dxl.torqueOff(i);
    dxl.setOperatingMode(i, OP_POSITION);
    dxl.torqueOn(i);
  }
  delay(1000);
  // for (int id = 1; id <= 2; id++) {
  //   while (abs(dxl.getPresentPosition(id)) > 5) {
  //     lerpToPos(id, 0);
  //     delay(1);
  //   }
  // }
  setPosRaw(1, 0);
  setPosRaw(2, 0);
  delay(1000);
}

void loop() {
  while (Serial.available () > 0)
    processIncomingByte (Serial.read ());
  //if (oldTargetPos != targetPos[0])
  lerpToPos(1, targetPos[0]);
  lerpToPos(2, targetPos[1]);
  // if (DEBUG_SERIAL.available()) {
  //   targetPos[0] = DEBUG_SERIAL.parseInt();
  //   DEBUG_SERIAL.print("Target Position of ID 1: ");
  //   DEBUG_SERIAL.println(targetPos[0]);
  //   setPosRaw(1, targetPos[0]);
  // }
  delay(1);
}

void printPos(int id) {
  DEBUG_SERIAL.print("Present Position of ID ");
  DEBUG_SERIAL.print(id);
  DEBUG_SERIAL.print(": ");
  DEBUG_SERIAL.println(dxl.getPresentPosition(id));
}

int degreesToRaw(float degrees) {
  return (int)(4096.0 * degrees / 360.0);
}

float rawToDegrees(int raw) {
  return 360.0 * raw / 4096.0;
}

void setPosDegrees(int id, float newPosDegrees) {
  setPosRaw(id, degreesToRaw(newPosDegrees));
}

void setPosRaw(int id, float newPosRaw) {
  dxl.setGoalPosition(id, newPosRaw);
}

float getPosDegrees(int id) {
  return rawToDegrees(dxl.getPresentPosition(id));
}

void lerpToPos(int id, int newPosRaw) {
  int oldPosRaw = servoPos[id - 1];
  int delta = newPosRaw - oldPosRaw;
  int step = 8 * delta / abs(delta);
  if (abs(delta) < 16) {
    setPosRaw(id, newPosRaw);
    servoPos[id - 1] = newPosRaw;
    return;
  }
  setPosRaw(id, oldPosRaw + step);
  servoPos[id - 1] += step;
}

void process_data (const char * data)
  {
  // for now just display it
  // (but you could compare it to some value, convert to an integer, etc.)
  char * newData = (char *)data;
  if (newData[0] == 'y') {
    newData[0] = '0';
    targetPos[0] = atoi(newData);
  } else if (newData[0] == 'p') {
    newData[0] = '0';
    targetPos[1] = atoi(data);
  }
    //DEBUG_SERIAL.println(data);
  }  // end of process_data

void processIncomingByte (const byte inByte)
  {
  static char input_line [MAX_INPUT];
  static unsigned int input_pos = 0;

  switch (inByte)
    {

    case '\n':   // end of text
      input_line [input_pos] = 0;  // terminating null byte

      // terminator reached! process input_line here ...
      process_data (input_line);

      // reset buffer for next time
      input_pos = 0;  
      break;

    case '\r':   // discard carriage return
      break;

    default:
      // keep adding if not full ... allow for terminating null byte
      if (input_pos < (MAX_INPUT - 1))
        input_line [input_pos++] = inByte;
      break;

    }  // end of switch

  } // end of processIncomingByte  