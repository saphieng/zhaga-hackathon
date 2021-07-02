import serial
from time import sleep

ser = serial.Serial(
    port = "COM9",
    baudrate = 115200,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    xonxoff = False,
    rtscts = True,
    dsrdtr = False,
    timeout =1
)

while True:
    if ser.isOpen():
        x = ser.readline().decode().strip()
        print("testing data: ", x)
        sleep(0.09375)
    sleep(1)






# import serial
# from time import sleep
# import os.path
# import sys
# import csv
# import operator

# count = 0
# mins = 0
# ini = 0
# LTR = 0
# RTL = 0
# prev1 = 0
# prev2 = 0
# filecontrol = 0

# ser = serial.Serial(
#     port = "COM9",
#     baudrate = 115200,
#     bytesize = serial.EIGHTBITS,
#     parity = serial.PARITY_NONE,
#     stopbits = serial.STOPBITS_ONE,
#     xonxoff = False,
#     rtscts = False,
#     dsrdtr = False,
#     timeout =1
# )

# def myfunc():
#     myfunc.counter += 1
#     return myfunc.counter
# myfunc.counter = 0
# count1 = myfunc()

# # str11 = 'restart'
# # str11 += '\n\r'
# # ser.write(str11.encode())
# # ser.readline().decode().strip()
# # sleep(3)

# str10 = 'clear'
# str10 += '\n\r'
# ser.write(str10.encode())
# ser.readline().decode().strip()
# sleep(2)

# while True:
#     str1 = 'get ltr'
#     str1 += '\n\r'
#     ser.write(str1.encode())
#     x1 = ser.readline().decode().strip()
#     x11 = int(x1)
#     sleep(0.25)

#     str2 = 'get rtl'
#     str2 += '\n\r'
#     ser.write(str2.encode())
#     x2 = ser.readline().decode().strip()
#     x22 = int(x2)
#     sleep(0.25)

#     str3 = 'get sens'
#     str3 += '\n\r'
#     ser.write(str3.encode())
#     x3 = ser.readline().decode().strip()
#     sleep(0.25)

#     str4 = 'get hold'
#     str4 += '\n\r'
#     ser.write(str4.encode())
#     x4 = ser.readline().decode().strip()
#     sleep(0.25)

#     time = str(mins) + ":" + str(count)

#     strfile = "PCR2_beam_80" + "_sens_" + x3 + "_Hold_" + x4 + "_" + str(count1) +".csv"
#     while os.path.isfile(strfile) and filecontrol == 0:
#         count1 = myfunc()
#         strfile = "PCR2_beam_80" + "_sens_" + x3 + "_Hold_" + x4 + "_" + str(count1) +".csv"
#     filecontrol = 1

#     with open(strfile, 'a', newline='') as f:
#             fieldnames = ['LTR','RTL','Time', 'LTR (Walking)','RTL (Walking)','Sensitivity','Hold']
#             thewriter = csv.DictWriter(f,fieldnames=fieldnames)
#             thewriter.writerow({'LTR (Walking)': LTR, 'RTL (Walking)':RTL, 'LTR': x11, 'RTL': x22,'Time': time ,'Sensitivity': x3,'Hold': x4})

#     if ini == 0:
#         prev1 = x11
#         prev2 = x22
#         ini += 1

#         with open(strfile, 'w+', newline='') as f:
#             fieldnames = ['LTR','RTL','Time', 'LTR (Walking)','RTL (Walking)','Sensitivity','Hold']
#             thewriter = csv.DictWriter(f,fieldnames=fieldnames)
#             thewriter.writeheader()
#     else:
#         if prev1-x11 != 0 and prev1 < x11:
#             LTR += x11-prev1
#         if prev2-x22 != 0 and prev2 < x22:
#             RTL += x22-prev2

#         if prev1 > x11:
#             LTR += x11
#         if prev2 > x22:
#             RTL += x22

#         prev1 = x11
#         prev2 = x22
        
#     print("LTR: " + x1,"RTL: " + x2, "Sensitivity: " + x3, "Hold: " + x4, "Time: " + str(mins) + ":" + str(count), "LTR (Walking): " + str(LTR), "RTL (Walking): " + str(RTL), sep = "    ", end = "\n\n")

#     count = count+1
#     if count >= 60:
#         mins = mins + 1
#         count = 0