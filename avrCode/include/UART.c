#define F_CPU 16000000L

#include "UART.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <util/delay.h>

void UartInit(){
	UCSR0A |= (1<<U2X0);
	UBRR0H = 0x00;
	UBRR0L = 16;
	
	UCSR0C |= 0x06;
	UCSR0B |= (1 << RXEN0);
	UCSR0B |= (1 << TXEN0);
}

unsigned char UartReceive(void){
	while (!(UCSR0A & (1<<RXC0)));
	return UDR0;
}
void UartTransmit(unsigned char data){
	while(!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}
void UartTxStr(char *str){
	for(int i=0; str[i]!='\0'; i++){
		UartTransmit(str[i]);	
	}
}

char getDatas[30];
char* UartRxStr(){
	
	int index = 0;
	unsigned char data;

	
	while(1){
		data = UartReceive();
		if(data == '\0'){
			getDatas[index] = '\0';
			break;
		}else{
			getDatas[index] = data;
			index++;
			//UartTransmit(data);
		}
	}
	//UartTxStr(buffer);
	return getDatas;
}

void AngleDataTx(int targetAngle, int currentAngle, int outPID){
	char tAngle[20];
	char cAngle[20];
	char oPID[10];
	char buffer[50] = "";
	sprintf(tAngle, "%d", targetAngle);
	sprintf(cAngle, "%d", currentAngle);
	sprintf(oPID, "%d", outPID);
	
	strcat(buffer, tAngle);
	strcat(buffer, ",");
	strcat(buffer, cAngle);
	strcat(buffer, ",");
	strcat(buffer, oPID);
	
	for(int i=0; buffer[i] != '\0'; i++){
		UartTransmit(buffer[i]);
	}
	_delay_ms(1);
}