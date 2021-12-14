/*
 * PID.c
 *
 * Created: 2021-12-13 오후 2:36:58
 *  Author: USER
 */ 
#include "PID.h"
#include "MILLIS.h"
#include "UART.h"

float integral;
float preAngle;
float pControl, iControl, dControl;
float kP,kI,kD;

void SetPidGain(float _p,float _i,float _d){
	kP = _p;
	kI = _i;
	kD = _d;
}

float PID(float targetAngle, int currentAngle){
	
	float err = targetAngle - currentAngle;
	pControl = kP * err;
	
	integral += err * GetDT();
	iControl = kI * integral;
	
	float dAngle = currentAngle - preAngle;
	dControl = -kD*(dAngle/GetDT());
	preAngle = currentAngle;
	
	float u = pControl + iControl + preAngle;
	
	
	
	return (u+127);
}