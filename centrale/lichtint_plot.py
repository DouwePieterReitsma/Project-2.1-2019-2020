from tkinter import *
from random import randint


class Plot:
    def __init__(self, f):
        # init global vars
        self.root=f
        self.s = 1
        self.x2 = 150

        global min
        global max

        min = 0
        max = 50
        self.y2 = self.value_to_y(randint(min, max))
        global running
        running = True
####################33
        self.canvas = Canvas(self.root, width=900, height=650)  # 0,0 is top left corner
        self.canvas.pack(expand=YES, fill=BOTH)

        self.canvas.create_text(80, 500, text='licht', anchor=E)
        self.canvas.create_text(150, 525, text='minuut', anchor=E)
        self.canvas.create_line(100, 500, 900, 500, width=2)  # x-axis
        self.canvas.create_line(100, 500, 100, 150, width=2)  # y-axis

        if running == True:
            self.canvas.after(300, self.step)

        for i in range(17):
            x = 100 + (i * 50)
            self.canvas.create_line(x, 500, x, 150, width=1, dash=(2, 5))
            self.canvas.create_text(x, 500, text='%d' % (1 * i), anchor=N)

        for i in range(8):
            y = 500 - (i * 50)
            self.canvas.create_line(100, y, 900, y, width=1, dash=(2, 5))
            self.canvas.create_text(90, y, text='%d' % (1 * i), anchor=E)

###############################3

    def value_to_y(self, val):
        return 450 - 5 * val
    def step(self):
        global s, x2, y2
        if self.s == 17:
            # new frame
            self.s = 1
            self.x2 = 50
            self.canvas.delete('temp')  # only delete items tagged as temp
        self.x1 = self.x2
        self.y1 = self.y2
        self.x2 = 50 + self.s * 50
        self.y2 = self.value_to_y(randint(min, max))
        self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='pink', tags='temp')
        self.s = self.s + 1