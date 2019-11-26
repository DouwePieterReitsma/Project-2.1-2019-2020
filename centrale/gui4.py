from tkinter import *
from tkinter import ttk
import threading
import devicedetector
from graphs import (TemperatureGraph, LightGraph)
import serial_protocol
import time


class Gui:
    def __init__(self, root):
        self.frame = root
        self.updater = devicedetector.DeviceDetector()
        self.current_unit = ''
        self.frame.title("Zonneschermbediening")
        self.frame.geometry("800x600")

        # tabs
        self.tab_parent = ttk.Notebook(self.frame)
        self.tab1 = Frame(self.tab_parent)
        self.tab2 = Frame(self.tab_parent)
        self.tab3 = Frame(self.tab_parent)

        self.tab_parent.add(self.tab1, text="Instellingen")
        self.tab_parent.add(self.tab2, text="Licht")
        self.tab_parent.add(self.tab3, text="Temperatuur")
        # self.tab_parent.pack(expand=1, fill='both')

        # initializes frames for the radiobuttons that hold the available ports options
        self.deviceButtonsFrame1 = Frame(self.tab1, width=100, height=100)
        self.deviceButtonsFrame2 = Frame(self.tab2, width=100, height=100)
        self.deviceButtonsFrame3 = Frame(self.tab3, width=100, height=100)

        # radio buttons listeners
        self.radio1 = IntVar()
        self.radio2 = IntVar()
        self.radio3 = IntVar()

        # update
        self.updateradio = threading.Thread(target=self.radiobuttons)
        self.updateradio.daemon = True
        self.updateradio.start()

        # settingframe
        self.setting_frame = Frame(self.tab1, width=400)
        self.setting_frame.grid(row=0, column=0)

        # inner settings frame
        self.inner_settings_frame = Frame(self.setting_frame)

        self.light_frame = Frame(self.tab2, bg="black")
        self.light_graph = LightGraph(self.light_frame, self.updater.return_dict())
        self.light_frame.grid(row=0, column=0)

        self.temp_frame = Frame(self.tab3, bg="black")
        self.temp_graph = TemperatureGraph(self.temp_frame, self.updater.return_dict())
        self.temp_frame.grid(row=0, column=0)

        self.tab_parent.pack(anchor=NE, expand=0, fill='both')

    def make_settings_screen(self, current_unit):
        self.inner_settings_frame.grid_forget()
        self.inner_settings_frame = Frame(self.setting_frame)
        self.inner_settings_frame.grid()

        self.current_unit = current_unit
        unit = self.updater.return_dict()[self.current_unit]

        Label(self.inner_settings_frame, text="Geselecteerde unit: " + self.current_unit).pack(anchor=NW, padx=(13, 0),
                                                                                               pady=(5, 5))

        self.buttonsframe = Frame(self.inner_settings_frame)
        self.framesies = Frame(self.inner_settings_frame)

        # buttons
        self.show_settingsbutton = Button(self.buttonsframe, text="Instellingen", command=self.show_settings)
        self.hide_settingsbutton = Button(self.buttonsframe, text="Instellingen verbergen", command=self.hide_settings)

        self.toggle_mode_button = Button(self.buttonsframe, text='Toggle Handmatige modus', command=lambda: self.toggle_mode_button_callback(unit))

        self.on_button = Button(self.buttonsframe, text="Aan", state=DISABLED, command=self.on_button_callback)
        self.off_button = Button(self.buttonsframe, text="Uit", state=DISABLED,  command=self.off_button_callback)

        min_uitrolstand = IntVar()
        max_uitrolstand = IntVar()
        device_name = StringVar()
        temp_threshold = IntVar()
        light_threshold = IntVar()

        min_uitrolstand.set(unit.arduino_settings['min_unroll_length'])
        max_uitrolstand.set(unit.arduino_settings['max_unroll_length'])
        device_name.set(unit.arduino_settings['device_name'])
        light_threshold.set(unit.arduino_settings['light_threshold'])
        temp_threshold.set(unit.arduino_settings['temperature_threshold'])

        MinLabelTabOne = Label(self.framesies, text="Minimale oprol:")
        MaxLabelTabOne = Label(self.framesies, text="Maximale uitrol:")
        DeviceNameLabelTabOne = Label(self.framesies, text="Apparaatnaam:")
        TemperatureThresholdLabel = Label(self.framesies, text='Drempelwaarde temperatuur:')
        LightThresholdLabel = Label(self.framesies, text='Drempelwaarde licht:')

        MinEntryTabOne = Entry(self.framesies, textvariable=min_uitrolstand)
        MaxEntryTabOne = Entry(self.framesies, textvariable=max_uitrolstand)
        DeviceNameEntryTabOne = Entry(self.framesies, textvariable=device_name)
        LightThresholdEntry = Entry(self.framesies, textvariable=light_threshold)
        TemperatureThresholdEntry = Entry(self.framesies, textvariable=temp_threshold)

        sendButton1 = Button(self.framesies, text="Opslaan",
                             command=lambda: self.send_button1_callback(min_uitrolstand.get()))
        sendButton2 = Button(self.framesies, text="Opslaan",
                             command=lambda: self.send_button2_callback(max_uitrolstand.get()))
        sendButton3 = Button(self.framesies, text="Opslaan",
                             command=lambda: self.send_button3_callback(device_name.get()))
        sendButton4 = Button(self.framesies, text="Opslaan",
                             command=lambda: self.send_button4_callback(light_threshold.get()))
        sendButton5 = Button(self.framesies, text="Opslaan",
                             command=lambda: self.send_button5_callback(temp_threshold.get()))

        self.toggle_mode_button.pack(anchor=W)
        self.on_button.pack(anchor=W)
        self.off_button.pack(anchor=W)
        self.show_settingsbutton.pack(anchor=W)

        MinLabelTabOne.grid(row=3, column=0, padx=15)
        MinEntryTabOne.grid(row=3, column=1, padx=15)
        MaxLabelTabOne.grid(row=4, column=0, padx=15, pady=15)
        MaxEntryTabOne.grid(row=4, column=1, padx=15, pady=15)
        DeviceNameLabelTabOne.grid(row=5, column=0, padx=0)
        DeviceNameEntryTabOne.grid(row=5, column=1, padx=15)
        LightThresholdLabel.grid(row=6, column=0, padx=15)
        LightThresholdEntry.grid(row=6, column=1, padx=15)
        TemperatureThresholdLabel.grid(row=7, column=0, padx=15)
        TemperatureThresholdEntry.grid(row=7, column=1, padx=15)

        sendButton1.grid(row=3, column=3, padx=15, pady=15)
        sendButton2.grid(row=4, column=3, padx=15, pady=15)
        sendButton3.grid(row=5, column=3, padx=15, pady=15)
        sendButton4.grid(row=6, column=3, padx=15, pady=15)
        sendButton5.grid(row=7, column=3, padx=15, pady=15)

        self.buttonsframe.pack(anchor=N, fill=X, padx=(15, 15), pady=(10, 20))

    def show_settings(self):
        self.framesies.pack(side=LEFT, pady=(0, 20), anchor=NW)
        self.show_settingsbutton.pack_forget()
        self.hide_settingsbutton.pack(anchor=W)

    def hide_settings(self):
        self.framesies.pack_forget()
        self.hide_settingsbutton.pack_forget()
        self.show_settingsbutton.pack(anchor=W)

    # handles selection of radiobuttons for selected ports
    def selection1_callback(self):
        self.current_unit = ("COM" + str(self.radio1.get()))
        self.make_settings_screen(self.current_unit)

    def light_graph_line_toggle_callback(self, port):
        self.light_graph.set_line_visibility(port, bool(self.radio2.get()))

    def temp_graph_line_toggle_callback(self, port):
        self.temp_graph.set_line_visibility(port, bool(self.radio3.get()))

    # function that makes and deletes the radiobuttons according to ports_list
    def radiobuttons(self):
        while True:
            self.updater.detect_devices()

            self.deviceButtonsFrame1.grid_forget()
            self.deviceButtonsFrame2.grid_forget()
            self.deviceButtonsFrame3.grid_forget()

            self.deviceButtonsFrame1 = Frame(self.tab1, width=100, height=100)
            self.deviceButtonsFrame2 = Frame(self.tab2, width=100, height=100)
            self.deviceButtonsFrame3 = Frame(self.tab3, width=100, height=100)

            if len(self.updater.return_ports_list()) > 0:
                for k, connection in self.updater.return_dict().items():
                    i = 0
                    Radiobutton(self.deviceButtonsFrame1, text=connection.port, variable=self.radio1,
                                value=str(connection.port)[3],
                                command=self.selection1_callback).pack(anchor=E,
                                                                       padx=(0, 30))
                    Checkbutton(self.deviceButtonsFrame2, text=connection.port, variable=self.radio2,
                                command=lambda: self.light_graph_line_toggle_callback(connection.port)).pack(anchor=E,
                                                                                    padx=(0, 30))

                    Checkbutton(self.deviceButtonsFrame3, text=connection.port, variable=self.radio3,
                                command=lambda: self.temp_graph_line_toggle_callback(connection.port)).pack(anchor=E,
                                                                                   padx=(0, 30))
                    self.updater.detect_devices()
                    i += 1

                self.deviceButtonsFrame1.grid_forget()
                self.deviceButtonsFrame2.grid_forget()
                self.deviceButtonsFrame3.grid_forget()

            self.deviceButtonsFrame1.grid(row=0, column=1)
            self.deviceButtonsFrame2.grid(row=0, column=1)
            self.deviceButtonsFrame3.grid(row=0, column=1)

            time.sleep(1)

    def toggle_mode_button_callback(self, unit):
        unit.arduino_settings['automatic_mode'] = not unit.arduino_settings['automatic_mode']

        if unit.arduino_settings['automatic_mode']:
            self.toggle_mode_button.configure(text='Toggle Handmatige modus')

            self.on_button.configure(state=DISABLED)
            self.off_button.configure(state=DISABLED)
        else:
            self.toggle_mode_button.configure(text='Toggle Automatische modus')

            self.on_button.configure(state=NORMAL)
            self.off_button.configure(state=NORMAL)

        unit.send_command(serial_protocol.SerialCommands.TOGGLE_AUTOMATIC_MODE)

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

    def send_button4_callback(self, value):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.SET_LIGHT_THRESHOLD, value)

    def send_button5_callback(self, value):
        if self.current_unit == '':
            return

        unit = self.updater.return_dict()[self.current_unit]

        unit.send_command(serial_protocol.SerialCommands.SET_TEMPERATURE_THRESHOLD, value)


root = Tk()
Gui(root)
root.mainloop()
