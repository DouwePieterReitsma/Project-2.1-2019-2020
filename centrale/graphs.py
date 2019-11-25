import time
from tkinter import *

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
from collections import defaultdict

style.use('ggplot')


class GraphBase:
    def __init__(self, root, serial_connections):
        self.root = root
        self.serial_connections = serial_connections
        # self.enabled_lines = {k: True for (k, v) in serial_connections.items()}  # enable all lines by default
        self.enabled_lines = defaultdict(lambda: False)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.p = self.figure.add_subplot(111)

        self.p.set_xlim([0, 60])

        self.canvas = FigureCanvasTkAgg(figure=self.figure, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=YES, fill=BOTH, anchor=W)

        self.ani = animation.FuncAnimation(self.figure, self.update, interval=1000)

    def update(self, frame):
        pass

    def set_line_visibility(self, line_name, value):
        self.enabled_lines[line_name] = value


class LightGraph(GraphBase):
    def __init__(self, root, serial_connections):
        super().__init__(root, serial_connections)

        self.figure.suptitle('Lichtintensiteit')

    def update(self, frame):
        self.p.clear()

        self.p.set_xlim([0, 60])
        self.p.set_xlabel('Minuten', fontsize=8)
        self.p.set_ylabel('Lichtintensiteit', fontsize=8)

        for k, connection in self.serial_connections.items():
            if self.enabled_lines[connection.port]:
                self.p.plot(range(1, len(connection.light_intensity_data) + 1), connection.light_intensity_data, '.-',
                            label=k)

        self.p.legend()


class TemperatureGraph(GraphBase):
    def __init__(self, root, serial_connections):
        super().__init__(root, serial_connections)

        self.figure.suptitle('Temperatuur')

    def update(self, frame):
        self.p.clear()

        self.p.set_xlim([0, 60])
        self.p.set_xlabel('Minuten', fontsize=8)
        self.p.set_ylabel('°C', fontsize=8)

        for k, connection in self.serial_connections.items():
            if self.enabled_lines[connection.port]:
                self.p.plot(range(1, len(connection.temperature_data) + 1), connection.temperature_data, '.-',
                            label=k)

        self.p.legend()
