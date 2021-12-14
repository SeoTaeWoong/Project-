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


int main(void)
{	
    /* Replace with your application code */
	UartInit();
    //Mpu6050Init();
	//MotorInit();
	//float outPID = 0;

	while(1){
// 		Mpu6050SangboFilter();
		
		UartTxStr(UartRxStr());
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
//		}
		
	}
	return 0;
}

