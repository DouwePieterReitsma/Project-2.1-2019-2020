from tkinter import *
from tkinter import ttk
import threading
import update_ports
import light
import temp

class frame_for_graph_light():
    def __init__(self, rt, ser):
        self.frame = rt
        self.licht_plot = light.Plot(self.frame)
        self.ser1 = ser
        self.readSerial()

    ## keeps taking the input from the serial connection and puts it into the funct
    def readSerial(self):
        c = self.ser1.read()
        c = str(int.from_bytes(c, "big"))
        self.licht_plot.step(c)
        self.frame.after(100, self.readSerial)  # check serial again soon


class frame_for_graph_temp():
    def __init__(self, rt, ser):
        self.frame = rt
        self.temp_plot = temp.Plot(self.frame)
        self.ser1 = ser
        self.readSerial()

    ## keeps taking the input from the serial connection and puts it into the funct
    def readSerial(self):
        c = self.ser1.read()
        c = str(int.from_bytes(c, "big"))
        self.temp_plot.step(c)
        self.frame.after(100, self.readSerial)  # check serial again soon




class gui():
    def __init__(self, root):
        self.frame = root
        self.updater = update_ports.update_ports(self.frame)
        self.current_unit = ''
        self.frame.title("Zonnescherm bediening")
        self.frame.geometry("1200x800")

        #tabs
        self.tab_parent = ttk.Notebook(self.frame)
        self.tab1 = ttk.Frame(self.tab_parent)
        self.tab2 = ttk.Frame(self.tab_parent)
        self.tab3 = ttk.Frame(self.tab_parent)

        self.tab_parent.add(self.tab1, text="Instellingen")
        self.tab_parent.add(self.tab2, text="Licht")
        self.tab_parent.add(self.tab3, text="Temperatuur")
        self.tab_parent.pack(expand=1, fill='both')

        #initializes frames for the radiobuttons that hold the available ports options
        self.frame1 = ttk.Frame(self.tab1)
        self.frame2 = ttk.Frame(self.tab2)
        self.frame3 = ttk.Frame(self.tab3)


        #radio buttons listeners
        self.radio1 = IntVar()
        self.radio2 = IntVar()
        self.radio3 = IntVar()


        #update the radiobuttons for ports
        self.updateradio = threading.Thread(target=self.radiobuttons(), args=(1,))
        self.updateradio.start()

        #settingframe
        self.setting_frame = ttk.Frame(self.tab1)
        #lightframe
        self.light_frame = ttk.Frame(self.frame2)
        #tempframe
        self.temp_frame = ttk.Frame(self.frame3)


        # ON OFF buttons
        ON = Button(self.setting_frame, text="ON")
        ON.pack(anchor=W, padx=(30, 0), pady=(30, 0))
        OFF = Button(self.setting_frame, text="OFF")
        OFF.pack(anchor=W, padx=(30, 30))



    def make_settings_screen(self, current_unit):
        self.setting_frame.pack_forget()
        self.setting_frame = ttk.Frame(self.tab1)

        self.current_unit = current_unit
        Label(self.setting_frame, text=self.current_unit).pack()
        framesies = ttk.Frame(self.setting_frame)

        ON = Button(framesies, text="ON")
        OFF = Button(framesies, text="OFF")
        MinLabelTabOne = Label(framesies, text="Minimale oprol:")
        MaxLabelTabOne = Label(framesies, text="Maximale uitrol:")
        DeviceNameLabelTabOne = Label(framesies, text="Device name")
        MinEntryTabOne = Entry(framesies)
        MaxEntryTabOne = Entry(framesies)
        DeviceNameEntryTabOne = Entry(framesies)
        buttonForward = Button(framesies, text="Send")
        buttonBack = Button(framesies, text="Send")

        ON.grid(row=0, column=0, padx=5)
        OFF.grid(row=1, column=0, padx=5)
        MinLabelTabOne.grid(row=2, column=0, padx=15, pady=15)
        MinEntryTabOne.grid(row=2, column=1, padx=15, pady=15)
        MaxLabelTabOne.grid(row=3, column=0, padx=15, pady=15)
        MaxEntryTabOne.grid(row=3, column=1, padx=15, pady=15)
        DeviceNameLabelTabOne.grid(row=5, column=0, padx=15, pady=15)
        DeviceNameEntryTabOne.grid(row=5, column=1, padx=15, pady=15)
        buttonForward.grid(row=3, column=3, padx=15, pady=15)
        buttonBack.grid(row=5, column=3, padx=15, pady=15)

        framesies.pack(anchor=W)
        self.setting_frame.pack(anchor=W)

    def make_light_screen(self, current_unit):
        self.current_unit = current_unit
        self.light_frame.pack_forget()
        self.light_frame = ttk.Frame(self.tab2, width=900, height=650)
        #self.framesies2 = ttk.Frame(self.light_frame, width=100, height=100)

        ser31 = self.updater.return_dict()[self.current_unit]
        frame_for_graph_light(self.light_frame, ser31)

        self.light_frame.pack(anchor=SW)

    def make_temp_screen(self, current_unit):
        self.current_unit = current_unit
        self.temp_frame.pack_forget()
        self.temp_frame = ttk.Frame(self.tab3, width=900, height=650)
        self.framesies3 = ttk.Frame(self.temp_frame, width=100, height=100)

        ser32 = self.updater.return_dict()[self.current_unit]
        frame_for_graph_temp(self.framesies3, ser32)

        self.framesies3.pack()
        self.temp_frame.pack(anchor=SW)



    #handles selection of radiobuttons for selected ports
    def selection1(self):
        self.current_unit = ("COM" + str(self.radio1.get()))
        self.make_settings_screen(self.current_unit)

    def selection2(self):
        self.current_unit = ("COM" + str(self.radio2.get()))
        self.make_light_screen(self.current_unit)

    def selection3(self):
        self.current_unit = ("COM" + str(self.radio3.get()))
        self.make_temp_screen(self.current_unit)


    #function that makes and deletes the radiobuttons according to ports_list
    def radiobuttons(self):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame1 = ttk.Frame(self.tab1)
        self.frame2 = ttk.Frame(self.tab2)
        self.frame3 = ttk.Frame(self.tab3)

        self.updateports = threading.Thread(target=self.updater.updatePorts(), args=(0,))
        self.updateports.start()


        if len(self.updater.return_ports_list()) > 0:
            for port in self.updater.return_ports_list():
                i = 0
                Radiobutton(self.frame1, text=str(port), variable=self.radio1, value=str(port)[3], command=self.selection1).pack(anchor=E,
                                                                                                          padx=(0, 30))
                Radiobutton(self.frame2, text=str(port), variable=self.radio2, value=str(port)[3], command=self.selection2).pack(anchor=E,
                                                                                                          padx=(0, 30))
                Radiobutton(self.frame3, text=str(port), variable=self.radio3, value=str(port)[3], command=self.selection3).pack(anchor=E,
                                                                                                          padx=(0, 30))
                self.updater.updatePorts()
                i += 1
        else:
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.frame3.pack_forget()

        self.frame1.pack(anchor=E)
        self.frame2.pack(anchor=NE)
        self.frame3.pack(anchor=E)
        self.frame.after(1000, self.radiobuttons)


root = Tk()
gui(root)
root.mainloop()


