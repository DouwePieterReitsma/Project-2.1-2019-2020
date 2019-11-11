from tkinter import *

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

# class Plot:
#     def __init__(self, f):
#         self.root= f
#         self.s = 1
#         self.x2 = 100
#         self.y2 = self.value_to_y(1)
#
#         self.canvas = Canvas(self.root, width=950, height=520)  # 0,0 is top left corner
#         self.canvas.pack(expand=YES, fill=BOTH)
#
#         self.canvas.create_text(80, 500, text='light', anchor=E)
#         self.canvas.create_text(150, 525, text='minuut', anchor=E)
#         self.canvas.create_line(100, 500, 900, 500, width=2)  # x-axis
#         self.canvas.create_line(100, 500, 100, 150, width=2)  # y-axis
#
#
#         for i in range(17):
#             x = 100 + (i * 50)
#             self.canvas.create_line(x, 500, x, 150, width=1, dash=(2, 5))
#             self.canvas.create_text(x, 500, text='%d' % (1 * i), anchor=N)
#
#         for i in range(8):
#             y = 500 - (i * 50)
#             self.canvas.create_line(100, y, 900, y, width=1, dash=(2, 5))
#             self.canvas.create_text(90, y, text='%d' % (1 * i), anchor=E)
#
#
#
#     def value_to_y(self, val):
#         return 450 - 5 * (val*10)
#
#     def step(self, c):
#         global s, x2, y2
#         if self.s == 18:
#             self.s = 1
#             self.x2 = 100
#             self.canvas.delete('temp')
#
#         self.x1 = self.x2
#         self.y1 = self.y2
#         self.x2 = 50 + self.s * 50
#         self.y2 = self.value_to_y(int(c))
#         self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='black', tags='temp')
#         self.s = self.s + 1

class Plot:
    def __init__(self, root):
        self.figure = Figure(figsize=(5,4), dpi=100)
        self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(figure=self.figure, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=YES, fill=BOTH)

    def value_to_y(self):
        pass

    def step(self, c):


        pass