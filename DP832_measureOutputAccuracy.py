#!/usr/bin/env python
import pyvisa as visa
import time
import datetime
import os
import DP832 as psu
import SDM3055 as dmm
from decimal import *

#--------------------------GLOBAL VARIABLES------------------------------------------
dmmModel = dmm.getModel()
psuModel = psu.getModel()
cmdDelay = Decimal('0.01') #delay in seconds (10 ms)
measDelay = Decimal('1') #delay in seconds to wait before starting dmm measurement, less than 1 seems to make DP832 read previous set value
pChan = 1 # channel to test
voltMin = Decimal('0.000')
voltMax = Decimal('32.000')
voltStep = Decimal('0.001')
currentLimit = Decimal('0.020') # set to something high enough that we don't current limit, but low enough incase something goes wrong
overCurrentLimit = Decimal('0.020') # set to same as currentLimit for now, for if we've reached currentLimit something has gone wrong
dmmMeasureMode = "average"  # take a single measurement, or multiple measurements and take average
dmmMeasureCount = 10 # if multiple measurements, take this many measurements for each voltage setting
load = 'open' # load measuring across, open for no load hooked directly to meter

#--------------------------GENERAL FUNCTIONS-----------------------------------------

def iteration(start, end, step):		#define a for loop function
    while start <= end:
        yield start
        start += step

#--------------------------------MAIN------------------------------------------------
time.sleep(1)
startTime = datetime.datetime.now()

# Open two files for writing results, file1 will be final complete file while file2 will be temporary
# file for holding measurement data incase we crash in middle of run so we don't lose data
fname = dmmModel + "_" + psuModel + "_CH" + str(pChan) + "_voltages_" + str(startTime.strftime('%Y%m%d%H%M%S'))
fname1 = fname + ".csv"
fname2 = fname + "_tempData.csv"
file1 = open(fname1, "w")
file2 = open(fname2, "w+")
# Log same basic info about test set up
file1.write("Test Setup Parameters\n")
file1.write("DMM Model: " + dmmModel + "\n")
file1.write("PSU Model: " + psuModel + "\n")
file1.write("PSU Channel: " + str(pChan) + "\n")
file1.write("Load: " + load + "\n")
file1.write("voltMin: " + str(voltMin) + "\n")
file1.write("voltMax: " + str(voltMax) + "\n")
file1.write("voltStep: " + str(voltStep) + "\n")
file1.write("currentLimit: " + str(currentLimit) + "\n")
file1.write("overCurrentLimit: " + str(overCurrentLimit) + "\n")
file1.write("dmmMeasureMode: " + dmmMeasureMode + "\n")
file1.write("dmmMeasureCount: " + str(dmmMeasureCount) + "\n")
file1.write("cmdDelay: " + str(cmdDelay) + "\n")
file1.write("measDelay: " + str(measDelay) + "\n")
file1.write("startTime: " + str(startTime) + "\n")

# write data header line
if(dmmMeasureMode == 'average'):
    file2.write("SetVoltage,PsuMeasureVoltage,DmmAverageVoltage,DmmMinimumVoltage,DmmMaximumVoltage,DmmStandardDeviation\n")
else:
    file2.write("SetVoltage,PsuMeasureVoltage,DmmMeasureVoltage\n")

initialTemp = psu.sysTemp()
#Initialize DMM (set to measure voltage auto ranging)
dmm.confV();

#Initialize PSU (set test channel off, 0V, OVP OFF, currentLimit, overCurrentLimit, OCP ON)
psu.selOutput(pChan)
psu.toggleOutput(pChan,'OFF')
psu.setVoltage(pChan,0)
psu.toggleOVP('OFF') # make sure OVP off
psu.setCurrent(pChan,currentLimit) # should be set to something reasonable incase something goes wrong
psu.setOCP(pChan,overCurrentLimit) # should be set to something reasonable incase something goes wrong
psu.toggleOCP('ON') # make sure OCP off
psu.toggleOutput(pChan,'ON')

for v in iteration(voltMin,voltMax,voltStep):
    psu.setVoltage(pChan,v)
    time.sleep(measDelay)
    psuReading = psu.measVolt(pChan)
    if(dmmMeasureMode == 'single'):
        dmmReading = dmm.measV('DC')
        #dmmReading = round(dmmReading, dmm.calcDigits(dmmReading))
        line = '%(setVolt)s,%(psuReading)s,%(dmmReading)s' %{'setVolt':v, 'psuReading':psuReading, 'dmmReading':dmmReading}
        print("Voltage Setting: " + str(v) + " V\tPSU Reading: " + str(psuReading) + " V\tDMM Reading: " + str(dmmReading) + "V")
        file2.write(line + "\n")
    if(dmmMeasureMode == 'average'):
        dmmAverageStats = dmm.measVoltStatistics(dmmMeasureCount)
        line = '%(setVolt)s,%(psuReading)s,%(measAvg)s,%(measMin)s,%(measMax)s,%(measStdDev)s' %{'setVolt':v, 'psuReading':psuReading, 'measAvg':dmmAverageStats['average'],
                'measMin':dmmAverageStats['minimum'], 'measMax':dmmAverageStats['maximum'], 'measStdDev':dmmAverageStats['stddev']}
        print("Voltage Setting: " + str(v) + " V\tPSU Reading: " + str(psuReading) + " V\tDMM Reading: " + str(dmm.convertResult(dmmAverageStats['average'])) + " V")
        file2.write(line + "\n")

    time.sleep(cmdDelay)

psu.toggleOutput(pChan,'OFF')
endTime = datetime.datetime.now()
file1.write("endTime: " + str(endTime) + "\n")
file1.write("elapsedTime: " + str(endTime - startTime) + "\n")
file1.write("DP832 Initial System Temp: %sC\n" %initialTemp)
endTemp = psu.sysTemp()
file1.write("DP832 Ending System Temp: %sC\n" %endTemp)
file1.write("Run Notes:\n")
file1.write("START DATA CAPTURE\n")

# copy file2 into end of file1
file2.seek(0,0)
file1.write(file2.read())

# close file resources and delete temp file2
file1.close()
file2.close()
os.remove(fname2)
