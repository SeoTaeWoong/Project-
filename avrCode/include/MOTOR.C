/*
 * MOTOR.C
 *
 * Created: 2021-12-13 오후 1:18:45
 *  Author: USER
 */ 
#include <avr/io.h>
#include "MOTOR.h"

void MotorInit(){
	DDRD |= (1<<PIND5) | (1<<PIND6) | (1<<PIND3);
	DDRB |= (1<<PINB3);
	TCCR0A = 0x83;
	TCCR0B = 0x02;
	TCCR2A = 0x83;
	TCCR2B = 0x02;
}

void MotorLeftPWM(int pwm, int motorDirection1, int motorDirection2){
	PORTD |= (motorDirection1 << PIND5) | (motorDirection2 << PIND6);
	OCR0A = pwm;
}

void MotorRightPWM(int pwm, int motorDirection1, int motorDirection2){
	PORTB = (motorDirection1 << PINB3);
	PORTD |= (motorDirection2 << PIND3);
	OCR2A = pwm;
}