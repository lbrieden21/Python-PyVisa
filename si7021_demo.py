#!/usr/bin/env python
#import smbus, ic_msg
from smbus2 import SMBusWrapper, i2c_msg
import time
import csv

with SMBusWrapper(1) as bus:
    # SI7021 address, 0x40
    # 0xE6 Write User Register, 0xBB - 1011 1011 - RH 11bit, Temp 11bit, Heater Off
    # msg = i2c_msg.write(0x40, [0xE6,0xBB])
    # bus.i2c_rdwr(msg)
    # time.sleep(0.3)

# Get I2C bus
# bus = smbus.SMBus(1)

    startTime = time.time()
    currentTime = startTime

    runTime = 10 # time to run test in seconds
# runTime = 60 * 60 * 24 # 1 day

    fileName = 'SI7021_tempAndHumidityData_' + str(int(startTime)) + '.csv'
    with open(fileName, 'w', newline='') as csvfile:
        dataWriter = csv.writer(csvfile, delimiter = ',')
        dataWriter.writerow(['Time (seconds)', 'Relative Humidity %', 'Celsius', 'Fahrenheit'])
        while currentTime < startTime + runTime:
            currentTime = int(time.time())

            # SI7021 address, 0x40
            # 0xE7 Read User Register
            # bus.write_byte(0x40, 0xE7)
            # time.sleep(0.3)
            # Read register data back, 1 byte
            # userReg = bus.read_byte(0x40)
            # print("UserReg: %s" %userReg)
            # time.sleep(0.5)

            # SI7021 address, 0x40
            # 0xF5 Select Relative Humidity NO HOLD Master Mode
            bus.write_byte(0x40, 0xF5)
            time.sleep(0.3)

            # Read data back, 2 bytes, Humidity MSB first
            data0 = bus.read_byte(0x40)
            data1 = bus.read_byte(0x40)

            # Convert the data
            humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
            # humidity = round(humidity, 2)

            # 0xE0 Grab temperature measurement that was made for RH measurement
            bus.write_byte(0x40, 0xE0)
            time.sleep(0.3)

            # Read data back, 2 bytes, Temperature MSB first
            data0 = bus.read_byte(0x40)
            data1 = bus.read_byte(0x40)

            # Convert the data
            cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
            fTemp = cTemp * 1.8 + 32
            # cTemp = round(cTemp, 2)
            # fTemp = round(fTemp, 2)

            print ("%d, %.2f%%, %.2fC, %.2fF" % (currentTime,humidity,cTemp,fTemp))
            dataWriter.writerow([currentTime, humidity, cTemp, fTemp])
            time.sleep(0.4)
