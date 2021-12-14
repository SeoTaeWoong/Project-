#ifndef _UART_H_
#define _UART_H_

#include <avr/io.h>

void UartInit(void);
unsigned char UartReceive(void);
void UartTransmit(unsigned char data);
void UartTxStr(char *str);
char* UartRxStr();
void AngleDataTx(int targetAngle, int currentAngle, int outPID);

#endif