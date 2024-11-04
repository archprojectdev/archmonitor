"""
Listener.py
"""
import json
import time
import traceback
import threading
import board
import pigpio

from gpiozero import CPUTemperature
from adafruit_pca9685 import PCA9685


def temperature_extraction(raw):
    """
    :param raw:
    :return:
    """
    data = raw.split("\n")[1].split(" ")[9]
    return int(float(data[2:]) / 1000)


def temperature_read(path):
    """
    :param path:
    :return:
    """
    sensor_file = open(path)
    raw = sensor_file.read()
    sensor_file.close()
    return raw


class Listener:
    """
    Class Listener
    """

    def __init__(self):

        self.modules = None

        # -------------------------------------------------------------

        self.pi = pigpio.pi()
        self.soc = CPUTemperature()

        # -------------------------------------------------------------

        self.i2c = board.I2C()
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 60

        self.pca_pwm_100 = 0xffff

        # -------------------------------------------------------------

        with open("config.json", "r") as file:
            self.config = json.load(file)

        # -------------------------------------------------------------

        self.infos = {
            "power": 0,
            "mode": self.config["mode"]["selected"],
            "led": self.config["led"]["selected"],

            "pwm_fan_soc": int(self.config["mode"][self.config["mode"]["selected"]]["fan_cpu"]["pwm_min"]),
            "pwm_fan_cpu": int(self.config["mode"][self.config["mode"]["selected"]]["fan_cpu"]["pwm_min"]),
            "pwm_fan_gpu": int(self.config["mode"][self.config["mode"]["selected"]]["fan_gpu"]["pwm_min"]),
            "pwm_fan_case": int(self.config["mode"][self.config["mode"]["selected"]]["fan_case"]["pwm_min"]),
            "pwm_pump": int(self.config["mode"][self.config["mode"]["selected"]]["pump"]["pwm"]),
            "pwm_pump_cpu": int(self.config["mode"][self.config["mode"]["selected"]]["pump"]["pwm"]),
            "pwm_pump_gpu": int(self.config["mode"][self.config["mode"]["selected"]]["pump"]["pwm"]),

            "rpm_fan_soc": 0,
            "rpm_fan_cpu": 0,
            "rpm_fan_gpu": 0,
            "rpm_fan_case": 0,
            "rpm_pump_cpu": 0,
            "rpm_pump_gpu": 0,

            "temp_soc": int(self.config["mode"]["soc"]["fan_soc"]["degree_min_targeted"]),
            "temp_wc_cpu": int(self.config["mode"][self.config["mode"]["selected"]]["fan_cpu"]["degree_min_targeted"]),
            "temp_wc_gpu": int(self.config["mode"][self.config["mode"]["selected"]]["fan_gpu"]["degree_min_targeted"]),
            "temp_case": int(self.config["mode"][self.config["mode"]["selected"]]["fan_case"]["degree_min_targeted"])
        }

        # -------------------------------------------------------------

        self.pwms = {
            "fan_soc": None,
            "fan_cpu": None,
            "fan_gpu": None,
            "fan_case": None,
            "pump_cpu": None,
            "pump_gpu": None
        }

        # -------------------------------------------------------------

        self.tach = {
            "fan_soc": 0, "fan_cpu": 0, "fan_gpu": 0, "fan_case": 0,
            "pump_cpu": 0, "pump_gpu": 0
        }

        self.tach_divider = {
            "fan_soc": 2, "fan_cpu": 2, "fan_gpu": 2, "fan_case": 2,
            "pump_cpu": 2, "pump_gpu": 2
        }

        tach_time = time.time()
        self.tach_time = {
            "fan_soc": tach_time, "fan_cpu": tach_time, "fan_gpu": tach_time, "fan_case": tach_time,
            "pump_cpu": tach_time, "pump_gpu": tach_time
        }

        # -------------------------------------------------------------

    def define_modules(self, modules):
        """
        :param modules:
        """
        self.modules = modules

    def pwm_by_temp(self, mode, target, value=0):
        """
        :param mode:
        :param target:
        :param value:
        :return:
        """

        degree_min = 0

        if target == "fan_soc":
            degree_min = self.config["mode"]["soc"]["fan_soc"]["degree_min_targeted"]
        elif target != "pump":
            degree_min = self.config["mode"][mode][target]["degree_min_targeted"]

        if target == "pump":

            pwm = self.config["mode"][mode][target]["pwm"]

        else:
            
            if target == "fan_soc":
                pwm_min = self.config["mode"]["soc"]["fan_soc"]["pwm_min"]
                pwm_max = self.config["mode"]["soc"]["fan_soc"]["pwm_max"]
                pmad = self.config["mode"]["soc"]["fan_soc"]["pwm_max_at_degree"]
            else:
                pwm_min = self.config["mode"][mode][target]["pwm_min"]
                pwm_max = self.config["mode"][mode][target]["pwm_max"]
                pmad = self.config["mode"][mode][target]["pwm_max_at_degree"]

            pwm = pwm_min

            if degree_min < value < pmad:

                pwm_gap = pwm_max - pwm_min
                degree_gap = pmad - degree_min
                value_gaped = value - degree_min
                divider = (degree_gap / value_gaped)

                pwm = pwm_min + (pwm_gap / divider)

            elif pmad <= value:

                pwm = pwm_max

        return int(pwm)

    def cb_fan_soc_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["fan_soc"] += 1

    def cb_fan_cpu_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["fan_cpu"] += 1

    def cb_fan_gpu_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["fan_gpu"] += 1

    def cb_fan_case_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["fan_case"] += 1

    def cb_pump_cpu_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["pump_cpu"] += 1

    def cb_pump_gpu_rpm(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.tach["pump_gpu"] += 1

    def cb_on(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.infos["power"] = 1

    def cb_off(self, gpio, level, tick):
        """
        :param gpio:
        :param level:
        :param tick:
        """
        self.infos["power"] = 0

    def rpm_calc(self, target):
        """
        rpm_calc()
        """

        tach_time = time.time()

        rpm = self.tach[target] / (tach_time - self.tach_time[target])
        rpm *= 60
        rpm = int(rpm / self.tach_divider[target])

        self.tach[target] = 0
        self.tach_time[target] = tach_time
        self.infos["rpm_" + target] = rpm

    def set_mode_silent(self):
        """
        set_mode_silent()
        """
        self.infos["mode"] = "silent"
        self.config["mode"]["selected"] = "silent"

        pwm_pump = self.pwm_by_temp(self.config["mode"]["selected"], "pump")

        self.infos["pwm_pump"] = pwm_pump
        self.infos["pwm_pump_cpu"] = pwm_pump
        self.infos["pwm_pump_gpu"] = pwm_pump

    def set_mode_performance(self):
        """
        set_mode_performance()
        """
        self.infos["mode"] = "performance"
        self.config["mode"]["selected"] = "performance"

        pwm_pump = self.pwm_by_temp(self.config["mode"]["selected"], "pump")

        self.infos["pwm_pump"] = pwm_pump
        self.infos["pwm_pump_cpu"] = pwm_pump
        self.infos["pwm_pump_gpu"] = pwm_pump

    def get_and_reveal(self):
        """
        get_and_reveal()
        """
        while True:

            # Get Temperature
            with open("temperature.txt", "r") as file:

                data = file.read()
                lines = data.split("\n")

                try:
                    for line in lines[:4]:
                        substring = line.split(":")
                        self.infos["temp_" + substring[0]] = int(substring[1])
                except:
                    print("Listener.py : Erreur de lecture du fichier temperature.txt")

            # Calc PWM Duty Cycle
            self.infos["pwm_fan_soc"] = self.pwm_by_temp(
                self.config["mode"]["selected"],
                "fan_soc",
                self.infos["temp_soc"])

            self.infos["pwm_fan_cpu"] = self.pwm_by_temp(
                self.config["mode"]["selected"],
                "fan_cpu",
                self.infos["temp_wc_cpu"])

            self.infos["pwm_fan_gpu"] = self.pwm_by_temp(
                self.config["mode"]["selected"],
                "fan_gpu",
                self.infos["temp_wc_gpu"])

            self.infos["pwm_fan_case"] = self.pwm_by_temp(
                self.config["mode"]["selected"],
                "fan_case",
                self.infos["temp_case"])

            # Change new PCA PWM Duty Cycle
            self.pca.channels[self.config["gpio"]["pwm_pca"]["fan_soc"]].duty_cycle = \
                int(self.pca_pwm_100 * (self.infos["pwm_fan_soc"] / 100))

            self.pca.channels[self.config["gpio"]["pwm_pca"]["fan_cpu"]].duty_cycle = \
                int(self.pca_pwm_100 * (self.infos["pwm_fan_cpu"] / 100))

            self.pca.channels[self.config["gpio"]["pwm_pca"]["fan_gpu"]].duty_cycle = \
                int(self.pca_pwm_100 * (self.infos["pwm_fan_gpu"] / 100))

            self.pca.channels[self.config["gpio"]["pwm_pca"]["fan_case"]].duty_cycle = \
                int(self.pca_pwm_100 * (self.infos["pwm_fan_case"] / 100))

            self.pca.channels[self.config["gpio"]["pwm_pca"]["pump"]].duty_cycle = \
                int(self.pca_pwm_100 * (self.infos["pwm_pump"] / 100))

            # Calc TACH
            self.rpm_calc("fan_soc")
            self.rpm_calc("fan_cpu")
            self.rpm_calc("fan_gpu")
            self.rpm_calc("fan_case")
            self.rpm_calc("pump_cpu")
            self.rpm_calc("pump_gpu")

            self.modules["display"].reveal(self.infos)
            time.sleep(1)

    def run(self):
        """
        run()
        """

        # Define POWER detection
        self.pi.set_mode(self.config["gpio"]["power"], pigpio.INPUT)
        self.pi.callback(self.config["gpio"]["power"], pigpio.LOW, self.cb_off)
        self.pi.callback(self.config["gpio"]["power"], pigpio.HIGH, self.cb_on)

        # ----------------------------------------------------------------

        # Define PCA PWM
        self.pca.channels[self.config["gpio"]["pwm_pca"]["fan_soc"]].duty_cycle = int(self.pca_pwm_100 / 2)
        self.pca.channels[self.config["gpio"]["pwm_pca"]["fan_cpu"]].duty_cycle = int(self.pca_pwm_100 / 2)
        self.pca.channels[self.config["gpio"]["pwm_pca"]["fan_gpu"]].duty_cycle = int(self.pca_pwm_100 / 2)
        self.pca.channels[self.config["gpio"]["pwm_pca"]["fan_case"]].duty_cycle = int(self.pca_pwm_100 / 2)
        self.pca.channels[self.config["gpio"]["pwm_pca"]["pump"]].duty_cycle = int(self.pca_pwm_100 / 2)

        # ----------------------------------------------------------------

        # Define TACH
        self.pi.set_mode(self.config["gpio"]["tach"]["fan_soc"], pigpio.INPUT)
        self.pi.set_mode(self.config["gpio"]["tach"]["fan_cpu"], pigpio.INPUT)
        self.pi.set_mode(self.config["gpio"]["tach"]["fan_gpu"], pigpio.INPUT)
        self.pi.set_mode(self.config["gpio"]["tach"]["fan_case"], pigpio.INPUT)
        self.pi.set_mode(self.config["gpio"]["tach"]["pump_cpu"], pigpio.INPUT)
        self.pi.set_mode(self.config["gpio"]["tach"]["pump_gpu"], pigpio.INPUT)

        # Run TACH Callback
        self.pi.callback(self.config["gpio"]["tach"]["fan_soc"], pigpio.RISING_EDGE, self.cb_fan_soc_rpm)
        self.pi.callback(self.config["gpio"]["tach"]["fan_cpu"], pigpio.RISING_EDGE, self.cb_fan_cpu_rpm)
        self.pi.callback(self.config["gpio"]["tach"]["fan_gpu"], pigpio.RISING_EDGE, self.cb_fan_gpu_rpm)
        self.pi.callback(self.config["gpio"]["tach"]["fan_case"], pigpio.RISING_EDGE, self.cb_fan_case_rpm)
        self.pi.callback(self.config["gpio"]["tach"]["pump_cpu"], pigpio.RISING_EDGE, self.cb_pump_cpu_rpm)
        self.pi.callback(self.config["gpio"]["tach"]["pump_gpu"], pigpio.RISING_EDGE, self.cb_pump_gpu_rpm)

        # ----------------------------------------------------------------

        get_and_reveal = threading.Thread(
            target=self.get_and_reveal,
            daemon=True)
        get_and_reveal.start()
