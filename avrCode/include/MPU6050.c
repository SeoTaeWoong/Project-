#define F_CPU 16000000L

#include <avr/interrupt.h>
#include <util/delay.h>
#include "MPU6050.h"
#include "MILLIS.h"


// Convert gyro values to degrees/sec
#define FS_SEL (32767 / 250) // 1도/s  = 131
#define RADIANS_TO_DEG (180/3.141592)

void Mpu6050Init();
void Mpu6050Write(unsigned char addr, unsigned char data);
unsigned char Mpu6050Read(char addr);
void Mpu6050GetRawData();
void Mpu6050Calibration();
void Mpu6050SetLastReadAngleData(unsigned long time,float axAngle,float ayAngle,float azAngle, float gxAngle, float gyAngle, float gzAngle);
void setAngles(float angleX, float angleY, float angleZ);

unsigned long last_readTime;
float last_axAngle, last_ayAngle, last_azAngle, last_gxAngle, last_gyAngle, last_gzAngle;
float base_ax, base_ay, base_az, base_gx, base_gy, base_gz;
float ax, ay, az, gx, gy, gz;
float filterAngleX, filterAngleY, filterAngleZ;
float dt;



inline unsigned long get_last_time(){return last_readTime;}
inline float get_last_axAngle(){return last_axAngle;}
inline float get_last_ayAngle(){return last_ayAngle;}
inline float get_last_azAngle(){return last_azAngle;}
inline float get_last_gxAngle(){return last_gxAngle;}
inline float get_last_gyAngle(){return last_gyAngle;}
inline float get_last_gzAngle(){return last_gzAngle;}

void Mpu6050Init(){
	TWCR = 0x04; //TWI활성화
	TWSR = 0x00; //Prescaler : 1, 상태초기화
	TWBR = 0x12; // 0b00001100, Fscl = 400KHZ(Fcpu/(16+2*TWBR*Prescaler) = F
	Mpu6050Write(0x6B, 0x00); //센서 ON
	Mpu6050Write(0x6C, 0x00);
	Mpu6050Write(0x1B, 0x08); // gyro set - 500/s로 설정
	Mpu6050Write(0x1A, 0x05); // DLPF 10Hz로 설정
	Mpu6050GetRawData();
 	Mpu6050Calibration();
 	MillisInit(F_CPU);
 	sei();
 	Mpu6050SetLastReadAngleData(Millis(),0,0,0,0,0,0);
}

//--------- MPU6050 ---------------------------------------
void Mpu6050Write(unsigned char addr, unsigned char data){ //자이로센서 설정
	TWCR = 0xA4; // TWINT TWSTA TWEN , 인터럽트 START BIT 활성화
	while((TWCR&0x80)==0x00); //전송 대기 TWINT
	while((TWSR&0xF8)!=0x08); //수신 대기

	TWDR=0xD0; //AD+W 저장
	TWCR=0x84; //전송
	while((TWCR&0x80)==0x00); //전송대기
	while((TWSR&0xF8)!=0x18); //ACK대기
	
	TWDR=addr; // RA
	TWCR=0x84; // 전송
	while((TWCR&0x80)==0x00);
	while((TWSR&0xF8)!=0x28); // ACK
	
	//---------------------------------------
	
	TWDR=data; // DATA
	TWCR=0x84; // 전송
	while((TWCR&0x80)==0x00);
	while((TWSR&0xF8)!=0x28); // ACK
	
	TWCR|=0x94; // P
	_delay_us(50);  // 50us
	
}


unsigned char Mpu6050Read(char addr) //자이로 센서 값 읽어오기
{
	unsigned char data; // data넣을 변수
	
	TWCR=0xA4; // S
	while((TWCR&0x80)==0x00); //통신대기
	while((TWSR&0xF8)!=0x08); //신호대기
	
	TWDR=0xD0; // AD+W
	TWCR=0x84; // 전송
	while((TWCR&0x80)==0x00); //통신대기
	while((TWSR&0xF8)!=0x18); //ACK
	
	TWDR=addr; // RA
	TWCR=0x84; //전송
	while((TWCR&0x80)==0x00); //통신대기
	while((TWSR&0xF8)!=0x28); //ACK
	TWCR=0xA4; // RS
	//----------------------------------

	while((TWCR&0x80)==0x00); //통신대기
	while((TWSR&0xF8)!=0x10); //ACK
	TWDR=0xD1; // AD+R
	TWCR=0x84; //전송

	while((TWCR&0x80)==0x00); //통신대기
	while((TWSR&0xF8)!=0x40); // ACK
	TWCR=0x84;//전송

	while((TWCR&0x80)==0x00); //통신대기
	while((TWSR&0xF8)!=0x58); //ACK
	data=TWDR;
	TWCR=0x94; // P
	_delay_us(50);  // 50us
	return data;
}


void Mpu6050GetRawData(){
	unsigned char mpuBuffer[13];
	
	mpuBuffer[0] = Mpu6050Read(0x3B);
	mpuBuffer[1] = Mpu6050Read(0x3C);
	mpuBuffer[2] = Mpu6050Read(0x3D);
	mpuBuffer[3] = Mpu6050Read(0x3E);
	mpuBuffer[4] = Mpu6050Read(0x3F);
	mpuBuffer[5] = Mpu6050Read(0x40);
	
	mpuBuffer[6] = Mpu6050Read(0x43);
	mpuBuffer[7] = Mpu6050Read(0x44);
	mpuBuffer[8] = Mpu6050Read(0x45);
	mpuBuffer[9] = Mpu6050Read(0x46);
	mpuBuffer[10] = Mpu6050Read(0x47);
	mpuBuffer[11] = Mpu6050Read(0x48);
	
	ax = (int)mpuBuffer[0] << 8 | (int)mpuBuffer[1];
	ay = (int)mpuBuffer[2] << 8 | (int)mpuBuffer[3];
	az = (int)mpuBuffer[4] << 8 | (int)mpuBuffer[5];
	gx = (int)mpuBuffer[6] << 8 | (int)mpuBuffer[7];
	gy = (int)mpuBuffer[8] << 8 | (int)mpuBuffer[9];
	gz = (int)mpuBuffer[10] << 8 | (int)mpuBuffer[11];
}

void Mpu6050SetLastReadAngleData(unsigned long time,float axAngle,float ayAngle,float azAngle, float gxAngle, float gyAngle, float gzAngle){
	last_readTime = time;
	last_axAngle=axAngle;
	last_ayAngle=ayAngle;
	last_azAngle=azAngle;
	last_gxAngle=gxAngle;
	last_gyAngle=gyAngle;
	last_gzAngle=gzAngle;
}

void Mpu6050Calibration(){
	
	int num_readings = 10;
	float accelX = 0;
	float accelY = 0;
	float accelZ = 0;
	
	float gyroX = 0;
	float gyroY = 0;
	float gyroZ = 0;
	
	Mpu6050GetRawData();
	
	for(int i = 0; i< num_readings; i++){
		Mpu6050GetRawData();
		accelX += ax;
		accelY += ay;
		accelZ += az;
		
		gyroX += gx;
		gyroY += gy;
		gyroZ += gz;
		_delay_ms(100);
	}
	accelX /= num_readings;
	accelY /= num_readings;
	accelZ /= num_readings;
	
	gyroX /= num_readings;
	gyroY /= num_readings;
	gyroZ /= num_readings;
	
	base_ax = accelX;
	base_ay = accelY;
	base_az = accelZ;
	base_gx = gyroX;
	base_gy = gyroY;
	base_gz = gyroZ;
}

void Mpu6050SangboFilter(){
	Mpu6050GetRawData();
	unsigned long t_now = Millis();
	
	float gyro_x = (gx - base_gx)/FS_SEL;
	float gyro_y = (gy - base_gy)/FS_SEL;
	float gyro_z = (gz - base_gz)/FS_SEL;
	
	float accel_x = ax;
	float accel_y = ay;
	float accel_z = az;
	
	float accel_angle_y = atan(-1*accel_x/sqrt(pow(accel_y,2) + pow(accel_z,2)))*RADIANS_TO_DEG;
	float accel_angle_x = atan(accel_y/sqrt(pow(accel_x,2) + pow(accel_z,2)))*RADIANS_TO_DEG;
	float accel_angle_z = 0;
	
	dt = (t_now - get_last_time())/1000.0;
	SetDT(dt);
	float gyro_angle_x = gyro_x*dt + get_last_axAngle();
	float gyro_angle_y = gyro_y*dt + get_last_ayAngle();
	float gyro_angle_z = gyro_z*dt + get_last_azAngle();

	float unfilter_gyro_angle_x = gyro_x*dt + get_last_gxAngle();
	float unfilter_gyro_angle_y = gyro_y*dt + get_last_gyAngle();
	float unfilter_gyro_angle_z = gyro_z*dt + get_last_gzAngle();

	float alpha = 0.96;
	float angleX = alpha*gyro_angle_x + (1.0 - alpha)*accel_angle_x;
	float angleY = alpha*gyro_angle_y + (1.0 - alpha)*accel_angle_y;
	float angleZ = gyro_angle_z;

	Mpu6050SetLastReadAngleData(t_now, angleX, angleY, angleZ, unfilter_gyro_angle_x, unfilter_gyro_angle_y, unfilter_gyro_angle_z);	
	
	//setAngles(gx - base_gx, gyro_y, gyro_z);
	setAngles(angleX, angleY, angleZ);
}

void setAngles(float angleX, float angleY, float angleZ){
	filterAngleX = angleX;
	filterAngleY = angleY;
	filterAngleZ = angleZ;
}

int GetMpu6050FilterAngleX(){
	return (int)filterAngleX;
}

int GetMpu6050FilterAngleY(){
	return (int)filterAngleY;
}

int GetMpu6050FilterAngleZ(){
	return (int)filterAngleZ;
}

