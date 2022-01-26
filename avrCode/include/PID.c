/*
 * PID.c
 *
 * Created: 2021-12-13 오후 2:36:58
 *  Author: USER
 */ 
#include "PID.h"
#include "MILLIS.h"
#include "UART.h"

double integral;
double lastAngle;
double pControl, iControl, dControl;
double* myCurrentAngle;
double* myOutput;
double* myTargetAngle;
double kp,ki,kd;
double err;
int limitMin, limitMax;
int sampleTime;
unsigned long lastTime;

void SetGainTunings(double _p,double _i,double _d){
	if(_p < 0 || _i < 0 || _d < 0) return;
	kp = _p;
	ki = _i;
	kd = _d;
	
	double sampleTimeInSec = ((double)sampleTime)/1000;
	
	pControl = _p;
	iControl = _i * sampleTimeInSec;
	dControl = _d / sampleTimeInSec;
	
}

void SetOutputLimits(int min, int max){
	if(min >= max) return;
	limitMax = max;
	limitMin = min;
}

void PIDInit(double* currentAngle, double* output, double* targetAngle,
		 double Kp, double Ki, double Kd){
	sampleTime = 100;
	SetOutputLimits(0,255);
	SetGainTunings(Kp, Ki, Kd);
	lastTime = Millis() - sampleTime;
	myOutput = output;
	myCurrentAngle = currentAngle;
	myTargetAngle = targetAngle;
}

void SetSampleTime(int time){
	sampleTime = time;
}


void PIDCompute(){
	
	unsigned long now = Millis();
	unsigned long time = (now - lastTime);
	if(time >= sampleTime){
		double currentAngle = *myCurrentAngle;
		
		err = *myTargetAngle - currentAngle;
		integral += (ki * err);
		if(integral > limitMax) integral = limitMax;
		else if(integral < limitMin) integral = limitMin;
		double dAngle = currentAngle - lastAngle;
		
		double output = kp * err + integral - kd * dAngle;
		
		if( output > limitMax) output = limitMax;
		else if( output < limitMin) output = limitMin;
		*myOutput = output;
		
		lastAngle = currentAngle;
		lastTime = now;
	}
}

int GetError(){
	return (int)err;
}