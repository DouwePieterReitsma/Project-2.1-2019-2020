from tkinter import *

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
import pandas as pd
import time

from threading import Thread


class GraphBase:
    def __init__(self, root, serial_connections):
        self.serial_connections = serial_connections

        # store data for each line / arduino
        self.data = {}

        self.updater = Thread(target=self.update)

        self.updater.daemon = False
        self.updater.start()

        self.figure = plt.figure(figsize=(5, 4), dpi=100)

        self.canvas = FigureCanvasTkAgg(figure=self.figure, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=YES, fill=BOTH, anchor=W)

    def update(self):
        pass


class LightGraph(GraphBase):
    def __init__(self, root, serial_connections):
        super().__init__(root, serial_connections)

        self.figure.suptitle('Lichtintensiteit')

    def update(self):
        while True:
            for k, connection in self.serial_connections.items():
                self.data[connection.port] = [light for (light, _, _) in connection.data]

            for k, v in self.data.items():
                plt.plot(range(1, len(v) + 1), v, '.-', label=k)

            plt.legend()
            plt.show()

            time.sleep(5)


class TemperatureGraph(GraphBase):
    def __init__(self, root, serial_connections):
        super().__init__(root, serial_connections)

        self.figure.suptitle('Temperatuur')

    def update(self):
        while True:
            for connection in self.serial_connections:
                self.data[connection.port] = [temperature for (_, temperature, _) in connection.data]
