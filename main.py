"""
main.py
"""

import os
import sys
import time
import signal
import subprocess
import archgui


from Listener import Listener
from Display import Display
from Spiled import Spiled


if __name__ == "__main__":

    display = Display()
    listener = Listener()
    spiled = Spiled()

    modules = {
        "archgui": archgui,
        "display": display,
        "listener": listener,
        "spiled": spiled
    }

    cmd_temperature = ['python', 'Temperature.py']
    pro_temperature = subprocess.Popen(cmd_temperature)

    def signal_handler(_, __):
        """
        :param _:
        :param __:
        """
        os.killpg(os.getpgid(pro_temperature.pid), signal.SIGTERM)
        # modules["spiled"].exit()
        # modules["listener"].exit()
        # modules["display"].exit()
        # modules["archgui"].exit()
        sys.exit(0)

    while True:
        time.sleep(1)
        if os.path.exists("temperature.txt"):
            break

    archgui.define_modules(modules)
    display.define_modules(modules)
    listener.define_modules(modules)
    spiled.define_modules(modules)

    main_uniqid = archgui.open(model="main", title="Archgui - Monitoring")
    archgui.define_main(main_uniqid)
    archgui.bind(
        uniqid=main_uniqid,
        binds=[
            {
                "item": "graph_interface",
                "bind_string": "<Button-1>",
                "bind_key": " button-1"
            }
        ])

    display.define_graph(main_uniqid, "graph_interface")
    display.generate()

    signal.signal(signal.SIGINT, signal_handler)

    spiled.run()
    listener.run()
    archgui.run()
