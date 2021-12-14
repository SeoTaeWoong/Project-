/*
 * PID.h
 *
 * Created: 2021-12-13 오후 2:36:45
 *  Author: USER
 */ 
#ifndef _PID_H_
#define _PID_H_

float PID(float targetAngle, int currentAngle);
void SetPidGain(float _p,float _i,float _d);

#endif