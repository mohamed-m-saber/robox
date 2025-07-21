#include <Servo.h>
#include <hiduniversal.h>
#include <usbhub.h>
#include <USB.h>

const byte NUM_JOINTS = 6;
const byte servoPins[NUM_JOINTS] = {4, 5, 6, 7, 8, 9};
const byte minAngle[NUM_JOINTS] = {0, 15, 0, 0, 0, 30};
const byte maxAngle[NUM_JOINTS] = {180, 125, 180, 180, 180, 95};
const byte zeroPos[NUM_JOINTS]  = {96, 95, 84, 90, 90, 30};

USB Usb;
HIDUniversal Hid(&Usb);
Servo servos[NUM_JOINTS];
byte currentPos[NUM_JOINTS], targetPos[NUM_JOINTS];
float originalInputValues[NUM_JOINTS] = {50, 50, 50, 50, 50, 50};
unsigned long lastMoveTime[NUM_JOINTS], servoStepDelays[NUM_JOINTS] = {10,10,10,10,10,10};

byte recordAngles[25][NUM_JOINTS];
byte nextMotion = 0;
bool joystickMode = true, commandReceived = false;
String cmd = "";
bool isPlaying = false;
byte currentMotion = 0;
unsigned long lastPositionTime = 0;

// Calibration logic (angle correction)
float applyCalibration(byte i, float val, bool forward) {
  if (i == 0) return forward ? val + (5.0 * val / 216.0 + 1.0 / 6.0) : val - (5.0 * val / 216.0 + 1.0 / 6.0);
  if (i == 1) return forward ? val + 4.639 : val - 4.639;
  if (i == 2) return forward ? val - 5.6363 : val + 5.6363;
  if (i == 3) return forward ? val - 0.3 : val + 0.3;
  return val;
}

// === Gamepad Parser ===
class GamepadParser : public HIDReportParser {
public:
  void Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf) override {
    if (!joystickMode || len < 19 || isPlaying) return;

    struct {
      byte index, incBtn, decBtn; 
       } 
       map[] = {
      {0, 12, 14}, {1, 11, 13}, {2, 9, 10},
      {3, 18, 17}, {4, 8, 7}, {5, 15, 16}
    };

    for (auto &m : map) {
      if (buf[m.incBtn] == 0xFF && targetPos[m.index] < maxAngle[m.index]) targetPos[m.index]++;
      if (buf[m.decBtn] == 0xFF && targetPos[m.index] > minAngle[m.index]) targetPos[m.index]--;
    }

    updateOriginalInputValues();
    Send_Position();
  }
} parser;

void setup() {
  Serial.begin(57600);
  delay(2000);

  for (byte i = 0; i < NUM_JOINTS; i++) {
    servos[i].attach(servoPins[i]);
    currentPos[i] = targetPos[i] = zeroPos[i];
    servos[i].write(currentPos[i]);
    lastMoveTime[i] = millis();
  }

  updateOriginalInputValues();
  Send_Position();

  if (Usb.Init() == -1) {
    Serial.println("USB Host Shield init failed");
    while (1);
  }

  Serial.println("USB Host ready. Insert controller.");
  Hid.SetReportParser(0, &parser);
}

void loop() {
  Usb.Task();
  parseCommand();
  updateServos();
}

void updateServos() {
  unsigned long now = millis();
  bool allReached = true;

  // Move servos to their target positions
  for (byte i = 0; i < NUM_JOINTS; i++) {
    if (currentPos[i] != targetPos[i]) {
      allReached = false;
      if (now - lastMoveTime[i] >= servoStepDelays[i]) {
        currentPos[i] += (currentPos[i] < targetPos[i]) ? 1 : -1;
        servos[i].write(currentPos[i]);
        lastMoveTime[i] = now;
        Send_Position();
      }
    }
  }

  // Handle playback progression
  if (isPlaying && allReached && now - lastPositionTime >= 2000) {
    currentMotion++;
    if (currentMotion >= nextMotion) {
      isPlaying = false; // End playback
      currentMotion = 0;
      Serial.println("Playback complete");
    } else {
      // Load next recorded position
      for (byte j = 0; j < NUM_JOINTS; j++) {
        targetPos[j] = recordAngles[currentMotion][j];
      }
      updateOriginalInputValues();
      Send_Position();
      lastPositionTime = now;
    }
  }
}

void parseCommand() {
  while (Serial.available()) {
    char c = Serial.read();
    cmd += c;
    if (c == 'X') commandReceived = true;
  }

  if (!commandReceived) return;
  cmd.trim(); cmd.remove(cmd.length() - 1); // remove 'X'

  // Ignore commands during playback except for stopping playback
  if (isPlaying && cmd != "Stop") {
    cmd = ""; commandReceived = false;
    return;
  }

  if (cmd == "Zero") {
    for (byte i = 0; i < NUM_JOINTS; i++) moveToTarget(i, zeroPos[i]);
    updateOriginalInputValues();
    Send_Position();
  } else if (cmd == "JoyMod") joystickMode = true;
  else if (cmd == "DeskMod") joystickMode = false;
  else if (cmd == "RM") record();
  else if (cmd == "DR" && nextMotion > 0) nextMotion--;
  else if (cmd == "ER") execute();
  else if (cmd == "Stop") {
    isPlaying = false;
    currentMotion = 0;
    Serial.println("Playback stopped");
  }
  else if (cmd.startsWith("D,") && cmd.endsWith(",A")) parseSerial();

  cmd = ""; commandReceived = false;
}

void parseSerial() {
  cmd.remove(0, 2); cmd.remove(cmd.length() - 2);
  byte values[NUM_JOINTS], i = 0;
  while (cmd.length() && i < NUM_JOINTS) {
    int comma = cmd.indexOf(',');
    values[i++] = (comma != -1) ? cmd.substring(0, comma).toInt() : cmd.toInt();
    cmd = (comma != -1) ? cmd.substring(comma + 1) : "";
  }

  for (byte j = 0; j < NUM_JOINTS; j++) {
    originalInputValues[j] = constrain(values[j], 0, 100);
    float angle = applyCalibration(j, angle, true);
    angle = map(originalInputValues[j], 0, 100, minAngle[j], maxAngle[j]);
    
    moveToTarget(j, angle);
  }
}

void moveToTarget(byte joint, float angle) {
  targetPos[joint] = constrain(round(angle), minAngle[joint], maxAngle[joint]);
}

void updateOriginalInputValues() {
  for (byte i = 0; i < NUM_JOINTS; i++) {
    float adjusted = applyCalibration(i, targetPos[i], false);
    originalInputValues[i] = constrain(map(adjusted, minAngle[i], maxAngle[i], 0, 100), 0, 100);
  }
}

void Send_Position() {
  Serial.print("A,");
  for (byte i = 0; i < NUM_JOINTS; i++) {
    Serial.print((byte)originalInputValues[i]);
    if (i < NUM_JOINTS - 1) Serial.print(",");
  }
  Serial.println(",D");
}

void record() {
  if (nextMotion >= 25) {
    Serial.println("Record buffer full");
    return;
  }
  for (byte i = 0; i < NUM_JOINTS; i++) {
    recordAngles[nextMotion][i] = currentPos[i];
  }
  nextMotion++;
  Serial.println("Position recorded");
}

void execute() {
  if (nextMotion == 0) {
    Serial.println("No recorded positions to execute");
    return;
  }
  isPlaying = true;
  currentMotion = 0;
  for (byte j = 0; j < NUM_JOINTS; j++) {
    targetPos[j] = recordAngles[0][j];
  }
  
  updateOriginalInputValues();
  Send_Position();
  lastPositionTime = millis();
}
