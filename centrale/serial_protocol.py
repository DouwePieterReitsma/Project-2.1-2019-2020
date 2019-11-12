import serial
import io
from enum import IntEnum
import time

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

    def send_command(self, c, param=''):
        self.ser.write('{0}:{1}\r\n'.format(c, param).encode('ascii'))

    def receive(self):
        return self.ser.readline().decode('ascii')

    def parse_serial(self, serial_str):
        args = serial_str.split(':')

        if len(args) < 2:
            return None

        fmt = int(args[0])

        if fmt == 0:
            return (fmt, args[1])

        if fmt == 1:
            light = int(args[1])
            temp = float(args[2])
            sunshade_status = bool(args[3])

            return (fmt, light, temp, sunshade_status)

        if fmt == 3:
            message = args[1]

            return (fmt, message)