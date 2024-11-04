"""
Display.py
"""

from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor, wait


class Display:
    """
    Class Display
    """
    def __init__(self):

        self.modules = None

        # -------------------------------------------------------------

        self.window = None
        self.graph = None

        # -------------------------------------------------------------

        self.dimension = (800, 480)

        # -------------------------------------------------------------

        img_background = Image.open("resource/template/background.png")
        img_config = Image.open("resource/template/config.png")

        img_led_a_on = Image.open("resource/template/led_a_on.png")
        img_led_a_off = Image.open("resource/template/led_a_off.png")

        img_led_b_on = Image.open("resource/template/led_b_on.png")
        img_led_b_off = Image.open("resource/template/led_b_off.png")

        img_led_c_on = Image.open("resource/template/led_c_on.png")
        img_led_c_off = Image.open("resource/template/led_c_off.png")

        img_performance_on = Image.open("resource/template/performance_on.png")
        img_performance_off = Image.open("resource/template/performance_off.png")

        img_silent_on = Image.open("resource/template/silent_on.png")
        img_silent_off = Image.open("resource/template/silent_off.png")

        img_echelon_on = Image.open("resource/template/echelon_on.png")
        img_echelon_off = Image.open("resource/template/echelon_off.png")

        self.text_font = ImageFont.truetype("resource/font/DroidSansMono.ttf", 20)
        self.text_color = (255, 255, 255)

        self.rpm_fan = []
        self.rpm_pump = []
        self.degree = []

        with ThreadPoolExecutor() as executor:
            executor.submit(self.create_txt_fan_rpm())
            executor.submit(self.create_txt_pump_rpm())
            executor.submit(self.create_txt_degree())

        # -------------------------------------------------------------

        self.images = {
            "background": img_background,
            "config": img_config,
            "led_a": {
                "on": img_led_a_on,
                "off": img_led_a_off,
            },
            "led_b": {
                "on": img_led_b_on,
                "off": img_led_b_off,
            },
            "led_c": {
                "on": img_led_c_on,
                "off": img_led_c_off,
            },
            "echelon": {
                "light": img_echelon_on,
                "dark": img_echelon_off,
            },
            "rpm_fan": self.rpm_fan,
            "rpm_pump": self.rpm_pump,
            "degree": self.degree,
            "silent": {
                "on": img_silent_on,
                "off": img_silent_off,
            },
            "performance": {
                "on": img_performance_on,
                "off": img_performance_off,
            }
        }

        # -------------------------------------------------------------

        self.figures = {}

        # -------------------------------------------------------------

        self.infos = {
            "power": None,
            "mode": "performance",
            "led": "a",

            "pwm_fan_soc": None,
            "pwm_fan_cpu": None,
            "pwm_fan_gpu": None,
            "pwm_fan_case": None,
            "pwm_pump_cpu": None,
            "pwm_pump_gpu": None,

            "rpm_fan_soc": None,
            "rpm_fan_cpu": None,
            "rpm_fan_gpu": None,
            "rpm_fan_case": None,
            "rpm_pump_cpu": None,
            "rpm_pump_gpu": None,

            "temp_soc": None,
            "temp_wc_cpu": None,
            "temp_wc_gpu": None,
            "temp_case": None,
        }

        self.new_infos = {
            "power": 0,
            "mode": "performance",
            "led": "a",

            "pwm_fan_soc": 0,
            "pwm_fan_cpu": 0,
            "pwm_fan_gpu": 0,
            "pwm_fan_case": 0,
            "pwm_pump_cpu": 0,
            "pwm_pump_gpu": 0,

            "rpm_fan_soc": 0,
            "rpm_fan_cpu": 0,
            "rpm_fan_gpu": 0,
            "rpm_fan_case": 0,
            "rpm_pump_cpu": 0,
            "rpm_pump_gpu": 0,

            "temp_soc": 0,
            "temp_wc_cpu": 0,
            "temp_wc_gpu": 0,
            "temp_case": 0,
        }

    def define_modules(self, modules):
        """
        :param modules:
        """
        self.modules = modules

    def define_graph(self, window, graph):
        """
        :param window:
        :param graph:
        """
        self.window = window
        self.graph = graph

    # ----------------------------------------------------------------------------------------
    # Create TXT
    # ----------------------------------------------------------------------------------------

    def create_txt_fan_rpm(self):
        """
        :param self:
        """
        for x in range(0, 3001, 50):
            canvas = Image.new("RGBA", (60, 22), color=(30, 30, 30, 255))
            image = ImageDraw.Draw(canvas)
            image.text(
                (0, 0),
                str(x),
                font=self.text_font,
                text_color=self.text_color
            )
            self.rpm_fan.append(canvas)

    def create_txt_pump_rpm(self):
        """
        :param self:
        """
        for x in range(0, 5001, 50):
            canvas = Image.new("RGBA", (60, 22), color=(30, 30, 30, 255))
            image = ImageDraw.Draw(canvas)
            image.text(
                (0, 0),
                str(x),
                font=self.text_font,
                text_color=self.text_color
            )
            self.rpm_pump.append(canvas)

    def create_txt_degree(self):
        """
        :param self:
        """
        for x in range(121):
            canvas = Image.new("RGBA", (40, 22), color=(38, 38, 38, 255))
            image = ImageDraw.Draw(canvas)
            image.text(
                (0, 0),
                str(x) + "°",
                font=self.text_font,
                text_color=self.text_color
            )
            self.degree.append(canvas)

    # ----------------------------------------------------------------------------------------
    # Pre Print Config
    # ----------------------------------------------------------------------------------------

    def pre_print_config(self):
        """
        print_config(self)
        """
        x = 16
        y = 24

        self.figures["config"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["config"])

    # ----------------------------------------------------------------------------------------
    # Pre Print LED
    # ----------------------------------------------------------------------------------------

    def pre_print_led(self):
        """
        print_led(self)
        """
        x = 157
        y = 24

        self.figures["led_a"]["on"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["led_a"]["on"])

        self.figures["led_a"]["off"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["led_a"]["off"])

        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures["led_a"]["off"])

        x = 246
        y = 24

        self.figures["led_b"]["on"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["led_b"]["on"])

        self.figures["led_b"]["off"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["led_b"]["off"])

        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures["led_b"]["on"])

        x = 335
        y = 24

        self.figures["led_c"]["off"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["led_c"]["off"])

        self.figures["led_c"]["on"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["led_c"]["on"])

        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures["led_c"]["on"])

    # ----------------------------------------------------------------------------------------
    # Pre Print Mode
    # ----------------------------------------------------------------------------------------

    def pre_print_mode(self):
        """
        print_mode(self)
        """
        x = 447
        y = 24

        self.figures["mode_silent"]["on"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["silent"]["on"])

        self.figures["mode_silent"]["off"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["silent"]["off"])

        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures["mode_silent"]["off"])

        x = 615
        y = 24

        self.figures["mode_performance"]["off"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["performance"]["off"])

        self.figures["mode_performance"]["on"] = self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(x, y),
            image=self.images["performance"]["on"])

        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures["mode_performance"]["on"])

    # ----------------------------------------------------------------------------------------
    # Pre Print Echelon
    # ----------------------------------------------------------------------------------------

    def pre_print_pwm_fan_soc(self):
        """
        print_pwm_fan_cpu(self)
        """
        dist = 22
        x = 150
        y = 108

        for i in range(20):
            self.figures["pwm_fan_soc"]["dark"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["dark"]))

            self.figures["pwm_fan_soc"]["light"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["light"]))

        for fig in self.figures["pwm_fan_soc"]["light"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_pwm_fan_cpu(self):
        """
        print_pwm_fan_cpu(self)
        """
        dist = 22
        x = 150
        y = 174

        for i in range(20):
            self.figures["pwm_fan_cpu"]["dark"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["dark"]))

            self.figures["pwm_fan_cpu"]["light"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["light"]))

        for fig in self.figures["pwm_fan_cpu"]["light"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_pwm_fan_gpu(self):
        """
        print_pwm_fan_gpu(self)
        """
        dist = 22
        x = 150
        y = 216

        for i in range(20):
            self.figures["pwm_fan_gpu"]["dark"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["dark"]))

            self.figures["pwm_fan_gpu"]["light"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["light"]))

        for fig in self.figures["pwm_fan_gpu"]["light"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_pwm_fan_case(self):
        """
        print_pwm_fan_case(self)
        """
        dist = 22
        x = 150
        y = 258

        for i in range(20):
            self.figures["pwm_fan_case"]["dark"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["dark"]))

            self.figures["pwm_fan_case"]["light"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["light"]))

        for fig in self.figures["pwm_fan_case"]["light"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_pwm_pump_cpu(self):
        """
        print_pwm_pump_cpu(self)
        """
        dist = 22
        x = 150
        y = 325

        for i in range(20):
            self.figures["pwm_pump_cpu"]["dark"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["dark"]))

            self.figures["pwm_pump_cpu"]["light"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["light"]))

        for fig in self.figures["pwm_pump_cpu"]["light"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_pwm_pump_gpu(self):
        """
        print_pwm_pump_gpu(self)
        """
        dist = 22
        x = 150
        y = 367

        for i in range(20):
            self.figures["pwm_pump_gpu"]["dark"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["dark"]))

            self.figures["pwm_pump_gpu"]["light"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x + (dist * i), y),
                image=self.images["echelon"]["light"]))

        for fig in self.figures["pwm_pump_gpu"]["light"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    # ----------------------------------------------------------------------------------------
    # Pre Print RPM
    # ----------------------------------------------------------------------------------------

    def pre_print_rpm_fan_soc(self):
        """
        print_rpm_fan_soc(self)
        """
        x = 634
        y = 112

        for image in self.images["rpm_fan"]:
            self.figures["rpm_fan_soc"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["rpm_fan_soc"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_rpm_fan_cpu(self):
        """
        print_rpm_fan_cpu(self)
        """
        x = 634
        y = 178

        for image in self.images["rpm_fan"]:
            self.figures["rpm_fan_cpu"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["rpm_fan_cpu"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_rpm_fan_gpu(self):
        """
        print_rpm_fan_gpu(self)
        """
        x = 634
        y = 219

        for image in self.images["rpm_fan"]:
            self.figures["rpm_fan_gpu"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["rpm_fan_gpu"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_rpm_fan_case(self):
        """
        print_rpm_fan_case(self)
        """
        x = 634
        y = 262

        for image in self.images["rpm_fan"]:
            self.figures["rpm_fan_case"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["rpm_fan_case"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_rpm_pump_cpu(self):
        """
        print_rpm_pump_cpu(self)
        """
        x = 634
        y = 329

        for image in self.images["rpm_pump"]:
            self.figures["rpm_pump_cpu"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["rpm_pump_cpu"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_rpm_pump_gpu(self):
        """
        print_rpm_pump_gpu(self)
        """
        x = 634
        y = 370

        for image in self.images["rpm_pump"]:
            self.figures["rpm_pump_gpu"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["rpm_pump_gpu"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    # ----------------------------------------------------------------------------------------
    # Pre Print TEMP
    # ----------------------------------------------------------------------------------------

    def pre_print_temp_soc(self):
        """
        print_temp_soc(self)
        """
        x = 144
        y = 433

        for image in self.images["degree"]:
            self.figures["temp_soc"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["temp_soc"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_temp_wc_cpu(self):
        """
        print_temp_wc_cpu(self)
        """
        x = 342
        y = 433

        for image in self.images["degree"]:
            self.figures["temp_wc_cpu"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["temp_wc_cpu"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_temp_wc_gpu(self):
        """
        print_temp_wc_gpu(self)
        """
        x = 542
        y = 433

        for image in self.images["degree"]:
            self.figures["temp_wc_gpu"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["temp_wc_gpu"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    def pre_print_temp_case(self):
        """
        print_temp_case(self)
        """
        x = 740
        y = 433

        for image in self.images["degree"]:
            self.figures["temp_case"].append(self.modules["archgui"].graph_draw_image(
                uniqid=self.window,
                graph=self.graph,
                location=(x, y),
                image=image))

        for fig in self.figures["temp_case"]:
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=fig)

    # ----------------------------------------------------------------------------------------
    # Generate
    # ----------------------------------------------------------------------------------------

    def generate(self):
        """
        test
        """
        self.modules["archgui"].graph_draw_image(
            uniqid=self.window,
            graph=self.graph,
            location=(10, 10),
            image=self.images["background"])

        self.figures["led_a"] = {
            "on": None,
            "off": None
        }

        self.figures["led_b"] = {
            "on": None,
            "off": None
        }

        self.figures["led_c"] = {
            "on": None,
            "off": None
        }

        self.figures["mode_silent"] = {
            "on": None,
            "off": None
        }

        self.figures["mode_performance"] = {
            "on": None,
            "off": None
        }

        self.figures["pwm_fan_soc"] = {
            "dark": [],
            "light": []}

        self.figures["pwm_fan_cpu"] = {
            "dark": [],
            "light": []}

        self.figures["pwm_fan_gpu"] = {
            "dark": [],
            "light": []}

        self.figures["pwm_fan_case"] = {
            "dark": [],
            "light": []}

        self.figures["rpm_fan_soc"] = []
        self.figures["rpm_fan_cpu"] = []
        self.figures["rpm_fan_gpu"] = []
        self.figures["rpm_fan_case"] = []

        self.figures["pwm_pump_cpu"] = {
            "dark": [],
            "light": []}

        self.figures["pwm_pump_gpu"] = {
            "dark": [],
            "light": []}

        self.figures["rpm_pump_cpu"] = []
        self.figures["rpm_pump_gpu"] = []

        self.figures["temp_wc_cpu"] = []
        self.figures["temp_wc_gpu"] = []
        self.figures["temp_soc"] = []
        self.figures["temp_case"] = []

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.pre_print_config()),
                executor.submit(self.pre_print_led()),
                executor.submit(self.pre_print_mode()),

                executor.submit(self.pre_print_pwm_fan_soc()),
                executor.submit(self.pre_print_pwm_fan_cpu()),
                executor.submit(self.pre_print_pwm_fan_gpu()),
                executor.submit(self.pre_print_pwm_fan_case()),
                executor.submit(self.pre_print_pwm_pump_cpu()),
                executor.submit(self.pre_print_pwm_pump_gpu()),

                executor.submit(self.pre_print_rpm_fan_soc()),
                executor.submit(self.pre_print_rpm_fan_cpu()),
                executor.submit(self.pre_print_rpm_fan_gpu()),
                executor.submit(self.pre_print_rpm_fan_case()),
                executor.submit(self.pre_print_rpm_pump_cpu()),
                executor.submit(self.pre_print_rpm_pump_gpu()),

                executor.submit(self.pre_print_temp_soc()),
                executor.submit(self.pre_print_temp_wc_cpu()),
                executor.submit(self.pre_print_temp_wc_gpu()),
                executor.submit(self.pre_print_temp_case())
            ]
            wait(futures)

    # ----------------------------------------------------------------------------------------
    # Print LED
    # ----------------------------------------------------------------------------------------

    def print_led_a(self):
        """
        print_led_a()
        """

        fig_led_a_back = self.figures["led_a"]["off"]
        fig_led_a_front = self.figures["led_a"]["on"]

        fig_led_b_back = self.figures["led_b"]["on"]
        fig_led_b_front = self.figures["led_b"]["off"]

        fig_led_c_back = self.figures["led_c"]["on"]
        fig_led_c_front = self.figures["led_c"]["off"]

        self.print_led_active(
            fig_led_a_back, fig_led_a_front,
            fig_led_b_back, fig_led_b_front,
            fig_led_c_back, fig_led_c_front)

        self.infos["led"] = "a"

    def print_led_b(self):
        """
        print_led_b()
        """
        fig_led_a_back = self.figures["led_a"]["on"]
        fig_led_a_front = self.figures["led_a"]["off"]

        fig_led_b_back = self.figures["led_b"]["off"]
        fig_led_b_front = self.figures["led_b"]["on"]

        fig_led_c_back = self.figures["led_c"]["on"]
        fig_led_c_front = self.figures["led_c"]["off"]

        self.print_led_active(
            fig_led_a_back, fig_led_a_front,
            fig_led_b_back, fig_led_b_front,
            fig_led_c_back, fig_led_c_front)

        self.infos["led"] = "b"

    def print_led_c(self):
        """
        print_led_c()
        """
        fig_led_a_back = self.figures["led_a"]["on"]
        fig_led_a_front = self.figures["led_a"]["off"]

        fig_led_b_back = self.figures["led_b"]["on"]
        fig_led_b_front = self.figures["led_b"]["off"]

        fig_led_c_back = self.figures["led_c"]["off"]
        fig_led_c_front = self.figures["led_c"]["on"]

        self.print_led_active(
            fig_led_a_back, fig_led_a_front,
            fig_led_b_back, fig_led_b_front,
            fig_led_c_back, fig_led_c_front)

        self.infos["led"] = "b"

    def print_led_active(self,
                         fig_led_a_back, fig_led_a_front,
                         fig_led_b_back, fig_led_b_front,
                         fig_led_c_back, fig_led_c_front):
        """
        print_led_c()
        """
        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_led_a_back)
        self.modules["archgui"].graph_bring_figure_to_front(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_led_a_front)

        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_led_b_back)
        self.modules["archgui"].graph_bring_figure_to_front(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_led_b_front)

        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_led_c_back)
        self.modules["archgui"].graph_bring_figure_to_front(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_led_c_front)

    # ----------------------------------------------------------------------------------------
    # Print Mode
    # ----------------------------------------------------------------------------------------

    def print_mode_silent_active(self):
        """
        print_mode_silent_active()
        """
        fig_silent_back = self.figures["mode_silent"]["off"]
        fig_silent_front = self.figures["mode_silent"]["on"]
        fig_performance_back = self.figures["mode_performance"]["on"]
        fig_performance_front = self.figures["mode_performance"]["off"]

        self.print_mode_active(fig_silent_back, fig_silent_front, fig_performance_back, fig_performance_front)

    def print_mode_performance_active(self):
        """
        print_mode_performance_active()
        """
        fig_silent_back = self.figures["mode_silent"]["on"]
        fig_silent_front = self.figures["mode_silent"]["off"]
        fig_performance_back = self.figures["mode_performance"]["off"]
        fig_performance_front = self.figures["mode_performance"]["on"]

        self.print_mode_active(fig_silent_back, fig_silent_front, fig_performance_back, fig_performance_front)

    def print_mode_active(self, fig_silent_back, fig_silent_front, fig_performance_back, fig_performance_front):
        """
        print_mode_active()
        """
        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_silent_back)
        self.modules["archgui"].graph_bring_figure_to_front(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_silent_front)
        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_performance_back)
        self.modules["archgui"].graph_bring_figure_to_front(
            uniqid=self.window,
            graph=self.graph,
            figure=fig_performance_front)

    # ----------------------------------------------------------------------------------------
    # Print TXT
    # ----------------------------------------------------------------------------------------

    def print_percent(self, target):
        """
        :param target:
        """
        value = int(self.new_infos[target] * 0.20)

        for x in range(value):
            self.modules["archgui"].graph_bring_figure_to_front(
                uniqid=self.window,
                graph=self.graph,
                figure=self.figures[target]["light"][x])

        for x in range(19 - value):
            self.modules["archgui"].graph_send_figure_to_back(
                uniqid=self.window,
                graph=self.graph,
                figure=self.figures[target]["light"][19 - x])

    def print_rpm(self, target):
        """
        :param target:
        """
        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures[target][self.new_infos[target]])

        self.modules["archgui"].graph_bring_figure_to_front(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures[target][self.new_infos[target]])

    def print_degree(self, target):
        """
        :param target:
        """
        self.modules["archgui"].graph_send_figure_to_back(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures[target][self.new_infos[target]])

        self.modules["archgui"].graph_bring_figure_to_front(
            uniqid=self.window,
            graph=self.graph,
            figure=self.figures[target][self.new_infos[target]])

    # ----------------------------------------------------------------------------------------
    # Reveal
    # ----------------------------------------------------------------------------------------

    def reveal(self, infos: dict):
        """
        :param infos:
        """

        self.new_infos = {
            "mode": infos["mode"],
            "led": infos["led"],
            "pwm_fan_soc": infos["pwm_fan_soc"],
            "pwm_fan_cpu": infos["pwm_fan_cpu"],
            "pwm_fan_gpu": infos["pwm_fan_gpu"],
            "pwm_fan_case": infos["pwm_fan_case"],
            "pwm_pump_cpu": infos["pwm_pump_cpu"],
            "pwm_pump_gpu": infos["pwm_pump_gpu"],
            "rpm_fan_soc": int(infos["rpm_fan_soc"] / 50),
            "rpm_fan_cpu": int(infos["rpm_fan_cpu"] / 50),
            "rpm_fan_gpu": int(infos["rpm_fan_gpu"] / 50),
            "rpm_fan_case": int(infos["rpm_fan_case"] / 50),
            "rpm_pump_cpu": int(infos["rpm_pump_cpu"] / 50),
            "rpm_pump_gpu": int(infos["rpm_pump_gpu"] / 50),
            "temp_wc_cpu": infos["temp_wc_cpu"],
            "temp_wc_gpu": infos["temp_wc_gpu"],
            "temp_soc": infos["temp_soc"],
            "temp_case": infos["temp_case"],
        }

        # --------------------------------

        if self.new_infos["mode"] != self.infos["mode"]:
            if infos["mode"] == "silent":
                self.print_mode_silent_active()
            if infos["mode"] == "performance":
                self.print_mode_performance_active()

        # --------------------------------

        if self.new_infos["pwm_fan_soc"] != self.infos["pwm_fan_soc"]:
            self.print_percent("pwm_fan_soc")

        if self.new_infos["pwm_fan_cpu"] != self.infos["pwm_fan_cpu"]:
            self.print_percent("pwm_fan_cpu")

        if self.new_infos["pwm_fan_gpu"] != self.infos["pwm_fan_gpu"]:
            self.print_percent("pwm_fan_gpu")

        if self.new_infos["pwm_fan_case"] != self.infos["pwm_fan_case"]:
            self.print_percent("pwm_fan_case")

        if self.new_infos["pwm_pump_cpu"] != self.infos["pwm_pump_cpu"]:
            self.print_percent("pwm_pump_cpu")

        if self.new_infos["pwm_pump_gpu"] != self.infos["pwm_pump_gpu"]:
            self.print_percent("pwm_pump_gpu")

        # --------------------------------

        if self.new_infos["rpm_fan_soc"] != self.infos["rpm_fan_soc"]:
            self.print_rpm("rpm_fan_soc")

        if self.new_infos["rpm_fan_cpu"] != self.infos["rpm_fan_cpu"]:
            self.print_rpm("rpm_fan_cpu")

        if self.new_infos["rpm_fan_gpu"] != self.infos["rpm_fan_gpu"]:
            self.print_rpm("rpm_fan_gpu")

        if self.new_infos["rpm_fan_case"] != self.infos["rpm_fan_case"]:
            self.print_rpm("rpm_fan_case")

        if self.new_infos["rpm_pump_cpu"] != self.infos["rpm_pump_cpu"]:
            self.print_rpm("rpm_pump_cpu")

        if self.new_infos["rpm_pump_gpu"] != self.infos["rpm_pump_gpu"]:
            self.print_rpm("rpm_pump_gpu")

        # --------------------------------

        if self.new_infos["temp_soc"] != self.infos["temp_soc"]:
            self.print_degree("temp_soc")

        if self.new_infos["temp_wc_cpu"] != self.infos["temp_wc_cpu"]:
            self.print_degree("temp_wc_cpu")

        if self.new_infos["temp_wc_gpu"] != self.infos["temp_wc_gpu"]:
            self.print_degree("temp_wc_gpu")

        if self.new_infos["temp_case"] != self.infos["temp_case"]:
            self.print_degree("temp_case")

        self.infos = self.new_infos
