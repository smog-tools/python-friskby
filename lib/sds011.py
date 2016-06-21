import serial


class SDS011(object):
    device = serial.Serial('/dev/ttyUSB0', baudrate=9600, stopbits=1, parity="N",  timeout=2)

    @classmethod
    def read(cls):
        s = cls.device.read(1)
        if ord(s) == int("AA",16):
            s = cls.device.read(1)
            if ord(s) == int("C0",16):
                s = cls.device.read(7)
                
                pm25hb = s[0]
                pm25lb = s[1]
                pm10hb = s[2]
                pm10lb = s[3]

                cs     = s[6]
                # we should verify the checksum... it is the sum of bytes 1-6 truncated...

                pm25 = float(pm2hb + pm2lb*256)/10.0
                pm10 = float(pm10hb + pm10lb*256)/10.0
                
                return (pm10 , pm25)
            else:
                raise OSError("Reading from serial device failed")
        else:
            raise OSError("Reading from serial device failed")