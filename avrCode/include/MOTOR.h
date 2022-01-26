/*
 * MOTOR.h
 *
 * Created: 2021-12-13 오후 1:18:05
 *  Author: USER
 */ 
#ifndef _MOTOR_H_
#define _MOTOR_H_

void MotorInit();
void MotorMove(int speed, int minSPD);
int GetCurrentSpeed();

#endif