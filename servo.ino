#include "Arduino.h"
#include <Servo.h>

#define UNITS int

const UNITS INIT_ANGLE = 90;
const UNITS GIANT_STEP = 5;
const UNITS SMALL_STEP = 1;
const int READ_DELAY = 10;

Servo servo[2];
UNITS currentAngle[2];

void setup() {
    servo[0].attach(5);
    servo[1].attach(6);
    Serial.begin(9600);
    for(int i = 0; i < 2; ++i) {
        servo[i].write(INIT_ANGLE);
        currentAngle[i] = INIT_ANGLE;
    }
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
        if(ch == 'l') {
            currentAngle[0] = safeNum(currentAngle[0] - SMALL_STEP);
        }
        if(ch == 'R') {
            currentAngle[0] = safeNum(currentAngle[0] + GIANT_STEP);
        }
        if(ch == 'L') {
            currentAngle[0] = safeNum(currentAngle[0] - GIANT_STEP);
        }
        if(ch == 'u') {
            currentAngle[1] = safeNum(currentAngle[1] + SMALL_STEP);
        }
        if(ch == 'd') {
            currentAngle[1] = safeNum(currentAngle[1] - SMALL_STEP);
        }
        if(ch == 'U') {
            currentAngle[1] = safeNum(currentAngle[1] + GIANT_STEP);
        }
        if(ch == ':') {
            currentAngle[1] = safeNum(currentAngle[1] - GIANT_STEP);
        }
        for(int i = 0; i < 2; ++i) {
            if(currentAngle[i] != lastAngle[i]) {
                servo[i].write(currentAngle[i]);
            }
        }
	}
    delay(READ_DELAY);
}