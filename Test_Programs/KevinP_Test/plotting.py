import pandas as pd
import matplotlib.pyplot as plt


dataFileFormatted = pd.read_csv('\\Users\\kjpar\\Desktop\\Test_KP\\Orbiview_v2\\Test_Programs\\KevinP_Test\\DATALOG.csv')
timeData = dataFileFormatted['Milliseconds']
altitudeData = dataFileFormatted['Altitude']
tempData = dataFileFormatted['Temperature']
pressureData = dataFileFormatted['Pressure']
accelXData = dataFileFormatted['AccelX']
accelYData = dataFileFormatted['AccelY']
accelZData = dataFileFormatted['AccelZ']
maxAccelZData = dataFileFormatted['MaxAccelZ']
altitudeStartData = dataFileFormatted['AltitudeStart']

plt.plot(timeData, altitudeData)

# Add labels and a title
plt.xlabel("X-axis Label")
plt.ylabel("Y-axis Label")
plt.title("Simple Line Plot")
plt.show()