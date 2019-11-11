import serial
import serial.tools.list_ports
import threading

class update_ports():

    def __init__(self, frame):
        self.ports_list = []
        self.dict = {}
        self.update = threading.Thread(target=self.updatePorts(), args=(1,))
        self.update.start()

    def updatePorts(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino"in p[1] and p[0] not in self.ports_list:
                self.ports_list.append(p[0])
                self.dict[str(p[0])] = serial.Serial(p[0], 19200)

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


