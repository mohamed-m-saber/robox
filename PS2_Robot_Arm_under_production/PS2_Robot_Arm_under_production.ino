// //#include <PS2X_lib.h>
// #include <Servo.h>

// byte button_handler(byte btn1, byte btn2);
// void execute();
// void servos_config();
// //void  joystick_config();
// void  joystick();
// void   zeroPosition();
// void   record();
// void moveSmooth(byte, byte);
// // Constants
// const byte NUM_JOINTS = 6;
// const byte stepDelay = 10;  // Delay between each degree step
// const byte stepSize = 1;    // Degrees per step

// // Servo setup
// Servo servos[NUM_JOINTS];
// // PS2 setup
// //PS2X ps2x;

// byte currentPos[NUM_JOINTS] = {90, 90, 90, 90, 70, 50};  // Initial positions
// const byte servoPins[NUM_JOINTS] = {4, 5, 6, 7, 8, 9};
// const byte zeroPos[NUM_JOINTS]  = {90, 90, 90, 90, 70, 50};  // Zero positions
// byte j[NUM_JOINTS];
// // Angle limits
// const byte minAngle[NUM_JOINTS] = {0, 15, 0, 0, 0, 20};
// const byte maxAngle[NUM_JOINTS] = {180, 125, 180, 180, 180, 95};

// // Serial input
// String receivedCommand = "";
// bool commandReceived = false;
// const byte numValues = NUM_JOINTS;
// byte receivedValues[numValues];

// byte v_angle[NUM_JOINTS] = {90, 90, 90, 90, 70, 50};
// String Robotic_Arm_Position = "";
// bool joystickMode ;
// byte record_angles[25][NUM_JOINTS];
// byte nxt_motion = 0;

// //right now, the library does NOT support hot-pluggable controllers, meaning
// //you must always either restart your Arduino after you connect the controller,
// //or call config_gamepad(pins) again after connecting the controller.

// int error = 0;
// byte type = 0;
// byte vibrate = 0;

// void setup() {
//   Serial.begin(57600);
//   delay(2000);
//   servos_config();
// //  error = ps2x.config_gamepad(13, 11, 10, 12, true, true); //GamePad(clock, command, attention, data, Pressures?, Rumble?)
//   joystickMode = true;  // Set default mode to joystick
//   //Serial.println("The Default Mode is Joystick. Use 'Zero', 'DeskMod', or 'RM' to change modes.");
// }

// void loop() {
//   Parse_data();
//   if (joystickMode == 1) {
//    // error = ps2x.config_gamepad(13, 11, 10, 12, true, true); //GamePad(clock, command, attention, data, Pressures?, Rumble?)
//     if(error==1){
//       return;
//     }
//     else{
//         joystick();
//     }
//   }
// }

// void Parse_data() {
//   while (Serial.available()) {
//     char c = Serial.read();
//     receivedCommand += c;
//     if (c == 'X') {
//       commandReceived = true;
//       //break; // optional, if you want to process one full command at a time
//     }
//   }

//   if (!commandReceived) return;

//   receivedCommand.trim();  // removes whitespace, but not 'E'
//   receivedCommand.remove(receivedCommand.length() - 1);  // remove the 'E' at the end

//   if (receivedCommand.equals("Zero")) {
//     //Serial.println("Zero Position Command Received");
//     zeroPosition();
//   }
//   else if (receivedCommand.equals("JoyMod")) {
//     //Serial.println("Joystick control enabled.");
//     joystickMode = true;
//   }
//   else if (receivedCommand.equals("DeskMod")) {
//     //Serial.println("Serial control enabled.");
//     joystickMode = false;
//   }

//   else if (receivedCommand.equals("RM")) {
// //    Serial.println("Record Mode enabled.");
//     record();
//     nxt_motion++;
//   }
//   else if (receivedCommand.equals("DR")) {
//     //Serial.println("Last Motion Deleted.");
//     nxt_motion--;
//   }

//   else if (receivedCommand.equals("ER")) {
//     //Serial.println("Excute Recorded Motion.");
//     execute();
//   }

//   else if (receivedCommand.startsWith("D,") && receivedCommand.endsWith(",A")) {
//     serial();
//   }
//   receivedCommand = "";
//   commandReceived = false;
//   delay(20);
// }




// // void Parse_data() {
// //   while (Serial.available()) {
// //     char c = Serial.read();
// //     receivedCommand += c;
// //     if (c == 'X') {  // or 'AX' if you prefer
// //       commandReceived = true;
// //     }
// //   }

// //   if (!commandReceived) return;

// //   receivedCommand.trim();  
// //   receivedCommand.remove(receivedCommand.length() - 1);  

// //   if (receivedCommand.equals("Zero")) {
// //     zeroPosition();
// //   }
// //   else if (receivedCommand.equals("JoyMod")) {
// //     joystickMode = true;
// //   }
// //   else if (receivedCommand.equals("DeskMod")) {
// //     joystickMode = false;
// //   }
// //   else if (receivedCommand.equals("RM")) {
// //     record();
// //     nxt_motion++;
// //   }
// //   else if (receivedCommand.equals("DR")) {
// //     nxt_motion--;
// //   }
// //   else if (receivedCommand.equals("ER")) {
// //     execute();
// //   }
// //   else if (receivedCommand.startsWith("D,") && receivedCommand.endsWith(",A")) {
// //     serial();
// //   }

// //   Serial.println("OK");  // ✅ ACK back to ROS side
// //   receivedCommand = "";
// //   commandReceived = false;
// //   delay(50);
// // }








// void serial() {
//   if (receivedCommand.startsWith("D,") && receivedCommand.endsWith(",A")) {
//     String content = receivedCommand;
//     content.remove(0, 2);  // Remove "D,"
//     content.remove(content.length() - 2, 2);  // Remove ",A"

//     String values[numValues];
//     int index = 0;

//     while (index < numValues && content.length() > 0) {
//       int commaIndex = content.indexOf(',');
//       if (commaIndex != -1) {
//         values[index] = content.substring(0, commaIndex);
//         content = content.substring(commaIndex + 1);
//       } else {
//         values[index] = content;
//         content = "";
//       }
//       index++;
//     }

//     if (index != NUM_JOINTS) {
//       //      Serial.println("Error: Incorrect number of values.");
//     } else {
//       bool success = true;
//       for (byte i = 0; i < NUM_JOINTS; i++) {
//         receivedValues[i] = values[i].toFloat();
//         if (isnan(receivedValues[i])) {
//           //          Serial.print("Conversion error at joint ");
//           //          Serial.println(i + 1);
//           success = false;
//           break;
//         }

//         // Clamp input to 0–100
//         receivedValues[i] = constrain(receivedValues[i], 0, 100);
//       }

//       if (success) {
//         for (byte i = 0; i < NUM_JOINTS; i++) {
//           byte mappedAngle = map(receivedValues[i], 0, 100, minAngle[i], maxAngle[i]);
//           moveSmooth(i, mappedAngle);
//         }
//         //        Serial.println("All joints moved.");
//       }
//       else {
// //        Serial.println("Invalid value(s) in command.");
//       }
//     }
//   }
//   else {
// //    Serial.println("Invalid command format.");
//   }
//   receivedCommand = "";
//   commandReceived = false;
// }

// void joystick(){

//   // Update controller state
//   //ps2x.read_gamepad(false, vibrate);

//   // Button values
//   //  byte circle = ps2x.Button(PSB_RED);
//   //  byte square = ps2x.Button(PSB_PINK);
//   //  byte triangle = ps2x.Button(PSB_GREEN);
//   //  byte cross = ps2x.Button(PSB_BLUE);
//   //  byte R2 = ps2x.Button(PSB_R2);
//   //  byte L2 = ps2x.Button(PSB_L2);
//   //  byte select = ps2x.Button(PSB_SELECT);
//   //  byte start = ps2x.Button(PSB_START);
//   //  // Analog values
//   //  byte leftX = ps2x.Analog(PSS_LX);
//   //  byte rightX = ps2x.Analog(PSS_RX);

//   // Joint logic


//   // j[0] = button_handler(ps2x.Button(PSB_RED), ps2x.Button(PSB_PINK));
//   // j[1] = button_handler(ps2x.Button(PSB_GREEN), ps2x.Button(PSB_BLUE));
//   // j[2] = button_handler(ps2x.Button(PSB_R2), ps2x.Button(PSB_L2));
//   // j[3] = analog_handler(ps2x.Analog(PSS_LX));   // Use analog stick direction
//   // j[4] = analog_handler(ps2x.Analog(PSS_RX));  // Use analog stick direction
//   // j[5] = button_handler(ps2x.Button(PSB_SELECT), ps2x.Button(PSB_START));
//   // //delay(500);
//   // // Output
// //  Serial.print("j1: "); Serial.println(j[0]);
// //  Serial.print("j2: "); Serial.println(j[1]);
// //  Serial.print("j3: "); Serial.println(j[2]);
// //  Serial.print("j4: "); Serial.println(j[3]);
// //  Serial.print("j5: "); Serial.println(j[4]);
// //  Serial.print("j6: "); Serial.println(j[5]);
// //  Serial.println("------------------------------");

//   for (byte i = 0; i < NUM_JOINTS; i++) {
//     updateJointAngle(i, j[i]);
//   }
// }

// int analog_handler(byte val) {
//   if (val > 140) return 1;   // Moved right
//   else if (val < 115) return -1;  // Moved left
//   else return 0;             // Centered
// }

// byte button_handler(byte btn1, byte btn2){
//   if (btn1 > btn2)
//     return 1;
//   else if (btn1 < btn2)
//     return -1;
//   else
//     return 0;
// }

// void moveSmooth(byte jointIndex, byte targetAngle) {
//   targetAngle = constrain(targetAngle, minAngle[jointIndex], maxAngle[jointIndex]);
//   byte current = currentPos[jointIndex];

// //  if (current == targetAngle) return;

//   byte direction = (targetAngle > current) ? 1 : -1;
//   for (byte pos = current; pos != targetAngle; pos += direction * stepSize) {
//     servos[jointIndex].write(pos);
//     delay(stepDelay);
//   }

//   currentPos[jointIndex] = targetAngle;
//   //  Serial.print("Joint ");
//   //  Serial.print(jointIndex + 1);
//   //  Serial.print(" moved to ");
//   //  Serial.println(targetAngle);
//   v_angle[jointIndex] = targetAngle;
//   Send_Position();
// }

// void zeroPosition() {
//   for (byte i = 0; i < NUM_JOINTS; i++) {
//     moveSmooth(i, zeroPos[i]);
//     currentPos[i] = zeroPos[i];  // Update current position to zero
//     v_angle[i] = zeroPos[i];
//   }
//   //  Serial.println("Robot arm moved to zero position.");
// }

// void updateJointAngle(byte joint, byte dir) {
//   // direction should be +1 or -1
//   if (joint < 0 || joint >= NUM_JOINTS) return; // avoid array out of bounds

//   v_angle[joint] += dir ;

//   // Constrain angle within min/max limits
//   v_angle[joint] = constrain( v_angle[joint], minAngle[joint] + 1, maxAngle[joint]);

//   moveSmooth(joint,  v_angle[joint]);
// }

// void Send_Position() {
//   Robotic_Arm_Position = "";
  
// //  if (joystickMode){
//     for (byte i = 0; i < NUM_JOINTS; i++) {
//       byte mappedAngle = map(v_angle[i], minAngle[i], maxAngle[i], 0 , 100);
//       Robotic_Arm_Position += String(mappedAngle);
//       if (i < NUM_JOINTS - 1) Robotic_Arm_Position += ",";
//     }
//     Serial.println("A," + Robotic_Arm_Position + ",D");
// //  }
// }

// void servos_config(){
//   for (byte i = 0; i < NUM_JOINTS; i++) {
//     servos[i].attach(servoPins[i]);
//     //servos[i].write(currentPos[i]);
//     moveSmooth(i, currentPos[i]);
//   }
// }

// void record(){
//   for (byte i = 0 ; i < NUM_JOINTS ; i++)
//   {
//     record_angles[nxt_motion][i] = currentPos[i];
//     //    Serial.print("move recorded ");
//     //    Serial.println(currentPos[i]);
//   }
// }

// void execute(){
//   for (byte i = 0 ; i < nxt_motion ; i++)
//   {
//     for (byte j = 0 ; j < NUM_JOINTS ; j++)
//     {
//       //servos[j].write(record_angles[i][j]);
//       moveSmooth(j, record_angles[i][j]);
//       //Serial.print("move executed ");
//       //Serial.println(record_angles[i][j]);
//     }
//     delay(1000);
//   }
// }




















#include <Servo.h>

const byte NUM_JOINTS = 6;
const byte servoPins[NUM_JOINTS] = {4, 5, 6, 7, 8, 9};
const byte zeroPos[NUM_JOINTS]  = {90, 90, 90, 90, 90, 30};
const byte minAngle[NUM_JOINTS] = {0, 15, 0, 0, 0, 30};
const byte maxAngle[NUM_JOINTS] = {180, 125, 180, 180, 180, 95};

Servo servos[NUM_JOINTS];
byte currentPos[NUM_JOINTS] = {90, 90, 90, 90, 90, 30};
byte targetPos[NUM_JOINTS];
unsigned long lastMoveTime[NUM_JOINTS];
unsigned long servoStepDelays[NUM_JOINTS];   // per-joint speed
String receivedCommand = "";
bool commandReceived = false;
const byte numValues = NUM_JOINTS;
byte receivedValues[numValues];
byte v_angle[NUM_JOINTS] = {90, 90, 90, 90, 70, 50};
String Robotic_Arm_Position = "";
bool joystickMode = false;
byte record_angles[25][NUM_JOINTS];
byte nxt_motion = 0;

void setup() {
  Serial.begin(57600);
  delay(2000);
  servos_config();

  for (byte i = 0; i < NUM_JOINTS; i++) {
    targetPos[i] = currentPos[i];
    lastMoveTime[i] = millis();
  }

  // ✳️ Set speed (lower = faster)
  servoStepDelays[0] = 8;   // joint 1
  servoStepDelays[1] = 10;  // joint 2
  servoStepDelays[2] = 12;  // joint 3
  servoStepDelays[3] = 10;  // joint 4
  servoStepDelays[4] = 8;   // joint 5
  servoStepDelays[5] = 10;  // joint 6
}

void loop() {
  Parse_data();
  updateServos();
}

void Parse_data() {
  while (Serial.available()) {
    char c = Serial.read();
    receivedCommand += c;
    if (c == 'X') {
      commandReceived = true;
    }
  }

  if (!commandReceived) return;

  receivedCommand.trim();
  receivedCommand.remove(receivedCommand.length() - 1);

  if (receivedCommand.equals("Zero")) {
    zeroPosition();
  } else if (receivedCommand.equals("JoyMod")) {
    joystickMode = true;
  } else if (receivedCommand.equals("DeskMod")) {
    joystickMode = false;
  } else if (receivedCommand.equals("RM")) {
    record();
    nxt_motion++;
  } else if (receivedCommand.equals("DR")) {
    if (nxt_motion > 0) nxt_motion--;
  } else if (receivedCommand.equals("ER")) {
    execute();
  } else if (receivedCommand.startsWith("D,") && receivedCommand.endsWith(",A")) {
    serial();
  }

  receivedCommand = "";
  commandReceived = false;
}

void serial() {
  String content = receivedCommand;
  content.remove(0, 2);
  content.remove(content.length() - 2, 2);

  String values[numValues];
  int index = 0;

  while (index < numValues && content.length() > 0) {
    int commaIndex = content.indexOf(',');
    if (commaIndex != -1) {
      values[index] = content.substring(0, commaIndex);
      content = content.substring(commaIndex + 1);
    } else {
      values[index] = content;
      content = "";
    }
    index++;
  }

  if (index == NUM_JOINTS) {
    bool success = true;
    for (byte i = 0; i < NUM_JOINTS; i++) {
      receivedValues[i] = values[i].toFloat();
      if (isnan(receivedValues[i])) {
        success = false;
        break;
      }
      receivedValues[i] = constrain(receivedValues[i], 0, 100);
    }

    if (success) {
      for (byte i = 0; i < NUM_JOINTS; i++) {
        byte mappedAngle = map(receivedValues[i], 0, 100, minAngle[i], maxAngle[i]);
        moveToTarget(i, mappedAngle);
      }
    }
  }
}

void servos_config() {
  for (byte i = 0; i < NUM_JOINTS; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(currentPos[i]);
  }
}

void moveToTarget(byte jointIndex, byte targetAngle) {
  targetPos[jointIndex] = constrain(targetAngle, minAngle[jointIndex], maxAngle[jointIndex]);
}

void updateServos() {
  unsigned long currentTime = millis();
  for (byte i = 0; i < NUM_JOINTS; i++) {
    if (currentPos[i] != targetPos[i]) {
      if (currentTime - lastMoveTime[i] >= servoStepDelays[i]) {
        lastMoveTime[i] = currentTime;
        if (currentPos[i] < targetPos[i]) currentPos[i]++;
        else if (currentPos[i] > targetPos[i]) currentPos[i]--;
        servos[i].write(currentPos[i]);
        v_angle[i] = currentPos[i];
        Send_Position();
      }
    }
  }
}

void zeroPosition() {
  for (byte i = 0; i < NUM_JOINTS; i++) {
    moveToTarget(i, zeroPos[i]);
  }
}

void record() {
  for (byte i = 0; i < NUM_JOINTS; i++) {
    record_angles[nxt_motion][i] = currentPos[i];
  }
}

void execute() {
  for (byte i = 0; i < nxt_motion; i++) {
    for (byte j = 0; j < NUM_JOINTS; j++) {
      moveToTarget(j, record_angles[i][j]);
    }
    delay(1000);
  }
}

void Send_Position() {
  Robotic_Arm_Position = "";
  for (byte i = 0; i < NUM_JOINTS; i++) {
    byte mappedAngle = map(v_angle[i], minAngle[i], maxAngle[i], 0, 100);
    Robotic_Arm_Position += String(mappedAngle);
    if (i < NUM_JOINTS - 1) Robotic_Arm_Position += ",";
  }
  Serial.println("A," + Robotic_Arm_Position + ",D");
}
