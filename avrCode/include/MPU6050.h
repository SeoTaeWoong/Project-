#ifndef _MPU6050_H_
#define _MPU6050_H_

#include <avr/io.h>

double GetMpu6050FilterAngleX();
double GetMpu6050FilterAngleY();
double GetMpu6050FilterAngleZ();

int GetMpu6050DefaultAccX();
int GetMpu6050DefaultAccY();
int GetMpu6050DefaultAccZ();

int GetMpu6050DefaultGyroX();
int GetMpu6050DefaultGyroY();
int GetMpu6050DefaultGyroZ();


void Mpu6050Init();
void Mpu6050SangboFilter();

#endif