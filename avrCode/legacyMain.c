#define F_CPU 16000000L
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "include/UART.h"
#include "include/MILLIS.h"
#include "include/MPU6050.h"
#include "include/PID.h"
#include "include/MOTOR.h"


double output;
double currentAngle;
double targetAngle = 0;
double Kp = 20.0;
double Ki = 150.0;
double Kd = 1.2;

int main(void)
{	
    /* Replace with your application code */
	MillisInit(F_CPU);
	sei();
	PIDInit(&currentAngle, &output, &targetAngle,Kp, Ki, Kd);
	UartInit();
    Mpu6050Init();
	MotorInit();
	//char * getControll;
	int minSPD = 90;
	//PID
	SetSampleTime(2);
	SetOutputLimits(-255,255);
// 	DDRD |= (1<<PIND6) | (1<<PIND7);
// 	DDRB |= ( 1<< PINB0) | ( 1<< PINB1) | (1<<PINB2) | (1<<PINB3);
// 	TCCR0A = 0x83;
// 	TCCR0B = 0x02;
// 	TCCR2A = 0x83;
// 	TCCR2B = 0x02;	
	unsigned prevTime = Millis();
	while(1){
// 		PORTD = (1 << PIND7);
// 		PORTB = ( 0 << PINB0) | ( 1<< PINB1) | (0<<PINB2)
// 		OCR0A = 255;
// 		OCR2A = 255;
 		Mpu6050SangboFilter(); 
 		currentAngle = GetMpu6050FilterAngleX();
 		PIDCompute();
 		MotorMove((int)output, minSPD);
 		
// 		DefaultAngleTx(GetMpu6050DefaultGyroX(),GetMpu6050DefaultGyroY(),GetMpu6050DefaultGyroZ(),GetMpu6050DefaultAccX(),GetMpu6050DefaultAccY(),GetMpu6050DefaultAccZ());
//		_delay_ms(10);		
		AngleDataTx(currentAngle, Kp, Ki);
		unsigned currentTime = Millis()-prevTime;
// 		if(currentTime > 500){
// 			char* getData =  UartRxStr();
// 			getData = strtok(getData,",");
// 			int cnt = 0;
// 			while(getData != NULL){
// 				if(cnt == 0){
// 					Kp = atof(getData);
// 				}else if(cnt == 1){
// 					Ki = atof(getData);
// 				}else if(cnt == 2){
// 					Kd = atof(getData);
// 				}
// 				getData = strtok(NULL, ",");
// 				cnt++;
// 			}
// 			prevTime = Millis();
// 			SetGainTunings(Kp, Ki, Kd);
// 			AngleDataTx(currentAngle, Kp, Ki);
// 		}


//		getControll = UartRxStr();
// 		switch(getControll){
// 			case "forward":
// 				int targetAngle = 30; // 원하는각도
// 				int currentAngle = GetMpu6050FilterAngleX(); //현재 각도
// 				
// 				AngleDataTx(targetAngle, currentAngle, (int)outPID);
// 				SetPidGain(1,1,1);
// 				
// 				outPID = PID(targetAngle, currentAngle);
// 				
// 				if(outPID > 200) {outPID = 200;}
// 				if(outPID < 100) {outPID = 100;}
// 				if(currentAngle > 50 || currentAngle < -50){ outPID = 0;}
// 				
// 				MotorLeftPWM(outPID, 1,0);
// 				MotorRightPWM(outPID, 1,0);
// 				break;
// 			case "backward":
// 				int targetAngle = -30; // 원하는각도
// 				int currentAngle = GetMpu6050FilterAngleX(); //현재 각도
// 				
// 				AngleDataTx(targetAngle, currentAngle, (int)outPID);
// 				SetPidGain(1,1,1);
// 				
// 				outPID = PID(targetAngle, currentAngle);
// 				
// 				if(outPID > 200) {outPID = 200;}
// 				if(outPID < 100) {outPID = 100;}
// 				if(currentAngle > 50 || currentAngle < -50){ outPID = 0;}
// 				
// 				MotorLeftPWM(outPID, 0,1);
// 				MotorRightPWM(outPID, 0,1);
// 				break;
// 			case "leftTurn":
// 				int targetAngle = 30; // 원하는각도
// 				int currentAngle = GetMpu6050FilterAngleX(); //현재 각도
// 				
// 				AngleDataTx(targetAngle, currentAngle, (int)outPID);
// 				SetPidGain(1,1,1);
// 				
// 				outPID = PID(targetAngle, currentAngle);
// 				
// 				if(outPID > 200) {outPID = 200;}
// 				if(outPID < 100) {outPID = 100;}
// 				if(currentAngle > 50 || currentAngle < -50){ outPID = 0;}
// 				
// 				MotorLeftPWM(outPID, 0,1);
// 				MotorRightPWM(outPID, 1,0);
// 				
// 				break;
// 			case "rightTurn":
// 				int targetAngle = 30; // 원하는각도
// 				int currentAngle = GetMpu6050FilterAngleX(); //현재 각도
// 				
// 				AngleDataTx(targetAngle, currentAngle, (int)outPID);
// 				SetPidGain(1,1,1);
// 				
// 				outPID = PID(targetAngle, currentAngle);
// 				
// 				if(outPID > 200) {outPID = 200;}
// 				if(outPID < 100) {outPID = 100;}
// 				if(currentAngle > 50 || currentAngle < -50){ outPID = 0;}
// 				
// 				MotorLeftPWM(outPID, 1,0);
// 				MotorRightPWM(outPID, 0,1);
// 				break;
// 			case "done":
// 			
// 				break;
// 		}
	}
	return 0;
}

