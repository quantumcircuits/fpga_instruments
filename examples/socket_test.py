import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from library.oscilloscopes.tek.tekscope import TekScope

ip_addr = '10.0.1.144'
ip_port = 4000

tek = TekScope("tek mso", ip_addr, ip_port, timeout=20)
tek.clear()
tek.reset()
value = tek.idn()
print(f"value={value}")

# tek.write('ACQUIRE:STATE STOP')

# tek.list_files("C:/Temp")
# tek.list_files("C:/Temp")
# tek.list_files("C:/Temp")
# value = tek.read_raw(1024)
# print(value)
# time.sleep(5)
# tek.list_files("C:/Temp")

# tek.write("FILESYSTEM:CWD?")
# # tek.opc()
# # value = tek.read_raw()
# # print(f"{value=}")
# value = tek.read_str(1024)
# print(f"{value=}")
        
# file_size = tek.get_file_size("C:/Temp/BRAD.WFM")
# print(f"{file_size=}")
tek.download_file("C:/Temp/BRAD.WFM")

# tek.write("FILESystem:READFile \"C:/Temp/BRAD.WFM\"")
# value = tek.query_raw('*OPC?', 1)
# print(f"opc value is {value}")
# imgData = tek.read_raw(file_size_bytes)
# file = open("brad.wfm", "wb")
# file.write(imgData)
# file.close()

# value = tek.query_int("WFMO:NR_P?")
# print(f"value={value}")

# value = tek.query_float("WFMO:XINCR?")
# print(f"value={value}")


# tek.write("HEADER 0")
# tek.write("DATA:SOUR CH1")
# tek.write("DAT:ENC SRI")   # Signed Binary Format, LSB order
# tek.write("DAT:WIDTH 1")

# tek.write("DAT:START 1")
# tek.write("DAT:STOP 1e10") # Set data stop to max
# recordLength = tek.query_int("WFMO:NR_P?")  # Query how many points are actually available
# tek.write("DAT:STOP {0}".format(recordLength)) # Set data stop to match points available
# print(f"{recordLength=}")

# # Fetch horizontal scaling factors
# xinc = tek.query_float("WFMO:XINCR?")
# xzero = tek.query_float("WFMO:XZERO?")
# pt_off = tek.query_int("WFMO:PT_OFF?")
# print(f"{xinc=}")
# print(f"{xzero=}")
# print(f"{pt_off=}")

# # Fetch vertical scaling factors
# ymult = tek.query_float("WFMO:YMULT?")
# yzero = tek.query_float("WFMO:YZERO?")
# yoff = tek.query_float("WFMO:YOFF?")
# print(f"{ymult=}")
# print(f"{yzero=}")
# print(f"{yoff=}")

# print("requesting curve data")
# value_array = tek.query_binary("curve?")
# print(f"value={value_array}")

    
# t0 = (-pt_off * xinc) + xzero
# xvalues = np.ndarray(recordLength, float)
# yvalues = np.ndarray(recordLength, float)
# for index, value in enumerate(value_array):
#     xvalues[index] = t0 + xinc * index # Create timestamp for the data point
#     yvalues[index] = float(value - yoff) * ymult + yzero # Convert raw ADC value into a floating point value

# for index, value in enumerate(xvalues):
#     print(f"[{index}]={value}")

# plt.plot(xvalues, yvalues)
# plt.show()


# my_instrument.write(':SAVe:WAVEform:FILEFormat SPREADSheet')
# my_instrument.write('SAVE:WAVEform ALL,\"E:/Temp.csv\"')

# values = read_wfm('brad.wfm')
# for index, value in enumerate(values[0]):
#     print(f"[{index}]={value}")

# tek.write("FILESYSTEM:CWD \"C:/Temp\"")
# files = tek.query_str("FILESYSTEM:LDIR?")
# value = tek.query_raw('*OPC?', 1)
# print(f"opc value is {value} ")
# print(f"{files=}")
# files = files.split(",")
# for file in files:
#     file_info = file.strip("\"").split(";")
#     print(file_info)
#     if file_info[0] == "Temp.png":
#         file_size_bytes = int(file_info[2])
#         break
# print(f"{file_size_bytes=}")
# tek.write('FILESystem:READFile \"C:/Temp/Temp.png\"')
# # # # # # print("read opc")
# # value = tek.read_raw(1)
# # print(f"raw value is {value}")
# # tek.write('*WAI')
# import time 
# # time.sleep(1)
# value = tek.query_raw('*OPC?', 1)
# print(f"opc value is {value}")
# imgData = tek.read_raw(file_size_bytes)
# file = open("temp.png", "wb")
# file.write(imgData)
# file.close()

# # # Generate a filename based on the current Date & Time
# # dt = datetime.now()
# # fileName = dt.strftime("%Y%m%d_%H%M%S.png")

# # # Save the transfered image to the hard drive of your PC
# # imgFile = open(fileSaveLocation + fileName, "wb")
# # imgFile.write(imgData)
# # imgFile.close()

# file = open("brad.wfm","wb")
# file.write(imgData)
# file.close()