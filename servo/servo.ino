#include "Arduino.h"
#include <Servo.h>

#define UNITS double

const UNITS INIT_ANGLE_UD = 105;
const UNITS INIT_ANGLE_LR = 100;
const UNITS GIANT_STEP = 5;
const UNITS SMALL_STEP = 0.5;
const int READ_DELAY = 10;
const UNITS STT_ANGLE = 50;
const UNITS END_ANGLE = 150;

Servo servo[2];
UNITS currentAngle[2];
UNITS cruiseStep = GIANT_STEP;

int in1 = 2, in2 = 3, in3 = 4, in4 = 5;
int shootLevel = 1;

void setPos() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
}

void setNeg() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
}

void setZero() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}

void setOpen() {
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void setClose() {
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void charge() {
  setOpen();
  delay(500 * shootLevel);
  setClose();
}

void setup() {
  servo[0].attach(A0);
  servo[1].attach(A1);
  
  servo[0].write(INIT_ANGLE_LR);
  currentAngle[0] = INIT_ANGLE_LR;
  servo[1].write(INIT_ANGLE_UD);
  currentAngle[1] = INIT_ANGLE_UD;
  
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
  Serial.begin(9600);
}

UNITS safeNum(UNITS x) {
  if(x < STT_ANGLE) return STT_ANGLE;
  if(x > END_ANGLE) return END_ANGLE;
  return x;
}

void loop() {
  if (Serial.available()) {
    char ch = Serial.read();
    UNITS lastAngle[2];
    for(int i = 0; i < 2; ++i) {
      lastAngle[i] = currentAngle[i];
    }
    if(ch == 'r') {
      currentAngle[0] = safeNum(currentAngle[0] - SMALL_STEP);
    }
    else if(ch == 'l') {
      currentAngle[0] = safeNum(currentAngle[0] + SMALL_STEP);
    }
    else if(ch == 'R') {
      currentAngle[0] = safeNum(currentAngle[0] - GIANT_STEP);
    }
    else if(ch == 'L') {
      currentAngle[0] = safeNum(currentAngle[0] + GIANT_STEP);
    }
    else if(ch == 'u') {
      currentAngle[1] = safeNum(currentAngle[1] + SMALL_STEP);
    }
    else if(ch == 'd') {
      currentAngle[1] = safeNum(currentAngle[1] - SMALL_STEP);
    }
    else if(ch == 'U') {
      currentAngle[1] = safeNum(currentAngle[1] + GIANT_STEP);
    }
    else if(ch == 'D') {
      currentAngle[1] = safeNum(currentAngle[1] - GIANT_STEP);
    }
    else if(ch == 'O') {
      currentAngle[1] = INIT_ANGLE_UD;
    }
    else if(ch == 'o') {
      currentAngle[0] = INIT_ANGLE_LR;
      currentAngle[1] = INIT_ANGLE_UD;
    }
    else if(ch == 'p') {
      currentAngle[0] = safeNum(currentAngle[0] + cruiseStep);
      if(currentAngle[0] == STT_ANGLE || currentAngle[0] == END_ANGLE) {
        cruiseStep = -cruiseStep;
      }
    }
    else if(ch == 'f') {
      setPos();
    }
    else if(ch == 'b') {
      setNeg();
    }
    else if(ch == 's') {
      setZero();
    }
    else if(ch == 'c') {
      charge();
    }
    else if(ch >= '1' && ch <= '5') {
      shootLevel = ch - '0';
    }

    for(int i = 0; i < 2; ++i) {
      if(currentAngle[i] != lastAngle[i]) {
        servo[i].write(currentAngle[i]);
      }
    }
  }
  delay(READ_DELAY);
}

