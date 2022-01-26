/*
 * MOTOR.C
 *
 * Created: 2021-12-13 오후 1:18:45
 *  Author: USER
 */ 

#include <avr/io.h>
#include "MOTOR.h"

#define MIN(a ,b) (a < b ? a : b)
#define MAX(a ,b) (a > b ? a : b)
#define ABS(a) ( a < 0 ? -a : a)

int currentSpeed;
double leftMotorSpeedFactor = 1.0;
double rightMotorSpeedFactor = 1.0;
void MotorInit(){
	DDRD |= (1<<PIND6) | (1<<PIND7);
	DDRB |= ( 1<< PINB0) | ( 1<< PINB1) | (1<<PINB2) | (1<<PINB3);
	TCCR0A = 0x83;
	TCCR0B = 0x02;
	TCCR2A = 0x83;
	TCCR2B = 0x02;
}

void MotorDirection(int speed){
	int leftMD1 = speed > 0? 0 : 1;
	int leftMD2 = speed > 0? 1 : 0;
	int rightMD1 = speed > 0? 0 : 1;
	int rightMD2 = speed > 0? 1 : 0;
	
// 	int leftMD1 = speed > 0? 1 : 0;
// 	int leftMD2 = speed > 0? 0 : 1;
// 	int rightMD1 = speed > 0? 1 : 0;
// 	int rightMD2 = speed > 0? 0 : 1;
	
	//양수 1010
	//음수 0101
	PORTD = (leftMD1 << PIND7);
	PORTB = ( leftMD2 << PINB0) | ( rightMD1<< PINB1) | (rightMD2<<PINB2);
}

void MotorLeftPWM(int pwm){
// 	PORTD = (0 << PIND5) | (1 << PIND6) | (0 << PIND3);
// 	PORTB = (1 << PINB3);
	OCR0A = pwm;
}

void MotorRightPWM(int pwm){
	OCR2A = pwm;
}

void MotorMove(int speed, int minSPD){
	int direction = 1;
	
	if(speed < 0){
		direction = -1;
		
		speed = MIN(speed, -1*minSPD);
		speed = MAX(speed, -255);	
	}else{
		speed = MAX(speed, minSPD);
		speed = MIN(speed, 255);
	}
	
	if(speed == currentSpeed) return;
	
	int realSpeed = MAX(minSPD, ABS(speed));
	
	MotorDirection(speed);

	MotorLeftPWM((int)(realSpeed * leftMotorSpeedFactor));
	MotorRightPWM((int)(realSpeed * rightMotorSpeedFactor));	

	
	currentSpeed = direction * realSpeed;
}

int GetCurrentSpeed(){
	return currentSpeed;
}