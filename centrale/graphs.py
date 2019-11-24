import time
from tkinter import *

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation

style.use('ggplot')

class GraphBase:
    def __init__(self, root, serial_connections):
        self.root = root
        self.serial_connections = serial_connections

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.p = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(figure=self.figure, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=YES, fill=BOTH, anchor=W)

        self.ani = animation.FuncAnimation(self.figure, self.update, interval=1000)

    def update(self, frame):
        pass


class LightGraph(GraphBase):
    def __init__(self, root, serial_connections):
        super().__init__(root, serial_connections)

        self.figure.suptitle('Lichtintensiteit')

    def update(self, frame):
        self.p.clear()

        for k, connection in self.serial_connections.items():
            self.p.plot(range(1, len(connection.light_intensity_data) + 1), connection.light_intensity_data, '.-',
                        label=k)

        self.p.legend()


class TemperatureGraph(GraphBase):
    def __init__(self, root, serial_connections):
        super().__init__(root, serial_connections)

        self.figure.suptitle('Temperatuur')

    def update(self, frame):
        self.p.clear()

        for k, connection in self.serial_connections.items():
            self.p.plot(range(1, len(connection.temperature_data) + 1), connection.temperature_data, '.-',
                        label=k)

        self.p.legend()
