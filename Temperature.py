"""
Temperature.py
"""

import os
import json
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from gpiozero import CPUTemperature


def extraction(raw):
    """
    :param raw:
    :return:
    """
    data = raw.split("\n")[1].split(" ")[9]
    return int(float(data[2:]) / 1000)


def read(filename):
    """
    :param filename:
    :return:
    """
    with open(filename) as file:
        raw = file.read()
    return raw


def replace_line(filename, line_number, text):
    """
    :param filename:
    :param line_number:
    :param text:
    """
    with open(filename) as file:
        lines = file.readlines()

    if line_number <= len(lines):
        lines[line_number - 1] = text + "\n"

        with open(filename, "w") as file:
            for line in lines:
                file.write(line)


class Temperature:
    """
    Class Temperature
    """

    def __init__(self):

        self.soc = CPUTemperature()

        with open("config.json", "r") as file:
            self.config = json.load(file)

        if os.path.exists("temperature.txt"):
            os.remove("temperature.txt")

        time.sleep(1)

        with open("temperature.txt", "x") as file:
            file.write("wc_cpu:0\n")
            file.write("wc_gpu:0\n")
            file.write("case:0\n")
            file.write("soc:0")

        while True:
            time.sleep(1)
            if os.path.exists("temperature.txt"):
                break


    def return_sensor(self, sensor, line):
        """
        :param sensor:
        :param line:
        """
        return line, sensor + ":" + str(extraction(read(self.config["sensors"][sensor])))

    def run(self):
        """
        run()
        """
        while True:

            with ThreadPoolExecutor() as executor:

                line = 1
                futures = []

                for sensor in self.config["sensors"]:
                    futures.append(executor.submit(self.return_sensor, sensor=sensor, line=line))
                    line += 1

                for future in as_completed(futures):
                    try:
                        line, txt = future.result()
                        replace_line("temperature.txt", line, txt)
                    except:
                        print("Temperature.py : Erreur de lecture du fichier temperature.txt")

            try:
                replace_line("temperature.txt", 4, "soc" + ":" + str(int(self.soc.temperature)))
            except:
                print("Temperature.py : Erreur de lecture du fichier temperature.txt")

            time.sleep(1)


temperature = Temperature()
temperature.run()
