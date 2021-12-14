#ifndef _MPU6050_H_
#define _MPU6050_H_

#include <avr/io.h>

int GetMpu6050FilterAngleX();
int GetMpu6050FilterAngleY();
int GetMpu6050FilterAngleZ();


void Mpu6050Init();
void Mpu6050SangboFilter();

#endif