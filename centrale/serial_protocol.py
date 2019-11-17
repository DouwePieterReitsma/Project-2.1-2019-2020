import serial
import io
from enum import IntEnum
import time
import threading

class SerialCommands(IntEnum):
    SET_TEMPERATURE_THRESHOLD = 0
    SET_LIGHT_THRESHOLD = 1
    SET_MAX_UNROLL_LENGTH = 2
    SET_MIN_UNROLL_LENGTH = 3
    SET_DEVICE_NAME = 4
    GET_TEMPERATURE_THRESHOLD = 5
    GET_LIGHT_THRESHOLD = 6
    GET_MAX_UNROLL_LENGTH = 7
    GET_MIN_UNROLL_LENGTH = 8
    GET_DEVICE_NAME = 9
    TOGGLE_AUTOMATIC_MODE = 10
    ROLL_SUNSHADES_UP = 11
    ROLL_SUNSHADES_DOWN = 12
    FACTORY_RESET = 13

class SerialProtocol:
    def __init__(self, port):
        self.ser = serial.Serial(port, 19200)
        self.port = port

        time.sleep(3) # arduino reboots every time a serial connection is established

        # list of tuples (light, temperature, sunshade_status)
        self.data = []

        self.arduino_settings = {'temperature_threshold': 0, 'light_threshold': 0, 'max_unroll_length': 0,
                                 'min_unroll_length': 0, 'device_name': ''}

        self.receiverThread = threading.Thread(target=self.receive)
        self.receiverThread.daemon = True
        self.receiverThread.start()

        # get settings values
        self.send_command(SerialCommands.GET_TEMPERATURE_THRESHOLD)

        time.sleep(1)

        self.send_command(SerialCommands.GET_LIGHT_THRESHOLD)

        time.sleep(1)

        self.send_command(SerialCommands.GET_MAX_UNROLL_LENGTH)

        time.sleep(1)

        self.send_command(SerialCommands.GET_MIN_UNROLL_LENGTH)

        time.sleep(1)

        self.send_command(SerialCommands.GET_DEVICE_NAME)

    def send_command(self, c, param=''):
        self.ser.write('{0}:{1}\r\n'.format(c, param).encode('ascii'))

    def receive(self):
        while True:
            line = self.ser.readline().decode('ascii')

            self.parse_serial(line)

    def parse_serial(self, line):
        args = line.split(':')

        fmt = int(args[0])

        if fmt == 0:
            caller = int(args[1]) # which GET_* function is the return value for
            value = args[2]

            if caller == SerialCommands.GET_TEMPERATURE_THRESHOLD:
                self.arduino_settings['temperature_threshold'] = float(value)

            if caller == SerialCommands.GET_LIGHT_THRESHOLD:
                self.arduino_settings['light_threshold'] = float(value)

            if caller == SerialCommands.GET_MAX_UNROLL_LENGTH:
                self.arduino_settings['max_unroll_length'] = int(value)

            if caller == SerialCommands.GET_MIN_UNROLL_LENGTH:
                self.arduino_settings['min_unroll_length'] = int(value)

            if caller == SerialCommands.GET_DEVICE_NAME:
                self.arduino_settings['device_name'] = str(value).strip()

        if fmt == 1:
            light = int(args[1])
            temp = float(args[2])
            sunshade_status = bool(args[3])

            self.data.append((light, temp, sunshade_status))

        if fmt == 3:
            message = args[1]


if __name__ == '__main__':
    print('Listening...')

    test = SerialProtocol(port='COM6')

    print('test')





