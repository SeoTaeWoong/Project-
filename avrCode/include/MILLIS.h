#ifndef _MILLIS_H_
#define _MILLIS_H_

volatile unsigned long timer1_millis;

ISR(TIMER1_COMPA_vect);
void MillisInit(unsigned long f_cpu);
unsigned long Millis(void);
float GetDT();
void SetDT(float _dt);
#endif