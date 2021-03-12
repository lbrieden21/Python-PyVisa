#!/usr/bin/env python
import time
from decimal import *
import visa
delay = 0.01 #delay in seconds (50 ms)

rm = visa.ResourceManager('@py')
# print(rm.list_resources())
# PSU = rm.open_resource("TCPIP::192.168.9.11::INSTR")
PSU = rm.open_resource("USB::0x1AB1::0x0E11::DP8C175205811::INSTR")


def getModel():
    return 'DP832'

def maxVoltage(chan): #define max voltage channel can be set to
    if(chan == 3):
        return 5.3
    else:
        return 32 

def selOutput(chan): #define a CHANNEL SELECT function
    cmd1 = ':INST:NSEL %s' %chan
    PSU.write(cmd1)
    time.sleep(delay) 

def toggleOutput(chan,state): #define a TOGGLE OUTPUT function
    cmd1 = ':OUTP CH%s,%s' %(chan, state)
    PSU.write(cmd1)
    time.sleep(delay)

def setVoltage(chan, val): #define a SET VOLTAGE function
    cmd1 = ':INST:NSEL %s' %chan
    cmd2 = ':VOLT %s' %val
    PSU.write(cmd1)
    time.sleep(delay)
    PSU.write(cmd2)
    time.sleep(delay)

def setCurrent(chan, val): #define a SET CURRENT function
    cmd1 = ':INST:NSEL %s' %chan
    cmd2 = ':CURR %s' %val
    PSU.write(cmd1)
    time.sleep(delay)
    PSU.write(cmd2)
    time.sleep(delay)

def setOVP(chan,val): #define a SET VOLT PROTECTION function
    cmd1 = ':INST:NSEL %s' %chan
    cmd2 = ':VOLT:PROT %s' %val
    PSU.write(cmd1)
    time.sleep(delay)
    PSU.write(cmd2)
    time.sleep(delay)

def toggleOVP(state): #define a TOGGLE VOLTAGE PROTECTION function
    cmd1 = ':VOLT:PROT:STAT %s' %state
    PSU.write(cmd1)
    time.sleep(delay)

def setOCP(chan,val): #define a SET CURRENT PROTECTION function
    cmd1 = ':INST:NSEL %s' %chan
    cmd2 = ':CURR:PROT %s' %val
    PSU.write(cmd1)
    time.sleep(delay)
    PSU.write(cmd2)
    time.sleep(delay)

def toggleOCP(state): #define a TOGGLE CURRENT PROTECTION function
    cmd1 = ':CURR:PROT:STAT %s' %state
    PSU.write(cmd1)
    time.sleep(delay)

def measVolt(chan): #define a MEASURE VOLTAGE function
    cmd1 = ':MEAS:VOLT? CH%s' %chan
    V = PSU.query(cmd1)
    V = Decimal(V)
    time.sleep(delay)
    return V

def measCurrent(chan): #define a MEASURE CURRENT function
    cmd1 = ':MEAS:CURR? CH%s' %chan
    C = PSU.query(cmd1)
    C = float(C)
    time.sleep(delay)
    return C

def measPower(chan): #define a MEASURE POWER function
    cmd1 = ':MEAS:POWE? CH%s' %chan
    P = PSU.query(cmd1)
    P = float(P)
    time.sleep(delay)
    return P

def measAll(chan): #define a MEASURE VOLTS, CURRENT & POWER  function
    cmd1 = ':MEAS:ALL? CH%s' %chan
    P = PSU.query(cmd1)
    time.sleep(delay)
    return P

def sysTemp(): #define get system temperature function
    cmd1 = ':SYST:SELF:TEST:TEMP?'
    T = PSU.query(cmd1)
    T = Decimal(T)
    time.sleep(delay)
    return T
