import tkinter as tk
from tkinter import ttk
import lichtint_plot
import plot_temp
from tkinter import *
import serial
import serial.tools.list_ports

def on_select(event=None):
    if event:
        if (event.widget.get() == 'Manual'):
            frame2.pack_forget()
            MinLabelTabOne = tk.Label(manual, text="Minimale oprol:")
            MaxLabelTabOne = tk.Label(manual, text="Maximale uitrol:")
            DeviceNameLabelTabOne = tk.Label(manual, text="Device name")
            MinEntryTabOne = tk.Entry(manual)
            MaxEntryTabOne = tk.Entry(manual)
            DeviceNameEntryTabOne = tk.Entry(manual)

            buttonForward = tk.Button(manual, text="Send")
            buttonBack = tk.Button(manual, text="Send")

            MinLabelTabOne.grid(row=2, column=0, padx=15, pady=15)
            MinEntryTabOne.grid(row=2, column=1, padx=15, pady=15)
            MaxLabelTabOne.grid(row=3, column=0, padx=15, pady=15)
            MaxEntryTabOne.grid(row=3, column=1, padx=15, pady=15)
            DeviceNameLabelTabOne.grid(row=5, column=0, padx=15, pady=15)
            DeviceNameEntryTabOne.grid(row=5, column=1, padx=15, pady=15)
            buttonForward.grid(row=3, column=3, padx=15, pady=15)
            buttonBack.grid(row=5, column=3, padx=15, pady=15)
            manual.pack(anchor=N, padx=(0, 30))
            frame1.pack(side=LEFT, anchor=N, padx=(0, 30))

        elif (event.widget.get() == 'Automatic'):
            frame1.pack_forget()

            automatic.pack()
            frame2.pack(side=LEFT)

## maakt het frame
centrale = tk.Tk()
centrale.title("Zonnescherm bediening")
centrale.geometry("1100x800")

## maakt de tabs
tab_parent = ttk.Notebook(centrale)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text="Home")
tab_parent.add(tab2, text="Instellingen")
tab_parent.add(tab3, text="Licht")
tab_parent.add(tab4, text="Temperatuur")
#####################

frame1 = ttk.Frame(tab2)
frame2 = ttk.Frame(tab2)
manual = ttk.Frame(frame1)
automatic = ttk.Frame(frame2)


##############

cb = ttk.Combobox(tab2, values=("Automatic", "Manual"))
cb.set("Manual")
cb.grid(row=0, column=0, padx=15, pady=15)
cb.pack()
cb.bind('<<ComboboxSelected>>', on_select)

ON = tk.Button(tab1, text="ON")
ON.pack(anchor=W, padx=(30, 0), pady=(30,0))
OFF = tk.Button(tab1, text="OFF")
OFF.pack(anchor=W, padx=(30, 30))
ON = tk.Button(tab2, text="ON")
ON.pack(anchor=W, padx=(30, 0), pady=(30,0))
OFF = tk.Button(tab2, text="OFF")
OFF.pack(anchor=W, padx=(30, 30))


radio = IntVar()
ports = list(serial.tools.list_ports.comports())
radio1 = IntVar()
radio2 = IntVar()
radio3 = IntVar()
radio4 = IntVar()
current_unit= ''

d = {}
for p in ports:
    d[str(p[0])] = serial.Serial(p[0], 19200)


def selection1():
    selection = "You selected the option " + ("COM" + str(radio1.get()))
    print(selection)
    current_unit = ("COM" + str(radio1.get()))
def selection2():
    selection = "You selected the option " + ("COM" + str(radio2.get()))
    print(selection)
    current_unit = ("COM" + str(radio1.get()))
def selection3():
    selection = "You selected the option " + ("COM" + str(radio3.get()))
    print(selection)
    current_unit = ("COM" + str(radio1.get()))
def selection4():
    selection = "You selected the option " + ("COM" + str(radio4.get()))
    print(selection)
    current_unit = ("COM" + str(radio1.get()))


def makeradioboxes(dict):
    i = 0
    for k in dict:
        Radiobutton(tab1, text=str(k), variable=radio1, value=str(k)[3], command=selection1).pack(anchor=E, padx=(0, 30))
        i+=1
    i = 0
    for k in dict:
        Radiobutton(tab2, text=str(k), variable=radio2, value=str(k)[3], command=selection2).pack(anchor=E, padx=(0, 30))
        i+=1
    i = 0
    for k in dict:
        Radiobutton(tab3, text=str(k), variable=radio3, value=str(k)[3],  command=selection3).pack(anchor=E, padx=(0, 30))
        i+=1
    i = 0
    for k in dict:
        Radiobutton(tab4, text=str(k), variable=radio4, value=str(k)[3],  command=selection4).pack(anchor=E, padx=(0, 30))
        i+=1

makeradioboxes(d)
lichtplot = lichtint_plot.Plot(tab3)
temperatuurplot = plot_temp.Plot(tab4)
################
tab_parent.pack(expand=1,fill= 'both')
print("~~"+ current_unit)
centrale.mainloop()
