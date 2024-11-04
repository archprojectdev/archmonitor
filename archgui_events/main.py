"""
Class Events
"""


class Events:
    """
    Class Events
    """
    def __init__(self):

        self.windows = None
        self.window = None
        self.model = None

        # -------------------------------

        self.figure = None

    def events(self, event, modules, values):
        """
        :param event:
        :param modules:
        :param values:
        """
        if event == 'graph_interface button-1':

            x = values["graph_interface"][0]
            y = values["graph_interface"][1]

            if 157 < x < int(157 + 88) and 24 < y < int(24 + 58):
                modules["display"].print_led_a()
                modules["spiled"].set_led_a()

            if 246 < x < int(246 + 88) and 24 < y < int(24 + 58):
                modules["display"].print_led_b()
                modules["spiled"].set_led_b()

            if 335 < x < int(335 + 88) and 24 < y < int(24 + 58):
                modules["display"].print_led_c()
                modules["spiled"].set_led_c()

            # ----------------------------------------------------

            if 447 < x < int(447 + 168) and 24 < y < int(24 + 58):
                modules["listener"].set_mode_silent()
                modules["display"].print_mode_silent_active()

            if 615 < x < int(615 + 168) and 24 < y < int(24 + 58):
                modules["listener"].set_mode_performance()
                modules["display"].print_mode_performance_active()
