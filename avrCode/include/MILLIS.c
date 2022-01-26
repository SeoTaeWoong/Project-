#include <avr/io.h>
#include <util/atomic.h>
#include <avr/interrupt.h>

#include "MILLIS.h"
double dt;

ISR(TIMER1_COMPA_vect){
	timer1_millis++;
}

void MillisInit(unsigned long f_cpu){
	unsigned long ctc_match_overflow;
	ctc_match_overflow = ((f_cpu/1000)/8);
	TCCR1B |= (1 << WGM12) | (1 << CS11);
	
	OCR1AH = (ctc_match_overflow >>8);
	OCR1AL = ctc_match_overflow;
	
	TIMSK1 |= (1 << OCIE1A);
}

unsigned long Millis(void){
	unsigned long millis_return;
	
	ATOMIC_BLOCK(ATOMIC_FORCEON){
		millis_return = timer1_millis;
	}
	return millis_return;
}

void SetDT(double _dt){
	dt = _dt;
}

double GetDT(){
	return dt;	
}