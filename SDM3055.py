#!/usr/bin/env python
import visa
import time
delay = 0.01 #delay in seconds (50 ms)

rm = visa.ResourceManager('@py')
#DMM = rm.open_resource('USB0::0xF4EC::0xEE38::SDM305C2150033::INSTR')
DMM = rm.open_resource('TCPIP::192.168.9.13::INSTR')

def getModel():
    return 'SDM3055'

def confV():
        cmd1 = 'CONF:VOLT:DC'
        time.sleep(delay)
        DMM.query(cmd1)

def convertResult(res):
        resultString = str(res) # make sure string

        # check if first character is a '+' or a '-'
        if(resultString[0] == '+'):
                boolSign = True
        elif(resultString[0] == '-'):
                boolSign = False

        # extract whole number with decimals
        if(boolSign == True):
                result = float(resultString.split("+",1)[1].split("E",1)[0])
        elif(boolSign == False):
                result = float(resultString.split("-",1)[1].split("E",1)[0])

        # determine exponent
        resultExp = float(resultString.split("E",1)[1])

        # apply power to whole number, store this number in a variable
        result = result*pow(10,resultExp)

        # if '+' then value = value
        # if '-' then value = -value
        if(boolSign == True):
                result = result
        elif(boolSign == False):
                result = -result
        return result

def measV(acdc):
        cmd1 = 'MEAS:VOLT:%s? AUTO' %acdc
        time.sleep(delay)

        # take in value and convert
        result = convertResult(DMM.query(cmd1))

        return result


def measI(acdc):
        cmd1 = 'MEAS:CURR:%s? AUTO' %acdc
        time.sleep(delay)
        # take in value as a string
        resultString = str(DMM.query(cmd1))

        # check if first character is a '+' or a '-'
        if(resultString[0] == '+'):
                boolSign = True
        elif(resultString[0] == '-'):
                boolSign = False

        # extract whole number with decimals
        if(boolSign == True):
                result = float(resultString.split("+",1)[1].split("E",1)[0])
        elif(boolSign == False):
                result = float(resultString.split("-",1)[1].split("E",1)[0])

        # determine exponent
        resultExp = float(resultString.split("E",1)[1])

        # apply power to whole number, store this number in a variable
        result = result*pow(10,resultExp)

        # if '+' then value = value
        # if '-' then value = -value
        if(boolSign == True):
                result = result
        elif(boolSign == False):
                result = -result

        # return value
        #print(str(result) + ' A')
        return result

# determine how many valid digits contained in the measurement
# *** PROBABLY SHOULD TAKE MEASUREMENT TYPE AND USE
# *** ALSO NEED BETTER SOLUTION, IF MEAS IS INCREASING, RANGE DOESN'T CHANGE UP UNTIL 24 COUNT
# *** HOWEVER, WHEN COUNTING DOWN RANGE DOESN'T CHANGE DOWN UNTIL 20 COUNT, WHICH MEANS THERE
# *** IS A 4 COUNT HYSTERESIS
# *** PROBABLY MAKE MORE SENSE TO CALL CONF? AFTER MEASUREMENT, WHICH WILL RETURN RANGE MEASUREMENT WAS TAKEN WITH
def calcDigits(meas):
        if(meas < .240): # 200mV range
                digits = 6
        elif(meas < 2.4): # 2V range
                digits = 5
        elif(meas < 24): # 20V range
                digits = 4
        elif(meas < 240): # 200V range
                digits = 3
        elif(meas < 1000): # 1000V range
                digits = 2
        else:
                digits = 0 # should be error?

        return digits

def measVoltStatistics(samps):
        confV();
        cmd1 = 'SAMP:COUN %s' %samps
        DMM.query(cmd1)
        time.sleep(delay)
        DMM.query('CALC:AVER:STAT ON')
        time.sleep(delay)
        DMM.query('INIT:IMM')
        time.sleep(delay)
        while (samps > int(convertResult(DMM.query('CALC:AVER:COUN?')))):
                time.sleep(delay)

        result = DMM.query('CALC:AVER:ALL?').strip('\n').split(',')
        stats = {
                "samples":samps,
                "average":result[0],
                "stddev":result[1],
                "maximum":result[2],
                "minimum":result[3]
        }

        time.sleep(delay)
        return stats

#def measOhm():
