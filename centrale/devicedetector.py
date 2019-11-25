import serial
import serial.tools.list_ports
import threading
import serial_protocol


class DeviceDetector:
    def __init__(self):
        self.ports_list = []
        self.dict = {}
        self.update = threading.Thread(target=self.detect_devices(), args=(1,))
        self.update.start()

    def detect_devices(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if p[0] not in self.ports_list:
                self.ports_list.append(p[0])
                self.dict[str(p[0])] = serial_protocol.SerialProtocol(p[0])

        for port in self.ports_list:
            bool = 1
            for p in ports:
                if port == p[0]:
                    bool = 0
            if bool:
                self.ports_list.remove(port)
                self.dict.pop(port)

        if len(ports) < 1:
            del self.ports_list[:]
            self.dict.clear()

    def return_ports_list(self):
        return self.ports_list

    def return_dict(self):
        return self.dict
