/*
 * GccApplication3.c
 *
 * Created: 2022-01-05 오전 10:17:24
 * Author : USER
 */ 

#include <avr/io.h>
#define F_CPU 16000000L
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

void DefaultAngleTx(int gx, int gy, int gz, int ax, int ay, int az){
	char gxBuffer[20];
	char gyBuffer[20];
	char gzBuffer[20];
	char axBuffer[20];
	char ayBuffer[20];
	char azBuffer[20];
	char buffer[50] = "";
	
	sprintf(gxBuffer, "%d", gx);
	sprintf(gyBuffer, "%d", gy);
	sprintf(gzBuffer, "%d", gz);
	sprintf(axBuffer, "%d", ax);
	sprintf(ayBuffer, "%d", ay);
	sprintf(azBuffer, "%d", az);
	
	strcat(buffer, gxBuffer);
	strcat(buffer, ",");
	strcat(buffer, gyBuffer);
	strcat(buffer, ",");
	strcat(buffer, gzBuffer);
	strcat(buffer, ",");
	strcat(buffer, axBuffer);
	strcat(buffer, ",");
	strcat(buffer, ayBuffer);
	strcat(buffer, ",");
	strcat(buffer, azBuffer);
	
	for(int i=0; buffer[i] != '\0'; i++){
		UartTransmit(buffer[i]);
	}
	_delay_ms(1);
	
}


int main(void)
{
	UartInit();
    /* Replace with your application code */
	
	//char *getData;
	
	int controll= 2;
	int maxSPD = 110;
	int minSPD = 125;
	float kp = 1.1;
	float ki = 1.2;
	float kd = 1.0;
	
	
	DDRD = (1<<PIND6) | (1<<PIND7);
	DDRB = (1<<PINB0) | (1<<PINB1) | (1<<PINB2) | (1<<PINB3) ;
	TCCR0A = 0x83;
	TCCR0B = 0x02;
	TCCR2A = 0x83;
	TCCR2B = 0x02;
	
    while (1) 
    {
		int cnt = 0;
		char buffer[200]="";
		char type[30]="";
		char motor[30]="";
		char *getData = UartRxStr();
		getData = strtok(getData,",");
		while(getData != NULL){
			if(strcmp("type:setData",type) == 0){
				if(cnt == 1){
					controll = atoi(getData);
				}else if(cnt == 2){
					maxSPD = atoi(getData);
				}else if(cnt == 3){
					minSPD = atoi(getData);
				}else if(cnt == 4){
					kp = atof(getData);
				}else if(cnt == 5){
					ki = atof(getData);
				}else if(cnt == 6){
					kd = atof(getData);
					strcat(buffer,"dataSettings:ok");
				}
				
			}else if(strcmp("type:getData",type) == 0){
				if(cnt == 1){
					char maxSPD_str[20]="";
					char minSPD_str[20]="";
					char controll_str[20]="";
					char kp_str[80]="";
					char ki_str[80]="";
					char kd_str[80]="";
					
					sprintf(maxSPD_str, "%d", maxSPD);
					sprintf(minSPD_str, "%d", minSPD);
					sprintf(controll_str, "%d", controll);
					sprintf(kp_str, "%d", (int)(kp*10));
					sprintf(ki_str, "%d", (int)(ki*10));
					sprintf(kd_str, "%d", (int)(kd*10));
					
					strcat(buffer, "type:responseData,controll:");
					strcat(buffer, controll_str);
					strcat(buffer, ",maxSPD:");
					strcat(buffer, maxSPD_str);
					strcat(buffer, ",minSPD:");
					strcat(buffer, minSPD_str);
					strcat(buffer, ",kp:");
					strcat(buffer, kp_str);
					strcat(buffer, ",ki:");
					strcat(buffer, ki_str);
					strcat(buffer, ",kd:");
					strcat(buffer, kd_str);

					
				}
			
			}else if(strcmp("type:controll",type) == 0){
				if(cnt == 1){
					strcat(motor, getData);
					strcat(buffer,"motorControll:ok");
				}
				
			}else{
				strcpy(type, getData);
			}
			getData = strtok(NULL, ",");
			cnt++;
		}
		
		UartTxStr(buffer);
		//UartTxStr("1.234");
		_delay_ms(100);
		//sprintf(buffer, "%d", cnt);
		if(strcmp("forward",motor)==0){
			OCR0A = 250;
			OCR2A = 250;
			PORTB = (0<<PINB0) | (1<<PINB1) | (0<<PINB2);
			PORTD = (1<<PINB7);
		}else if(strcmp("backward",motor)==0){
			OCR0A = 250;
			OCR2A = 250;
			PORTB = (1<<PINB0) | (0<<PINB1) | (1<<PINB2);
			PORTD = (0<<PINB7);
		}else if(strcmp("rightTurn",motor)==0){
			OCR0A = 200;
			OCR2A = 0;
			PORTB = (0<<PINB0) ;
			PORTD = (1<<PINB7);
		}else if(strcmp("leftTurn",motor)==0){
			OCR0A = 0;
			OCR2A = 200;
			PORTB = (1<<PINB1) | (0<<PINB2);
		}else if(strcmp("done",motor)==0){
			OCR0A = 0;
			OCR2A = 0;
			PORTB = (0<<PINB0) | (0<<PINB1) | (0<<PINB2);
			PORTD = (0<<PINB7);
		}
		
    }
	
}

