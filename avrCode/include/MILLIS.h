#ifndef _MILLIS_H_
#define _MILLIS_H_

volatile unsigned long timer1_millis;

ISR(TIMER1_COMPA_vect);
void MillisInit(unsigned long f_cpu);
unsigned long Millis(void);
double GetDT();
void SetDT(double _dt);
#endif