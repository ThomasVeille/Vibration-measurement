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

> [!NOTE]
> You can also use a power supply 0-5V to change the value between this 2 values and check the different result.

## What does the code do ?

On the **MPU-6050.ino**, you can edit some setting to do the measurement like the **DURATION_SECONDS**.
To have the information of the vibration, first you need to upload the **MPU-6050.ino** code on the ESP32 board.
> [!NOTE]
> You can check the number of the COM use by the card at this moment, you need to know him for next step

> [!WARNING]
> AFTER THE UPLOAD DONE, YOU NEED TO CLOSE THE IDE ARDUINO PAGE !

Now you can open, the file **vibration_capture_analysis.py** file and edit the COM number with the number you read on the IDE ARDUINO. Also, you need to add folder to save the csv file and the graphs on the **OUTPUT_DIR** variable.
At the top of the pyton file, you have the different command to install the different need to do the graphs.
After you can start the script and wait for few minutes. At the end, differents graphs will appears with the analysis.
