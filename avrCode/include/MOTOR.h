/*
 * MOTOR.h
 *
 * Created: 2021-12-13 오후 1:18:05
 *  Author: USER
 */ 
#ifndef _MOTOR_H_
#define _MOTOR_H_

void MotorInit();
void MotorLeftPWM(int pwm, int motorDirection1, int motorDirection2);
void MotorRightPWM(int pwm, int motorDirection1, int motorDirection2);

#endif