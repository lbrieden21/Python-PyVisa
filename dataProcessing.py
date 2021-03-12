import numpy as np

data = np.genfromtxt('sampleData.csv', delimiter=',', names=True)
# for row in data:
#     print(row['SetVoltage'], row['PsuMeasureVoltage'],row['DmmAverageVoltage'])
ax1.plot(data['SetVoltage'],data['PsuMeasureVoltage'],color='r', label='PSU Reading')
