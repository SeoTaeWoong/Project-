/*
 * PID.h
 *
 * Created: 2021-12-13 오후 2:36:45
 *  Author: USER
 */ 
#ifndef _PID_H_
#define _PID_H_

void PIDCompute();
void SetGainTunings(double _p,double _i,double _d);
void SetOutputLimits(int min, int max);
void PIDInit(double* currentAngle, double* output, double* targetAngle, double Kp, double Ki, double Kd);
void SetSampleTime();
int GetError();

#endif