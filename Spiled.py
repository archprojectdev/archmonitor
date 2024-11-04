"""
Spiled.py
"""

import ws2812
import spidev
import time
import json
import threading


class Spiled:
    """
    Class Spiled
    """

    def __init__(self):

        self.modules = None

        # -------------------------------------------------------------

        with open("config.json", "r") as file:
            self.config = json.load(file)

        # -------------------------------------------------------------

        self.spi = spidev.SpiDev()

        self.spi.open(0, 0)
        self.spi.max_speed_hz = 250000
        self.spi.mode = 0

        # -------------------------------------------------------------

        self.lock = False
        self.phase = 0
        self.count = 0

        # -------------------------------------------------------------

        self.tr = 0
        self.tg = 0
        self.tb = 0

    def define_modules(self, modules):
        """
        :param modules:
        """
        self.modules = modules

    def set_led_a(self):
        """
        set_led_a()
        """
        self.lock = True
        time.sleep(0.1)

        self.phase = 0
        self.count = 0
        self.config["led"]["selected"] = "a"

        self.tr = int(self.config["led"]["a"]["color"]["r"] * (self.count / 100))
        self.tg = int(self.config["led"]["a"]["color"]["g"] * (self.count / 100))
        self.tb = int(self.config["led"]["a"]["color"]["b"] * (self.count / 100))

        self.lock = False

    def set_led_b(self):
        """
        set_led_b()
        """
        self.lock = True
        time.sleep(0.1)

        self.phase = 0
        self.count = self.config["led"]["b"]["intensity-mini"]
        self.config["led"]["selected"] = "b"

        self.tr = int(self.config["led"]["b"]["color"]["r"] * (self.count / 100))
        self.tg = int(self.config["led"]["b"]["color"]["g"] * (self.count / 100))
        self.tb = int(self.config["led"]["b"]["color"]["b"] * (self.count / 100))

        self.lock = False

    def set_led_c(self):
        """
        set_led_c()
        """
        self.lock = True
        time.sleep(0.1)

        self.phase = 0
        self.count = self.config["led"]["c"]["intensity-mini"]
        self.config["led"]["selected"] = "c"

        self.tr = int(self.config["led"]["c"]["color_0"]["r"] * (self.count / 100))
        self.tg = int(self.config["led"]["c"]["color_0"]["g"] * (self.count / 100))
        self.tb = int(self.config["led"]["c"]["color_0"]["b"] * (self.count / 100))

        self.lock = False

    def relight(self):
        """
        relight()
        """

        while True:

            if not self.lock:

                if self.config["led"]["selected"] == "a":
                    self.led_type_a()

                if self.config["led"]["selected"] == "b":
                    self.led_type_b()

                if self.config["led"]["selected"] == "c":
                    self.led_type_c()

            else:

                time.sleep(0.1)
                while True:
                    if not self.lock:
                        break
                    time.sleep(0.1)

    def led_type_a(self):
        """
        led_type_a()
        """

        tr = int(self.config["led"]["a"]["color"]["r"])
        tg = int(self.config["led"]["a"]["color"]["g"])
        tb = int(self.config["led"]["a"]["color"]["b"])

        fi = [[tr, tg, tb]] * self.config["led"]["number"]
        ws2812.write2812(self.spi, fi)

        self.count = 0
        time.sleep(1 / (self.config["led"]["a"]["speed"] * 10))

    def led_type_b(self):
        """
        led_type_b()
        """
        if self.phase == 0:

            self.tr = int(self.config["led"]["b"]["color"]["r"] * (self.count / 100))
            self.tg = int(self.config["led"]["b"]["color"]["g"] * (self.count / 100))
            self.tb = int(self.config["led"]["b"]["color"]["b"] * (self.count / 100))

            fi = [[self.tr, self.tg, self.tb]] * self.config["led"]["number"]
            ws2812.write2812(self.spi, fi)

            self.count += 1

            if self.count == 100:
                self.phase = 1

        elif self.phase == 1:

            self.tr = int(self.config["led"]["b"]["color"]["r"] * (self.count / 100))
            self.tg = int(self.config["led"]["b"]["color"]["g"] * (self.count / 100))
            self.tb = int(self.config["led"]["b"]["color"]["b"] * (self.count / 100))

            fi = [[self.tr, self.tg, self.tb]] * self.config["led"]["number"]
            ws2812.write2812(self.spi, fi)

            self.count -= 1

            if self.count == self.config["led"]["b"]["intensity-mini"]:
                self.phase = 0

        time.sleep(1 / (self.config["led"]["b"]["speed"] * 10))

    def led_type_c(self):
        """
        led_type_c()
        """
        if self.phase == 0:

            self.tr = int(self.config["led"]["c"]["color_0"]["r"] * (self.count / 100))
            self.tg = int(self.config["led"]["c"]["color_0"]["g"] * (self.count / 100))
            self.tb = int(self.config["led"]["c"]["color_0"]["b"] * (self.count / 100))

            fi = [[self.tr, self.tg, self.tb]] * self.config["led"]["number"]
            ws2812.write2812(self.spi, fi)

            self.count += 1

            if self.count == 100:
                self.phase = 1

        elif self.phase == 1:

            self.tr = int(self.config["led"]["c"]["color_0"]["r"] * (self.count / 100))
            self.tg = int(self.config["led"]["c"]["color_0"]["g"] * (self.count / 100))
            self.tb = int(self.config["led"]["c"]["color_0"]["b"] * (self.count / 100))

            fi = [[self.tr, self.tg, self.tb]] * self.config["led"]["number"]
            ws2812.write2812(self.spi, fi)

            self.count -= 1

            if self.count == self.config["led"]["c"]["intensity-mini"]:
                self.count = 0
                self.phase = 2

        elif self.phase == 2:

            self.count += 1
            seq = 50
            
            color_a = self.config["led"]["c"]["color_0"]
            color_b = self.config["led"]["c"]["color_1"]
            
            ar = int(color_a["r"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            ag = int(color_a["g"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            ab = int(color_a["b"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            
            br = int(color_b["r"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            bg = int(color_b["g"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            bb = int(color_b["b"] * (self.config["led"]["c"]["intensity-mini"] / 100))

            if ar >= br:
                tr = ar - br
            else:
                tr = br - ar
                
            if ag >= bg:
                tg = ag - bg
            else:
                tg = bg - ag
                
            if ab >= bb:
                tb = ab - bb
            else:
                tb = bb - ab

            tr = int((tr / seq) * self.count)
            tg = int((tg / seq) * self.count)
            tb = int((tb / seq) * self.count)

            if ar >= br:
                self.tr = ar - tr
            else:
                self.tr = ar + tr
                
            if ag >= bg:
                self.tg = ag - tg
            else:
                self.tg = ag + tg
                
            if ab >= bb:
                self.tb = ab - tb
            else:
                self.tb = ab + tb

            fi = [[self.tr, self.tg, self.tb]] * self.config["led"]["number"]
            ws2812.write2812(self.spi, fi)

            if self.count == seq:
                self.count = self.config["led"]["c"]["intensity-mini"]
                self.phase = 3

        elif self.phase == 3:

            self.tr = int(self.config["led"]["c"]["color_1"]["r"] * (self.count / 100))
            self.tg = int(self.config["led"]["c"]["color_1"]["g"] * (self.count / 100))
            self.tb = int(self.config["led"]["c"]["color_1"]["b"] * (self.count / 100))

            fi = [[self.tr, self.tg, self.tb]] * self.config["led"]["number"]
            ws2812.write2812(self.spi, fi)

            self.count += 1

            if self.count == 100:
                self.phase = 4

        elif self.phase == 4:

            self.tr = int(self.config["led"]["c"]["color_1"]["r"] * (self.count / 100))
            self.tg = int(self.config["led"]["c"]["color_1"]["g"] * (self.count / 100))
            self.tb = int(self.config["led"]["c"]["color_1"]["b"] * (self.count / 100))

            fi = [[self.tr, self.tg, self.tb]] * self.config["led"]["number"]
            ws2812.write2812(self.spi, fi)

            self.count -= 1

            if self.count == self.config["led"]["c"]["intensity-mini"]:
                self.count = 0
                self.phase = 5

        elif self.phase == 5:

            self.count += 1
            seq = 50

            color_a = self.config["led"]["c"]["color_0"]
            color_b = self.config["led"]["c"]["color_1"]
            
            ar = int(color_a["r"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            ag = int(color_a["g"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            ab = int(color_a["b"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            
            br = int(color_b["r"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            bg = int(color_b["g"] * (self.config["led"]["c"]["intensity-mini"] / 100))
            bb = int(color_b["b"] * (self.config["led"]["c"]["intensity-mini"] / 100))

            if br >= ar:
                tr = br - ar
            else:
                tr = ar - br
                
            if bg >= ag:
                tg = bg - ag
            else:
                tg = ag - bg
                
            if bb >= ab:
                tb = bb - ab
            else:
                tb = ab - bb

            tr = int((tr / seq) * self.count)
            tg = int((tg / seq) * self.count)
            tb = int((tb / seq) * self.count)

            if br >= ar:
                self.tr = br - tr
            else:
                self.tr = br + tr
                
            if bg >= ag:
                self.tg = bg - tg
            else:
                self.tg = bg + tg
                
            if bb >= ab:
                self.tb = bb - tb
            else:
                self.tb = bb + tb

            fi = [[self.tr, self.tg, self.tb]] * self.config["led"]["number"]
            ws2812.write2812(self.spi, fi)

            if self.count == seq:
                self.count = self.config["led"]["c"]["intensity-mini"]
                self.phase = 0

        time.sleep(1 / (self.config["led"]["c"]["speed"] * 10))

    def run(self):
        """
        run()
        """

        thd_relight = threading.Thread(
            target=self.relight,
            daemon=True)
        thd_relight.start()
