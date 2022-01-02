#include "Arduino.h"
#include <Servo.h>

#define UNITS double

const UNITS INIT_ANGLE = 90;
const UNITS GIANT_STEP = 5;
const UNITS SMALL_STEP = 0.5;
const int READ_DELAY = 10;

Servo servo[2];
UNITS currentAngle[2];
UNITS cruiseStep = GIANT_STEP;

int in1 = 2, in2 = 3;

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

void setup() {
  servo[0].attach(A0);
  servo[1].attach(A1);
  
  for(int i = 0; i < 2; ++i) {
    servo[i].write(INIT_ANGLE);
    currentAngle[i] = INIT_ANGLE;
  }
  
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  
  Serial.begin(9600);
}

UNITS safeNum(UNITS x) {
  if(x < 0) return 0;
  if(x > 180) return 180;
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
      currentAngle[0] = safeNum(currentAngle[0] + SMALL_STEP);
    }
    else if(ch == 'l') {
      currentAngle[0] = safeNum(currentAngle[0] - SMALL_STEP);
    }
    else if(ch == 'R') {
      currentAngle[0] = safeNum(currentAngle[0] + GIANT_STEP);
    }
    else if(ch == 'L') {
      currentAngle[0] = safeNum(currentAngle[0] - GIANT_STEP);
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
    else if(ch == 'o') {
      currentAngle[0] = currentAngle[1] = INIT_ANGLE;
    }
    else if(ch == 'c') {
      currentAngle[0] = safeNum(currentAngle[0] + cruiseStep);
      if(currentAngle[0] == 0 || currentAngle[0] == 180) {
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

    for(int i = 0; i < 2; ++i) {
      if(currentAngle[i] != lastAngle[i]) {
        servo[i].write(currentAngle[i]);
      }
    }
  }
  delay(READ_DELAY);
}

