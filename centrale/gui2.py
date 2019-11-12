from tkinter import *
from tkinter import ttk
import threading
import update_ports
import light
import temp
import serial_protocol
import time

class gui():
    def __init__(self, root):
        self.frame = root
        self.updater = update_ports.update_ports(self.frame)
        self.current_unit = ''
        self.frame.title("Zonnescherm bediening")
        self.frame.geometry("1200x800")


        #tabs
        self.tab_parent = ttk.Notebook(self.frame)
        self.tab1 = Frame(self.tab_parent)
        self.tab2 = Frame(self.tab_parent)
        self.tab3 = Frame(self.tab_parent)

        # label for devices available
        self.deviceslabelframe = Frame(self.tab1, width=1200, height=20)
        self.deviceslabelframe.pack(anchor=N, fill=Y, expand=False)
        self.deviceslabelframe = Frame(self.tab2, width=1200, height=20)
        self.deviceslabelframe.pack(anchor=N, fill=Y, expand=False)
        self.deviceslabelframe = Frame(self.tab3, width=1200, height=20)
        self.deviceslabelframe.pack(anchor=N, fill=Y, expand=False)


        self.tab_parent.add(self.tab1, text="Instellingen")
        self.tab_parent.add(self.tab2, text="Licht")
        self.tab_parent.add(self.tab3, text="Temperatuur")
        self.tab_parent.pack(expand=1, fill='both')

        #initializes frames for the radiobuttons that hold the available ports options
        self.frame1 = Frame(self.tab1)
        self.frame2 = Frame(self.tab2)
        self.frame3 = Frame(self.tab3)



        #radio buttons listeners
        self.radio1 = IntVar()
        self.radio2 = IntVar()
        self.radio3 = IntVar()


        #update the radiobuttons for ports
        self.updateradio = threading.Thread(target=self.radiobuttons(), args=(1,))
        self.updateradio.start()

        #settingframe
        self.setting_frame = Frame(self.tab1,  width=100, height=100, bg="black")


        #lightframe
        self.light_frame = Frame(self.tab2)
        #tempframe
        self.temp_frame = Frame(self.tab3)


        # ON OFF buttons
        ON = Button(self.setting_frame, text="ON")
        ON.pack(anchor=W, padx=(30, 0), pady=(30, 0))
        OFF = Button(self.setting_frame, text="OFF")
        OFF.pack(anchor=W, padx=(30, 30))


    def make_settings_screen(self, current_unit):
        self.setting_frame.pack_forget()
        self.setting_frame = Frame(self.tab1, width=100, height=100,)


        self.current_unit = current_unit
        Label(self.setting_frame, text="Geselecteerde unit: " + self.current_unit).pack(anchor=NW, padx=(20,0), pady=(5,5))

        self.buttonsframe = Frame(self.setting_frame, width=100, height=50)
        self.framesies = Frame(self.setting_frame)


        ####buttons
        self.show_settingsbutton = Button(self.buttonsframe, text="settings", command=self.show_settings)
        self.hide_settingsbutton = Button(self.buttonsframe, text="hide settings", command=self.hide_settings)

        ON = Button(self.buttonsframe, text="ON", command=self.onButtonCallback)
        OFF = Button(self.buttonsframe, text="OFF", command=self.offButtonCallback)

        min_uitrolstand = IntVar()
        max_uitrolstand = IntVar()
        device_name = StringVar()

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.GET_MIN_UNROLL_LENGTH)

        # time.sleep(1)

        min_uitrolstand.set(unit.parse_serial(unit.receive())[1])

        unit.send_command(serial_protocol.SerialCommands.GET_MAX_UNROLL_LENGTH)

        # time.sleep(1)

        max_uitrolstand.set(unit.parse_serial(unit.receive())[1])

        unit.send_command(serial_protocol.SerialCommands.GET_DEVICE_NAME)

        # time.sleep(1)

        device_name.set(unit.parse_serial(unit.receive())[1])



        MinLabelTabOne = Label(self.framesies, text="Minimale oprol:")
        MaxLabelTabOne = Label(self.framesies, text="Maximale uitrol:")
        DeviceNameLabelTabOne = Label(self.framesies, text="Device name")
        MinEntryTabOne = Entry(self.framesies, textvariable=min_uitrolstand)
        MaxEntryTabOne = Entry(self.framesies, textvariable=max_uitrolstand)
        DeviceNameEntryTabOne = Entry(self.framesies, textvariable=device_name)
        sendButton1 = Button(self.framesies, text="Send", command= lambda: self.sendButton1Callback(min_uitrolstand.get()))
        sendButton2 = Button(self.framesies, text="Send", command= lambda: self.sendButton2Callback(max_uitrolstand.get()))
        sendButton3 = Button(self.framesies, text="Send", command= lambda: self.sendButton3Callback(device_name.get()))

        ON.pack(anchor=W)
        OFF.pack(anchor=W)
        self.show_settingsbutton.pack(anchor=W)

        MinLabelTabOne.grid(row=3, column=0, padx=15, pady=15)
        MinEntryTabOne.grid(row=3, column=1, padx=15, pady=15)
        MaxLabelTabOne.grid(row=4, column=0, padx=15, pady=15)
        MaxEntryTabOne.grid(row=4, column=1, padx=15, pady=15)
        DeviceNameLabelTabOne.grid(row=5, column=0, padx=15, pady=15)
        DeviceNameEntryTabOne.grid(row=5, column=1, padx=15, pady=15)
        sendButton1.grid(row=3, column=3, padx=15, pady=15)
        sendButton2.grid(row=4, column=3, padx=15, pady=15)
        sendButton3.grid(row=5, column=3, padx=15, pady=15)


        self.setting_frame.pack(anchor=W, fill=Y, expand=False, side=LEFT)
        self.buttonsframe.pack(anchor=NW, fill=X, expand=False, side=LEFT, padx=(20,0))

    def show_settings(self):
        self.framesies.pack(anchor=S, padx=100, pady=10)
        self.show_settingsbutton.pack_forget()
        self.hide_settingsbutton.pack()

    def hide_settings(self):
        self.framesies.pack_forget()
        self.hide_settingsbutton.pack_forget()
        self.show_settingsbutton.pack()





    #handles selection of radiobuttons for selected ports
    def selection1(self):
        self.current_unit = ("COM" + str(self.radio1.get()))
        self.make_settings_screen(self.current_unit)

    def selection2(self):
        self.current_unit = ("COM" + str(self.radio2.get()))
        print(self.current_unit)

    def selection3(self):
        self.current_unit = ("COM" + str(self.radio3.get()))
        print(self.current_unit)



    #function that makes and deletes the radiobuttons according to ports_list
    def radiobuttons(self):

        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame1 = Frame(self.tab1, width=100, height=100)
        self.frame2 = Frame(self.tab2)
        self.frame3 = Frame(self.tab3)


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
            self.setting_frame.pack_forget()
            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.frame3.pack_forget()


        self.frame1.pack(anchor=E, fill=Y, expand=False, side=RIGHT)
        self.frame2.pack(anchor=NE)
        self.frame3.pack(anchor=E)
        self.frame.after(1000, self.radiobuttons)

    def onButtonCallback(self):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.ROLL_SUNSHADES_DOWN)

    def offButtonCallback(self):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.ROLL_SUNSHADES_UP)

    def sendButton1Callback(self, value):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.SET_MIN_UNROLL_LENGTH, value)

    def sendButton2Callback(self, value):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.SET_MAX_UNROLL_LENGTH, value)

    def sendButton3Callback(self, value):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.SET_DEVICE_NAME, value)



root = Tk()
gui(root)
root.mainloop()
