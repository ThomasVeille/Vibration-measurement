# VIBRATION MEASUREMENT

## Overview

This projet allow to measure some vibration with the MPU-6050 sensor and analyse the data of the measurement. A Python script is use to do the analyse and to do different graph of the the axes.

## Connection with the ESP32 board

### A-MPU-6050 

| MPU-6050 | ESP32 Pin |
|--------------------|--------|
|**VCC**              | 3V3     |
|**GND**              | GND     |
|**SDA**              | SD0     |
|**SCL**              | SL0     |

### B-Motor 

| Motor | ESP32 Pin |
|--------------------|--------|
|**VCC**              | 5V     |
|**GND**              | GND     |

## What does the code do ?

To have the information of the vibration, first you need to upload the **MPU-6050.ino** code on the ESP32 board.
> [!NOTE]
> You can check the number of the COM use by the card at this moment, you need to know him for next step

> [!WARNING]
> AFTER THE UPLOAD DONE, YOU NEED TO CLOSE THE IDE ARDUINO PAGE !

Now you can open, the file **vibration_capture_analysis.py** file and edit the COM number with the number you read on the IDE ARDUINO. At the top of the pyton file, you have the different command to install the different need to do the graphs.
