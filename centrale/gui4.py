from tkinter import *
from tkinter import ttk
import threading
import update_ports
import graphs
import serial_protocol


class LightGraphFrame:
    def __init__(self, rt, ser):
        self.frame = rt
        self.light_graph = graphs.LightGraph(self.frame, ser)


class TemperatureGraphFrame:
    def __init__(self, rt, ser):
        self.frame = rt
        self.temperature_graph = graphs.TemperatureGraph(self.frame, ser)


class Gui():
    def __init__(self, root):
        self.frame = root
        self.updater = update_ports.update_ports(self.frame)
        self.current_unit = ''
        self.frame.title("Zonnescherm bediening")
        self.frame.geometry("1200x800")

        # tabs
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

        # initializes frames for the radiobuttons that hold the available ports options
        self.frame1 = Frame(self.tab1)
        self.frame2 = Frame(self.tab2)
        self.frame3 = Frame(self.tab3)

        # radio buttons listeners
        self.radio1 = IntVar()
        self.radio2 = IntVar()
        self.radio3 = IntVar()

        # update the radiobuttons for ports
        self.updateradio = threading.Thread(target=self.radiobuttons(), args=(1,))
        self.updateradio.start()

        # settingframe
        self.setting_frame = Frame(self.tab1, width=100, height=100)
        # lightframe
        self.light_frame = Frame(self.tab2)
        # tempframe
        self.temp_frame = Frame(self.tab3)
        self.setting_frame.pack()

    def make_settings_screen(self, current_unit):
        self.setting_frame.pack_forget()
        self.setting_frame = Frame(self.tab1, width=100, height=100, )

        self.current_unit = current_unit
        Label(self.setting_frame, text="Geselecteerde unit: " + self.current_unit).pack(anchor=NW, padx=(20, 0),
                                                                                        pady=(5, 5))

        self.buttonsframe = Frame(self.setting_frame, width=100, height=50)
        self.framesies = Frame(self.setting_frame)

        ####buttons
        self.show_settingsbutton = Button(self.buttonsframe, text="settings", command=self.show_settings)
        self.hide_settingsbutton = Button(self.buttonsframe, text="hide settings", command=self.hide_settings)

        ON = Button(self.buttonsframe, text="ON", command=self.on_button_callback)
        OFF = Button(self.buttonsframe, text="OFF", command=self.off_button_callback)

        min_uitrolstand = IntVar()
        max_uitrolstand = IntVar()
        device_name = StringVar()

        unit = self.updater.return_dict()[self.current_unit]

        min_uitrolstand.set(unit.arduino_settings['min_unroll_length'])
        max_uitrolstand.set(unit.arduino_settings['max_unroll_length'])
        device_name.set(unit.arduino_settings['device_name'])

        MinLabelTabOne = Label(self.framesies, text="Minimale oprol:")
        MaxLabelTabOne = Label(self.framesies, text="Maximale uitrol:")
        DeviceNameLabelTabOne = Label(self.framesies, text="Device name")
        MinEntryTabOne = Entry(self.framesies, textvariable=min_uitrolstand)
        MaxEntryTabOne = Entry(self.framesies, textvariable=max_uitrolstand)
        DeviceNameEntryTabOne = Entry(self.framesies, textvariable=device_name)
        sendButton1 = Button(self.framesies, text="Send",
                             command=lambda: self.send_button1_callback(min_uitrolstand.get()))
        sendButton2 = Button(self.framesies, text="Send",
                             command=lambda: self.send_button2_callback(max_uitrolstand.get()))
        sendButton3 = Button(self.framesies, text="Send", command=lambda: self.send_button3_callback(device_name.get()))

        ON.pack(anchor=W)
        OFF.pack(anchor=W)
        self.show_settingsbutton.pack(anchor=W)

        MinLabelTabOne.grid(row=3, column=0, padx=15)
        MinEntryTabOne.grid(row=3, column=1, padx=15)
        MaxLabelTabOne.grid(row=4, column=0, padx=15, pady=15)
        MaxEntryTabOne.grid(row=4, column=1, padx=15, pady=15)
        DeviceNameLabelTabOne.grid(row=5, column=0, padx=15, pady=15)
        DeviceNameEntryTabOne.grid(row=5, column=1, padx=15, pady=15)
        sendButton1.grid(row=3, column=3, padx=15, pady=15)
        sendButton2.grid(row=4, column=3, padx=15, pady=15)
        sendButton3.grid(row=5, column=3, padx=15, pady=15)

        self.setting_frame.pack(anchor=W, fill=Y, expand=False, side=LEFT)
        self.light_frame.pack(anchor=E, fill=Y, expand=False, side=RIGHT)
        self.buttonsframe.pack(anchor=NW, fill=X, expand=False, side=LEFT, padx=(20, 0))
        self.tab_parent.pack(expand=1, fill='both')

    def show_settings(self):
        self.framesies.pack(anchor=S, padx=100, pady=10)
        self.show_settingsbutton.pack_forget()
        self.hide_settingsbutton.pack()

    def hide_settings(self):
        self.framesies.pack_forget()
        self.hide_settingsbutton.pack_forget()
        self.show_settingsbutton.pack()

    # handles selection of radiobuttons for selected ports
    def selection1_callback(self):
        self.current_unit = ("COM" + str(self.radio1.get()))
        self.make_settings_screen(self.current_unit)

    def selection2_callback(self):
        self.current_unit = ("COM" + str(self.radio2.get()))
        self.light_frame.pack_forget()
        self.light_frame = Frame(self.tab2, bg="black")
        LightGraphFrame(self.light_frame, self.updater.return_dict())
        self.light_frame.pack(anchor=NW, expand=True)
        self.tab_parent.pack(anchor=NE, expand=0, fill='both')

    def selection3_callback(self):
        self.current_unit = ("COM" + str(self.radio3.get()))
        self.temp_frame.pack_forget()
        self.temp_frame = Frame(self.tab3, bg="black")
        TemperatureGraphFrame(self.temp_frame, self.updater.return_dict())
        self.temp_frame.pack(anchor=E, fill=Y, expand=False, side=RIGHT)
        self.tab_parent.pack(expand=1, fill='both')

    # function that makes and deletes the radiobuttons according to ports_list
    def radiobuttons(self):

        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame1 = Frame(self.tab1, width=100, height=100)
        self.frame2 = Frame(self.tab2, width=100, height=100)
        self.frame3 = Frame(self.tab3, width=100, height=100)

        self.updateports = threading.Thread(target=self.updater.updatePorts(), args=(0,))
        self.updateports.start()

        if len(self.updater.return_ports_list()) > 0:

            for port in self.updater.return_ports_list():
                i = 0
                Radiobutton(self.frame1, text=str(port), variable=self.radio1, value=str(port)[3],
                            command=self.selection1_callback).pack(anchor=E,
                                                                   padx=(0, 30))
                Radiobutton(self.frame2, text=str(port), variable=self.radio2, value=str(port)[3],
                            command=self.selection2_callback).pack(anchor=E,
                                                                   padx=(0, 30))
                Radiobutton(self.frame3, text=str(port), variable=self.radio3, value=str(port)[3],
                            command=self.selection3_callback).pack(anchor=E,
                                                                   padx=(0, 30))
                self.updater.updatePorts()
                i += 1

            self.frame1.pack_forget()
            self.frame2.pack_forget()
            self.frame3.pack_forget()

        self.frame1.pack(anchor=E, fill=Y, expand=False, side=RIGHT)
        self.frame2.pack(anchor=E, fill=Y, expand=False, side=RIGHT)
        self.frame3.pack(anchor=E, fill=Y, expand=False, side=RIGHT)
        self.frame.after(1000, self.radiobuttons)

    def on_button_callback(self):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.ROLL_SUNSHADES_DOWN)

    def off_button_callback(self):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.ROLL_SUNSHADES_UP)

    def send_button1_callback(self, value):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.SET_MIN_UNROLL_LENGTH, value)

    def send_button2_callback(self, value):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.SET_MAX_UNROLL_LENGTH, value)

    def send_button3_callback(self, value):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.SET_DEVICE_NAME, value)

        unit.send_command(serial_protocol.SerialCommands.GET_DEVICE_NAME)


root = Tk()
Gui(root)
root.mainloop()
