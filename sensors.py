"""
Display.py
"""

import glob

sensors = glob.glob("/sys/bus/w1/devices/28*/w1_slave")

while True:
    print("################################""")
    print("")
    for sensor in sensors:
        print("---------------------")
        print(sensor)
        print("")
