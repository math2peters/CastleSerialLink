import numpy as np
import serial

class ESCSerial(serial.Serial):

    def __init__(self, serial_port, device_id=0, baudrate=9600):


        self.serial_link = serial.Serial.__init__(serial_port, baudrate=baudrate)

        self.device_id = device_id

        self.register_dictionary = {"voltage": 0, "ripple": 1, "current": 2, "throttle": 3, "power": 4, "speed": 5,
                                    "temp": 6, "BEC voltage": 7, "BEC current": 8, "Raw NTC": 9, "RAW linear": 10,
                                    "link live": 25, "fail safe": 26, "e stop": 27, "packet in": 28, "packet out": 29,
                                    "check bad": 30, "packet bad": 31, "write throttle": 128, "write fail safe": 129,
                                    "write e stop": 130, "write packet in": 131, "write packet out": 132,
                                    "write check bad": 133, "write packet bad": 134
                                    }

        self.scale_dictionary = {"voltage": 20.0, "ripple": 4.0, "current": 50.0, "throttle": 1.0, "power": 0.2502,
                                 "speed": 20416.66, "temp": 30.0, "BEC voltage": 4.0, "BEC current": 4.0 ,
                                 "Raw NTC": 63.8125, "RAW linear": 30.0, "link live": -1, "fail safe": -1,
                                 "e stop": -1, "packet in": -1, "packet out": -1, "check bad": -1, "packet bad": -1,
                                 }


    def calc_checksum(self, b):
        intlist = [int(a) for a in b]

        if np.sum(intlist) % 256 == 0:
            return True
        else:
            return False

    def append_checksum(self, array):
        array.append((0 - np.sum(array)) % 256)
        return array

    def convert_response(self, var, rsp):
        values = rsp[:2]

        scale = self.scale_dictionary[var]
        if scale == -1:
            return values[0] * 256 + values[[1]]
        else:
            return values[0] * 256 + values[[1]] * scale / 2042.0


    def write_var(self, var, s):
        assert 0 <= s < 256**2
        write_array = [128 + self.device_id,
                     self.write_dictionary[var],
                     int(s // 256), s % 256]
        write_array = self.append_checksum(write_array)
        self.serial_link.write(write_array)
        rsp = self.serial_link.read(3)
        return rsp

    def read_var(self, var):
        read_array = [128, self.read_dictionary[var],
                      0, 0]
        read_array = self.append_checksum(read_array)
        self.serial_link.write(read_array)
        rsp = self.serial_link.read(3)

        if len(rsp) == 3 and self.checksum(rsp):
            return self.convert_response(var, rsp)

        else:
            return b''
